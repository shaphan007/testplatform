# coding=gbk
# 通用视图调度
from django.contrib.auth.decorators import login_required

from .mgr import ProjectHandler, ModuleHandler, EnvHandler
from .case import CaseHandler, PlanHandler, ResultHandler, StepHandler, HttpApiHandler, TagHandler
from .accout import login, logout, register, current_user, UserHandler


def _common_dispatcher(request, Handler):
    if request.method == 'GET':
        return Handler.query(request)
    if request.method == "POST":
        return Handler.add(request)
    if request.method == "DELETE":
        return Handler.delete(request)
    if request.method == "PUT":
        return Handler.update(request)


# 返回指定视图

def dispatcher_project(request):
    return _common_dispatcher(request, ProjectHandler)

@login_required
def dispatcher_module(request):
    return _common_dispatcher(request, ModuleHandler)


def dispatcher_env(request):
    return _common_dispatcher(request, EnvHandler)


def dispatcher_case(request):
    return _common_dispatcher(request, CaseHandler)


def dispatcher_step(request):
    return _common_dispatcher(request, StepHandler)


# @csrf_exempt  #增加装饰器跳过csrf验证
def dispatcher_httpapi(request):
    return _common_dispatcher(request, HttpApiHandler)


def dispatcher_tag(request):
    return _common_dispatcher(request, TagHandler)


def dispatcher_plan(request):
    return _common_dispatcher(request, PlanHandler)


def dispatcher_run(request):
    return PlanHandler.run(request)  # 直接返回


def dispatcher_result(request):
    return _common_dispatcher(request, ResultHandler)

def dispatcher_user(request):
    return _common_dispatcher(request, UserHandler)
