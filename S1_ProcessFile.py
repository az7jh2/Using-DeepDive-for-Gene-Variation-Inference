# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 16:53:14 2017

@author: hill103
"""

"""
step 1: 读取数据，进行统计描述
注意：
1.文本中存在一些重复articles，有些是完全一样，有些是长度不一致
应对：按开始字符来识别重复articles，取长度最长的一个
2.文本中存在内容为null的row
应对：去除该row
3.有些row的文本中存在\t
应对：采用正则表达式将其替换为空格
4.postgresql不支持\0x00字符(表示unicode NUL)
应对：暂无好方法，只能删除该row，共21行，另外有2行含有\字符，会引起end-of-copy marker corrupt error，也被删除
"""

import csv
import matplotlib.pyplot as plt
import os
import json
import re
from random import shuffle

#-----------------------------------------------------------------------------#
def readData(variant_file, text_file, label):
    # 读取variant_file和text_file，返回数据dict
    # label用于加在ID前，以区分train和test
    f1 = open(variant_file, "rb")
    f2 = open(text_file, "rt")
    reader1 = csv.reader(f1)
    # 变量名依次为"ID", "Gene", "Variation", "Class"
    reader1.next()
    # 读入data
    data = []
    for row in reader1:
        if len(row) == 4:
            data.append({"ID":label+"_"+row[0].strip(), "Gene":row[1].strip(),
                     "Variation":row[2].strip(), "Class":int(row[3].strip())})
        elif len(row) == 3:
            data.append({"ID":label+"_"+row[0].strip(), "Gene":row[1].strip(),
                     "Variation":row[2].strip(), "Class":-1})
        else:
            raise Exception("Error in reading variant file!")
    # 添加text信息
    # 使用正则表达式处理\t
    f2.readline()
    for row, d in zip(f2.readlines(), data):
        d["Text"] = re.sub(r"\s+", " ", row.split("||")[1].strip())
        d["Text_Length"] = len(d["Text"])
    return data
    

def countFrequency(lst):
    # 计算list中各元素的frequency，并按频率降序排列
    count = {}
    for element in lst:
        count[element] = count.get(element, 0) + 1
    # 返回name和frequency两个list
    name = []
    freq = []
    for k, v in sorted(count.items(), key=lambda x:x[1], reverse=True):
        name.append(k)
        freq.append(v)
    return name, freq
    
    
def exploreDistribution(lst, index, title):
    # 对list中的元素做bar图，看分布
    # 超过index个元素的，其余命名为"Others"
    name, freq = countFrequency(lst)
    if len(name) > index:
        tmp_sum = 0
        for i in range(index, len(name)):
            tmp_sum += freq[i]
        name[index:] = ["Others"]
        freq[index:] = [tmp_sum]
    # 作图
    fig = plt.figure()
    plt.bar(range(len(name)), freq, align="center")
    plt.xticks(range(len(name)), name)
    plt.ylabel("Frequency")
    plt.title(title)
    # 横坐标斜着排列
    fig.autofmt_xdate()
    plt.show()
    
    
def getUniElement(data, key):
    # 统计字典中key的非重复列表
    # 采用set来判断重复元素，注意set是无序的
    output = set()
    for d in data:
        if d[key] not in output:
            output.add(d[key])
    print "Number of unique %s elements: %d." % (key, len(output))
    return sorted(list(output))
    

def getLongestText(indexs, data):
    # 从多个索引中，返回具有最大articles长度的索引
    if len(indexs) == 1:
        return indexs[0]
    text_len = []
    for i in indexs:
        text_len.append(data[i]["Text_Length"])
    # 寻找最大articles长度
    tmp_index = text_len.index(max(text_len))
    return indexs[tmp_index]
    
        
def getUniText(data):
    # 返回非重复的articles
    # 利用dict的key来判断重复元素，注意dict是无序的
    # 采用前50个字符来判断articles是否重复，记录下index，最后选取文本长度最长的
    tmp_dict = {}
    for i in range(len(data)):
        if data[i]["Text"] == "null":
            continue
        # 采用前50个字符来判断articles是否重复
        text_pre = data[i]["Text"][:50]
        if tmp_dict.has_key(text_pre):
            tmp_dict[text_pre].append(i)
        else:
            tmp_dict[text_pre] = [i]
    # 选取长度最长的articles对应的index
    tmp_index = []
    for item in tmp_dict.values():
        tmp_index.append(getLongestText(item, data))
    # 按顺序返回对应的id和text
    output = []
    for i in sorted(tmp_index):
        output.append([data[i]["ID"], data[i]["Text"]])
    print "Number of unique articles: %d." % len(output)
    return output
#-----------------------------------------------------------------------------#

# main function
cwd = os.getcwd()

train_text_file = os.path.join(cwd, "RawData", "training_text")
train_variant_file = os.path.join(cwd, "RawData", "training_variants")
test_text_file = os.path.join(cwd, "RawData", "test_text")
test_variant_file = os.path.join(cwd, "RawData", "test_variants")

train_data = readData(train_variant_file, train_text_file, "Train")
test_data = readData(test_variant_file, test_text_file, "Test")
"""
# 统计数据中gene和variation的分布
exploreDistribution([d["Gene"] for d in train_data], 5, "Gene Distribution in Train Data")
exploreDistribution([d["Variation"] for d in train_data], 5, "Variation Distribution in Train Data")
exploreDistribution([d["Gene"] for d in test_data], 5, "Gene Distribution in Test Data")
exploreDistribution([d["Variation"] for d in test_data], 5, "Variation Distribution in Test Data")
"""
"""
# 统计数据中因变量的9个类别分布
count = {}
for category in [d["Class"] for d in train_data]:
        count[category] = count.get(category, 0) + 1
name = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
count_for_plot = []
for num_str in name:
    count_for_plot.append(count[int(float(num_str))])
# bar图
plt.figure()
plt.bar(range(len(name)), count_for_plot, align="center")
plt.xticks(range(len(name)), name)
plt.ylabel("Frequency")
plt.title("Category Distribution of Dependent Variable")
plt.show()
"""
# 获取非重复的基因列表，保存成json格式
with open("gene_list.json", "w") as f:
    json.dump(getUniElement(train_data, "Gene"), f, indent=4)
# 获取非重复的变异列表，保存成json格式
with open("variation_list.json", "w") as f:
    json.dump(getUniElement(train_data, "Variation"), f, indent=4)
# 获取非重复的articles，保存成csv格式
with open("articles.tsv", "wb") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerows(getUniText(train_data))
# 在训练集中，随机3:1分出训练集和验证集，并保存成csv格式
l = range(len(train_data))
shuffle(l)
flag = [False] * len(train_data)
# 前1/4的数据，设置为验证集
for i in range(int(len(train_data) / 4.0)):
    flag[l[i]] = True
f1 = open("train_labels.tsv", "wb")
f2 = open("valid_labels.tsv", "wb")
writer_train = csv.writer(f1, delimiter="\t")
writer_valid = csv.writer(f2, delimiter="\t")
for i, d in enumerate(train_data):
    # True表示验证集，False表示训练集
    if flag[i]:
        writer_valid.writerow([d["Gene"], d["Variation"], d["Class"]-1])
    else:
        writer_train.writerow([d["Gene"], d["Variation"], d["Class"]-1])
f1.close()
f2.close()