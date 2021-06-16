//测试任务
function list_plan(params){
    $.ajax({
        type: 'get',
        data: params,
        url: '/api/plan/',
        cache: false,
        contentType: 'application/json; charset=utf-8',
        success: function(result,TextStatus){
            if(result.retcode===200){
                repaint_planlist(result);
            }else if(result.retcode===403){
                console.log('未登录,开始重定向')
                location.href = result.to
            }
        },
        error: function (){
            console('获取失败')
        },
    })
}

//重绘页面
function repaint_planlist(result){
    retlist = result.retlist;
    //先删除列表现有内容
    $('.card-body tbody tr').remove()
    //添加新的内容
    if(retlist.length>0){
        for (const res of retlist){
            let tr = $('<tr></tr>')
            //创建行内容
            tr.append($('<td></td>').text(res.id),
                $('<td></td>').text(res.name),
                $('<td></td>').text(res.project?res.environment.project:'N/A'),
                $('<td></td>').text(res.executor?res.executor.username:'N/A'),
                $('<td></td>').text(res.environment?res.environment.desc:'N/A'),
                $('<td></td>').text(res.status),
                $('<td></td>').text(res.exec_counts),
                $('<td></td>').text(res.desc),
                $('<td></td>').append($('<button></button>').text('运行').addClass('btn btn-pill btn-sm btn-success').click(function () {
                        run_plan(res.id);
                    }),
                    $('<a></a>').text('查看').addClass('btn btn-pill btn-sm btn-info').attr('href',`plan_view.html?plan_id=${res.id}`),
                    $('<button></button>').text('删除').addClass('btn btn-pill btn-sm btn-danger').attr('data-toggle',"modal").attr('data-target',"#dangerModal")),
            );

            $('.card-body tbody').append(tr) //添加数据
        }
    }
}

//新增测试项目表单
function attach_plan(params){
    //项目
    common_attach('/api/project/','[name="project_id"]');
    //项目关联模块更新
    select_onchange('[name="project_id"]','[name="module_id"]','/api/module/')
    //项目关联环境更新
    select_onchange('[name="project_id"]','[name="env_id"]','/api/env/')

}
//select选择监听
function select_onchange(source,target,url){
    //监听源
    $(source).change(function (){
        //选中项--value 对应数据的id
        let selected = $(this).children('option:selected').val();
        //动态更新目标select
        update_select(target,{'project_id':selected},url);
    })
}


//新增测试计划表单
function new_plan(){
    const csrftoken = getCookie('csrftoken'); //从cookie获取django的crsftoken
    //获取信息
    let project_id = $('[name="project_id"] option:selected').val();
    let module_id = $('[name="module_id"] option:selected').val();
    let status = $('[name="status"] option:selected').val();
    let env_id = $('[name="env_id"] option:selected').val();
    let name = $('[name="name"]').val();
    let desc= $('[name="desc"]').val();
    let executor_id = current_user('id')
    console.log('executor_id:'+executor_id)
    //提交
    $.ajax({
        type: 'post',
        data: JSON.stringify({'desc':desc,'name':name,'environment_id':env_id,'executor_id':'2','status':status,'project_id':project_id}),
        url: '/api/plan/',
        cache: false,
        contentType: 'application/json; charset=utf-8',
        headers: {'X-CSRFToken': csrftoken},
        success: function (result,TextStatus){
            console.log('success');
            $('[data-dismiss="modal"]').click();
            console.log(result);
            list_plan(); //重新列出测试计划
        },
        error:function (result,TextStatus){
            console.log('fail');
            $('[data-dismiss="modal"]').click();
            console.log(result);
        },
    })
}

