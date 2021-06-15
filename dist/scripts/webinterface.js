//列出接口
function list_httpapi(params){
    $.ajax({
        type: 'get',
        data: params,
        url: '/api/httpapi/',
        cache: false,
        contentType: 'application/json; charset=utf-8',
        success: function(result,TextStatus){
            repaint_apilist(result);
        },
        error: function (){
            console('获取失败')
        },
    })
}

//重绘页面
function repaint_apilist(result){
    retlist = result.retlist;
    //先删除列表现有内容
    $('.card-body tbody tr').remove()
    //添加新的内容
    if(retlist.length>0){
        for (const res of retlist) {
            let tr = $('<tr></tr>')
            //创建行内容
            tr.append($('<td></td>').text(res.id),
                $('<td></td>').text(res.method),
                $('<td></td>').text(res.path).addClass('auto-ellipsis'),
                $('<td></td>').text(res.content_type),
                $('<td></td>').text(res.data).addClass('auto-ellipsis'),
                $('<td></td>').text(res.headers).addClass('auto-ellipsis'),
                $('<td></td>').text(res.module.name),
                $('<td></td>').text(res.desc),
                $('<td></td>').append($('<a></a>').text('编辑').addClass('btn btn-pill btn-sm btn-info').attr('href',`webinterface_view.html?api_id=${res.id}`),
                    $('<button></button>').text('删除').addClass('btn btn-pill btn-sm btn-danger').attr('data-toggle',"modal").attr('data-target',"#dangerModal")),
            );

            $('.card-body tbody').append(tr) //添加数据
        }
    }
}

//新增接口按钮监听
function newApi_btn(){
    //项目列表更新
    common_attach('/api/project/','[name="project_id"]');
    //根据选中项目动态更新模块
    select_onchange('[name="project_id"]','[name="module_id"]','/api/module/');
}



//新增httpapi
function add_httpapi(){
    //获取数据
    let module_id = $('select[name="module_id"] option:selected').val();
    let method = $('select[name="method"] option:selected').val();
    let content_type =$('select[name="content_type"] option:selected').val();
    let auth_type =$('select[name="auth_type"] option:selected').val();
    let path = $('input[name="path"]').val().trim();
    let headers = $('input[name="headers"]').val().trim();
    let data = $('input[name="data"]').val().trim();
    let desc = $('input[name="desc"]').val().trim();

    //请求参数检查
    if(!auth_type){
        alert('请选择认证方式');
        return null
    }

    //构造请求参数
    let payload=JSON.stringify({'module_id':module_id,
        'method':method,'content_type':content_type,'auth_type':auth_type,
        'path':path,'headers':headers,'data':data,'desc':desc
    })
    //提交数据
    $.ajax({
        type: 'post',
        data: payload,
        url: '/api/httpapi/',
        cache: false,
        contentType: 'application/json; charset=utf-8',
        success: function(result,TextStatus){
            console.log('保存成功');
            //隐藏蒙层--点击取消按钮
            $('[data-dismiss="modal"][type="reset"]').click();
            //更新列表
            list_httpapi();
        },
        error: function (result){
            console('提交失败'+result.msg)
        },
    })
}


function webinterface_view(_id) {
    $.ajax({
        type: 'get',
        data: {'id': _id},
        url: '/api/httpapi/',
        contentType: 'application/json; charset=utf-8',
        success: function (result, textStatus) {
            let httpapi = result.retlist[0];
            $('input[name="desc"]').val(httpapi.desc);  //更新描述
            $('input[name="path"]').val(httpapi.path);
            $('input[name="data"]').val(httpapi.data);
            $('input[name="headers"]').val(httpapi.headers);
            //更新模块
            target_selected('select[name="module"]',httpapi.module.id)
            //更新请求方法
            target_selected('select[name="method"]',httpapi.method)
        },
        error: function () {
            console.log('没找到哦');
        }
    });
}

function delete_httpapi(_id) {
    return common_delete(_id,'/api/httpapi/')
}

function addFunctionAlty(value, row, index) {
    return [
        `<a id="edit" class="btn btn-pill btn-sm btn-info" href="webinterface_view.html?api_id=${row.id}">查看</a>`,
        '<button id="delete" class="btn btn-pill btn-sm btn-danger" data-toggle="modal" data-target="#delete_modal">删除</button>',
    ].join('');
}

let operateEvents = {
    'click #edit': function (e, value, row, index) {
    },'click #delete': function (e, value, row, index) {
        function to_delete_item() {
            console.log('delete,row: '+row.id)
            delete_httpapi(row.id)
        }
        $('.modal-footer .btn-danger').unbind('click').click(to_delete_item);
    },
};

const columns= [{
    checkbox: true
},{
    title: 'ID',
    field: 'id',
    //visible: false
}, {
    title: '请求方法',
    field: 'method',
    formatter: parse_method,
}, {
    title: '请求路径',
    field: 'path',
},{
    title: '数据类型',
    field: 'content_type',
    formatter: parse_content_type,
},{
    title: '参数',
    field: 'data',
    cellStyle: formatTableUnit,
    formatter: paramsMatter,
},{
    title: '请求头',
    field: 'headers',
    cellStyle: formatTableUnit,
    formatter: paramsMatter,
},{
    title: '模块',
    field: 'module.name',
},{
    title: '描述',
    field: 'desc',
},{
    title: '操作',
    events: operateEvents,//给按钮注册事件
    formatter: addFunctionAlty//表格中增加按钮
}
];


function parse_method(value, row, index) {
    let span = $('<span></span>').addClass('badge')
    if(value===0){
        span.text('GET').addClass('badge-info')
    }else if(value===1){
        span.text('POST').addClass('badge-info')
    }else if(value===2){
        span.text('PUT').addClass('badge-info')
    }
    else if(value===3){
        span.text('DELETE').addClass('badge-info')
    }else {
        span.text('unknown').addClass('badge-dark')
    }
    return span.prop("outerHTML")  //返回html内容
}
function parse_content_type(value, row, index) {
    let span = $('<span></span>').addClass('badge')
    if(value===0){
        span.text('application/json').addClass('badge-info')
    }else if(value===1){
        span.text('application/x-www-form-urlencoded').addClass('badge-info')
    }else {
        span.text('unknown').addClass('badge-dark')
    }
    return span.prop("outerHTML")  //返回html内容
}
