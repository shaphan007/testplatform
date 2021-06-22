# coding=gbk


def info_handler(in_params, position_keys=None, option_keys=None):
    info = {}
    # 必填参数
    if position_keys is not None:
        for key in position_keys:
            if key not in in_params and not key.endswith('_ids'):
                return False
            info[key] = in_params[key]
    # 选填参数
    if option_keys is not None:
        for key in option_keys:
            if key in in_params and not key.endswith('_ids'):
                info[key] = in_params[key]
    return info


if __name__ == '__main__':
    position_keys = ['desc', 'module_id', 'project_id']  # 必填参数列表
    option_keys = ['status', 'tag_ids']
    in_params ={'desc': '555', 'module_id': '7', 'project_id': '62'}

    info = info_handler(in_params, position_keys=position_keys, option_keys=option_keys)
    print(info)
