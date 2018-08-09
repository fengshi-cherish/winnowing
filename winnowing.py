# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 23:02:27 2018

@author: Cherish
"""

import re, os

def preprocessing(filename):
    with open(filename) as f:
        content = f.read()
        pattern = re.compile(r'[\s+] | [^a-zA-Z]')  #去除所有空白字符或者标点符号
        content = pattern.sub('', content)
        content = content.lower()
        return content
    

def gengerate_n_gram(string, n):
    n_gram = []
    for i in range(len(string) - n + 1):
        n_gram.append(string[i:i + n])
    return n_gram



def calculate_hashing_set(n_gram, Base, n):
    hashinglist = []
    hash = 0
    
    first_gram = n_gram[0]
    
    #单独计算第一个n_gram的哈希值
    for i in range(n):
        hash += ord(first_gram[i]) * (Base**(n - i - 1))
    hashinglist.append(hash)
    
    
    for i in range(1, len(n_gram)):
        pre_gram = n_gram[i-1]
        this_gram = n_gram[i]
        hash = (hash - ord(pre_gram[0])*(Base**(n-1)))*Base + ord(this_gram[n - 1])
        hashinglist.append(hash)
        
    return hashinglist

#核心函数，计算一篇文章哈希值的数据摘要，算法为winnowing
def winnowing(hashinglist, t, n):
    window = t - n + 1
    min_val = 0
    min_index  = 0
    fingerprint = {}
    for i in range(len(hashinglist) - window + 1):
        temp = hashinglist[i:i + window]
        min_val = temp[0]
        min_index = 0
        for j in range(window):
            if temp[j] <= min_val:
                min_val = temp[j]
                min_index = j
        if (i + min_index) not in fingerprint.keys():
            fingerprint[i + min_index] = min_val
    return fingerprint


#比较两个文档的相似性
def comparison(fingerprint_1, fingerprint_2):
    count = 0
    size = min(len(fingerprint_1), len(fingerprint_2))
    for i in fingerprint_1.values():
        for j in fingerprint_2.values():
            if i == j:
                count += 1
                break
    return count / size

if __name__ == '__main__':
    dirpath = os.getcwd()
    n = 5
    t = 9
    Base = 17
    print('n = 5, t = 9' )
    path_1 = dirpath + '\\text1.txt'
    path_2 = dirpath + '\\text2.txt'
    fingerprint_1 = winnowing(calculate_hashing_set(gengerate_n_gram(preprocessing(path_1), n), Base, n), t, n)
    fingerprint_2 = winnowing(calculate_hashing_set(gengerate_n_gram(preprocessing(path_2), n), Base, n), t, n)
    similiarize = comparison(fingerprint_1, fingerprint_2)
    print('两篇文章的相似度为{:5f}'.format(similiarize))
    