#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: leslie
# date: 2017-08-24
# email: 249893977@qq.com

# cluster的高频词
def top_terms_per_cluster(km, cluster_n, vectorizer):
    print("Top terms per cluster:")

    order_centroids = km.cluster_centers_.argsort()[:, ::-1]

    terms = vectorizer.get_feature_names()
    for i in range(cluster_n):
        print("Cluster %d:" % i, end='')
        for ind in order_centroids[i, :10]:
            print(' %s' % terms[ind], end='')
        print()


# 随机获取cluster中的一条文本
def get_random_text(cluster, n, mean, std):
    while True:
        try:
            ind = cluster.index[np.random.randint(n)]
            text = cluster[ind]
            if len(text) > (mean - std) and len(text) < (mean + std):
                break
        except ValueError:
            print(ValueError)
            
            
    return text
            

# 在聚类中找出最长公共字符串
def length_of_longest_common_substr_in_cluster(cluster, n, mean, std):
    if n > 50000:
        print('数组太长了，做不了')
        return -1
    
    flag_text = get_random_text(cluster, n, mean, std)
    
    common_count = 0
    longest_common_length = mean - std
    longest_common_str = None
    print('max length change to: {}'.format(longest_common_length))
    
    for text in cluster:
        common_str = lcs_dp(flag_text , text)
        length = len(commons_str)
        if length > longest_common_length:
            if length <= mean:
                longest_common_length = length
                longest_common_str = common_str
                print('max length change to: {}, {}'.format(longest_common_length, longest_common_str))
            common_count += 1
        elif length > longest_common_length / 2:
            common_count += 1
        else:
            continue
    
    ratio = float(common_count/n)
    print('common ratio: {}'.format(round(ratio, 2)))
    
    return ratio, longest_common_str