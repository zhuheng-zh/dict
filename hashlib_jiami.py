#加密方法
import  hashlib
passwd="123aamm"
hash=hashlib.md5()#md5对象
hash.update(passwd.encode())#加密
passwd=hash.hexdigest()#获取加密后的密码
print(passwd)