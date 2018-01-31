#! coding=utf-8

try:
    from index.DockerPullBase import *
except ImportError:
    from DockerPullBase import *

from concurrent import futures

import pymysql
import os
import sys
"""
#插入settings的文件目录到系统环境变量
#这是没有办法了
"""
settings_path = os.path.dirname(__file__.replace('index','docker_manager'))
print('路径', settings_path)
sys.path.append(settings_path)
import settings



class DockerPull(BasePull):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def single_pull(self, repository_and_tag):
        """
        这个是使用老方法推送的
        :param repository_and_tag:
        :return:
        """
        repository, tag = repository_and_tag
        tag = (lambda tag: tag if tag else "latest")(tag)
        self.tag = repository + "_" + tag
        self.result = self.client.pull(repository, tag=tag)
        return self

    def mutil_pull(self, repository_and_tag_list):
        """
        使用老方法推送的
        :param repository_and_tag_list:
        :return:
        """
        repository_and_tag_list = list(repository_and_tag_list)
        with futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            res = executor.map(self.single_pull, repository_and_tag_list)
        return res

    def image_isExsit(self, repository_and_tag):
        """
        这是使用新方法的的子方法
        :param repository_and_tag:
        :return:

        """
        repository, tag = repository_and_tag
        flag = [i for i in self.client.images.list() if repository + ':' + tag in i.tags]
        if flag:
            # 镜像已经存在
            return 1
        else:
            # 镜像不存在
            return 0


class DockerLogs(BaseLogsProcess):
    def init_db(self):
        host_dict = settings.DATABASES.get('default')
        conn = pymysql.connect(host_dict.get('HOST'),
                               host_dict.get('USER'),
                               host_dict.get('PASSWORD'),
                               host_dict.get('NAME'),
                               )
        cur = conn.cursor()
        return cur

    def gen_logs(self, **kwargs):
        """
        将下载状态写入数据库，方便以后查询
        :param kwargs:
        :return:
        """
        cur = self.init_db()
        if kwargs.get('status', ''):
            status = {
                'complete': {'PullStatus': 1},
                'failed': {'PullStatus': 2},
            }
            cur.execute("""update index_imagepull set PullStatus='%d' where ImageName='%s'""" % (int(status.get(kwargs.get('status')).get('PullStatus')),kwargs.get('update_tag')))
            cur.execute("""commit;""")

    def status_log(self, **kwargs):
        """
        根据pid判断下载状态，把状态写入数据库
        :param:tag 是repository_and_tag的元祖
        :return:
        """
        if 'pid' in kwargs and 'repository_and_tag' in kwargs:
            if not self.pid_isExsit(pid=kwargs.get('pid')):
                p = DockerPull(method='New_method')
                if not p.image_isExsit(kwargs.get('repository_and_tag')):
                    self.gen_logs(status='failed', update_tag='_'.join(kwargs.get('repository_and_tag')))
                else:
                    self.gen_logs(status='complete', update_tag='_'.join(kwargs.get('repository_and_tag')))


if __name__ == "__main__":
    repository = sys.argv[1]
    tag = sys.argv[2]
    try:
        DP = DockerPull()
        DP.single_pull((repository, tag))
    except docker.errors.APIError:
        print("连接网路超时，请稍后再试！")


