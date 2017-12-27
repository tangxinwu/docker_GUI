from django.shortcuts import render,HttpResponse
from index.DockerCheck import *
from index.DockerContainer import *
from django.views.decorators.csrf import csrf_exempt
from index.DockerPull import *
from index.models import *
import subprocess


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
    ##显示镜像的数量和名字
    d_k = DockerCheck()
    d_k.set_object('images')
    images = d_k.list_objects()
    notifications = ImagePull.objects.filter(PullStatus__in=(0, 2))
    d_p = DockerLogs()

    #检测镜像下载的状态
    for object in notifications:
        d_p.status_log(pid=object.pid, repository_and_tag=tuple(object.ImageName.split('_')))
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
                ##更新传入的镜像名字对应的镜像存在的情况##
                if flag.filter(PullStatus=0):
                    DL = DockerLogs()
                    if DL.pid_isExsit(pid=flag.get(PullStatus=0).pid):
                        return HttpResponse("正在下载的镜像")
                if flag.filter(PullStatus=2):
                    flag.delete()

            script_file_path = os.path.join(os.path.dirname(__file__), 'DockerPull.py')
            try:
                process = subprocess.Popen('pythonw %s %s %s' %(script_file_path, repository, tag), shell=True ,stdout=subprocess.PIPE)
            except:
                process = subprocess.Popen('python3 %s %s %s &' %(script_file_path, repository, tag), shell=False, stdout=subprocess.PIPE)
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
    return HttpResponse('没有输入！')


@csrf_exempt
def create_container(request):
    """
    根据镜像创建容器
    :param request:
    :return:
    """
    if request.POST:
        create_params = request.POST.get('create_params', '')
        p = DockerContainer()
    return HttpResponse(p.container_run(eval(create_params)))


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
            return HttpResponse("%s 没有在运行状态!" %(container_name))
    return HttpResponse("没有输入")


@csrf_exempt
def image_detail(request):
    """
    查询镜像的详细信息
    :param request:
    :return:
    """
    if request.POST:
        image_name = request.POST.get("image_name", "").split(",")[0] #多个标签对应的是一个镜像，只取一个
        dc = DockerCheck()
        dc.set_object('images')
        return HttpResponse(str(dc.get_image_status(image_name)))
    return HttpResponse("xxx")


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
    return HttpResponse("xxx")


@csrf_exempt
def create_local_registry(request):
    """
    创建本地仓库
    :param request:
    :return:
    """
    if request.POST:
        action = request.POST.get("action", "")
        DP = DockerPull(method="New_method")
        if action == "check_registry":
            flag = DP.image_isExsit(("registry", "latest"))
            if not flag:
                return HttpResponse(flag)
    return render(request, "local_registry.html", locals())
