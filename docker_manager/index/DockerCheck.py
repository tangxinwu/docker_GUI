#! coding=utf-8
"""
docker 查询参数

"""


import docker
type_params = ('containers', 'images',)


class DockerCheck:
    """
    docker 容器查询的主类
    """
    def __init__(self, socket=None):
        """
        初始化docker链接
        :param socket: 如果是本机的话默认是空的参数
        :return: 返回自身
        """
        self.type = ""
        if not socket:
            self.client = docker.from_env()
        else:
            # 先看下参数设置把
            pass
        self.selected_object = ""

    def set_object(self, object_type):
        """
        设置处理的对象类型
        :param object_type: 两种类型containers，images
        :return:
        """
        if object_type not in type_params:
            return "params must be in %s" % (str(type_params))
        self.type = object_type

    def list_objects(self):
        """
        直接列出所有的object
        :return: 返回所有的对象
        """
        return getattr(self.client, self.type).list(all=True)

    def select_object(self, **kwargs):
        """
        对象选择
        :param kwargs:使用解包的方式传递参数方便扩展
        :return: 返回选择的对象
        """
        name = kwargs.get('name', '')
        if not self.type or not name:
            return "params error!Must be name or not uesd set_object method!"
        self.selected_object = getattr(self.client, self.type).get(name)
        return self.selected_object

    def change_container_status(self, selected_object, action):
        """
        如果选择的对象是容器的话 可以使用此方法变换容器状态
        :param selected_object: 被选择的容器对象
        :param action: 希望容器变换的状态
        :return: 没有错误的话 返回信息
        """
        if action == "start":
            selected_object.start()
        if action == "stop":
            selected_object.stop()
        if action == 'restart':
            selected_object.restart()
        if action == 'delete':
            selected_object.stop()
            selected_object.remove()
        return "%s is completed!" % action

    def delete_image(self, image_name):
        """
        对镜像进行的操作
        :param:输入要删除的标签
        :return:
        """
        try:
            self.client.images.remove(image_name)
            return "镜像 %s 成功被移除！" % image_name
        except:
            return "镜像 %s 移除失败，检查是否有容易正在使用他！" % image_name

    def get_image_status(self, image_name):
        """
        获取镜像的详细说明
        :return: 返回镜像的详细字符串
        """
        return self.select_object(name=image_name).attrs

    def check_cpuusage(self):
        """
        获取运行容器的的当前内部的cpu占用率
        cpu使用率的算法为
        var res <---- remote api response

        var cpuDelta = res.cpu_stats.cpu_usage.total_usage -  res.precpu_stats.cpu_usage.total_usage;
        var systemDelta = res.cpu_stats.system_cpu_usage - res.precpu_stats.system_cpu_usage;
        var RESULT_CPU_USAGE = cpuDelta / systemDelta * 100;
        :return:返回单个容器的使用率， (int)
        """
        all_params = self.selected_object.stats(stream=False)
        total_usage = all_params.get("cpu_stats").get("cpu_usage").get("total_usage")
        system_cpu_usage = all_params.get("cpu_stats").get("system_cpu_usage")
        precpu_usage = all_params.get("precpu_stats").get("cpu_usage").get("total_usage")
        precpu_system_usage = all_params.get("precpu_stats").get("system_cpu_usage")
        cpuDelta = total_usage - precpu_usage
        systemDelta = system_cpu_usage - precpu_system_usage
        RESULT_CPU_USAGE = cpuDelta / systemDelta * 100
        cpuCore = all_params.get("cpu_stats").get("online_cpus")
        cpu_usage = round(RESULT_CPU_USAGE * cpuCore, 2)
        return cpu_usage

    def check_memoryusage(self):
        """
        返回当前容器内的内存使用率情况
        现在的算法是
        p1 = y1.get("memory_stats").get("stats").get("total_active_anon")
        p2 = y1.get("memory_stats").get("limit")
        p1/p2
        :return:返回内存使用率（int）
        """
        all_params = self.selected_object.stats(stream=False)
        total_memory = all_params.get("memory_stats").get("limit")
        current_memory = all_params.get("memory_stats").get("stats").get("total_active_anon")
        memory_usage = current_memory/total_memory*100
        return memory_usage


