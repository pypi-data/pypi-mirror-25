#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect
from logging import getLogger
from functools import update_wrapper

import tools
import ujson

from .config import config
from .redisfun import redisfun
from .userdata import usercard
logger = getLogger(__name__)

from vwalila import mqfun

def send_then_wait(job_name, job_data, is_inner_task=False):
    return mqfun.send_then_wait(job_name, job_data, is_inner_task=is_inner_task)


def send_only(job_name, job_data):
    return mqfun.send_only(job_name, job_data)


def send_only_for_log(job_name, job_data):
    return mqfun.send_only_for_log(job_name, job_data)

def timemagic(task_obj):
    def task_wrapper(worker, job):
        body = {}
        try:
            req = loadreq(job)
            mysess = req.pop('mysess', '')
            # 更新用户登录信息
            usercard_update(mysess)
            # 获取参数
            kw = handle_arg(req, task_obj)
            # 执行函数
            logger.debug("input: %s", kw)
            b_time = tools.now_time()
            return_data = task_obj(**kw)
            e_time = tools.now_time()
            logger.debug("output: %s", return_data)
            do_ms = e_time - b_time
            if return_data is None:
                body['data'] = {}
            else:
                body['data'] = return_data
            body['do_ms'] = do_ms
        except Exception as e:
            if len(e.args) >= 2:
                body['status'] = e.args[0]
                body['msg'] = e.args[1]
            else:
                body['status'] = 999
                body['msg'] = e.args[0]
            logger.error(body['msg'], exc_info=True)
        return ujson.dumps(package_data(**body), ensure_ascii=False)
    return update_wrapper(task_wrapper, task_obj)


def handle_arg(req, task_obj):
    """
    处理参数
    """
    argspec = inspect.getargspec(task_obj)
    if argspec.defaults:
        # 必选参数 =  全部参数[ :-有默认值的参数的数量]
        required = argspec.args[:-len(argspec.defaults)]
    else:
        required = argspec.args
    # 如果入参和必选参数的交集不等于必选参数
    if set(req) & set(required) != set(required):
        if config['debug']:
            absent = set(required) - set(req)
            raise ValueError(618, u'缺少主要参数 {}'.format(' '.join(absent)))
        else:
            raise ValueError(618, u'缺少主要参数')
    # 如果有可变参数 直接塞进去就好了
    if argspec.keywords:
        kw = req
    else:
        kw = {}
        for x in argspec.args:
            args = req.get(x, None)
            if args is None:
                continue
            kw[x] = args
    return kw


def usercard_update(mysess):
    """
    更新用户登录信息
    """
    userdata_str = redisfun.get_sess_str(mysess)
    if userdata_str:
        userdata = ujson.loads(userdata_str)
        userdata['mysess'] = mysess
    else:
        userdata = {}
    # 更新用户登录信息
    usercard.update(userdata)


def loadreq(data):
    """
    加载请求
    """
    req = ujson.loads(data)
    # 扔掉
    req.pop('user_ip', '')
    req.pop('seqnum', '')
    req.pop('web_st', '')
    req.pop('user_agent', '')
    return req


def package_data(data=None, status=None, msg=None, do_ms=None):
    """ 在外面包裹一层
    :data:
    :status:
    :return: -> dict
        {'body': data, # if data True
        'status': 200,
        'msg': 'ok',
        'seqnum': now_time()}
    """
    if not status:
        status = 200
    if not msg:
        msg = 'ok'
    structure = {
        'status': status,
        'ip': config['g_ip'],
        'do_ms': do_ms or 0,
        'msg': msg,
        'seqnum': tools.now_time()
    }
    if config['debug']:
        structure['Git_HEAD'] = config['git_version']
    if not data is None:
        structure['body'] = data
    return structure
