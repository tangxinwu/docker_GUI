# # import numpy as np
# # from sklearn.svm import SVC
# # from sklearn import random_projection
# #
# # #
# # # temp = list()
# # # temp1 = list()
# # # f = open(r'd:\ssss.txt')
# # # for i in f.readlines():
# # #     temp.append([float(i.split()[0]),])
# # #     temp1.append(float(i.split()[1]))
# # # x = np.array(temp)
# # # print(x)
# # # y = np.array(temp1)
# # # print(y)
# # # t = np.array([[70015]])
# # # clf = SVC()
# # # clf.set_params(kernel="linear").fit(x,y)
# # # print(clf.predict(t))
# #
# #
# # # def get_data(DATA_FILE_PATH,FIT_METHOD,TEST_DATA):
# # #     temp = list()
# # #     temp1 = list()
# # #     temp3 = list()
# # #     with open(DATA_FILE_PATH) as f:
# # #         for i in f.readlines():
# # #             temp.append([float(i.split()[0]), ])
# # #             temp1.append(float(i.split()[1]))
# # #     x = np.array(temp) #训练集
# # #     y = np.array(temp1) #特征集标签
# # #     for i in TEST_DATA:
# # #         tmp = list()
# # #         tmp.append(float(i))
# # #         temp3.append(tmp)
# # #     print(y)
# # #     t = np.array(temp3)
# # #     clf = SVC()
# # #     clf.set_params(kernel=FIT_METHOD).fit(x,y)
# # #     return clf.predict(t)
# # #
# # #
# # # x = get_data(r'd:\ssss.txt','linear',(3000,4000))
# # # print(x)
# # #
# # #
# #
# # import os
# # from subprocess import Popen,PIPE
# # from concurrent import futures
# #
# #
# # # def show(cmd):
# # # cmd = r"docker pull nginx"
# # # p = Popen(cmd,shell=True,stdout=PIPE,stderr=PIPE)
# # #
# # # try:
# # #     while True:
# # #         print(p.stdout.__next__().decode('GBK'))
# # # except StopIteration:
# # #     print('ending..')
# # # finally:
# # #     p.stdout.close()
# #
# # # cmd_list = ['dir c:\\','docker pull nginx ',]
# # # with futures.ThreadPoolExecutor(max_workers=2) as executor:
# # #     res = executor.map(show,cmd_list)
# #
# # # print(len(list(res)))
# # # print(res.gi_running)
# #
# # # import os
# # # from subprocess import Popen
# # #
# # # def floder_size(path):
# # #     for i in os.walk(path):
# # #         os.system('du -sh %s' %i[0])
# # #
# # # floder_size('c:')
# #
# # # from subprocess import PIPE,Popen,STDOUT
# # # import locale
# # # import os
# # #
# # # p = Popen('docker pull nginx', shell=True ,stdout=PIPE,stderr=PIPE)
# # # def xiecheng(a):
# # #     yield from a
# # #
# # # for i in xiecheng(p.stdout):
# # #     print(i.decode(locale.getpreferredencoding()))
# # #
# # # print('end..')
# #
# # import os
# #
# #
import os
import sys

def show(path):
    for i in os.walk(path, followlinks=True):
        try:
            print(i[1])
            if i[1]:
                for k in i[i]:
                    file_path = os.path.join(i[0],k)
                    file_size = os.path.getsize(file_path)/1024**2
                    result = str(file_path) + '-->' + str(file_size) + ' MB' + "\n"
                    print result
                    f.write(result)
        except OSError:
            continue


f = open("/tmp/log.txt","a+")
path = sys.argv[1]
show(path)
f.close()


