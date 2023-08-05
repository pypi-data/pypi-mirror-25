#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
2017/08/31 created by sillyemperor@163.com
python disconfig client version 0.0.0.1
实现逻辑见：http://disconf.readthedocs.io/zh_CN/latest/design/src/disconf-client%E8%AF%A6%E7%BB%86%E8%AE%BE%E8%AE%A1%E6%96%87%E6%A1%A3.html

按照Disconf的模型，每个Client代表一套app+evn+version。
配置数据分为文件（file）和项目（item）。

配置数据分别以三种状态存放，分别是：
代码：客户代码通过调用辅助函数conf_file和conf_item将配置项注册到内存，系统需要的配置项都必须注册
本地文件：如果提供本地文件路径，则运行系统在文件系统中缓存配置数据
Disconf Web：最新配置项
内存：运行时使用

加载顺序：
1 首先加载代码，注册配置项
2 尝试加载本地文件，更新内存
3 尝试加载WEB端数据，更新内存和文件
4 尝试开始监听

"""
import os.path, os
import http
import json
from kazoo.client import KazooClient
import socket
import uuid
import logging
import functools
import traceback
from urllib2 import HTTPError


class FileWatcher:
    def __init__(self, client, file_name, file_data):
        self.client = client
        self.file_name = file_name
        self.file_data = file_data

    def __call__(self, event):
        print self.file_name, event
        self.client.update_file_from_remote(self.file_name)
        self.client.watch_file(self.file_name, self.file_data)


class ItemWatcher:
    def __init__(self, client, item, value):
        self.client = client
        self.item = item
        self.value = value

    def __call__(self, event):
        print self.item, event
        self.client.update_item_from_remote(self.item)
        self.client.watch_item(self.item, self.value)


def parse_properties(lines):
    for l in lines:
        l  =l.strip()
        if not l:
            continue
        if l.startswith('#'):
            continue
        idx = l.find('=')
        if idx < 0:
            continue
        key, value = l[:idx].strip(), l[idx+1:].strip()
        yield key, value


#简易加锁文件写入
class LockedFileWriter:
    """
    常规使用方式
    try:
        with LockedFileWriter('./hello.txt') as fp:
          fp.write('hello')
    except:
      pass
    """
    def __init__(self, file, mode):
        self.file = file
        self.open_mode = mode
        self.acquire()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def acquire(self):
        os.mkdir(self.file+'.lock')

    def release(self):
        try:
            os.rmdir(self.file+'.lock')
        except:
            traceback.print_stack()

    def write(self, value):
        with open(self.file, self.open_mode) as fp:
            fp.write(value)


# 加锁写文件，辅助函数
def lock_write(file, value, mode='w+'):
    try:
        with LockedFileWriter(file, mode=mode) as fp:
            fp.write(value)
    except:
        pass


def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


class Client:
    def __init__(self):
        self.files = {}
        self.items = {}
        self.cache = {}

    def __getitem__(self, key):
        return key in self.cache and self.cache[key] or None

    def update_from_source(self):
        for file_name, file_content in self.files.items():
            prefix = file_name[:-11]
            for key, value in parse_properties(file_content.split('\n')):
                self.cache['{prefix}.{key}'.format(
                    prefix=prefix,
                    key=key
                )] = value
        for item, value in self.items.items():
            self.cache[item.strip()] = value.strip()

    def conf_disconf(self, conf_dir):
        """执行Disconf基础配置"""
        if not os.path.exists(conf_dir):
            raise Exception('基础配置必须提供')

        conf_file = os.path.join(conf_dir, 'disconf.properties')
        if not os.path.exists(conf_file):
            raise Exception('基础配置必须提供')

        with open(conf_file) as fp:
            app_config = dict(parse_properties(fp.readlines()))
            self.app = app_config['disconf.app']
            self.env = app_config['disconf.env']
            self.version = app_config['disconf.version']
            self.api_server = app_config['disconf.conf_server_host']
            self.base_dir = 'disconf.user_define_download_dir' in app_config and app_config[
                'disconf.user_define_download_dir'] or None

            if self.has_local() and not os.path.isabs(self.base_dir):
                dir = os.path.dirname(conf_file)
                self.base_dir = os.path.join(dir, self.base_dir)
                ensure_dir(self.base_dir)

    def update_local_files(self):
        if not self.has_local():
            return#如果没有提供，表示不需要本地存储

        #先把内存向同步到本地，如果不存在的话
        files_dir = os.path.join(os.path.abspath(self.base_dir), 'files')
        ensure_dir(files_dir)
        for file_name, file_content in self.files.items():
            file_path = os.path.join(files_dir, file_name)
            if os.path.exists(file_path):
                continue
            lock_write(file_path, file_content)
        items_dir = os.path.join(os.path.abspath(self.base_dir), 'items')
        ensure_dir(items_dir)
        for item, value in self.items.items():
            file_path = os.path.join(items_dir, item+'.txt')
            if os.path.exists(file_path):
                continue
            lock_write(file_path, value)
        #再把本地文件内容加载到内存
        for file_name in os.listdir(files_dir):
            if '.properties' != file_name[-11:]:
                continue
            prefix = file_name[:-11]
            with open(os.path.join(files_dir, file_name), 'rt') as fp:
                file_content = fp.read()
                for key, value in parse_properties(file_content.split('\n')):
                    self.cache[prefix + '.' + key] = value
        for file_name in os.listdir(items_dir):
            if '.txt' != file_name[-4:]:
                continue
            key = os.path.basename(file_name)[:-4]
            with open(os.path.join(items_dir, file_name), 'rt') as fp:
                value = fp.read().strip()
                self.cache[key] = value

    def update_from_remote(self):
        for file_name in self.files.keys():
            try:
                self.update_file_from_remote(file_name)
            except HTTPError as e:
                logging.debug('%s %s', e.url, e)
        for item in self.items.keys():
            try:
                self.update_item_from_remote(item)
            except HTTPError as e:
                logging.debug('%s %s', e.url, e)

    def update_file_from_remote(self, file_name):
        r = http.get('%s/api/config/file' % self.api_server, data=dict(
            app=self.app, env=self.env, version=self.version, key=file_name
        ))
        self.set_file_config(file_name, r)

    def update_item_from_remote(self, item):
        r = http.get('%s/api/config/item' % self.api_server, data=dict(
            app=self.app, env=self.env, version=self.version, key=item
        ))
        m = json.loads(r)
        if m['status'] == 1:
            value = m['value']
            self.set_item_config(item, value)

    def set_item_config(self, key, value):
        self.items[key] = value
        self.cache[key] = value.strip()
        self.write_to_local('items', key+'.txt', value)

    def set_file_config(self, file_name, file_content):
        self.files[file_name] = file_content
        prefix = file_name[:-11]
        for key, value in parse_properties(file_content.split('\n')):
            self.cache[prefix + '.' + key] = value.strip()
        self.write_to_local('files', file_name, file_content)

    def has_local(self):
        return hasattr(self, 'base_dir') and os.path.exists(self.base_dir)

    def write_to_local(self, config_type, name, content):
        if not self.has_local():
            return#如果没有提供，表示不需要本地存储
        dir = os.path.join(os.path.abspath(self.base_dir), config_type)
        lock_write('%s/%s'%(dir, name), content, 'w+')

    def fetch_zk(self):
        r = http.get('%s/api/zoo/hosts' % self.api_server)
        m = json.loads(r)
        if m['status'] == 1:
            zk_hosts = m['value']
            logging.debug('fetch zk_hosts=%s', zk_hosts)
            self.zk = KazooClient(hosts=zk_hosts)
            self.zk.start()
        r = http.get('%s/api/zoo/prefix' % self.api_server)
        m = json.loads(r)
        if m['status'] == 1:
            self.zk_prefix = m['value']
            logging.debug('fetch zk_hosts=%s', self.zk_prefix)

    def start_watch(self):
        self.fetch_zk()
        for file_name, file_content in self.files.items():
            self.watch_file(file_name, file_content)
        for item, value in self.items.items():
            self.watch_item(item, value)

    def watch_file(self, file_name, value):
        self.do_watch(file_name, 'file', json.dumps(dict(parse_properties(value.split('\n')))), FileWatcher)

    def watch_item(self, item, value):
        self.do_watch(item, 'item', value.encode('utf-8'), ItemWatcher)

    def do_watch(self, file_name, type, value, watcher):
        watch_node = '{prefix}/{app_name}_{version}_{env}/{type}/{file_name}'.format(
            prefix=self.zk_prefix,
            app_name=self.app,
            version=self.version,
            env=self.env,
            file_name=file_name,
            type=type
        )
        node_name = '{watch_node}/{host_name}'.format(
            watch_node=watch_node,
            host_name=socket.gethostname() + '_' + uuid.uuid4().hex + '_python'
        )
        try:
            self.zk.ensure_path(watch_node)
            self.zk.create(node_name, value=value, ephemeral=True)
            self.zk.get(watch_node, watch=watcher(self, file_name, value))
        except Exception as ex:
            logging.error('watch node faile err=%s', ex.message)



_client = Client()


# 装饰函数，增加配置文件
def config_file(name, def_val=None, meta=_client):
    meta.set_file_config('%s.properties'%name, def_val)

    def _wrap_conf_fun(f):
        @functools.wraps(f)
        def _wrap(key):
            return meta['%s.%s'%(name, key)]
        return _wrap
    return _wrap_conf_fun


# 装饰函数，增加配置项
def config_item(name, def_val=None, meta=_client):
    meta.set_item_config(name, def_val)

    def _wrap_conf_fun(f):
        @functools.wraps(f)
        def _wrap():
            return meta[name]
        return _wrap
    return _wrap_conf_fun


def start(base_dir='./disconf'):
    _client.conf_disconf(base_dir)
    _client.update_from_source()
    _client.update_local_files()
    _client.update_from_remote()
    _client.start_watch()

    return _client