# coding=utf8
from __future__ import print_function

import os
import sys
import time
import json
import random
import urllib
import sqlite3
import hashlib
from qiniuManager import progress, http, __version__

# from qiniu import Auth, __version__ as sdk_version
from qiniuManager.utils import urlsafe_base64_encode, Auth, str_len


def db_ok(function):
    def func_wrapper(self, *args, **kwargs):
        if self.db and self.cursor:
            return function(self, *args, **kwargs)
        else:
            print ("Failed To Access {}, please check you authority".format(self.config_path).title())
            return ''
    return func_wrapper


def access_ok(function):
    def access_wrap(self, *args, **kwargs):
        if self.access and self.secret:
            return function(self, *args, **kwargs)
        else:
            print("Please Set At Lease one pair of usable access and secret".title())
            return ''
    return access_wrap


def auth(function):
    def auth_ok(self, *args, **kwargs):
        if self.auth:
            return function(self, *args, **kwargs)
        else:
            self.get_auth()
            if not self.auth:
                print("failed to initialize the authorization".title())
                return ''
            else:
                return function(*args, **kwargs)
    return auth_ok


def get_md5(path):
    if os.path.exists(path):
        hash_md5 = hashlib.md5()
        with open(path, 'rb') as handle:
            for chuck in iter(lambda: handle.read(4096), b""):
                hash_md5.update(chuck)
        return hash_md5.hexdigest()
    else:
        raise IOError


class Config(object):
    def __init__(self):
        self.config_path = os.path.join(os.path.expanduser("~"), '.qiniu.sql')
        self.db = None
        self.cursor = None
        self.API_keys = 'API_keys'
        self.SPACE_ALIAS = 'spaceAlias'
        self.init_db()

    def init_db(self):
        try:
            self.db = sqlite3.connect(self.config_path)
            self.cursor = self.db.cursor()
            self.cursor.execute("CREATE TABLE IF NOT EXISTS {} ("
                                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                "access VARCHAR(64) NOT NULL UNIQUE,"
                                "secret VARCHAR(64) NOT NULL,"
                                "discard INTEGER NOT NULL DEFAULT 0)".format(self.API_keys))
            self.cursor.execute("CREATE TABLE IF NOT EXISTS {} ("
                                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                "name VARCHAR(50) NOT NULL DEFAULT '',"
                                "alias VARCHAR(50) NOT NULL DEFAULT '',"
                                "as_default INTEGER NOT NULL DEFAULT 0)".format(self.SPACE_ALIAS))
        except Exception as e:
            print(e)

    @db_ok
    def get_one_access(self):
        self.cursor.execute("select access, secret from {} WHERE discard = 0".format(self.API_keys))
        result = self.cursor.fetchall()
        if not result:
            return '', ''
        return random.choice(result)

    @db_ok
    def access_list(self, include_discard=True):
        sql = "select * from {} ".format(self.API_keys)
        if not include_discard:
            sql += "where discard = 0"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if not result:
            return None
        return result

    @db_ok
    def add_access(self, access, secret):
        """Though two pair of key pair is allowed, but I hate to operate on this"""
        self.cursor.execute("delete from {}".format(self.API_keys))
        self.cursor.execute("insert into {} (access, secret) "
                            "VALUES ('{}', '{}')".format(self.API_keys, access, secret))

    @db_ok
    def set_space(self, space, alias=''):
        self.cursor.execute("update {} set as_default = 0".format(self.SPACE_ALIAS))
        self.cursor.execute("select id from {} WHERE name = '{}'".format(self.SPACE_ALIAS, space))
        result = self.cursor.fetchone()
        if result:
            if alias:
                self.cursor.execute("update {} set alias = '{}', as_default=1"
                                    " WHERE id = {}".format(self.SPACE_ALIAS, alias, result[0]))
            else:
                self.cursor.execute("update {} set as_default=1 WHERE id = {}".format(self.SPACE_ALIAS,
                                                                                      result[0]))
        else:
            self.cursor.execute("insert into {} (name, alias, as_default)"
                                " VALUES ('{}', '{}', 1)".format(self.SPACE_ALIAS, space, alias))
        return True

    @db_ok
    def get_space(self, space_name):
        self.cursor.execute("select name, alias from {} WHERE name = '{}'".format(self.SPACE_ALIAS, space_name))
        result = self.cursor.fetchone()
        if result:
            return result
        return '', ''

    @db_ok
    def remove_space(self, space_name):
        """default space may be deleted, so you must set the default manually"""
        self.cursor.execute("delete from {} WHERE name = '{}'".format(self.SPACE_ALIAS, space_name))

    @db_ok
    def get_space_list(self):
        self.cursor.execute("select name, alias from {}".format(self.SPACE_ALIAS))
        return self.cursor.fetchall()

    @db_ok
    def get_default_space(self):
        self.cursor.execute("select name, alias from {} WHERE as_default = 1".format(self.SPACE_ALIAS))
        result = self.cursor.fetchone()
        if result:
            return result
        return '', ''

    def __del__(self):
        if self.db:
            self.db.commit()
            self.db.close()


