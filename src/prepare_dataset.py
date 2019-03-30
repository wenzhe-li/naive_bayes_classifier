# coding=utf-8
# @Time    : 2019/3/24
# @Author  : Scott Li
# @Contact : liwz17@mails.tsinghua.edu.cn
# @Version : 2.1 - released
# @Notes   : use the words bag model and head information

import time
import json
import re
from collections import Counter


def prepare_dataset():
    start = time.strftime("%Y%m%d %X", time.localtime())

    with open('./trec06c-utf8/label/index', 'r', encoding='utf-8') as f:
        labels = [line.split()[0] for line in f.readlines()]

    with open('./trec06c-utf8/label/index', 'r', encoding='utf-8') as f:
        paths = [line.split()[1] for line in f.readlines()]

    inputs = list()  # 每封邮件中词的计数
    priority = list()  # 信头-优先级
    send_address = list()  # 发件人一致性
    receive_address = list()  # 收件人一致性
    times = list()  # 发信时间

    for path in paths:
        with open('./trec06c-utf8/data_cut'+path[7:], 'r', encoding='utf-8') as f:
            head, content = f.read().split('\n\n', 1)
            try:
                hour = re.search('Date: .*([0-9]{2}):.*:.*', head).group(1)
                if int(hour) <= 6:
                    times.append(0)
                else:
                    times.append(1)
            except:
                times.append(-1)
            try:
                send1 = re.search('Received: from ([0-9a-zA-Z\.]*) ', head).group(1)
                send2 = re.search('From: .*@([0-9a-zA-Z\.]*)', head).group(1)
                if send1 == send2:
                    send_address.append(1)
                else:
                    send_address.append(0)
            except:
                send_address.append(0)
            try:
                receive1 = re.search('for <([@0-9a-zA-Z\.]*)>', head).group(1)
                receive2 = re.search('\nTo: ([@0-9a-zA-Z\.]*)', head).group(1)
                if receive1 == receive2:
                    receive_address.append(1)
                else:
                    receive_address.append(0)
            except:
                receive_address.append(0)
            if re.search('X-Priority: ([0-9])', head) is None:
                priority.append(-1)
            else:
                p = re.search('X-Priority: ([0-9])', head).group(1)
                priority.append(int(p))
            # 过滤标点符号
            filterate = re.compile(u'[^\u4E00-\u9FA5]')
            content = filterate.sub(r' ', content)
            # 空格去重
            content = re.sub('\s\s+', ' ', content)
            words = content.split()
            words = Counter(words)
            inputs.append(words)

    sample = dict()
    sample['input'] = inputs
    sample['label'] = labels
    sample['priority'] = priority
    sample['send_address'] = send_address
    sample['receive_address'] = receive_address
    sample['times'] = times

    with open('sample.json', 'w', encoding='utf-8') as json_file:
        json.dump(sample, json_file, ensure_ascii=False)

    end = time.strftime("%Y%m%d %X", time.localtime())

    print('from %s to %s' % (start, end))
