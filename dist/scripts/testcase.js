//======================================private fun====================================

//列出用例
function list_case(params) {
  $.ajax({
    type: 'get',
    data: params,
    url: '/api/case/',
    contentType: 'application/json; charset=utf-8',
    success: function (result, TextStatus) {
      if(result.retcode===200){
        repaint_caselist(result);
      }else if(result.retcode===403){
        console.log('未登录,开始重定向')
        location.href = result.to
      }
    },
    error: function () {
      console.log('获取失败');
    },
  })
}

//重绘页面
function repaint_caselist(result) {
  retlist = result.retlist;
  //先删除列表现有内容
  $('.card-body tbody tr').remove()
  //添加新的内容
  if (retlist.length > 0) {
    for (const res of retlist) {
      let tr = $('<tr></tr>')
      taglist = res.tags.map((value,index)=>{return value.name}) //收集标签名
      //创建行内容
      tr.append($('<td></td>').text(res.id),
        $('<td></td>').text(res.desc),
        $('<td></td>').text(res.project.name),
        $('<td></td>').text(res.module.name),
        $('<td></td>').append($('<span></span>').text(res.status).addClass('badge').addClass(res.status ? 'badge-success' : 'badge-dark')),
        $('<td></td>').text(taglist.join(',')),
        $('<td></td>').append($('<a></a>').text('编辑').addClass('btn btn-pill btn-sm btn-info').attr('href', `case_view.html?case_id=${res.id}`),
          $('<button></button>').text('删除').addClass('btn btn-pill btn-sm btn-danger').attr('data-toggle', "modal").attr('data-target', "#dangerModal")),
      );
      $('.card-body tbody').append(tr) //添加数据
    }
  }
}

//用例详情
function case_view(case_id) {
  $.ajax({
    type: 'get',
    data: {'id': case_id},
    url: '/api/case/',
    contentType: 'application/json; charset=utf-8',
    success: function (result, textStatus) {
      if(result.retcode===200){
        paint_case_view(result);
      }else if(result.retcode===403){
        console.log('未登录,开始重定向')
        location.href = result.to
      }
    },
    error: function () {
      console.log('没找到哦');
    }
  });
}

function paint_case_view(result){
  testcase = result.retlist[0];
  $('input[name="desc"]').val(testcase.desc);  //更新描述
  $('.c-switch-input[name="status"]').prop('checked',testcase.status);  //更新状态
  //更新下拉列表--项目
  common_attach('/api/project/', 'select[name="project_id"]', testcase.module.project);
  //更新下拉列表--模块
  common_attach('/api/module/', 'select[name="module_id"]', testcase.module.id);
  //模块选择框关联项目选择
  select_onchange('select[name="project_id"]', 'select[name="module_id"]', '/api/module/',);

  //拷贝例行模板
  let row_temp = $('.card-footer tbody tr:nth-last-child(1)');
  //测试用例刷新
  if (testcase.steps.length > 0) {
    console.log('update steplist')
    //删除所有行
    $('.card-footer tbody tr').each(function () {
      $(this).remove();
    });
    for (let step of testcase.steps) {
      // 新增一行
      $('.card-footer tbody').append(row_temp[0].outerHTML);
      // 填充序号
      $('.card-footer tbody tr:nth-last-child(1) h5').text(step.step_no)
      // 填充步骤id
      $('.card-footer tbody tr:nth-last-child(1) span').attr('title',step.id)
      // 填充接口
      common_attach('/api/httpapi/', 'tr:nth-last-child(1) select[name="httpapi_id"]',
        step.httpapi, {'module_id': testcase.module.id});
      // 填充预期结果
      $('.card-footer tbody tr:nth-last-child(1) input[name="expect"]').val(step.expected);
      // 填充描述
      $('.card-footer tbody tr:nth-last-child(1) input[name="step_desc"]').val(step.desc);
    }
  } else {
    //更新接口下拉
    let seleted_module = $('select[name="httpapi_id"] option:selected').val(); //查看当前选择的模块
    let res = common_attach('/api/httpapi/', 'select[name="httpapi_id"]', seleted_module);
    $('.card-footer tbody tr:nth-last-child(1) input[name="step_desc"]').val('');
  }
}

