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
    # �������
    print(f'����ؼ��֣�{position_keys}')
    for key in in_params:
        print (key)
    if position_keys is not None:
        for key in position_keys:
            print(f'����ؼ��֣�{key}')
            if key not in in_params and not key.endswith('_ids'):
                return JsonResponse({'retcode': 500, 'msg': "�������Ϊ��", 'error': f"{key}Ϊ�����������Ϊ��"})
            info[key] = in_params[key]

    # ѡ�����
    if option_keys is not None:
        for key in option_keys:
            if key in in_params and not key.endswith('_ids'):
                info[key] = in_params[key]

    return info


def filter_query(resp_tmp, query_obj):
    """
    @param resp_tmp:  �������ݸ�ʽģ��
    @param query_obj: ��ѯ�������ݶ���
    @return: ��ģ���ʽ�ĵ�������
    """
    item_dict = resp_tmp['retlist'][0]
    item = {}
    for k, v in item_dict.items():
        if isinstance(v, dict):
            # print(f'�����ֵ�:{k}')
            if hasattr(query_obj, k) and getattr(query_obj, k):
                item[k] = model_to_dict(getattr(query_obj, k),
                                        fields=v.keys())  # ��Ӧ���ֶ�getattr(query_obj, k)  ���磺project.admin
            else:
                item[k] = None
            print(item[k])
        elif isinstance(v, list):
            fields = v[0].keys()
            print(fields)
            # print(f"�б����ݲ�ѯ:{k}")
            if hasattr(query_obj, k):
                # print("�����ѯ")
                # item['member'] = list(project.members.all().values('id', 'username', 'email', 'first_name'))
                item[k] = list(getattr(query_obj, k).all().values(*fields))
            else:
                # print("�����ѯ")
                # item['modules'] = list(project.module_set.all().values('id', 'name', 'desc'))
                item[k] = list(getattr(query_obj, k[0:-1] + '_set').values(*fields))
            # print(item[k])
        else:
            # print(f"��ʼ������ͨ��������{k}")
            # �ж�value �Ƿ�Ϊ��Ӧ����� -- �ж������Ƿ�Ϊmodel
            value = getattr(query_obj, k)
            if isinstance(value, Model):
                item[k] = value.id
            # ��ʽ��ʱ��
            elif k.endswith('_time'):
                item[k] = value.strftime('%Y-%m-%d/%H:%M')
            else:
                item[k] = value
            # print(item[k])
    # print(item)
    return item
