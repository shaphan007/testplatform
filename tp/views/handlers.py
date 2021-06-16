# coding=gbk
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import transaction
import json
from django.db.models import Model
from django.forms import model_to_dict
from django.http import JsonResponse
from ..plugins import info_handler, filter_query
import yaml

from tp.models import Tag, Case

M2M_dict = {
    'member_ids': User,
    'tag_ids': Tag,
    'case_ids': Case,
}


# position_keys  or option_keys  如果是空值如何处理
def isparam(param, position_keys, option_keys):
    if param in position_keys or param in option_keys:
        return True
    return False


# 读取yaml文件
def read_yaml(path):
    with open(path, encoding='utf8') as f:
        return yaml.safe_load(f.read())


class CommonView:
    @staticmethod
    def operate_add(request, db_model, position_keys=None, option_keys=None):
        # 多对多关系字典
        in_params = json.loads(request.body)
        print(f"add入参：{in_params}")
        info = info_handler(in_params, position_keys=position_keys, option_keys=option_keys)  # 返回一个字典
        print(f"add出参：{info}")
        if not isinstance(info, dict):  # 判断返回的是否是字典
            return info  # 返回的为JsonResponse
        try:
            with transaction.atomic():  # 添加事务回滚
                # 模型数据对象
                info['created_by'] = request.user  # 添加当前用户为创建者
                mod_obj = db_model.objects.create(**info)
                # 多对多关联
                for key in in_params:
                    if key.endswith('_ids') and isinstance(in_params[key], list) and isparam(key, position_keys,
                                                                                             option_keys):  # 判断是否以_ids 结尾 & 为list类型
                        M = M2M_dict[key]  # User
                        # 根据模型取出对应的数据
                        objs = [M.objects.get(pk=_id) for _id in in_params[key]]
                        # 模型数据对象进行关联
                        m2m_field = getattr(mod_obj, key.split('_')[0] + 's')
                        m2m_field.add(*objs)
                return JsonResponse({'retcode': 200, 'msg': "添加成功", 'id': mod_obj.id})
        except Exception as e:
            return JsonResponse({'retcode': 500, 'msg': "添加失败", 'error': repr(e)})  # repr 返回精简的模块信息

    @staticmethod
    def operate_delete(request, db_model, position_keys=None, option_keys=None):
        # 获取删除对象id
        in_params = request.GET
        info = info_handler(in_params, position_keys, option_keys)

        if not isinstance(info, dict):
            return info
        try:
            mod_obj = db_model.objects.get(**info)
            # 删除项目
            mod_obj.delete()
            return JsonResponse({'retcode': 200, 'msg': "删除成功"})
        except Exception as e:
            return JsonResponse({'retcode': 500, 'msg': "删除失败", 'error': repr(e)})

    @staticmethod
    def operate_update(request, db_model, position_keys=None, option_keys=None):
        _id = request.GET.get('id')
        print(f'_id:{_id}')
        in_params = json.loads(request.body)

        # 选填参数
        info = info_handler(in_params, position_keys, option_keys)
        print(f'参数：{info}')
        if not isinstance(info, dict):
            return info
        try:
            mod_obj = db_model.objects.get(pk=_id)
            for key in in_params:
                if key.endswith('_ids') and isinstance(in_params[key], list):  # 判断是否以_ids 结尾 & 为list类型
                    M = M2M_dict[key]
                    # 根据模型取出对应的数据
                    objs = [M.objects.get(pk=_id) for _id in in_params[key]]
                    # 模型数据对象进行关联
                    m2m_field = getattr(mod_obj, key.split('_')[0] + 's')  # mod_obj.members
                    # 清除原来关系  -- 多对多
                    m2m_field.clear()
                    # 重新关联成员
                    m2m_field.add(*objs)
            for k, v in info.items():
                mod_obj.__setattr__(k, v)  # object.__setattr__(属性名，属性值)
            mod_obj.update_by = request.user  # 添加更新者信息
            mod_obj.save()
            return JsonResponse({'retcode': 200, 'msg': "更新成功", 'id': mod_obj.id})
        except Exception as e:
            return JsonResponse({'retcode': 500, 'msg': "更新失败", 'error': repr(e)})

    @staticmethod
    def operate_query(request, db_model, position_keys=None, option_keys=None):
        in_params = request.GET
        info = info_handler(in_params, option_keys=option_keys)
        if db_model == Tag:
            # 判断入参是否有case_id
            if 'case_id' in info:
                info['case'] = info.pop('case_id')
        try:
            retlist = []
            # 获取分页数据-- page_index,page_size
            page_index = in_params.get('page_index', 1)
            page_size = in_params.get('page_size', 5)
            # 初始化分页器对象
            paginator = Paginator(list(db_model.objects.filter(**info)), page_size)
            # 根据页码提供当前页的内容
            queryset = paginator.get_page(page_index)

            # query_list = db_model.objects.filter(**info)  # 查询数据库对应条件的数据
            # for query_obj in query_list:
            for query_obj in queryset:
                # 根据响应模板判断响应参数类型，从而做具体处理
                resp_tmp = read_yaml('tp/query_resp_temp.yml')[db_model.__name__]  # 读取返回数据模板
                item = filter_query(resp_tmp, query_obj)  # 整合数据
                retlist.append(item)
            return JsonResponse({'retcode': 200, 'msg': "查询成功", 'retlist': retlist, 'total': paginator.count})
        except Exception as e:
            return JsonResponse({'retcode': 500, 'msg': "查询失败", 'error': repr(e)})
