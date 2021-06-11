from django.contrib.auth.models import User
from django.test import TestCase
from .models import Project, Module, Case, Step
from .models import HttpApi, Tag, Result, Environment, Plan


# Create your tests here.

class TestM2M(TestCase):
    def setUp(self) -> None:
        # 用户
        self.user = User.objects.create_user(username='admin', password='123456', first_name='管理员')

        # 项目
        self.test_pro = Project.objects.create(name='松勤测试平台', create_by=self.user, admin=self.user)
        # 模块
        self.test_mod = Module.objects.create(name='第三方支付-微信', project=self.test_pro, create_by=self.user)
        # 环境
        self.test_env = Environment.objects.create(desc='阿里云', project=self.test_pro, create_by=self.user)
        # 计划
        self.test_plan = Plan.objects.create(name='生辰纲', environment=self.test_env, create_by=self.user)
        # 标签
        self.test_tag = Tag.objects.create(name='冒烟测试', create_by=self.user)
        # 用例
        self.test_case = Case.objects.create(desc='支付接口用例001', module=self.test_mod, create_by=self.user)
        self.test_case.tags.add(self.test_tag)  # 用例添加标签
        # 步骤
        self.test_step = Step.objects.create(desc='test_step', case=self.test_case, create_by=self.user)
        # 接口
        self.test_api = HttpApi.objects.create(desc='合同新增接口', module=self.test_mod, create_by=self.user)

        # 报告
        self.test_report = Result.objects.create(plan=self.test_plan, create_by=self.user)

    def test_case_step(self):
        # 查询某用例下面的步骤
        steps = self.test_case.step_set.filter()
        Step.objects.create(desc="step2", case=self.test_case, create_by=self.user)
        print(steps)

    def test_case_tag(self):
        tags = self.test_case.tags.all()
        print(tags)

    def test_user_pro(self):
        # 查询项目管理员-正向查询
        user1 = self.test_pro.admin
        print(user1)

        # 反向查询-- 当前用户管理的项目
        # admin 为项目表中，admin 字段的 releate_name
        user2 = self.user.admin.all()
        print(user2)

    def test_iexact_query(self):
        setps = Step.objects.filter(desc__iexact="test_step")
        print(setps)

    def test_tags(self):
        # 通过标签查找测试用例
        # self.test_tag.tags_set
        cases = Case.objects.filter(tags__name=self.test_tag)
        print(cases)
