# coding=utf-8
# @Time    : 2019/3/24
# @Author  : Scott Li
# @Contact : liwz17@mails.tsinghua.edu.cn
# @Version : 2.1 - released
# @Notes   : use the words bag model and head information

from dataset_utils import *
import json
import numpy as np


def validate():
    print('Loading input and features')
    with open('./sample.json', 'r', encoding='utf-8') as json_file:
        vector = json.load(json_file)
    with open('./features.json', 'r', encoding='utf-8') as json_file:
        features = json.load(json_file)

    inputs = vector['input']
    labels = vector['label']
    send_address = vector['send_address']
    times = vector['times']

    vector_len = len(inputs[0])
    features = features['features']

    # 设置随机种子为1
    rng = np.random.RandomState(1)
    rand_ix = rng.permutation(TOTAL_SIZE)
    inputs = np.array(inputs)[rand_ix].tolist()
    labels = np.array(labels)[rand_ix].tolist()
    TRAIN_SIZE = 4 * SINGLE_SIZE

    avg_recall = 0  # 召回率
    avg_precision = 0  # 精确率
    avg_accuracy = 0  # 准确率
    avg_error_rate = 0  # 错误率

    for i in range(5):
        print('Round ', i)
        train_inputs = list()
        train_labels = list()
        validate_inputs = list()
        validate_labels = list()

        # 划分数据集
        for j in range(5):
            if j == i:
                validate_inputs = inputs[j*SINGLE_SIZE:((j+1)*SINGLE_SIZE)]
                validate_labels = labels[j*SINGLE_SIZE:((j+1)*SINGLE_SIZE)]
            else:
                train_inputs.extend(inputs[j*SINGLE_SIZE:((j+1)*SINGLE_SIZE)])
                train_labels.extend(labels[j*SINGLE_SIZE:((j+1)*SINGLE_SIZE)])

        spam_sum = dict()  # 垃圾邮件中每个词出现的次数
        ham_sum = dict()  # 非垃圾邮件中每个词出现的次数
        for j in features:
            spam_sum[j] = 0
            ham_sum[j] = 0

        total_spam = 0  # 垃圾邮件个数
        total_ham = 0  # 非垃圾邮件个数
        total_words_spam = 0  # 垃圾邮件总长度
        total_words_ham = 0  # 非垃圾邮件总长度

        priority_spam = [0, 0, 0, 0, 0, 0, 0]  # 垃圾邮件中各优先级邮件出现次数
        priority_ham = [0, 0, 0, 0, 0, 0, 0]  # 非垃圾邮件中各优先级邮件出现次数
        send_spam = [0, 0]  # 垃圾邮件中发件人一致性统计
        send_ham = [0, 0]  # 非垃圾邮件中发件人一致性统计
        time_spam = [0, 0, 0]  # 垃圾邮件中发信时间区域统计
        time_ham = [0, 0, 0]  # 非垃圾邮件中发信时间区域统计

        # 遍历训练集
        for j in range(TRAIN_SIZE):
            if train_labels[j] == 'spam':
                total_spam = total_spam + 1
                send_spam[send_address[j]] += 1
                time_spam[times[j] + 1] += 1
                for k in train_inputs[j].keys():
                    total_words_spam += train_inputs[j][k]
                    if k in spam_sum:
                        spam_sum[k] += train_inputs[j][k]
            else:
                total_ham = total_ham + 1
                send_ham[send_address[j]] += 1
                time_ham[times[j] + 1] += 1
                for k in train_inputs[j].keys():
                    total_words_ham += + train_inputs[j][k]
                    if k in ham_sum:
                        ham_sum[k] += + train_inputs[j][k]

        p_spam = total_spam / TRAIN_SIZE
        p_ham = total_ham / TRAIN_SIZE

        nss = 0  # spam->spam
        nsh = 0  # spam->ham
        nhs = 0  # ham->spam
        nhh = 0  # ham->ham

        print('Validating')
        for j in range(SINGLE_SIZE):
            words = validate_inputs[j]
            h_spam = np.log(p_spam) +\
                10 * np.log((send_spam[send_address[j]] + 1) / (total_spam + 2)) +\
                np.log((time_spam[times[j] + 1] + 1) / (total_spam + 3))
            h_ham = np.log(p_ham) +\
                10 * np.log((send_ham[send_address[j]] + 1) / (total_ham + 2)) +\
                np.log((time_ham[times[j] + 1] + 1) / (total_ham + 3))
            for k in words.keys():
                if k in spam_sum:
                    h_spam = h_spam + np.log((words[k] * spam_sum[k] + 1) / (total_words_spam + vector_len))
                    h_ham = h_ham + np.log((words[k] * ham_sum[k] + 1) / (total_words_ham + vector_len))
            if h_spam > h_ham:
                output = 'spam'
            else:
                output = 'ham'
            if output == validate_labels[j]:
                if output == 'ham':
                    nhh += 1
                else:
                    nss += 1
            else:
                if output == 'ham':
                    nhs += 1
                else:
                    nsh += 1

        recall = nss / (nss + nsh)
        precision = nss / (nss + nhs)
        accuracy = (nhh + nss) / SINGLE_SIZE
        error_rate = (nsh + nhs) / SINGLE_SIZE

        # print('recall: ', recall)
        # print('precision: ', precision)
        print('accuracy: ', accuracy)
        # print('error_rate: ', error_rate)
        # print('F: ', 2 * recall * precision / (recall + precision))

        avg_recall += recall
        avg_precision += precision
        avg_accuracy += accuracy
        avg_error_rate += error_rate

    avg_recall /= 5    
    avg_precision /= 5
    avg_accuracy /= 5
    avg_error_rate /= 5

    print('avg_recall: ', avg_recall)
    print('avg_precision: ', avg_precision)
    print('avg_accuracy: ', avg_accuracy)
    print('avg_error_rate: ', avg_error_rate)
    print('avg_F: ', 2 * avg_recall * avg_precision / (avg_recall + avg_precision))


if __name__ == '__main__':
    validate()