import paramiko


class SshClient:

    def __init__(self, host, port=22, user='root', password=None, keyfile=None):
        # self.ssh = paramiko.SSHClient()
        # self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # self.ssh.connect(hostname=host, port=port, username=user, password=password)
        self.__transport = paramiko.Transport((host, port))
        if password is not None:
            self.__transport.connect(username=user, password=password)
            return
        if keyfile is not None:
            self.__private_key = paramiko.RSAKey.from_private_key_file(keyfile)
            self.__transport.connect(username=user, pkey=self.__private_key)

    def upload(self, local_path, remote_path):
        _sftp = paramiko.SFTPClient.from_transport(self.__transport)
        _sftp.put(local_path, remote_path)
    
    def download(self, remote_path, local_path):
        _sftp = paramiko.SFTPClient.from_transport(self.__transport)
        _sftp.get(remote_path, local_path)

    def cmd(self, cmd):
        _ssh = paramiko.SSHClient()
        _ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        _ssh._transport = self.__transport
        _, stdout, stderr = _ssh.exec_command(cmd)
        _err = stderr.read().decode().strip('\n')
        if not _err:
            result = stdout.read().decode().strip('\n')
            return result
        else:
            return None

    def __del__(self):
        self.__transport.close()


sc = SshClient('127.0.0.1', 22, 'root',  keyfile='/root/.ssh/id_rsa')
sc.upload('example.ini', '/tmp/example.ini')
sc.download('/tmp/example.ini', './123.txt')
print(sc.cmd('ls /home/ -l'))