//用户所关联项目
function attach_projects(testcase) {
  $.ajax({
    type: 'get',
    data: {},
    url: '/api/project/',
    contentType: 'application/json; charset=utf-8',
    success: function (result, textStatus) {
      let select_btn = $('select[name="project_id"]')
      //清除原有option只保留默认
      select_btn.children('option').remove()
      select_btn.append('<option>选择项目</option>')
      projects = result.retlist;
      for (const project of projects) {
        //重新关联项目列表
        select_btn.append($('<option></option>').val(project.id).text(project.name));
      }
      //查看默认选项
      select_btn.children('option').each(function () {
        if ($(this).val() == testcase.module.project) {
          $(this).attr('selected', '');
        }
      });
    },
    error: function () {
      console.log('没找到哦');
    }
  });
}
//关联模块
function attach_modules(testcase) {
  $.ajax({
    type: 'get',
    data: {},
    url: '/api/module/',
    contentType: 'application/json; charset=utf-8',
    success: function (result, textStatus) {
      let select_btn = $('select[name="module_id"]')
      //清除原有option只保留默认
      select_btn.children('option').remove()
      select_btn.append('<option>选择模块</option>')
      items = result.retlist;
      for (const item of items) {
        //重新关联项目列表
        select_btn.append($('<option></option>').val(item.id).text(item.name));
      }
      //查看默认选项
      select_btn.children('option').each(function () {
        if ($(this).val() == testcase.module.id) {
          $(this).attr('selected', '');
        }
      });
    },
    error: function () {
      console.log('没找到哦');
    }
  });
}

//保存step
function save_step(target,case_id){
  const csrftoken = getCookie('csrftoken');
  //逻辑--如果存在就发送修改请求，如果不存在，就发送创建请求
  let _id = $(target).parent().parent().find('td:nth-child(1) span').attr('title');

  let step_no = $(target).parent().parent().find('td:nth-child(1)').text();
  let httpapi_id = $(target).parent().parent().find('[name="httpapi_id"]').val();
  let expected = $(target).parent().parent().find('[name="expect"]').val();
  let step_desc = $(target).parent().parent().find('[name="step_desc"]').val();
  console.log(_id)
  if(_id){
    $.ajax({
      type: 'put',
      data: JSON.stringify({'step_no':step_no,'httpapi_id':httpapi_id,'expected':expected,'desc':step_desc,'case_id':case_id,'status':0}),
      url: '/api/step/?id='+_id,
      contentType: 'application/json; charset=utf-8',
      headers: {'X-CSRFToken': csrftoken},
      success: function (result,TextStatus){
        console.log('success');
      },
      error:function (result,TextStatus){
        console.log('fail'+result.msg);
      },
    })
  }else{
    $.ajax({
      type: 'post',
      data: JSON.stringify({'step_no':step_no,'httpapi_id':httpapi_id,'expected':expected,'desc':step_desc,'case_id':case_id,'status':0}),
      url: '/api/step/',
      cache: false,
      contentType: 'application/json; charset=utf-8',
      headers: {'X-CSRFToken': csrftoken},
      success: function (result,TextStatus){
        //回写ID
        $(target).parent().parent().find('td:nth-child(1)').append('<span></span>');
        $(target).parent().parent().find('td:nth-child(1) span').attr('title',result.id)
        //再新增1行

      },
      error:function (result,TextStatus){
        console.log('fail'+result.msg);
      },
    })
  }
}

