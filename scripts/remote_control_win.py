import os
import time
# import cv2
import itchat


send_msg = u"{消息助手}: 暂时无法回复"
usage_msg = u"使用方法: \n1.运行CMD命令: cmd xxx\n" \
            u"例如关机命令: \ncmd shutdown -s -t 0\n"\
            u"2.获取当前用户: cap\n3.启用消息助手: ast\n" \
            u"4.关闭消息助手: astc"

flag = 0
now = time.localtime()
# filename = str(now.tm_day) + str(now.tm_hour) + str(now.tm_min) + str(now.tm_sec) + '.txt'
filename = "xxoo.txt"
fd = open(filename, 'w')


@itchat.msg_register('Text')
def text_reply(msg):
    global flag
    message = msg['Text']
    fromName = msg['FromUserName']
    toName = msg['ToUserName']

    if toName == "filehelper":
        # if message == "cap":
        #     cap = cv2.VideoCapture(0)
        #     ret, img = cap.read()
        #     cv2.imwrite("weixinTemp.jpg", img)
        #     itchat.send('@img@%s'%u'weixinTemp.jpg', 'filehelper')
        #     cap.release()
        if message[0:3] == "cmd":
            os.system(message.strip(message[0:4]))
        if message == "ast":
            flag = 1
            itchat.send("消息助手已开启", "filehelper")
        if message == "astc":
            flag = 0
            itchat.send("消息助手已关闭", "filehelper")
    elif flag == 1:
        itchat.send(send_msg, fromName)
        fd.write(message)
        fd.write("\n")
        fd.flush()


if __name__ == '__main__':
    itchat.auto_login()
    itchat.send(usage_msg, "filehelper")
    itchat.run()