import docker
import re


class DockerContainer:
    def __init__(self):
        pass

    def _init_client(self):
        """
        初始化API的连接方式
        :return:
        """
        return docker.from_env()

    def container_run(self, args):
        """
        从镜像创建容器
        :param args: 从前端传入的创建容器的参数dict
        :return:
        """
        temp = list()
        for i in args:
            if i.split(',')[1] in ('true', 'false'):
                temp.append((i.split(',')[0], eval(i.split(',')[1].replace(i.split(',')[1][0], i.split(',')[1][0].upper()))))
            else:
                temp.append((i.split(',')[0], i.split(',')[1]))
        params = dict(temp)
        image = params.pop('image')
        command = params.pop('command')

        try:
            self._init_client().containers.run(image, command, kwargs=params)
            result = '%s 创建成功！' % (params.get('name'))

        except docker.errors.APIError as e:
            print('显示错误上', str(e))
            already_exsit_error = re.findall('is already in use by container', str(e))
            execute_file_not_found_error = re.findall('executable file not found in \$PATH', str(e))
            if already_exsit_error:
                result = params.get('name') + ' 已经存在！'
            if execute_file_not_found_error:
                result = '命令' + command + "在环境变量中没有找到！"
                self._init_client().containers.remove(params.get('name'))

        except docker.errors.ContainerError as e:
            print("显示错误", str(e))
            run_command_error = re.findall('returned non-zero exit status', str(e))
            if run_command_error:
                result = command + ' 该镜像里面没有此命令'
        finally:
            return result

    @classmethod
    def execute_command(cls, container_name, cmd):
        """
        执行容器中的命令
        :return:
        """
        client = cls()._init_client()
        selected_container = client.containers.get(container_name)
        return selected_container.exec_run(cmd)




