"""testplatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import dispatcher_project, dispatcher_module, dispatcher_env
from .views import dispatcher_case
from .views import dispatcher_httpapi, dispatcher_result, dispatcher_run, dispatcher_plan, \
    dispatcher_step
from .views import dispatcher_tag
from .views import login, logout, register, current_user, dispatcher_user

urlpatterns = [
    path('project/', dispatcher_project),
    path('module/', dispatcher_module),
    path('env/', dispatcher_env),
    path('case/', dispatcher_case),

    path('step/', dispatcher_step),
    path('tag/', dispatcher_tag),
    path('httpapi/', dispatcher_httpapi),
    path('plan/', dispatcher_plan),
    path('result/', dispatcher_result),

    # 执行计划
    path('run/plan/', dispatcher_run),

    # 用户相关
    path('user/login/', login),
    path('user/logout/', logout),
    path('user/register/', register),
    path('user/current/', current_user),
    path('user/list/', dispatcher_user),
]
