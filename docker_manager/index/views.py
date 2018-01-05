from django.shortcuts import render,HttpResponse
from index.DockerCheck import *
from index.DockerContainer import *
from django.views.decorators.csrf import csrf_exempt
from index.DockerPull import *
from index.models import *
import subprocess
import json


# Create your views here.


@csrf_exempt
def index(request):
    d_k = DockerCheck()
    d_k.set_object('containers')
    containers = d_k.list_objects()
    if request.POST:
        action = request.POST.get('action', '')
        container_name = request.POST.get('container_name', '')
        container = d_k.select_object(name=container_name)
        result = d_k.change_container_status(container, action)
        return HttpResponse(result)
    return render(request, 'index.html', locals())


@csrf_exempt
def images_management(request):
    # 显示镜像的数量和名字
    d_k = DockerCheck()
    d_k.set_object('images')
    images = d_k.list_objects()
    notifications = ImagePull.objects.filter(PullStatus__in=(0, 2))
    d_p = DockerLogs()

    # 检测镜像下载的状态
    for OBJECT in notifications:
        d_p.status_log(pid=OBJECT.pid, repository_and_tag=tuple(OBJECT.ImageName.split('_')))
    notifications_len = len(notifications)
    return render(request, 'images_management.html', locals())


@csrf_exempt
def pull_images(request):
    if request.POST:
        repository = request.POST.get('repository', '')
        tag = (lambda tag: tag if tag else "latest")(request.POST.get('tag', ''))
        try:
            d_p = DockerPull(method='New_method')
            if d_p.image_isExsit(repository_and_tag=(repository, tag)):
                return HttpResponse("已经存在的镜像")
            flag = ImagePull.objects.filter(ImageName=repository + '_' + tag)
            # 此分支只处理flag存在的情况，传入的下载的镜像名字，检测数据库条目，如果存在下载的镜像对应的条目
            if flag:
                # 更新传入的镜像名字对应的镜像存在的情况##
                if flag.filter(PullStatus=0):
                    DL = DockerLogs()
                    if DL.pid_isExsit(pid=flag.get(PullStatus=0).pid):
                        return HttpResponse("正在下载的镜像")
                if flag.filter(PullStatus=2):
                    flag.delete()

            script_file_path = os.path.join(os.path.dirname(__file__), 'DockerPull.py')
            try:
                process = subprocess.Popen('pythonw %s %s %s' % (script_file_path, repository, tag), shell=True, stdout=subprocess.PIPE)
            except:
                process = subprocess.Popen('python3 %s %s %s &' % (script_file_path, repository, tag), shell=False, stdout=subprocess.PIPE)
            finally:
                ImagePull.objects.create(ImageName=repository + '_' + tag, PullStatus=0, pid=process.pid)

        except docker.errors.APIError:
            return HttpResponse("连接服务器超时或者镜像不存在！")

        return HttpResponse("正在下载 %s" % (repository + "_" + tag))
    return HttpResponse('没有输出')


@csrf_exempt
def status_check(request):
    """
    保留功能
    :param request:
    :return:
    """
    if request.POST:
        image_name = eval(list(request.POST.keys())[0]).get('name')[0]
        if image_name:
            status = ImagePull.objects.filter(ImageName=image_name)[0].PullStatus
            return HttpResponse(status)
    for i in request.META.keys():
        print(i)
    return HttpResponse(request.META.get("PATH_INFO"))


@csrf_exempt
def create_container(request):
    """
    根据镜像创建容器
    :param request:
    :return:
    """
    if request.POST:
        create_params = eval(request.POST.get('create_params', ''))
        port_list = eval(request.POST.get("port_list", ""))
        protocl_list = eval(request.POST.get("protocl_list", ""))
        p = DockerContainer()
        # js处理数组方法不是太熟 放到后台来处理传入的端口映射
        if any(port_list):
            temp_port_list1 = port_list[::2]   # 存放外部端口
            temp_port_list2 = port_list[1::2]  # 存放内部端口
            temp_proctol_list = protocl_list   # 存放每个端口对应的协议
            result1 = ["/".join(i) for i in list(zip(temp_port_list1, temp_proctol_list))]
            result2 = list(zip(result1, map(int, temp_port_list2)))
            create_params.append("ports,%s" % str(dict(result2)))
        return HttpResponse(p.container_run(create_params))
    return HttpResponse("没有输入！")


@csrf_exempt
def container_exec(request):
    """
    容器中运行命令
    :param request:
    :return:返回运行结果到前端
    """
    if request.POST:
        container_name = request.POST.get('container_name', '')
        cmd = request.POST.get('cmd', '')
        try:
            return HttpResponse(DockerContainer.execute_command(container_name, cmd))
        except docker.errors.APIError:
            return HttpResponse("%s 没有在运行状态!" % container_name)
    return HttpResponse("没有输入")


@csrf_exempt
def image_detail(request):
    """
    查询镜像的详细信息
    :param request:
    :return:
    """
    if request.POST:
        image_name = request.POST.get("image_name", "").split(",")[0]  # 多个标签对应的是一个镜像，只取一个
        dc = DockerCheck()
        dc.set_object('images')
        return HttpResponse(str(dc.get_image_status(image_name)))
    return HttpResponse("没有输入！")


@csrf_exempt
def delete_image(request):
    """
    删除镜像
    :param request:
    :return:
    """
    if request.POST:
        image_name = request.POST.get("image_name", "")
        dc = DockerCheck()
        dc.set_object("image")
        res = dc.delete_image(image_name)
        return HttpResponse(res)
    return HttpResponse("没有输入！")


@csrf_exempt
def create_local_registry(request):
    """
    本地仓库显示界面
    :param request:
    :return:
    """
    dp = DockerCheck()
    dp.set_object("containers")
    if request.POST.get("registry_name", ""):  # 传入本地仓库名字 查询本地仓库镜像
        registry_name = request.POST.get("registry_name", "")
        port = dp.select_object(name=registry_name).attrs.get("NetworkSettings").get("Ports").get("5000/tcp")[0].get("HostPort")
        cmd = "curl -XGET http://localhost:%s/v2/_catalog" % str(port)
        res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        temp_res = re.findall("{.*?}", str(list(res.stdout)))
        image_list = eval(temp_res[0]).get("repositories")
        tags_list = dict()
        for image in image_list:
            cmd = "curl -XGET http://localhost:%s/v2/%s/tags/list" % (str(port), image)
            print(cmd)
            res = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE)
            temp_res = re.findall("{.*?}", str(list(res.stdout)))
            print(temp_res)
            tags_list.update({eval(temp_res[0]).get("name"): eval(temp_res[0]).get("tags")[0]})
        return HttpResponse(json.dumps(tags_list, ensure_ascii=False))
    all_containers = dp.list_objects()
    res = list()
    for i in all_containers:
        for k in i.image.attrs.get("RepoTags"):
            if "registry" in k:
                res.append(i)
                break
    return render(request, "local_registry.html", locals())