//plan详情页面
function plan_view(plan_id){
    $.ajax({
        type: 'get',
        data: {'id':plan_id},
        url: '/api/plan/',
        async: true,
        contentType: 'application/json; charset=utf-8',
        success:function (result, textStatus) {
            if(result.retcode===200){
                repaint_plan_view(result);
            }else if(result.retcode===403){
                console.log('未登录,开始重定向')
                location.href = result.to
            }
        },
        error:function (){
            console.log('没找到哦');
        }
    });
    //绑定修改按钮点击方法---提交修改
    $('[type="submit"]').click(function () {
        update_testplan(plan_id);
    })
}
function repaint_plan_view(result) {
    let plan = result.retlist[0];
    $('input[name="name"]').val(plan.name);
    $('input[name="desc"]').val(plan.desc);
    //更新下拉列表--项目
    common_attach('/api/project/', 'select[name="project_id"]', plan.environment.project);
    //更新下拉列表--环境
    common_attach('/api/env/', 'select[name="env_id"]', plan.environment.id);
    //环境选择框关联项目选择
    select_onchange('select[name="project_id"]', 'select[name="env_id"]', '/api/env/',);

    //拷贝例行模板
    let row_temp = $('.card-footer tbody tr:nth-last-child(1)');
    //测试用例刷新
    if (plan.cases.length > 0) {
        console.log('update caselist')
        //删除所有行
        $('.card-footer tbody tr').each(function () {
            $(this).remove();
        });
        for (let testcase of plan.cases) {
            //新增一行
            $('.card-footer tbody').append(row_temp[0].outerHTML);
            //填充模块
            common_attach('/api/module/', 'tr:nth-last-child(1) select[name="module_id"]',
              testcase.module_id, {'project_id': plan.environment.project});
            //填充用例
            common_attach('/api/case/', 'tr:nth-last-child(1) select[name="case_id"]',
              testcase.id, {'module_id': testcase.module_id});
            //填充描述
            $('.card-footer tbody tr:nth-last-child(1) input[name="case_desc"]').val(testcase.desc);

        }
    } else {
        //更新模块下拉
        common_attach('/api/module/', 'select[name="module_id"]', plan.environment.project);
        //更新用例下拉
        let seleted_module = $('select[name="module_id"] option:selected').val(); //查看当前选择的模块
        let res = common_attach('/api/case/', 'select[name="case_id"]', seleted_module);
        $('.card-footer tbody tr:nth-last-child(1) input[name="case_desc"]').val(res.desc);
    }
}

//提交修改
function update_testplan(id) {
    const csrftoken = getCookie('csrftoken'); //从cookie获取django的crsftoken
    //获取信息
    const name = $('input[name="name"]').val();
    const desc = $('input[name="desc"]').val();
    const env_id = $('select[name="env_id"] option:selected').val();
    const project_id = $('select[name="project_id"] option:selected').val();
    let cases = []
    $('select[name="case_id"] option:selected').each(function () {
        cases.push($(this).val())
    });  //测试用例sID

    //提交信息
    $.ajax({
        type: 'put',
        data: JSON.stringify({'name':name,'desc':desc,'environment_id':env_id,'case_ids':cases,'project_id':project_id}),
        url: '/api/plan/?id='+id,
        cache: false,
        contentType: 'application/json; charset=utf-8',
        headers: {'X-CSRFToken': csrftoken},
        success: function (result,TextStatus){
            console.log('success')
            console.log(result)
            //返回计划列表页面
            window.location.href='testplan.html'
        },
        error:function (result,TextStatus){
            console.log('fail'+result.msg)
        },
    })
}

//运行测试计划
function run_plan(id){
    alert('运行计划:'+id);
    $.ajax({
        type: 'get',
        data: {'id':id},
        url: '/api/run/plan/',
        contentType: 'application/json; charset=utf-8',
        success:function () {
            alert('运行成功')
        },
        error:function (){
            alert('运行失败，服务器错误')
        }
    })
}

function delete_plan(_id) {
    return common_delete(_id,'/api/plan/')
}

function addFunctionAlty(value, row, index) {
    return [
        '<button id="run" class="btn btn-pill btn-sm btn-success" >运行</button>',
        `<a id="edit" class="btn btn-pill btn-sm btn-info" href="plan_view.html?plan_id=${row.id}">编辑</a>`,
        '<button id="delete" class="btn btn-pill btn-sm btn-danger" data-toggle="modal" data-target="#delete_modal">删除</button>',
    ].join('');
}

let operateEvents = {
    'click #run': function (e, value, row, index) {
        run_plan(row.id);
    },
    'click #edit': function (e, value, row, index) {
    },'click #delete': function (e, value, row, index) {
        function to_delete_item() {
            console.log('delete,row: '+row.id)
            delete_plan(row.id)
        }
        $('.modal-footer .btn-danger').unbind('click').click(to_delete_item);
    },
};

const columns = [{
    checkbox: true
}, {
    title: 'ID',
    field: 'id',
    //visible: false
}, {
    title: '计划名称',
    field: 'name',
}, {
    title: '项目',
    field: 'project.name',
}, {
    title: '测试人员',
    field: 'executor',
}, {
    title: '测试环境',
    field: 'environment.desc',
}, {
    title: '状态',
    field: 'status',
    formatter:parse_status,
}, {
    title: '执行次数',
    field: 'exec_counts',
}, {
    title: '描述',
    field: 'desc',
}, {
    title: '操作',
    events: operateEvents,//给按钮注册事件
    formatter: addFunctionAlty//表格中增加按钮
}
];

function parse_status(value, row, index) {
    let span = $('<span></span>').addClass('badge')
    if(value===0){
        span.addClass('badge-light').text('未执行')
    }else if(value===1){
        span.addClass('badge-info').text('执行中')
    }else if(value===2){
        span.addClass('badge-warning').text('中断')
    }else if(value===3){
        span.addClass('badge-success').text('已执行')
    }
    return span.prop("outerHTML")  //返回html内容
}