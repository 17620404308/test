import ddt
import unittest
from api.users import Users
from common.logger import log
from common.read_excel import excelUtil
ddt_data = excelUtil.read_excel()

@ddt.ddt
class TestRegister(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = Users()


    @classmethod
    def tearDownClass(cls):
        pass

    @ddt.data(*ddt_data)
    # @ddt.unpack
    def test_register(self, dict_data):
        """测试数据：{0}"""
        description, userId, username, passwd ,sex,tel,addr= dict_data["description"], dict_data["userId"],  dict_data["username"], dict_data["passwd"],dict_data['sex'],dict_data['tel'],dict_data=['addr']
        print(description)
        print(userId)
        result = self.user.user_register(username, passwd,sex,tel,addr)
        log.logger.debug("【用例名】 {} == >> 用户ID ：{}, 用户名 ：{}，密码 ：{}".format(description, userId, username, passwd))
        log.logger.debug("error_code ==>> 期望结果：{}， 实际结果：{}".format(0, result["error_code"]))
        try:
            self.assertEqual(result["code"], 0)
            # self.assertEqual(result["msg"]["userId"], int(userId))
            log.logger.debug("登录成功")
        except AssertionError as e:
            log.logger.debug("登录失败")
            raise AssertionError

if __name__ == '__main__':
    unittest.main()
