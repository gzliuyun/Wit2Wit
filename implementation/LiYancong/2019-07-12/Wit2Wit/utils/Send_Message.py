#!/usr/bin/env python
# coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import json


# 接口的文档在这里
# https://help.aliyun.com/document_detail/101414.html?spm=a2c4g.11186623.2.11.6d4b3e2cs9orJ8
def send_message(mobile, code):
    # client = AcsClient('<accessKeyId>', '<accessSecret>', 'cn-hangzhou')
    client = AcsClient('LTAIjTtYFp6YT8Hi', 'SnBhv9lAno1S1unOYNzhIkD5YA19cf', 'cn-hangzhou')  # 改前两个参数
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', mobile)
    request.add_query_param('SignName', "豆博士工作室")  # 改这里
    request.add_query_param('TemplateCode', "SMS_151768608")  # 改这里
    code_msg = "{\"code\": " + "\"" + code + "\"}"
    request.add_query_param('TemplateParam', code_msg)

    response = client.do_action(request)
    response = json.loads(response)
    if response['Code'] == "OK":
        return True
    else:
        return False
