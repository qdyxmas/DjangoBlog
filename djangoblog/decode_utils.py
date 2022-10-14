import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class AesEcbCrypto:
    @staticmethod
    def str_to_bytes(s):
        """
        字符串转 byte 数组, utf8 编码
        """
        return s.encode('utf8')

    @staticmethod
    def bytes_to_str(bs):
        """
        byte 数组转字符串, utf8 编码
        """
        return bs.decode('utf8')

    @staticmethod
    def hexstr_to_bytes(s):
        """
        16进制字符串转换成bytes
        """
        return bytes.fromhex(s)

    @staticmethod
    def pad(s):
        """
        填充数据
        """
        s_encode = s.encode("utf8")
        bs = AES.block_size
        return s + (bs - len(s_encode) % bs) * chr(bs - len(s_encode) % bs)

    @staticmethod
    def unpad(s):
        """
        去掉填充数据
        """
        return s[0:-ord(s[-1])]

    def __init__(self, key='01107d949e15811e9315348178904ee4'):
        # 初始化加密器
        self.aes = AES.new(self.hexstr_to_bytes(key), AES.MODE_ECB)

    def encrypt(self, text):
        # 字符串转 byte 数组
        text_bytes = self.str_to_bytes(self.pad(text))
        # 加密
        encrypted_text = self.bytes_to_str(base64.encodebytes(self.aes.encrypt(text_bytes))).replace('\n', '')
        return encrypted_text

    def decrypt(self, text):
        # 字符串转 byte 数组
        text_base64 = self.str_to_bytes(self.pad(text))
        # base64 byte 数组 转 byte 数组
        text_bytes = base64.decodebytes(text_base64)
        # 解密
        decrypted_text = self.unpad(self.bytes_to_str(self.aes.decrypt(text_bytes)))
        return decrypted_text

aes_ecb = AesEcbCrypto()
if __name__ == '__main__':
    KEY = '01107d949e15811e9315348178904ee4'
    aes_ecb = AesEcbCrypto(KEY)
    data = u'''aa'''
    print(aes_ecb.encrypt(data))
    data = """"""
    # print(aes_ecb.decrypt('Y4kSyfQl4VOApsnxkmvunqFEwpI1j1bxMW8bqxqAgZLxOdnxvfB8aZAFza8h3re5vqtGxN+1/aj3KBkHPkVu2N+seNq0Bq4FFo0P+/jTvKp4OsikYad4TDR48u0gfVw90slLCwvyUnGlP+xBpCxiszhexXqN4946NsBbnhg8cIeTWWwVIivKXgIlJ8Oa5p6W+rjJvxwZ4MidBiNo3kGqqg1N89f4SvcFvPHdJeAsDs4='))
