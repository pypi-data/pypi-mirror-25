#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string,re
from collections import defaultdict
import jieba



if __name__ == '__main__':
	text1 = '#楚乔传# #赵丽颖快乐大本营# @赵丽颖 replay [心][心][心]#鹿晗# @M鹿M 140.611 快乐//@Yusunly:赵丽颖[心][心]'
	#get_backward_match_features(text1)
	X = "AGGTAB"
	Y = "GXTXAYB"
	print("Length of LCS is "), lcs_dp(X , Y)



# 获取后向最大匹配的关键词
def get_backward_match_features(text, keys, replace = False, min_len = 1, max_len = 10):
	ind_pairs = backward_max_match(text, keys, min_len, max_len)
	
	features = []
	for start, end in ind_pairs:
		if replace:
			features.insert(0, keys.get(text[start: end]))
		else:
			features.insert(0, text[start: end])
		
	return features

# 后向最大匹配
def backward_max_match(text, keys, min_len = 1, max_len = 10):
	ind_list = []
	ind = len(text)
	
	while(ind > 0):
		j = ind - max_len
		
		while(j < ind):
			if j < 0:
				j += 1
				continue
				
			word = text[j: ind]
			if word in keys:
				ind_list.append((j, ind))
				ind = j + 1
				break
			else:
				j += 1
				
		ind -= 1
	return ind_list

# 最长公共子串
def lcs_dp(a, b):
	lengths = [[0 for j in range(len(b)+1)] for i in range(len(a)+1)]
	# row 0 and column 0 are initialized to 0 already
	for i, x in enumerate(a):
		for j, y in enumerate(b):
			if x == y:
				lengths[i+1][j+1] = lengths[i][j] + 1
			else:
				lengths[i+1][j+1] = max(lengths[i+1][j], lengths[i][j+1])
	# read the substring out from the matrix
	result = ""
	x, y = len(a), len(b)
	while x != 0 and y != 0:
		if lengths[x][y] == lengths[x-1][y]:
			x -= 1
		elif lengths[x][y] == lengths[x][y-1]:
			y -= 1
		else:
			assert a[x-1] == b[y-1]
			result = a[x-1] + result
			x -= 1
			y -= 1
	return result

# A Naive recursive Python implementation of LCS problem
# 效率低，建议使用lcs_dp
def lcs(X, Y, m, n):
 
	if m == 0 or n == 0:
		return 0
	elif X[m-1] == Y[n-1]:
		return 1 + lcs(X, Y, m-1, n-1)
	else:
		return max(lcs(X, Y, m, n-1), lcs(X, Y, m-1, n));