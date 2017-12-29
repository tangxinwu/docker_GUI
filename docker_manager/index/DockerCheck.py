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
            return "params error!Must be type or name!"
        return getattr(self.client, self.type).get(name)

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



