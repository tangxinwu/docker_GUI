#! coding=utf-8
from abc import ABC, abstractmethod
import docker
import psutil

BasePull_params = ['method',]

class BasePull(ABC):
    """
    docker下载的基类
    """
    def __init__(self, **kwargs):
        """
        使用字典参数method=New_method /其他任意参数来选择使用新的还是老的方法初始化
        默认值 老方法
        :param kwargs:
        """
        if list(kwargs.keys()) > BasePull_params:
            print("没有此类参数")
        self.client = (lambda client: client if kwargs.get('method') == 'New_method' else docker.APIClient())(docker.from_env())
        print(self.client)
        self.tag = ""
        self.result = ""

    @abstractmethod
    def single_pull(self, repository_and_tag):
        """
        单个下载镜像进程
        :return:
        """

    @abstractmethod
    def mutil_pull(self, repository_and_tag_list):
        """
        多个下载进程
        :return:
        """
    @abstractmethod
    def image_isExsit(self, repository_and_tag):
        """
        判断镜像是否存在
        :param repository_and_tag:
        :return:
        """


class BaseLogsProcess(ABC):
    """
    处理日志的基类,判断是否下载成功
    """
    def pid_isExsit(self,pid):
        """
        使用psutil库检查下载进程是否存在
        这个其实可以不放到此类里面
        :param pid: 传入的下载进程的pid 保存在数据库
        :return:
        """
        if pid in psutil.pids():
            ##下载进程存在
            return 1
        else:
            ##下载进程结束
            return 0

    @abstractmethod
    def init_db(self):
        """
        初始化存放状态的位置
        :return:
        """

    @abstractmethod
    def gen_logs(self, **kwargs):
        """
        生成日志的
        :return:
        """

    @abstractmethod
    def status_log(self, **kwargs):
        """
        读取下载日志
        :return:
        """