# #
# #
# # def copy_file(source_path, destination_path):
# #     os.system("copy %s %s" % (source_path, destination_path))
# #     gen_log(str(source_path), r'd:/')
# #
# #
# # def gen_log(content, log_path=r'd:/file_log.txt'):
# #     with open(log_path, 'a+') as f:
# #         f.write(content + '\n')
# #
# # import shutil
# # import locale
# # import codecs
# #
# # def FallBack(log_file):
# #     with codecs.open(log_file, encoding="utf-8") as f:
# #         data = f.readlines()
# #     for i in data:
# #         print("目标路径", i)
# #         print("源路径", os.path.join('/tmp/modify_files', os.path.basename(i)))
# #         # shutil(os.path.join('/tmp/modify_files', os.path.basename(i)), i)
# #
# # FallBack(r"C:\Users\唐鑫吾\Desktop\chaiyou\modify_files\log.txt")
# #
# #
#
# from urllib.request import urlopen
# import re
# import os
# from concurrent import futures
# import time
#
# package_url1 = "http://repo.mysql.com/yum/mysql-5.7-community/el/7/x86_64/"
#
# data1 = urlopen(package_url1).read()
# saved_path = "/tmp"
#
# d1 = re.findall(b"HREF=\".*?\"", data1)
# d2 = map((lambda x: x if b".rpm" in x else ""), d1)
# d3 = [i for i in d2 if i]
# d4 = [i.replace(b'HREF=\"', b'').replace(b'\"', b'') for i in d3]
# d5 = [i.decode("utf8") for i in d4]
#
# def redownload_pull(rpm_name, origin_data):
#     with open(rpm_name, "wb+") as f:
#         f.write(origin_data)
#
#
#
# def single_pull(rpm_name):
#     origin_path = package_url1 + rpm_name
#     local_path = os.path.join(saved_path, rpm_name)
#     if os.path.isfile(local_path):
#         time.sleep(0.1)
#         origin_data = urlopen(origin_path).read()
#         origin_size = len(origin_data)
#         local_size = os.path.getsize(local_path)
#         if origin_size == local_size:
#             os.system("""echo -e "\033[32m%s is exsited! Skipped...\033[0m" """ % (rpm_name))
#         else:
#             os.system("""echo -e "\033[32mRedownload %s\033[0m" """ % (rpm_name))
#             redownload_pull(rpm_name, origin_data)
#     else:
#         res = os.system("wget %s -O %s" % (origin_path, local_path))
#         print(res)
#
#
# with futures.ThreadPoolExecutor(max_workers=4) as executor:
#     res = executor.map(single_pull, d5)
#
# #######################################
# from urllib import urlopen
# import re
# import os
#
# package_url1 = "http://repo.mysql.com/yum/mysql-5.7-community/el/7/x86_64/"
# saved_path = "/tmp"
#
# data1 = urlopen(package_url1).read()
#
# d1 = re.findall("HREF=\".*?\"", data1)
# d2 = map((lambda x: x if ".rpm" in x else ""), d1)
# d3 = [i for i in d2 if i]
# d4 = [i.replace('HREF=\"', '').replace('\"', '') for i in d3]
# d5 = [i for i in d4]
#
# def single_pull(rpm_name):
#     os.system("wget %s -O %s" % (package_url1 + rpm_name, os.path.join(saved_path, rpm_name)))
#
# def redownload_pull(rpm_name, origin_data):
#     f = open(rpm_name, "wb+")
#     f.write(origin_data)
#     f.close()
#
#
# for i in d5:
#     current_list = os.listdir(saved_path)
#     if i in current_list:
#         origin_data = urlopen(package_url1 + i).read()
#         origin_size = len(origin_data)
#         local_size = os.path.getsize(os.path.join(saved_path, i))
#         if origin_size == local_size:
#             os.system("""echo -e "\033[32m%s is exsited! Skipped...\033[0m" """ % (i))
#             continue
#         else:
#             os.system("""echo -e "\033[32mRedownload %s\033[0m" """ %(i))
#             redownload_pull(i, origin_data)
#             continue
#     single_pull(i)
#

import codecs

f = codecs.open(r"C:\Users\唐鑫吾\Desktop\tbsb4.txt",encoding="utf-8")
data = f.read().replace("\n", "")
print(data)
f.close()

import re
sn_data1 = re.findall("sn:.*?readme: ", data)
new_sn = [i.replace("sn: ", "").replace("readme: ", "") for i in sn_data1]
print(new_sn)
readme_data = re.findall("readme: .*?sn: ", data)
# print(readme_data)
new_readme = [i.replace("readme: ","").replace("sn: ", "").replace("\r", " ") for i in readme_data]
print(new_readme)

all_data = zip(new_sn, new_readme)
# print(list(all_data))
f = codecs.open(r"C:\Users\唐鑫吾\Desktop\tbsn6.txt", "w")
for i in all_data:
    # print(i[0])
    f.writelines(i[0] + i[1] + "\n")

f.close()

import os

def check_static_file(reqeust):
    base_path = r"/home/www/resources/online_data/pdf_reader/resource"
    passed_path = reqeust.GET.get("path", "")
    if path:
        try:
            temp_res = os.listdir(os.path.join(base_path, passed_path))
            result = [str(os.path.join(base_path, passed_path)), [], []]
            for i in temp_res:
                if os.path.isdir(os.path.join(base_path, passed_path), i):
                    result[1].append(i)
                else:
                    result[2].append(i)
            return HttpResponse(result)
        except OSError:
            return HttpResponse("Not such type")
    return HttpResponse("No input selected!")