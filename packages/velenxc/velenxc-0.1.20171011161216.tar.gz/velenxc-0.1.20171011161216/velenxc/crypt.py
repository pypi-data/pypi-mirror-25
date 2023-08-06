
import re
import hashlib


class Crypt(object):
    """
    加密类，封装了md5、AES等算法
    """

    @classmethod
    def md5(cls, text):
        """ md5加密算法

        :param text 被加密的文本

        :return 加密的密文
        """
        try:
            text = text.encode(encoding='utf-8')
        except Exception:
            pass

        m = hashlib.md5(text)
        return m.hexdigest()


class ChineseCoding(object):
    """ 对中文做编码，适用于分类特征中的中文分类转成数字分类表达 """

    @classmethod
    def check_chinese(cls, string):
        re_chinese = re.compile(r'[\u4e00-\u9fa5]+')
        if re_chinese.search(string):
            return True

        return False
