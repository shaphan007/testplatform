# coding=gbk
import json
import logging
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Model
from django.forms import model_to_dict
from django.http import JsonResponse

from tp.models import Tag, Case

def info_handler(in_params, position_keys=None, option_keys=None):
    info = {}
    # 必填参数
    print(f'必填关键字：{position_keys}')
    for key in in_params:
        print (key)
    if position_keys is not None:
        for key in position_keys:
            print(f'必填关键字：{key}')
            if key not in in_params and not key.endswith('_ids'):
                return JsonResponse({'retcode': 500, 'msg': "必填参数为空", 'error': f"{key}为必填参数不能为空"})
            info[key] = in_params[key]

    # 选填参数
    if option_keys is not None:
        for key in option_keys:
            if key in in_params and not key.endswith('_ids'):
                info[key] = in_params[key]

    return info


def filter_query(resp_tmp, query_obj):
    """
    @param resp_tmp:  返回数据格式模板
    @param query_obj: 查询到的数据对象
    @return: 按模板格式的单条数据
    """
    item_dict = resp_tmp['retlist'][0]
    item = {}
    for k, v in item_dict.items():
        if isinstance(v, dict):
            # print(f'处理字典:{k}')
            if hasattr(query_obj, k) and getattr(query_obj, k):
                item[k] = model_to_dict(getattr(query_obj, k),
                                        fields=v.keys())  # 对应的字段getattr(query_obj, k)  例如：project.admin
            else:
                item[k] = None
            print(item[k])
        elif isinstance(v, list):
            fields = v[0].keys()
            print(fields)
            # print(f"列表数据查询:{k}")
            if hasattr(query_obj, k):
                # print("反向查询")
                # item['member'] = list(project.members.all().values('id', 'username', 'email', 'first_name'))
                item[k] = list(getattr(query_obj, k).all().values(*fields))
            else:
                # print("正向查询")
                # item['modules'] = list(project.module_set.all().values('id', 'name', 'desc'))
                item[k] = list(getattr(query_obj, k[0:-1] + '_set').values(*fields))
            # print(item[k])
        else:
            # print(f"开始处理普通类型数据{k}")
            # 判断value 是否为对应的外键 -- 判断类型是否为model
            value = getattr(query_obj, k)
            if isinstance(value, Model):
                item[k] = value.id
            # 格式化时间
            elif k.endswith('_time'):
                item[k] = value.strftime('%Y-%m-%d/%H:%M')
            else:
                item[k] = value
            # print(item[k])
    # print(item)
    return item
