//列出报告
function list_result(params){
    $.ajax({
        type: 'get',
        data: params,
        url: '/api/result/',
        cache: false,
        contentType: 'application/json; charset=utf-8',
        success: function(result,TextStatus){
            repaint_resultlist(result);
        },
        error: function (){
            console.log('获取失败');
        },
    })
}

//重绘页面
function repaint_resultlist(result){
    retlist = result.retlist;
    //先删除列表现有内容
    $('.card-body tbody tr').remove()
    //添加新的内容
    if(retlist.length>0){
        for (const res of retlist) {
            let tr = $('<tr></tr>')
            //创建行内容
            tr.append($('<td></td>').text(res.id),
                $('<td></td>').text(res.plan?res.plan.name:'N/A'),
                $('<td></td>').text(res.project?res.project.name:'N/A'),
                $('<td></td>').text(res.start_time),
                $('<td></td>').text(res.end_time),
                $('<td></td>').text(res.case_num),
                $('<td></td>').text(res.pass_num),
                $('<td></td>').text(res.failed_num),
                $('<td></td>').append($('<a></a>').text('查看').addClass('btn btn-pill btn-sm btn-info').attr('href',`report_view.html?report_id=${res.id}`),
                    $('<button></button>').text('删除').addClass('btn btn-pill btn-sm btn-danger').attr('data-toggle',"modal").attr('data-target',"#dangerModal")),
            );

            $('.card-body tbody').append(tr) //添加数据
        }
    }
}

function report_view(_id){
    $.ajax({
        type: 'get',
        data: {'id':_id},
        url: '/api/result/',
        cache: false,
        contentType: 'application/json; charset=utf-8',
        success: function(result,TextStatus){
            let failed_num = result.retlist[0].failed_num;
            let pass_num = result.retlist[0].pass_num;
            chart_paint(['失败数', '通过数', ],[failed_num, pass_num]);
        },
        error: function (){
            console.log('获取失败');
        },
    })

}

function delete_result(_id) {
    return common_delete(_id,'/api/result/')
}


function chart_paint(label_list,data_list){
    let doughnutChart = new Chart(document.getElementById('canvas-3'), {
        type: 'doughnut',
        data: {
            labels: label_list, //
            datasets: [{
                data: data_list, //
                backgroundColor: ['#FF6384', '#36A2EB', ],
                hoverBackgroundColor: ['#FF6384', '#36A2EB', ]
            }]
        },
        options: {
            responsive: true
        }
    }); // eslint-disable-next-line no-unused-vars
}

function addFunctionAlty(value, row, index) {
    return [
        `<a id="edit" class="btn btn-pill btn-sm btn-info" href="report_view.html?report_id=${row.id}">查看</a>`,
        '<button id="delete" class="btn btn-pill btn-sm btn-danger" data-toggle="modal" data-target="#delete_modal">删除</button>',
    ].join('');
}

let operateEvents = {
    'click #edit': function (e, value, row, index) {
    },'click #delete': function (e, value, row, index) {
        function to_delete_item() {
            console.log('delete,row: '+row.id)
            delete_result(row.id)
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
    title: '测试计划',
    field: 'plan.name',
}, {
    title: '测试人员',
    field: 'executor',
}, {
    title: '开始时间',
    field: 'start_time',
    cellStyle: formatTableUnit,
    formatter: paramsMatter,
}, {
    title: '结束时间',
    field: 'end_time',
    cellStyle: formatTableUnit,
    formatter: paramsMatter,
}, {
    title: '用例数',
    field: 'case_num',
}, {
    title: '通过数',
    field: 'pass_num',
}, {
    title: '失败数',
    field: 'failed_num',
}, {
    title: '操作',
    events: operateEvents,//给按钮注册事件
    formatter: addFunctionAlty//表格中增加按钮
}
];


