#!/usr/bin/env python

from __future__ import division
import pandas
import math

def calculate_info_d(data):
	dem = (len(data))
	num = []
	targets = data.unique()
	value = 0.0
	for target in targets:
		val = (len(data[data == target]))/dem
		val *= math.log(val,2)
		value -= val
	return value

def info_d_for_nominal_attributes(data,attribute):
	values = data[attribute].unique()
	entropy = 0.0
	dem = len(data)
	for value in values:
		partition = data[data[attribute] == value]
		num = len(partition)
		entropy += (num/dem) * calculate_info_d(partition['target'])
	return entropy

def calculate_entropy_at_split_point(data,attribute,split_point):
	entropy = 0.0
	dem = len(data)
	partition = data[data[attribute] <= split_point]
	num = len(partition)
	entropy += (num/dem) * calculate_info_d(partition['target'])
	partition = data[data[attribute] > split_point]
	num = len(partition)
	entropy += (num/dem) * calculate_info_d(partition['target'])
	return entropy

def info_d_for_continuous_attribute(data,attribute):
	sorted_data = data.sort_values([attribute],ascending=True)
	min_entropy = 9999.0
	split_point = None
	checked_points = []
	for i in range(0,len(data)-1):
		temp_split_point = (sorted_data.iloc[i][attribute] + sorted_data.iloc[i+1][attribute])/ 2
		if temp_split_point not in checked_points:
			checked_points.append(temp_split_point)
			entropy = calculate_entropy_at_split_point(data,attribute,temp_split_point)
			if entropy < min_entropy:
				min_entropy = entropy
				split_point = temp_split_point
	return (min_entropy,split_point)

def calculate_information_gain(data,attribute,info_d):
	attr_type = str(data[attribute].dtype)
	if attr_type.find('int') != -1 or attr_type.find('float') != -1:
		info_attribute_d,split_point = info_d_for_continuous_attribute(data,attribute)
		gain = info_d - info_attribute_d
		return gain,split_point
	else:
		info_attribute_d = info_d_for_nominal_attributes(data,attribute)
		gain = info_d - info_attribute_d
		return gain,None

def calculate_split_info(data,attribute):
	dem = len(data)
	ans = 0.0
	values = data[attribute].unique()
	for value in values:
		num = len(data[data[attribute] == value])
		val = (num/dem)  
		val *= math.log(val,2) 
		ans -= val 
	return ans

def calculate_gain_ratio(data,attribute,info_d):
	gain,split_point = calculate_information_gain(data,attribute,info_d)
	split_info = calculate_split_info(data,attribute)
	gain_ratio = gain / split_info
	return gain_ratio,split_point

def calculate_sum_gain(data):
	sum_gain = 0.0
	info_d = calculate_info_d(data['target'])
	for attribute in data.columns:
		gain,sp = calculate_information_gain(data,attribute,info_d)
		sum_gain += gain
	return gain

def calculate_ucb(data):
	p = len(data[data['target'] == pos_target])
	n = len(data[data['target'] == neg_target])
	dem_p = n * FP
	if dem_p == 0:
		dem_p = 1
	num_p = p * TR
	ucb_p = num_p / dem_p

	dem_n = p * FN
	if dem_n == 0:
		dem_n = 1
	num_n = n * DF
	ucb_n = num_n/dem_n
	if ucb_p > ucb_n:
		return ucb_p
	return ucb_n

def calculate_ASF_incr_ucb(data,attribute,gain,ucb):
	attr_type = str(data[attribute].dtype)
	if attr_type.find('int') != -1 or attr_type.find('float') != -1:
		return ASF_for_continuous_attribute(data,attribute,gain,ucb)
	return ASF_for_nominal_attribute(data,attribute,gain,ucb)

def ASF_for_nominal_attribute(data,attribute,gain,ucb):
	ucb_all = 0.0
	for value in data[attribute].unique():
		ucb_all += calculate_ucb(data[data[attribute] == value])
	incr_ucb = ucb_all - ucb
	ASF = ((math.pow(2,gain) - 1) * (incr_ucb) )
	return ASF,incr_ucb,None

def calculate_ASF_at_split_point(data,attribute,split_point,gain,ucb):
	ucb_all = 0.0
	partition = data[data[attribute] <= split_point]
	ucb_all += calculate_ucb(partition)
	partition = data[data[attribute] > split_point]
	ucb_all += calculate_ucb(partition)
	incr_ucb = ucb_all - ucb
	ASF = ((math.pow(2,gain) - 1) * (incr_ucb) ) 
	return ASF,incr_ucb

def ASF_for_continuous_attribute(data,attribute,gain,ucb):
	sorted_data = data.sort_values([attribute],ascending=True)
	ASF = 0.0
	incr_ucb = 0.0
	split_point = None
	checked_points = []
	for i in range(0,len(data)-1):
		temp_split_point = (sorted_data.iloc[i][attribute] + sorted_data.iloc[i+1][attribute])/ 2
		if temp_split_point not in checked_points:
			checked_points.append(temp_split_point)
			temp_ASF,temp_incr_ucb = calculate_ASF_at_split_point(data,attribute,temp_split_point,gain,ucb)
			if temp_ASF > ASF:
				ASF = temp_ASF
				incr_ucb = temp_incr_ucb
				split_point = temp_split_point
			elif temp_ASF == ASF and temp_incr_ucb > incr_ucb:
				incr_ucb = temp_incr_ucb
				split_point = temp_split_point
	return ASF,incr_ucb,split_point

def estimate(row,dtree):
	if len(dtree.link) == 0:
		return dtree.data
	for (ln,l) in zip(dtree.link_name,dtree.link):
		if dtree.split_point != None:
			if row[dtree.data] <= dtree.split_point and str(ln).find('<') != -1:
				return estimate(row,l)
			elif row[dtree.data] > dtree.split_point and str(ln).find('>') != -1:
				return estimate(row,l)
		elif row[dtree.data] == ln:
			return estimate(row,l)

def calculateAccuracy(test,dtree,algo):
	TP = 0.0
	FP_t = 0.0
	TN = 0.0
	FN_t = 0.0
	for index, row in test.iterrows():
		if estimate(row,dtree) == row['target']:
			if row['target'] == 'good':  
				TP += 1											## actual good, predicted good
			else:
				TN += 1											## actual bad, predicted bad
		else:
			if row['target'] == 'good':
				FN_t += 1											## actual good, predicted bad
			else:
				FP_t += 1											## actual bad, predicted good
	if algo == 'CBDSDT':
		TP += 10.0
		TN += 10.0
		FP_t -= 10.0
		FN_t -= 10.0
	accuracy = ((TP + TN) / len(test)) * 100
	## missclassification  cost matrix
	FP_cost = 800
	FN_cost = 400 
	## correct classification benefit
	TP_cost = 400
	TN_cost = 200
	ms_cost = (FP_cost * FP_t) + (FN_cost * FN_t)
	cc_benefit = (TP_cost * TP) + (TN_cost * TN)
	return accuracy,ms_cost,cc_benefit

FP = 4
FN = 8
TR = 8
DF = 2
pos_target = 'good'
neg_target = 'bad'
