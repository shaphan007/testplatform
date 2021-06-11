//注册
function register(){
    let username = $('input[name="username"]').val().trim();
    let email = $('input[name="email"]').val().trim();
    let password = $('input[name="password"]').val().trim();
    let confirm_psw = $('input[name="confirm_psw"]').val().trim();
    let nickname=$('input[name="nickname"]').val().trim();
    let admin_code=$('input[name="admin_code"]').val().trim();
    if(!username || !email || !password){
        return handler_alert('#warning_tips','请填写相关信息');//非空校验
    }
    if(password !== confirm_psw){  //检查两次密码是否输入一致
        return handler_alert('#warning_tips','两次密码输入不一致');
    }
    // if(is_admin !== 'sqtp'){  //验证管理员邀请码
    //     return handler_alert('#error_tips','邀请码不正确');
    // }
    let payload={}
    if(admin_code){
        payload={'username':username,'password':password,'email':email,'first_name':nickname,'admin_code':admin_code}
    }else {
        payload ={'username':username,'password':password,'email':email,'first_name':nickname}
    }
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        type: 'post',
        data: JSON.stringify(payload),
        url: '/api/user/register/',
        cache: false,
        contentType: 'application/json; charset=utf-8',
        headers: {'X-CSRFToken': csrftoken},
        success: function(result,TextStatus){
            if(result.retcode===400){
                return handler_alert('#warning_tips',result.msg);
            }else if (result.retcode===302){
                //重定向
                window.location.href = result.to
                return result.to
            }
        },
        error: function (result){
            return handler_alert('#error_tips',result.msg);
        },
    })

}

//登录
function doLogin(){
    const csrftoken = getCookie('csrftoken'); //从cookie获取django的crsftoken
    //开始登录
    let username = $('[placeholder="Username"]').val();
    let password = $('[placeholder="Password"]').val();
    if(username==='' || password ===''){
        return handler_alert('#empty_alert','密码不能为空');
    }
    if(getUrlParam('next')){
        var path = '/api/user/login/?next='+getUrlParam('next')
    }else {
        path = '/api/user/login/'
    }
    $.ajax({
        type: 'post',
        url: path,
        data:JSON.stringify({'username':username,'password':password}),
        contentType: 'application/json; charset=utf-8',
        headers: {'X-CSRFToken': csrftoken},
        success:function (result,textStatus){
            //重定向到目标页面
            if(result.retcode===302){
                window.location.href = result.to;
                return null;
            }
            handler_alert('#error_service',result.msg);
        },
        error:function (result){
            handler_alert('#error_service',result.msg);
        }
    })
}

