#coding=utf-8
from __future__ import division
from __future__ import print_function
import os
import sys
import paramiko
import stat
import time
import datetime
import hashlib
import threading

class ssher(object):
    #user:passwd@127.0.0.1:22
    def __init__(self, host,remote_filename = None):
        self.client = None
        self.port = 22
        self.user,self.host = tuple(host.split('@'))
        self.user,self.passwd = tuple(self.user.split(':'))
        if (len(self.host.split(':')) == 2):
            self.port = int(self.host.split(':')[1])   
            self.host = self.host.split(':')[0]
        self.remote_file_size = None
        self.last_line = b''
        self.remote_filename = remote_filename
        self.client = None
        self.sftp_client = None
    def __del__(self):
        try:
            self.sftp_client.close()
        except:
            pass
        try:
            self.client.close()
        except:
            pass

    
    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.host,22,self.user,self.passwd)
        self.sftp_client = self.client.open_sftp() #paramiko.SFTPClient.from_transport(self.client.get_transport())
        return self.client
    def close(self):
        if (self.sftp_client != None):
            self.sftp_client.close()
            self.sftp_client = None
        if (self.client != None):
            self.client.close()
            self.client = None        

    def exist(self,remote_path):
        try:          
            return stat.S_ISDIR(self.sftp_client.lstat(remote_path).st_mode) 
        except IOError:
            return False
    def mkdir(self,remote_path):
        try:
            return self.sftp_client.mkdir(remote_path)
        except:
            return False
    def mkdirs(self,remote_path):
        r = remote_path.split('/')
        for i in range(2,len(r) + 1):
            if self.exist('/'.join(r[0:i])) == False:
                self.mkdir('/'.join(r[0:i]))
    
    def execute(self,cmd,fnout):
        if (not self.client):
            self.connect()
        chan = self.client.get_transport().open_channel(kind='session')
        print('\rexec :{0}'.format(cmd))
        chan.get_pty()  
        chan.exec_command(cmd)

        buff_size = 1024
        stdout = b""
        stderr = b""
        while not chan.exit_status_ready():
            if chan.recv_ready():
                t = chan.recv(buff_size)
                stdout += t
                if (fnout != None):
                    print(t, end="")
            if chan.recv_stderr_ready():
                t = chan.recv_stderr(buff_size)
                if (fnout != None):
                    print(t, end="")
                stderr += t
            time.sleep(0.1)
        retcode = chan.recv_exit_status()
        while chan.recv_ready():
            t = chan.recv(buff_size)
            if (fnout != None):
                print(t, end="")
            stdout += t
        while chan.recv_stderr_ready():
            t = chan.recv_stderr(buff_size)
            if (fnout != None):
                print(t, end="")
            stderr += t

        chan.close()
        return retcode, stdout, stderr

    def execute2(self,cmd,fnout):
        if (not self.client):
            self.connect()
        chan = self.client.get_transport().open_channel(kind='session')
        print('exec :{0}'.format(cmd))
        chan.get_pty()  
        chan.exec_command(cmd)

        buff_size = 1024
        stdout = b""
        stderr = b""
        while not chan.exit_status_ready():
            if chan.recv_ready():
                t = chan.recv(buff_size)
                stdout += t
                if (fnout != None):
                    print(t, end="")
                yield (0,t)
            if chan.recv_stderr_ready():
                t = chan.recv_stderr(buff_size)
                if (fnout != None):
                    print(t, end="")
                stderr += t
                yield (0,t)
            time.sleep(0.1)
        retcode = chan.recv_exit_status()
        while chan.recv_ready():
            t = chan.recv(buff_size)
            if (fnout != None):
                print(t, end="")
            stdout += t
            yield (0,t)
        while chan.recv_stderr_ready():
            t = chan.recv_stderr(buff_size)
            if (fnout != None):
                print(t, end="")
            stderr += t
            yield (0,t)

        chan.close()
        yield (1,retcode)


    #[(local ,remote)]
    def sendfiles(self,sendfiles,check = False):
        def callback2(size, file_size):
            pass       
        bakcup = None
        nw = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        for (local,remote) in sendfiles:
            if self.exist(os.path.dirname(remote)) == False:
                self.mkdirs(os.path.dirname(remote))
            if bakcup != None and self.exist(os.path.dirname(bakcup)) == False:
                self.mkdirs(os.path.dirname(bakcup))
            if (bakcup != None):
                self.execute('sudo cp {0} {1}_{2}'.format(remote,bakcup,nw))
            print('sftp :{0}'.format(remote))
            sys.stdout.flush()
            self.sftp_client.put(local,remote,callback=callback2)
            if (check == True):
                l_md5 = local_md5sum(local)
                r_md5 = remote_md5sum(ssh,remote)
                if (l_md5 != r_md5):
                    print('sftp {3} fail:local:{0},remote:{1}'.format(l_md5,r_md5,v))
        
    def local_md5sum(self,filename):     
        fd = open(filename,"rb")  
        fcont = fd.read()  
        fd.close()           
        fmd5 = hashlib.md5(fcont)  
        return fmd5.hexdigest()

    def remote_md5sum(self,filename):
        retcode, stdout, stderr = self.execute('md5sum {0}'.format(filename))
        if (retcode == 0):
            return stdout.split("  ")[0]
        else:
            return None

    def listdir(self,folder,extensions):
        ls = os.listdir(folder)
        #os.path.isfile(folder + "/" + x)
        if extensions:
            return [x for x in ls if  os.path.splitext(x)[1][1:] in extensions]
        else:
            return ls

    def listdir2(self,folder):
        dirname = os.path.dirname(folder)
        basename = os.path.basename(folder)
        ls = os.listdir(dirname)
        if extensions:
            return [x for x in ls if  os.path.splitext(x)[1][1:] in extensions]
        else:
            return ls   
    def cat(self,path,yd = True):
        if not self.sftp_client:
            self.connect()
        fstat = self.sftp_client.stat(path)
        remote_file = self.sftp_client.open(path, 'r')
        sz = 0
        last_line = b''
        rt = ''
        while sz > 0:
            last_line = last_line + remote_file.read(1024)
            sz = sz - 1024
            line = ''
            try:
                line = last_line.decode()
            except Exception as e:
                print(e)
            last_line = b''
            if (yd):
                yield line
            else:
                rt = rt + line
        remote_file.close()
        if (yd == False):
            return rt
        
    def tail(self):
        if not self.sftp_client:
            self.connect()
        fstat = self.sftp_client.stat(self.remote_filename)
        if self.remote_file_size is not None:
            if self.remote_file_size < fstat.st_size:
                remote_file = self.sftp_client.open(self.remote_filename, 'r')
                remote_file.seek(self.remote_file_size, 0)
                sz = remote_file.stat().st_size - self.remote_file_size
                self.remote_file_size = remote_file.stat().st_size
                while sz > 0:
                    self.last_line = self.last_line + remote_file.read(1024)
                    sz = sz - 1024
                    line = ''
                    try:
                        line = self.last_line.decode()
                    except Exception as e:
                        print(e)
                    self.last_line = b''
                    yield line
                    
                remote_file.close()
        else:
            self.remote_file_size = fstat.st_size - 5000
            if (self.remote_file_size < 0):
                self.remote_file_size = 0

