#!/usr/bin/env python

import pandas
import globalFunc
import math

def ID3(data):
	splitting_attribute = None
	split_point = None
	max_gain = 0.0
	info_d = globalFunc.calculate_info_d(data['target'])
	for attribute in data.columns:
		if attribute != 'target' and len(data[attribute].unique()) > 1:
			gain,temp_split_point = globalFunc.calculate_information_gain(data,attribute,info_d)
			if gain > max_gain:
				max_gain = gain
				splitting_attribute = attribute
				split_point = temp_split_point
	return splitting_attribute,split_point

def C45(data):
	splitting_attribute = None
	max_gain_ratio = 0.0
	split_point = None
	info_d = globalFunc.calculate_info_d(data['target'])
	for attribute in data.columns:
		if attribute != 'target' and len(data[attribute].unique()) > 1:
			gain_ratio,temp_split_point = globalFunc.calculate_gain_ratio(data,attribute,info_d)
			if gain_ratio > max_gain_ratio:
				max_gain_ratio = gain_ratio
				splitting_attribute = attribute
				split_point = temp_split_point
	return splitting_attribute,split_point

def CBDSDT(data):
	splitting_attribute = None
	split_point = None
	max_ASF = 0.0
	max_incr_ucb = 0.0
	info_d = globalFunc.calculate_info_d(data['target']) 
	ucb = globalFunc.calculate_ucb(data)
	sum_gain = globalFunc.calculate_sum_gain(data)
	for attribute in data.columns:
		if attribute != 'target' and len(data[attribute].unique()) > 1:
			gain,sp = globalFunc.calculate_information_gain(data,attribute,info_d) 
			ASF,incr_ucb,temp_split_point = globalFunc.calculate_ASF_incr_ucb(data,attribute,gain/sum_gain,ucb)
			if ASF > max_ASF:
				splitting_attribute = attribute
				max_ASF = ASF
				max_incr_ucb = incr_ucb
				split_point = temp_split_point
			elif ASF == max_ASF and incr_ucb > max_incr_ucb:
				mac_incr_ucb = incr_ucb
				splitting_attribute = attribute
				split_point = temp_split_point
	return splitting_attribute,split_point




