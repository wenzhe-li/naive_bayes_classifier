# coding=utf-8
# @Time    : 2019/3/24
# @Author  : Scott Li
# @Contact : liwz17@mails.tsinghua.edu.cn
# @Version : 2.1 - released
# @Notes   : use the words bag model and head information

import json

lowerbound = 5  # 词频下界
upperbound = 1500  # 词频上界


def extract_features():
    with open('./sample.json', 'r', encoding='utf-8') as json_file:
        sample = json.load(json_file)

    inputs = sample['input']
    labels = sample['label']

    features = dict()

    # 统计每一个词在所有邮件中出现的次数
    for i in range(len(labels)):
        for word in inputs[i].keys():
            if word in features:
                features[word] = features[word] + inputs[i][word]
            else:
                features[word] = inputs[i][word]

    # 应用上下界，并且去除单个字
    vec = [k for k, v in features.items() if v > lowerbound and v < upperbound and len(k) > 1]

    # 应用停用表
    with open('./stopwords.txt', 'r', encoding='utf-8') as text_file:
        text = text_file.read()
    stopwords = text.split()

    for word in stopwords:
        if word in vec:
            vec.remove(word)

    print('number of features: ', len(vec))

    result = dict()
    result['features'] = vec

    with open('features.json', 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, ensure_ascii=False)
