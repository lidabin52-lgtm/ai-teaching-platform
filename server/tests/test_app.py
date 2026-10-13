"""
后端单元测试示例
"""
import unittest
import json
import sys
import os

# 将项目根目录添加到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from run import create_app


class TestCaseBase(unittest.TestCase):
    """测试基类"""

    def setUp(self):
        """每个测试方法执行前：创建测试客户端"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def tearDown(self):
        """每个测试方法执行后：清理资源"""
        pass


class HealthCheckTestCase(TestCaseBase):
    """健康检查接口测试"""

    def test_health_check(self):
        """测试健康检查接口返回正常"""
        response = self.client.get('/api/health')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 200)


class AuthTestCase(TestCaseBase):
    """用户认证接口测试"""

    def test_login_missing_params(self):
        """测试登录缺少参数"""
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps({}),
            content_type='application/json',
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)

    def test_register_missing_params(self):
        """测试注册缺少参数"""
        response = self.client.post(
            '/api/auth/register',
            data=json.dumps({}),
            content_type='application/json',
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)


class CourseTestCase(TestCaseBase):
    """课程接口测试"""

    def test_get_course_list(self):
        """测试获取课程列表"""
        response = self.client.get('/api/courses')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('list', data['data'])


if __name__ == '__main__':
    unittest.main()
