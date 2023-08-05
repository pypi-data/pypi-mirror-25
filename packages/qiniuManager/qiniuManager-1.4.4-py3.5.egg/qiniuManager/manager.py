# coding=utf8
from __future__ import print_function

import os
import sys
import time
import json
import urllib
import sqlite3
import hashlib
import fnmatch

from qiniuManager import progress, http, __version__
from qiniuManager.utils import urlsafe_base64_encode, Auth, str_len
from qiniuManager.crypto import decrypt, encrypt

__all__ = ['Qiniu', 'Config']


def db_ok(func):
    """
    确认数据库可用
    """
    def func_wrapper(self, *args, **kwargs):
        if self.db and self.cursor:
            return func(self, *args, **kwargs)
        else:
            print("Failed To Access {}, please check you authority".format(self.config_path).title())
            return ''
    return func_wrapper


def access_ok(func):
    """
    确认qiniu API key可用
    """
    def access_wrap(self, *args, **kwargs):
        if self.access and self.secret:
            return func(self, *args, **kwargs)
        else:
            print("Please Set At Lease one pair of usable access and secret".title())
            return ''
    return access_wrap


def auth(func):
    def auth_ok(self, *args, **kwargs):
        if self.auth:
            return func(self, *args, **kwargs)
        else:
            self.get_auth()
            if not self.auth:
                print("failed to initialize the authorization".title())
                return ''
            else:
                return func(*args, **kwargs)
    return auth_ok


def get_md5(path):
    """
    计算本地文件 md5
    :param path: str => path to file
    :return: str => md5
    """
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
        """
        初始化本地数据库
        """
        try:
            self.db = sqlite3.connect(self.config_path)
            self.cursor = self.db.cursor()
            self.cursor.execute("CREATE TABLE IF NOT EXISTS {} ("
                                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                "access VARCHAR(64) NOT NULL UNIQUE,"
                                "secret VARCHAR(64) NOT NULL, "
                                "x INTEGER NOT NULL DEFAULT 0)".format(self.API_keys))
            self.cursor.execute("CREATE TABLE IF NOT EXISTS {} ("
                                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                "name VARCHAR(50) NOT NULL DEFAULT '',"
                                "alias VARCHAR(50) NOT NULL DEFAULT '',"
                                "as_default INTEGER NOT NULL DEFAULT 0)".format(self.SPACE_ALIAS))
        except Exception as e:
            print(e)

    @db_ok
    def get_one_access(self):
        """
        从本地数据库获取API key，若没有，返回('', '')
        已解密
        :return tuple => ('ak', 'sk')
        """
        self.cursor.execute("select * from {} ".format(self.API_keys))
        fetch = self.cursor.fetchone()
        if not fetch:
            return '', ''
        else:
            return decrypt(fetch[1]) if fetch[3] else fetch[1], \
                   decrypt(fetch[2]) if fetch[3] else fetch[2]

    @db_ok
    def add_access(self, access, secret):
        """
        添加API ak，sk 到本地数据库
        (在数据库可访问的情况下)
        :param access: str => ak
        :param secret: str => sk
        :return: None
        """
        def add_key():
            self.cursor.execute("insert into {} (access, secret, x) "
                                "VALUES ('{}', '{}', 1)".format(self.API_keys, encrypt(access), encrypt(secret)))

        try:
            self.cursor.execute("delete from {}".format(self.API_keys))
            add_key()
        except:
            """
            旧版本SQLite处理
            """
            self.cursor.execute("drop table {}".format(self.API_keys))
            self.init_db()
            add_key()

    @db_ok
    def set_space(self, space, alias=''):
        """
        设置某存储空间为默认访问空间
        或
        添加新的存储空间并设置为默认访问空间
        :param space: str => 存储空间名
        :param alias: str => 关联域名，测试域名
        :return: None
        """
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

    @db_ok
    def get_space(self, space_name):
        """
        获取本地数据库中指定空间信息
        :param space_name: str
        :return:
        """
        self.cursor.execute("select name, alias from {} WHERE name = '{}'".format(self.SPACE_ALIAS, space_name))
        result = self.cursor.fetchone()
        if result:
            return result
        return '', ''

    @db_ok
    def remove_space(self, space_name):
        """
        删除本地数据库中存储的空间名，
        可能删除默认空间名，需要手动重新设置默认空间
        由于空间误删后恢复的可能性很大，没有进一步获取用户的确认信息，需要使用者考虑清楚
        :param space_name: str
        :return None
        """
        self.cursor.execute("delete from {} WHERE name = '{}'".format(self.SPACE_ALIAS, space_name))

    @db_ok
    def get_space_list(self):
        """
        获取本地已经存储的空间列表
        :return: list
        """
        self.cursor.execute("select name, alias from {}".format(self.SPACE_ALIAS))
        return self.cursor.fetchall()

    @db_ok
    def get_default_space(self):
        """
        获取默认存储空间
        :return: tuple
        """
        self.cursor.execute("select name, alias from {} WHERE as_default = 1".format(self.SPACE_ALIAS))
        result = self.cursor.fetchone()
        if result:
            return result
        return '', ''

    def __del__(self):
        if self.db:
            """一次性commit"""
            self.db.commit()
            self.db.close()


