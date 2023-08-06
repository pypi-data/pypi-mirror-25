import re

_OPERATOR_MAPPING = {
    "!": "!=",
    "~": "LIKE",
    "!~": "NOT LIKE"
}


def _get_operator(string):
    """
    解析字符串获得操作符和字段名
    :param string:
    :return:
    """
    o = re.findall("^([a-zA-Z_]+)(?:\[(.+)\])?$", string)
    if len(o) < 1:  # 匹配失败
        raise Exception('Illegal syntax of expression: ' + string)
    o = list(o[0])  # 原先是tuple
    if len(o[1]) < 1:  # 未填写操作符，默认等号
        o[1] = '='
    if o[1] in _OPERATOR_MAPPING:
        o[1] = _OPERATOR_MAPPING[o[1]]
    return o


def _parse_condition(*args):
    """
    解析条件语句
    :param args:
    :return:
    """
    conj = 'AND'
    if len(args) < 1:
        raise ValueError('This method need at least one param!')
    elif len(args) == 1 and isinstance(args[0], str):  # SQL格式
        return args[0], None
    elif len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], tuple):  # SQL格式带参数
        return args
    elif len(args) == 2 and isinstance(args[0], str):  # 单行，=号
        cond = {args[0]: args[1]}
    elif len(args) == 3 and isinstance(args[0], str):  # 单行
        cond = {'%s[%s]' % (args[0], str(args[1])): args[2]}
    elif isinstance(args[0], dict):
        cond = args[0]
        if len(args) == 2 and isinstance(args[1], str):
            conj = args[1]
    else:
        raise ValueError('Illegal param!')
    return _parse_dict_condition(cond, conj)


def _parse_dict_condition(obj, conj='AND'):
    """
    由字典
    :param obj: 字典对象
    :param conj: 连接词
    :return:
    """
    if conj not in ['AND', 'OR']:  # 检查连接词是否合法
        raise ValueError('Unknown conjunction: ' + conj)
    cond = ''
    value_set = []  # 存放预编译用参数
    for (k, v) in obj.items():
        if isinstance(v, dict):  # 解析嵌套
            op = re.findall('\((.+)\).?', k)
            if len(op) < 1:
                raise Exception('Illegal syntax of expression: ' + k)
            inner = _parse_dict_condition(v, op[0])  # 递归解决此类嵌套
            cond += ' %s (%s)' % (conj, inner[0])
            value_set += inner[1]
            continue
        o = _get_operator(k)
        if isinstance(v, list):
            not_ = ''
            if o[1] in ['<>', '><']:  # 为BETWEEN
                if not len(v) == 2:
                    raise Exception('Illegal length for value: ' + str(v))
                if o[1] == '<>':
                    not_ = 'NOT '
                cond += ' %s (`%s` %sBETWEEN ? AND ?)' % (conj, o[0], not_)
            else:  # 为IN
                if o[1] == '!=':  # 不用判断!，已经被转为!=
                    not_ = 'NOT '
                cond += ' %s `%s` %sIN (' % (conj, o[0], not_) \
                        + ('?,' * len(v))[:-1] + ')'
            value_set += v
        else:
            cond += " %s `%s` %s ?" % (conj, o[0], o[1])
            value_set.append(v)
    return cond[len(conj) + 2:], value_set


print(_parse_condition('`id` = 2'))

print(_parse_condition('id', 2))

print(_parse_condition('id', '>=', 2))

print(_parse_condition({
    'id[>=]': 2,
    'date[>=]': '2017-1-1',
    '(OR)vip': {
        'is_vip': True,
        'is_svip': True,
        'has_vip[!]': ['vip', 'svip', 'ssvip']
    },
    'level[<>]': [2, 20]
}))

print(_parse_condition({
    'id[>=]': 2,
    'date[>=]': '2017-1-1',
    '(OR)vip': {
        'is_vip': True,
        'is_svip': True,
        'has_vip[!]': ['vip', 'svip', 'ssvip']
    },
    'level[<>]': [2, 20]
}, 'OR'))

'''
usage: 仅一次
where('cond')
where('cond', param)

可叠加
where('a', '1') `a`=1
where('a', '>=','1') `a`>=1
where(('a', '1'), ('b', '>','1')) `a`=1 AND `b`>1
where({
})
'''
