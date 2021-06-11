# coding=gbk

class StatusConf:
    http_method = (
        'get',
        'post',
        'put',
        'delete'
    )
    content_types = (
        'application/json',
        'application/x-www-form-urlencoded',
    )

    # 定义一个子类，存储步骤状态值
    class step_status:
        standby = 0
        running = 1
        breaked = 2
        success = 3
        falied = 4
        error = 5

    class plan_status:
        standby = 0
        running = 1
        breaked = 2
        done = 3
