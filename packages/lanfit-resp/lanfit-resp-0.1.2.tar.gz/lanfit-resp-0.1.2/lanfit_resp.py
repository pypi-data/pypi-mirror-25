# -*- coding: utf-8 -*-
import re
from flask import jsonify, request
from lanfit_exceptions import CustomException

LINK_SUB_PATTERN = re.compile('<[^?]+\?')


def get_json(r):
    if not r.ok:
        errmsg = '{}: {}'.format(r.status_code, r.reason)
        raise CustomException(errcode=r.status_code, errmsg=errmsg)
    return r.json()


def wrap_resp(r):
    """将requests的Response转化为flask的Response
    并带有link信息
    """
    j = get_json(r)
    resp = jsonify(j)
    link = r.headers.get('link')
    if link:
        repl = '<{}?'.format(request.base_url)
        resp.headers['Link'] = LINK_SUB_PATTERN.sub(repl, link)
    return resp


def get_ok_json(r):
    """errcode不为0的结果抛出异常,其余返回json"""
    j = get_json(r)
    if j.get('errcode'):
        raise CustomException(**j)
    return j
