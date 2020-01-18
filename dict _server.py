"""
dict 服务端
功能:请求逻辑处理
并发模型：tcp 多进程并发
"""
import time
import  dict_db
from socket import  *
from  multiprocessing import  Process
import  sys
import  signal
#全局变量
HOST='0.0.0.0'
PORT=10086
ADDR=(HOST,PORT)
#创建数据库连接
db=dict_db.Database()
#处理注册
def do_register(connfd,name,passwd):
    if db.register(name,passwd):
        connfd.send(b'OK')
    else:
        connfd.send(b'FAIL')
#处理登录
def do_login(connfd,name,passwd):
    if db.login(name,passwd):
        connfd.send(b'OK')
    else:
        connfd.send(b'FAIL')
#处理查单词
def do_query(connfd,name,word):#查询单词
    db.insert_history(name,word)#插入历史记录
    #data->mean/None
    data=db.query(word)
    if data:
        msg="%s:%s"%(word,data)
        connfd.send(msg.encode())
    else:
        connfd.send("没有该单词".encode())
#查历史记录
def do_history(connfd,name):
    # data=db.history(name)
    # if data:
    #     connfd.send(str(data).encode())
    # else:
    #     connfd.send("未查询到历史记录".encode())
    result=db.history(name)#获取历史记录
    if not result:
        connfd.send(b'FAIL')
        return
    else:
        connfd.send(b'OK')
        for r in result:
            time.sleep(0.1)
            msg="%s  %s   \t%s"%r
            connfd.send(msg.encode())
        time.sleep(0.1)
        connfd.send(b'##')
def handle(connfd):
    while True:
        request=connfd.recv(1024).decode()
        tmp=request.split(' ')
        if not request or tmp[0]=='E':
            return
        elif tmp[0]=='R':
            do_register(connfd,tmp[1],tmp[2])
        elif tmp[0]=='L':
            do_login(connfd,tmp[1],tmp[2])
        elif tmp[0]=='Q':
            # Q name word
            do_query(connfd,tmp[1],tmp[2])
        elif tmp[0]=='H':
            # H name
            do_history(connfd,tmp[1])
def main():
    #创建监听套接字
    s=socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(3)
    #处理僵尸进程
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    #循环等待处理客户端连接
    print("Listen then port 10086")
    while True:
        try:
            c,addr=s.accept()
            print("Connect from ",addr)
        except KeyboardInterrupt:
            s.close()
            db.close()
            sys.exit("退出服务端")
        except Exception as  e:
            print(e)
            continue
        #为客户端创建进程
        p=Process(target=handle,args=(c,))
        p.start()

if __name__ == '__main__':
    main()