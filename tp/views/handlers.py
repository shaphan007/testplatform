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


# position_keys  or option_keys  ����ǿ�ֵ��δ���
def isparam(param, position_keys, option_keys):
    if param in position_keys or param in option_keys:
        return True
    return False


# ��ȡyaml�ļ�
def read_yaml(path):
    with open(path, encoding='utf8') as f:
        return yaml.safe_load(f.read())


class CommonView:
    @staticmethod
    def operate_add(request, db_model, position_keys=None, option_keys=None):
        # ��Զ��ϵ�ֵ�
        in_params = json.loads(request.body)
        print(f"add��Σ�{in_params}")
        info = info_handler(in_params, position_keys=position_keys, option_keys=option_keys)  # ����һ���ֵ�
        print(f"add���Σ�{info}")
        if not isinstance(info, dict):  # �жϷ��ص��Ƿ����ֵ�
            return info  # ���ص�ΪJsonResponse
        try:
            with transaction.atomic():  # �������ع�
                # ģ�����ݶ���
                info['created_by'] = request.user  # ��ӵ�ǰ�û�Ϊ������
                mod_obj = db_model.objects.create(**info)
                # ��Զ����
                for key in in_params:
                    if key.endswith('_ids') and isinstance(in_params[key], list) and isparam(key, position_keys,
                                                                                             option_keys):  # �ж��Ƿ���_ids ��β & Ϊlist����
                        M = M2M_dict[key]  # User
                        # ����ģ��ȡ����Ӧ������
                        objs = [M.objects.get(pk=_id) for _id in in_params[key]]
                        # ģ�����ݶ�����й���
                        m2m_field = getattr(mod_obj, key.split('_')[0] + 's')
                        m2m_field.add(*objs)
                return JsonResponse({'retcode': 200, 'msg': "��ӳɹ�", 'id': mod_obj.id})
        except Exception as e:
            return JsonResponse({'retcode': 500, 'msg': "���ʧ��", 'error': repr(e)})  # repr ���ؾ����ģ����Ϣ

    @staticmethod
    def operate_delete(request, db_model, position_keys=None, option_keys=None):
        # ��ȡɾ������id
        in_params = request.GET
        info = info_handler(in_params, position_keys, option_keys)

        if not isinstance(info, dict):
            return info
        try:
            mod_obj = db_model.objects.get(**info)
            # ɾ����Ŀ
            mod_obj.delete()
            return JsonResponse({'retcode': 200, 'msg': "ɾ���ɹ�"})
        except Exception as e:
            return JsonResponse({'retcode': 500, 'msg': "ɾ��ʧ��", 'error': repr(e)})

    @staticmethod
    def operate_update(request, db_model, position_keys=None, option_keys=None):
        _id = request.GET.get('id')
        print(f'_id:{_id}')
        in_params = json.loads(request.body)

        # ѡ�����
        info = info_handler(in_params, position_keys, option_keys)
        print(f'������{info}')
        if not isinstance(info, dict):
            return info
        try:
            mod_obj = db_model.objects.get(pk=_id)
            for key in in_params:
                if key.endswith('_ids') and isinstance(in_params[key], list):  # �ж��Ƿ���_ids ��β & Ϊlist����
                    M = M2M_dict[key]
                    # ����ģ��ȡ����Ӧ������
                    objs = [M.objects.get(pk=_id) for _id in in_params[key]]
                    # ģ�����ݶ�����й���
                    m2m_field = getattr(mod_obj, key.split('_')[0] + 's')  # mod_obj.members
                    # ���ԭ����ϵ  -- ��Զ�
                    m2m_field.clear()
                    # ���¹�����Ա
                    m2m_field.add(*objs)
            for k, v in info.items():
                mod_obj.__setattr__(k, v)  # object.__setattr__(������������ֵ)
            mod_obj.update_by = request.user  # ��Ӹ�������Ϣ
            mod_obj.save()
            return JsonResponse({'retcode': 200, 'msg': "���³ɹ�", 'id': mod_obj.id})
        except Exception as e:
            return JsonResponse({'retcode': 500, 'msg': "����ʧ��", 'error': repr(e)})

    @staticmethod
    def operate_query(request, db_model, position_keys=None, option_keys=None):
        in_params = request.GET
        info = info_handler(in_params, option_keys=option_keys)
        if db_model == Tag:
            # �ж�����Ƿ���case_id
            if 'case_id' in info:
                info['case'] = info.pop('case_id')
        try:
            retlist = []
            # ��ȡ��ҳ����-- page_index,page_size
            page_index = in_params.get('page_index', 1)
            page_size = in_params.get('page_size', 5)
            # ��ʼ����ҳ������
            paginator = Paginator(list(db_model.objects.filter(**info)), page_size)
            # ����ҳ���ṩ��ǰҳ������
            queryset = paginator.get_page(page_index)

            # query_list = db_model.objects.filter(**info)  # ��ѯ���ݿ��Ӧ����������
            # for query_obj in query_list:
            for query_obj in queryset:
                # ������Ӧģ���ж���Ӧ�������ͣ��Ӷ������崦��
                resp_tmp = read_yaml('tp/query_resp_temp.yml')[db_model.__name__]  # ��ȡ��������ģ��
                item = filter_query(resp_tmp, query_obj)  # ��������
                retlist.append(item)
            return JsonResponse({'retcode': 200, 'msg': "��ѯ�ɹ�", 'retlist': retlist, 'total': paginator.count})
        except Exception as e:
            return JsonResponse({'retcode': 500, 'msg': "��ѯʧ��", 'error': repr(e)})