class Qiniu(object):
    """
    七牛云资源管理
    """
    def __init__(self):
        self.config = Config()
        self.access, self.secret = self.config.get_one_access()
        self.auth = None
        self.checked_spaces = set()
        self.COL_WIDTH = 35
        self.total_size = 0

        self.prepared = False
        self.pre_upload_info = None
        self.progressed = 0
        self.total = 0
        self.title = ''
        self.file_handle = None
        self.block_status = []
        self.default_space, self.default_alias = self.config.get_default_space()

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
        """
        输出七牛云请求调试信息
        :param feed: SockFeed => 响应
        :return: None
        """
        # ENV
        print("\033[01;33mEnv:\033[00m")
        print("\n".join(["\033[01;31m{}\033[00m {}".format(i, j) for i, j in [('Tool Ver.', __version__),
                                                                              ('Py Ver.', sys.version)]]))
        # HTTP Response
        print("\033[01;33mResponse:\033[00m")
        print('{}'.format(feed.head))
        print("\n".join(["{} : {}".format(i, feed.header[i]) for i in feed.header]))
        # HTTP entity
        print('\n{}'.format(feed.data), "\n\033[01;33mEOF\033[00m")

    def next_space(self):
        """
        获取下一个需要尝试查找的空间
        :return: str => 空间名称
        """
        res = filter(lambda x: x[0] not in self.checked_spaces, self.config.get_space_list())
        if res:
            if filter.__class__ is type:
                # py3
                return list(res)[0][0]
            return res[0][0]

    @auth
    def export_download_links(self, space=None):
        """
        导出下载链接，包括私有空间，默认输出链接到终端，可重定向到其他文件
        :param space: str => 需要导出的空间名称
        :return: 私有链接地址
        """
        if not space:
            space, alias = self.default_space, self.default_alias

        info, data = self.__get_list_in_space(space, mute=True)
        if not info:
            return True, "\r\n".join([self.private_download_link(i['key'].encode('utf8'), space) for i in data])
        return False, info

    @auth
    def regular_download_link(self, target, space=None):
        """
        视空间为开放公开空间，返回已编码的链接
        不会检查该文件是否存在
        :param target: str => 空间中的文件名
        :param space: str => 指定空间名，否则为默认空间
        :return: str => 下载链接
        """
        if not space:
            space, alias = self.default_space, self.default_alias
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
        """
        获取私有下载链接，1小时有效
        :param target: str => 文件名
        :param space: str => 指定空间名，否则为默认空间
        :return: str => 私有下载链接
        """
        link = self.regular_download_link(target, space)
        private_link = self.auth.private_download_url(link, expires=3600)
        return private_link

    @auth
    def download(self, target, space=None, directory=None, is_debug=False):
        """
        调用进度条，下载文件
        :param target: str => 文件名
        :param space: str => 指定空间名，否则为默认空间
        :param directory: str => 下载到指定目录, 相对目录或绝对目录
        :param is_debug: bool => 是否输出调试信息
        :return: None
        """
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
            space = self.default_space
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
        """
        删除指定空间中文件
        :param target: str => 文件名
        :param space: str => 指定空间或默认空间
        :return: None
        """
        if not space:
            space = self.default_space
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
        """
        检查单个文件`详细`信息
        :param target: str => 文件名
        :param space: str => 指定空间或默认空间开始往下查找
        :param is_debug: bool => 是否输出调试信息
        :return: None
        """
        if not space:
            space = self.default_space
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
    def list(self, space=None, reverse=True, by_date=True,
             is_debug=False, get_sum=True, find_pattern=None,
             greater=None, littler=None):
        """
        列出指定空间或默认空间中的所有文件
        :param space: str => 指定空间或默认空间
        :param reverse: bool => 反向排序
        :param by_date: bool => 默认按时间排序，否则按大小排序
        :param is_debug: bool => 是否输出调试信息
        :param get_sum: bool => 是否计算文件总大小
        :param find_pattern: str => 文件查找正则
        :param greater: int => 文件大小底线
        :param littler: int => 文件大小高线
        :return: (状态码, 输出到终端的字符串)
        """
        if not space:
            space = self.default_space
        _, data = self.__get_list_in_space(space, is_debug=is_debug, mute=True)

        if data:
            if by_date:
                def sort_tool(x):
                    return x['putTime']
            else:
                def sort_tool(x):
                    return x['fsize']

            if greater is not None:
                chew = sorted(filter(lambda x: x['fsize'] >= greater, data),
                              key=sort_tool, reverse=reverse)

            elif littler is not None:
                chew = sorted(filter(lambda x: x['fsize'] <= littler, data),
                              key=sort_tool, reverse=reverse)

            else:
                chew = sorted(filter(lambda x: fnmatch.fnmatch(x['key'], u"{}".format(find_pattern)), data)
                              if find_pattern else data, key=sort_tool, reverse=reverse)

            for i in chew:
                self.total_size += i['fsize']

            tmp = "\r\n".join(["  {}  {}  {}".format(i['key'],
                                                     '·' * (self.COL_WIDTH - str_len(u"{}".format(i['key']))),
                                                     http.unit_change(i['fsize']))
                               for i in chew])
            if tmp:
                ret = "\033[01;32m{}\033[00m\r\n".format(space) + tmp
            else:
                return True, ''

            if get_sum:

                ret += "\r\n\r\n  \033[01;31m{}\033[00m  \033[01;32m{}\033[00m  \033[01;31m{}\033[00m".format(
                    'Total',
                    '·' * (self.COL_WIDTH - len('total')),
                    http.unit_change(self.total_size))
            return True, ret
        else:
            return False, "There is no file in \033[01;31m{}\033[00m".format(space)

    @auth
    def list_all(self, reverse=True, by_date=True, find_pattern=None,
                 greater=None, littler=None):
        """
        列出当前数据库中存储的所有空间的文件列表，统计总大小
        :param reverse: bool => 是否在单个空间中反向排序
        :param by_date: bool => 是否在单个空间中按照时间排序，否则按大小排序
        :param find_pattern: str => 文件查找正则
        :param greater: int => 文件大小底线
        :param littler: int => 文件大小高线
        """
        spaces = self.config.get_space_list()
        if not spaces:
            return False, "没有保存任何空间信息"

        if find_pattern or greater or littler:
            chew = []
            for i in spaces:
                state, result = self.list(space=i[0], reverse=reverse,
                                          by_date=by_date, get_sum=False,
                                          find_pattern=find_pattern,
                                          greater=greater, littler=littler)
                if state and result or not state and result:
                    chew.append(result)

        else:
            chew = [self.list(space=i[0], reverse=reverse, by_date=by_date, get_sum=False)[1] for i in spaces]

        if chew:
            return True, "\r\n\r\n".join(chew) + "\r\n\r\n  \033[01;31m{}\033[00m  \033[01;32m{}\033[00m " \
                                                 " \033[01;31m{}\033[00m".format('Total',
                                                                                 '·' * (self.COL_WIDTH - len('total')),
                                                                                 http.unit_change(self.total_size))
        else:
            return False, "空无一物"

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
            # print("No such space as \033[01;31m{}\033[00m".format(space))
            return "No such space as \033[01;31m{}\033[00m".format(space), []
        data = json.loads(feed.data)
        if 'error' in data:
            return "Error Occur: \033[01;31m{}\033[00m @\033[01;35m{}\033[00m".format(data['error'], space), []
        else:
            return '', data['items']

    @access_ok
    def get_auth(self):
        """
        计算授权码
        :return: auth
        """
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
            space = self.default_space
            token = self.auth.upload_token(space, file_name, 7200)
        # mime_type = self.get_mime_type(path)
        if not space:
            self.progressed = self.total
            self.fail_reason = "默认上传请设置默认空间名"
            return
        md5 = get_md5(path)
        self.file_handle = open(path, 'rb')
        # self.title = file_name
        self.total = os.stat(path).st_size + 2
        self.progressed = 0
        self.pre_upload_info = (file_name, md5, space,
                                token, 0, self.upload_host)
        self.prepared = True

    @progress.bar()
    def upload(self, abs_path, space=None):
        """
        调用进度条，上传文件到指定空间或默认空间
        """
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