//删除步骤
function delete_step(target) {
  const csrftoken = getCookie('csrftoken')
  let _id = $(target).parent().parent().find('td:nth-child(1) span').attr('title');
  if(_id) {
    $.ajax({
      type: 'delete',
      data: {},
      url: '/api/step/?id=' + _id,
      contentType: 'application/json; charset=utf-8',
      headers: {'X-CSRFToken': csrftoken},
      success: function (result, TextStatus) {
        //判断请求的retcode
        let retcode = result.retcode
        if (retcode === 200) {
          //删除该行
          $(target).parent().parent().remove();
          resort_stepNO();
        } else {
          console.log('删除失败');
        }
      },
      error: function (result, TextStatus) {
        console.log('fail' + result.msg);
      },
    })
  }else {
    $(target).parent().parent().remove();
    resort_stepNO();
  }
}

//提交用例修改
function update_case(_id) {
  const  csrftoken = getCookie('csrftoken')
  //获取信息
  const desc = $('input[name="desc"]').val();
  const status = $('.c-switch-input[name="status"]').prop("checked");
  const module = $('select[name="module_id"] option:selected').val();
  let project_id = $('select[name="project_id"] option:selected').val();
  let steps = table_data(0, 5);  // 从序号到测试步骤
  let kwargs = {'desc': desc, 'status': status, 'moudle_id': module,'project_id':project_id ,'step_list': steps}
  //提交信息
  $.ajax({
    type: 'put',
    data: JSON.stringify(kwargs),
    url: '/api/case/?id='+_id,
    contentType: 'application/json; charset=utf-8',
    headers: {'X-CSRFToken': csrftoken},
    success: function (result, TextStatus) {
      console.log('success');
      //返回测试用例列表
      window.location.href='testcase.html';
    },
    error: function (result, TextStatus) {
      console.log('fail');
    },
  })
}

//新增测试用例表单
function attach_case(params) {
  //项目
  common_attach('/api/project/', '[name="project_id"]');
  //项目关联模块更新
  select_onchange('[name="project_id"]', '[name="module_id"]', '/api/module/')
}

function new_case() {
  const csrftoken = getCookie('csrftoken');
  //收集数据
  let module_id = $('select[name="module_id"] option:selected').val();
  let project_id = $('select[name="project_id"] option:selected').val();
  let desc = $('input[name="desc"]').val();
  //提交
  $.ajax({
    type: 'post',
    data: JSON.stringify({'desc': desc, 'module_id': module_id,'project_id':project_id}),
    url: '/api/case/',
    cache: false,
    contentType: 'application/json; charset=utf-8',
    headers: {'X-CSRFToken': csrftoken},
    success: function (result, TextStatus) {
      $('[data-dismiss="modal"]').click();
      $('#res_table').bootstrapTable('refresh'); //刷新
    },
    error: function (result, TextStatus) {
      $('[data-dismiss="modal"]').click();
      alert('服务器错误，添加失败');
    },
  })
}

function delete_case(_id) {
  return common_delete(_id,'/api/case/')
}

function addFunctionAlty(value, row, index) {
  return [
    `<a id="edit" class="btn btn-pill btn-sm btn-info" href="case_view.html?case_id=${row.id}">查看</a>`,
    '<button id="delete" class="btn btn-pill btn-sm btn-danger" data-toggle="modal" data-target="#delete_modal">删除</button>',
  ].join('');
}

let operateEvents = {
  'click #edit': function (e, value, row, index) {
  },'click #delete': function (e, value, row, index) {
    function to_delete_item() {
      console.log('delete,row: '+row.id)
      delete_case(row.id)
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
  title: '描述',
  field: 'desc',
}, {
  title: '项目',
  field: 'project.name',
},{
  title: '模块',
  field: 'module.name',
},{
  title: '状态',
  field: 'status',
  formatter:parse_status,
},{
  title: '标签',
  field: 'tags',
  formatter:parse_tag,
},{
  title: '操作',
  events: operateEvents,//给按钮注册事件
  formatter: addFunctionAlty//表格中增加按钮
}
]

function parse_tag(value, row, index) {
  return value.map((v,index)=>{return v.name})
}

function parse_status(value, row, index) {
  let span = $('<span></span>').addClass('badge')
  if(value){
    span.addClass('badge-success').text(value)
  }else {
    span.addClass('badge-dark').text(value)
  }
  return span.prop("outerHTML")  //返回html内容
}