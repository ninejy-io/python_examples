# Only use on linux/unix system
import pexpect


def login_ssh_password(host="127.0.0.1", port=22, user="root", password="123456"):
    ssh = pexpect.spawn("ssh -p {} {}@{}".format(port, user, host))
    i = ssh.expect(['password:', 'continue connecting (yes/no)?'], timeout=5)
    if i == 0:
        ssh.sendline(password)
    elif i == 1:
        ssh.sendline("yes\n")
        ssh.expect("password: ")
        ssh.sendline(password)
    index = ssh.expect(["#", pexpect.EOF, pexpect.TIMEOUT])

    if index == 0:
        print("logging in as root!")
        # ssh.interact()
    elif index == 1:
        print("logging in as non-root!")
    elif index == 2:
        print("logging process exit...")
    elif index == 3:
        print("logging timeout exit")


def login_ssh_key():
    pass


if __name__ == '__main__':
    login_ssh_password(user='cjy', password='wobuxianggaosunimima')