class Qiniu(object):
    """Single Line"""
    def __init__(self):
        self.config = Config()
        self.access, self.secret = self.config.get_one_access()
        self.auth = None
        self.checked_spaces = set()
        self.COL_WIDTH = 35

        self.prepared = False
        self.pre_upload_info = None
        self.progressed = 0
        self.total = 0
        self.title = ''
        self.file_handle = None
        self.block_status = []

        self.start_stamp = 0

        self.state = False
        self.avg_speed = ''
        self.last_failed = None
        self.retry_count = 0
        self.MAX_RETRY = 10
        self.fail_reason = None

        # API restrict
        self.R_BLOCK_SIZE = 4 * 1024 * 1024
        self.list_host = "https://rsf.qbox.me"
        self.manager_host = 'https://rs.qbox.me'
        self.upload_host = 'https://up.qbox.me'
        self.get_auth()

    def __del__(self):
        if self.file_handle:
            self.file_handle.close()

    @staticmethod
    def print_debug(feed):
        # ENV
        print("\033[01;33mEnv:\033[00m")
        print("\n".join(["\033[01;31m{}\033[00m {}".format(i, j) for i, j in [('Py Ver.', sys.version), ('Tool Ver.', __version__)]]))
        # HTTP Response
        print("\033[01;33mResponse:\033[00m")
        print('{}'.format(feed.head))
        print("\n".join(["{} : {}".format(i, feed.header[i]) for i in feed.header]))
        # HTTP entity
        print('\n{}'.format(feed.data), "\n\033[01;33mEOF\033[00m")

    def next_space(self):
        res = filter(lambda x: x[0] not in self.checked_spaces, self.config.get_space_list())
        if res:
            if filter.__class__ is type:
                # py3
                return list(res)[0][0]
            return res[0][0]

    @auth
    def export_download_links(self, space=None):
        if not space:
            space, alias = self.config.get_default_space()

        state, data = self.__get_list_in_space(space, mute=True)
        if state:
            for i in data:
                print(self.private_download_link(i['key'].encode('utf8'), space))

    @auth
    def regular_download_link(self, target, space=None):
        if not space:
            space, alias = self.config.get_default_space()
        else:
            temp_space, alias = self.config.get_space(space)

        if alias:
            host = "http://{}".format(alias)
        else:
            host = "http://{}.qiniudn.com".format(space)
        # link = os.path.join(host, urllib.quote(target))
        if sys.version_info.major == 3:
            from urllib.parse import quote
            return os.path.join(host, quote(target))
        return os.path.join(host, urllib.quote(target))

    @auth
    def private_download_link(self, target, space=None):
        link = self.regular_download_link(target, space)
        private_link = self.auth.private_download_url(link, expires=3600)
        return private_link

    @auth
    def download(self, target, space=None, directory=None, is_debug=False):
        if directory:
            save_path = os.path.join(directory, os.path.basename(target))
        else:
            save_path = os.path.basename(target)
        link = self.private_download_link(target, space)
        downloader = http.HTTPCons(is_debug)
        downloader.request(link)
        feed = http.SockFeed(downloader, 4096)
        start = time.time()
        feed.http_response(save_path)
        if is_debug:
            print("\033[01;33mResponse:\033[00m")
            print('{}'.format(feed.head))
            print("\n".join(["{} : {}".format(i, feed.header[i]) for i in feed.header]))

        if not feed.http_code == 200:
            print("\033[01;31m{}\033[00m not exist !".format(target))
            if feed.file_handle:
                os.unlink(feed.file_handle.name)
            return False
        end = time.time()
        size = int(feed.header.get('Content-Length', 1))
        print("\033[01;31m{}\033[00m downloaded @speed \033[01;32m{}/s\033[00m"
              .format(target,
                      http.unit_change(size / (end - start))))

    @auth
    def rename(self, target, to_target, space=None, is_debug=False):
        """I don't want to move files between buckets,
        so you can not move file to different bucket by default"""
        if not space:
            space = self.config.get_default_space()[0]
        manager_rename = http.HTTPCons(debug=is_debug)
        url = self.manager_host + '/move/{}/{}/force/false'.format(
            urlsafe_base64_encode("{}:{}".format(space, target)),
            urlsafe_base64_encode("{}:{}".format(space, to_target))
        )
        manager_rename.request(url,
                               headers={'Authorization': 'QBox {}'.format(self.auth.token_of_request(url))})
        feed = http.SockFeed(manager_rename)
        feed.disable_progress = True
        feed.http_response()
        data = feed.data
        if 'error' in data:
            data = json.loads(data)
            print("Error Occur: \033[01;31m{}\033[00m".format(data['error']))
        else:
            print("\033[01;31m{}\033[00m now RENAME as \033[01;32m{}\033[00m".format(target, to_target))

    @auth
    def remove(self, target, space=None):
        if not space:
            space = self.config.get_default_space()[0]
        prompt = 'Are You Sure to \033[01;31mDELETE\033[00m `\033[01;32m{}\033[00m` from \033[01;34m{}\033[00m ? y/n '.format(target, space)
        try:
            if sys.version_info.major == 2:
                if not raw_input(prompt).lower().startswith('y'):
                    return False
            else:
                if not input(prompt).lower().startswith('y'):
                    return False
        except:
            return False

        manager_remove = http.HTTPCons()
        url = self.manager_host + '/delete/{}'.format(urlsafe_base64_encode("{}:{}".format(space, target)))
        manager_remove.request(url,
                               headers={'Authorization': 'QBox {}'.format(self.auth.token_of_request(url))})
        feed = http.SockFeed(manager_remove)
        feed.disable_progress = True
        feed.http_response()
        data = feed.data
        if 'error' in data:
            data = json.loads(data)
            print("Error Occur: \033[01;31m{}\033[00m".format(data['error']))
        else:
            print("`\033[01;31m{}\033[00m` DELETED from \033[01;34m{}\033[00m".format(target, space))

    @auth
    def check(self, target, space=None, is_debug=False):
        if not space:
            space = self.config.get_default_space()[0]
        self.checked_spaces.add(space)
        manager_check = http.HTTPCons(is_debug)
        url = self.manager_host + '/stat/{}'.format(urlsafe_base64_encode("{}:{}".format(space, target)))
        manager_check.request(url,
                              headers={'Authorization': 'QBox {}'.format(self.auth.token_of_request(url))})
        feed = http.SockFeed(manager_check)
        feed.disable_progress = True
        feed.http_response()
        if is_debug:
            self.print_debug(feed)

        if not feed.data:
            print("no such file \033[01;31m{}\033[00m in \033[01;32m{}\033[00m".format(target, space))
            nx_space = self.next_space()
            if nx_space:
                return self.check(target, nx_space, is_debug=is_debug)
            return False
        data = json.loads(feed.data)
        if 'error' in data:
            print("Error Occur: \033[01;31m{}\033[00m".format(data['error']))
        else:
            print("  {}  {}  {}".format('Space', '.' * (self.COL_WIDTH - len('Space')), "\033[01;32m{}\033[00m".format(space)))
            print("  {}  {}  {}".format('Filename', '·' * (self.COL_WIDTH - len('filename')), target))
            print("  {}  {}  {} ({})".format('Size', '·' * (self.COL_WIDTH - len('size')),
                                             "\033[01;37m{}\033[00m".format(http.unit_change(data['fsize'])),
                                             data['fsize']))
            print("  {}  {}  {}".format('MimeType',  '·' * (self.COL_WIDTH - len('MimeType')), data['mimeType']))
            print("  {}  {}  {} ({})".format('Date', '·' * (self.COL_WIDTH - len('date')),
                                             "\033[01;37m{}\033[00m".format(time.strftime('%Y-%m-%d %H:%M:%S',
                                                                            time.localtime(data['putTime']/10000000))),
                                             data['putTime']))

    @auth
    def list(self, space=None, is_debug=False):
        # TODO:: 分页支持
        if not space:
            space = self.config.get_default_space()[0]
        state, data = self.__get_list_in_space(space, is_debug=is_debug, mute=True)

        if state and data:
            total_size = 0
            print("\033[01;32m{}\033[00m".format(space))
            for i in sorted(data, key=lambda x: x['putTime'], reverse=True):
                print("  {}  {}  {}".format(i['key'],
                                            '·' * (self.COL_WIDTH - str_len(u"{}".format(i['key']))),
                                            http.unit_change(i['fsize'])))
                total_size += i['fsize']
            print("\n  \033[01;31m{}\033[00m  \033[01;32m{}\033[00m  \033[01;31m{}\033[00m".format(
                'Total',
                '·' * (self.COL_WIDTH - len('total')),
                http.unit_change(total_size)))
        elif state and not data:
            print("There is no file in \033[01;31m{}\033[00m".format(space))

    @auth
    def list_all(self):
        spaces = self.config.get_space_list()
        if not spaces:
            print("I don't Know any of them")
            return False

        total_size = 0
        for i in spaces:
            state, data = self.__get_list_in_space(i[0], mute=True)
            if state:
                if data:
                    print("\033[01;32m{}\033[00m".format(i[0]))
                    for target in sorted(data, key=lambda x: x['putTime'], reverse=True):
                        print("  {}  {}  {}".format(target['key'],
                                                    '·' * (self.COL_WIDTH - str_len(u'{}'.format(target['key']))),
                                                    http.unit_change(target['fsize'])))
                        total_size += target['fsize']
        print("\n  \033[01;31m{}\033[00m  \033[01;32m{}\033[00m  \033[01;31m{}\033[00m".format(
            'Total',
            '·' * (self.COL_WIDTH - len('total')),
            http.unit_change(total_size)))

    def __get_list_in_space(self, space, mute=False, is_debug=False):
        space_list = http.HTTPCons(is_debug)
        url = self.list_host + '/list?bucket={}'.format(space)
        space_list.request(url,
                           headers={'Authorization': 'QBox {}'.format(self.auth.token_of_request(url))})
        feed = http.SockFeed(space_list, 1024)
        feed.disable_progress = mute
        feed.http_response()
        if is_debug:
            self.print_debug(feed)

        if not feed.data:
            print("No such space as \033[01;31m{}\033[00m".format(space))
            return False, []
        data = json.loads(feed.data)
        if 'error' in data:
            print("Error Occur: \033[01;31m{}\033[00m @\033[01;35m{}\033[00m".format(data['error'], space))
            return False, []
        else:
            return True, data['items']

    @access_ok
    def get_auth(self):
        try:
            self.auth = Auth(self.access, self.secret)
        except:
            self.auth = None

    def __make_url(self, path, **kwargs):
        url = list(['{0}/mkfile/{1}'.format(self.pre_upload_info[-1], os.stat(path).st_size)])
        key = os.path.basename(path)
        url.append('key/{0}'.format(urlsafe_base64_encode(key)))
        url.append('fname/{0}'.format(urlsafe_base64_encode(key)))

        if kwargs:
            for k, v in kwargs.items():
                url.append('{0}/{1}'.format(k, urlsafe_base64_encode(v)))
        url = '/'.join(url)
        # print url
        return url

    @auth
    def __pre_upload(self, path, space=None):
        file_name = os.path.basename(path)
        if space:
            token = self.auth.upload_token(space, file_name, 7200)
        else:
            space, _ = self.config.get_default_space()
            token = self.auth.upload_token(space, file_name, 7200)
        # mime_type = self.get_mime_type(path)
        md5 = get_md5(path)
        self.file_handle = open(path, 'rb')
        # self.title = file_name
        print(file_name)
        self.total = os.stat(path).st_size + 2
        self.progressed = 0
        self.pre_upload_info = (file_name, md5, space,
                                token, 0, self.upload_host)
        self.prepared = True

    @progress.bar(100)
    def upload(self, abs_path, space=None):
        """upload data"""
        if not self.prepared:
            self.__pre_upload(abs_path, space)
            self.start_stamp = time.time()
        if not self.last_failed:
            data = self.file_handle.read(self.R_BLOCK_SIZE)
            self.retry_count = 0
        else:
            data = self.last_failed
            self.retry_count += 1
            if self.retry_count > self.MAX_RETRY:
                self.progressed = self.total
                self.fail_reason = "超过最大重传限制"
                return False
        if not data:
            # total submit
            file_url = self.__make_url(abs_path)
            mkfile = http.HTTPCons()
            mkfile.request(file_url, 'POST',
                           {'Authorization': 'UpToken {}'.format(self.pre_upload_info[3])},
                           data=','.join(self.block_status))
            feed = http.SockFeed(mkfile)
            feed.disable_progress = True
            feed.http_response()
            if not feed.data:
                self.progressed = self.total
                self.fail_reason = "服务器未响应合并操作"
                return False
            try:
                data = json.loads(feed.data)
                avg_speed = http.unit_change(self.progressed / (time.time() - self.start_stamp))
                self.progressed = self.total
                if data.get('key', '') == self.pre_upload_info[0]:
                    self.state = True
                    self.avg_speed = '{}/s'.format(avg_speed)
                    return True
            except:
                self.fail_reason = "合并操作响应无效"
            return False

        # block upload
        done = False
        try:
            labor = http.HTTPCons()
            labor.request('{0}/mkblk/{1}'.format(self.pre_upload_info[-1], len(data)),
                          'POST',
                          {'Authorization': 'UpToken {}'.format(self.pre_upload_info[3])},
                          data=data)
            feed = http.SockFeed(labor)
            feed.disable_progress = True
            feed.http_response()
            if '401' in feed.head:
                self.progressed = self.total
                self.fail_reason = "上传凭证无效"
                return False
            self.block_status.append(json.loads(feed.data).get('ctx'))
            done = True
            self.last_failed = None
        except:
            self.last_failed = data

        if done:
            self.progressed += len(data)
        # print self.progressed, self.total


