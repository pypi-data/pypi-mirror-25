# coding=utf8
import os

import sys
from result2 import Result, Ok, Err
from utils import getpath
from qiniu import Auth, put_file

class SyncProcessor(object):
    def __init__(self, reponsitoryConfig):
        self.reponsitoryConfig = reponsitoryConfig
        self.q = None

    def auth(self):
        rs = self.reponsitoryConfig.client()
        if rs == Result.Ok:
            self.q = rs()
            return Ok('')
        return Err('Err:Invalid AK and SK')
            

    def iterFiles(self):
        for root, dirs, files in os.walk(self.reponsitoryConfig.abs_path):
            folder_name = os.path.split(root)[-1] if root != self.reponsitoryConfig.abs_path else ""
            for filename in files:
                if "." in filename and (not filename.startswith('.')):
                    file_key = "/".join([folder_name, filename]) if folder_name else filename
                    file_path = os.path.join(root, filename)
                    yield file_key, file_path

    def upfile(self, fk, fn):
        """
        实际上传文件
        :param fk:
        :type fk:
        :param fn:
        :type fn:
        :return: 
        :rtype:
        """
        try:
            token = self.q.upload_token(self.reponsitoryConfig.bucket, fk, 120)
            ret, info = put_file(token, fk, fn)
            assert ret['key'] == fk, 'up faild'
            return Ok('')
        except:
            return Err('Err:upfile %s faild' % fk)


class ReponsitoryConfig(object):
    """
    封装对当前目录的配置读取
    """
    def __init__(self):
        self.abs_path = os.path.abspath('.')
        self.ak = ''
        self.sk = ''
        self. bucket = ''

    def set_lock(self):
        with open(getpath(self.abs_path, '.reps'), 'w') as f:
            f.write('%s %s %s' % (self.ak, self.sk, self.bucket))
            f.close()

    def check_lock(self):
        return os.path.exists(getpath(self.abs_path, '.reps'))

    def new_reponsitory(self, ak, sk, bk):
        """
        新建rep
        :param ak:
        :type ak:
        :param sk:
        :type sk:
        :return:
        :rtype:
        """
        if self.check_lock():
            return Err("Err:Folder already inited!")
        self.ak = ak
        self.sk = sk
        self.bucket = bk
        self.set_lock()
        return Ok('')


    def update_reponsitory(self, ak, sk, bk):
        """
        更新rep
        :param ak:
        :type ak:
        :param sk:
        :type sk:
        :return:
        :rtype:
        """
        if not self.check_lock():
            return Err("Err:Folder not inited!")
        self.ak = ak
        self.sk = sk
        self.bucket = bk
        self.set_lock()
        return Ok('')


    def client(self):
        if self.check_lock():
            with open(getpath(self.abs_path, '.reps'), 'r') as f:
                ak, sk, bk = f.read().split(' ')
                self.ak = ak.strip()
                self.sk = sk.strip()
                self.bucket = bk.strip()
                return Ok(Auth(self.ak, self.sk))
        return Err("Err:Folder not inited!")
            

        



    