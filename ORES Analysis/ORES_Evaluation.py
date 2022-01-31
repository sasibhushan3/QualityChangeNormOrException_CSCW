''' This code computes the precision, recall and coverage for the time series based on ORES predictions.
	
	ECP, BinSeG and PELT are various CPD algorithms which predict the change in article quality in time series.

	To compare the performance of the Hybrid model(Best of ECP, BinSeG and PELT), we are using the ORES predictor/classifier.

	We use ORES predictor to predict the labels of all revisions of an article and we convert them into
	time series of change points (per month).

	We compute the same metrics (precision, recall and coverage) for this time series based on ORES predictions and compare
	with the ones obtained with Hybrid model.


	The dataset for a sample set of articles is in sample_dataset.json file
	The sample ORES predicted time series is in sample_articles_ores_timeseries_permonth.json file
'''
import argparse
from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import changepoint_detection as cd
import seaborn
import os
import pandas as pd
from sklearn.preprocessing import normalize
import json
import sys

def make_set(arr, end):
	if(len(arr) == 0):
		return []
	t0 = 0
	T = end
	final_set = []
	if(t0 != arr[0]):
		final_set.append((0, arr[0]-1))
	for point in range(len(arr)-1):
		final_set.append((arr[point], arr[point+1] -1 ))
	if(arr[-1] != T):
		final_set.append((arr[-1], T))
	return final_set

def jaccard(A, B):
	if A or B:
		return len(A & B) / len(A | B)
	else:
		return 1.0

def compute_coverage(est, chg):
	if(chg == [] or est == []):
		return 0
	qual = 0
	for a in chg:
		jcs = []
		for a1 in est:
			real_set = set(x for x in range(a[0], a[1] + 1))
			predicted_set = set(x for x in range(a1[0], a1[1] + 1))
			jcs.append(jaccard(real_set, predicted_set))
		qual += (a[1] - a[0] + 1) * max(jcs)
	qual /= float(est[-1][1]+1)
	return qual

def tp_set(est, chg, M):
	count = 0
	rem_set = est.copy()
	for x in chg:
		temp_rem = []
		c = 0
		for y in range(len(rem_set)):
			if(abs(x - rem_set[y]) <= M):
				c = y
				count+=1
				break
			temp_rem.append(rem_set[y])
		temp_rem = temp_rem + rem_set[c+1:]
		rem_set = temp_rem.copy()

	return count


# Command line arguments
parser = argparse.ArgumentParser(description='Read Arguments for running ORES evaluator')
parser.add_argument('--dataset_path', type=str, nargs='?', default='sample_dataset.json',
                                        help='path of the dataset')
parser.add_argument('--ores_timeseries_path', type=str, nargs='?', default='sample_articles_ores_timeseries_permonth.json',
                                        help='path of the ORES predicted time series dataset')
args = parser.parse_args()

with open(args.dataset_path,'r') as f:
	dict_1 = json.load(f)

with open(args.ores_timeseries_path,'r') as f:
	dict_ores = json.load(f)
	
pages = list(dict_1.keys())
covs = []
precs = []
recs = []
for page in pages:
	data = dict_1[page]
	timestamps = list(data.keys())
	l1 = []
	for timestamp in timestamps:
		l1.append(np.asarray(data[timestamp]))

	arr = np.asarray(l1)
	old_feats = arr[:, 0 : -1]

	X = old_feats
	X = normalize(X, axis=0)
	y = arr[:, -1]
	data = np.array(X)

	temp1 = list(dict_ores[page].keys())
	y_ores = []
	for i in temp1:
		y_ores.append(dict_ores[page][i])

	# ORES Breakpoints (changepoints)
	my_bkps = []
	for id, gt in enumerate(y_ores):
		if(gt == 1):
			my_bkps.append(id)
	if(len(my_bkps) == 0 or my_bkps[-1] != len(X)):
		my_bkps.append(len(X))

	# Original Breakpoints
	bkps = []
	for id, gt in enumerate(y):
		if(gt == 1):
			bkps.append(id)
	if(len(bkps) == 0 or bkps[-1] != len(X)):
		bkps.append(len(X))

	estimates = my_bkps[:-1]
	gts = bkps[:-1]

	est = make_set(estimates, len(X)-1)
	chg = make_set(gts, len(X)-1)
	cov = compute_coverage(est, chg)
	covs.append(cov)
	tps = tp_set(estimates, gts, 5)
	if(len(estimates) != 0):
		pr = tps / float(len(estimates))
	else:
		pr = 0
	if(len(gts) != 0):
		rec = tps / float(len(gts))
	else:
		rec = 0
	if(pr == 0 and rec == 0):
		f1 = 0
	else:
		f1 = (2 * pr * rec) / float(pr + rec)
	precs.append(pr)
	recs.append(rec)


print("Coverage is: ", np.mean(covs))
print("Precision is: ", np.mean(precs))
print("Recall is: ", np.mean(recs))