//弹出创建新镜像窗口
function NewImages_pop() {
    $('#popmodal').modal();
    $('#popmodal .modal-title').empty();
    $('#popmodal .modal-title').append('获取新镜像');

}

//拉取镜像
function Pull_images() {
    $('#popmodal').modal();
    var repository = $('#repository').val();
    var tag = $('#tag').val();
    $.post('/pull_images/',{'repository':repository,'tag':tag},function (result) {
        alert(result);
    })
    // window.location.reload();

}

//创建容器
function create_container() {
    var input_objects = $('#created_modal :text');
    var checkbox_objects = $('#created_modal :checkbox');
    var params = new Array();
    input_objects.each(function (k,v) {
        params.push(v.id + ',' + v.value);
    });

    checkbox_objects.each(function (k,v) {
        if (v.checked){
            params.push(v.id + ',' + v.checked)
        }
    });
    var result = JSON.stringify(params);
    $.post('/create_container/',{'create_params':result},function (result) {
        alert(result);
    })
}

//容器内执行命令
function container_exec() {
    var container_name = $('#container_name').val();
    var cmd = $('#cmd').val();
    $.post('/container_exec/',{'container_name':container_name,'cmd': cmd},function (result) {
       //alert(result);
        $("#cmd_result").append("运行命令" + cmd + "的结果如下：" + "\n");
        $("#cmd_result").append(result);
        $("#cmd_result").append("命令执行完成！" + "\n");
    });
}

//弹出下载仓库镜像框

function registry_confirm()
{
    $.post("/local_registry/", {"action" : "check_registry"},function (result) {
        if (result == 0){
            event.returnValue = confirm("没有找到仓库镜像，是否下载？");
            if (event.returnValue){
                $.post("/pull_images/",{'repository':"registry",'tag':"latest"},function (result) {
                    alert(result)
                    // if (result == "true"){
                    //     alert("开始创建仓库容器！");
                    //     //弹出自定义端口界面
                    //     $("#custom_port").modal();
                    //     var outer_port = $("#outer_port").val();
                    //     var inner_port = $("#inner_port").val();
                    //     //默认的协议类型是tcp
                    //     var protocl = "tcp"
                    //     //使用其他默认参数创建容器
                    //     var params = "{'command':'bash', 'image':'registry:latest','init':'true','name':'local_registry','tty':'true'," + "'ports':{" + outer_port + "/" + protocl + ":" + inner_port +"}}"
                    //     var result = JSON.stringify(params);
                    //     alert(result)
                    //     $.post("/create_container/", {'create_params':result},function (res) {
                    //         alert(res);
                    //
                    //     })
                    //
                    // }



                });
            }else {
                window.history.back();
            }
        }
    });

    // alert("sdasda" + event.returnValue);
}

//弹出自定义仓库界面
function custom_registry() {
    $("#custom_port").modal();

}