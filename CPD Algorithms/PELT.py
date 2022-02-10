''' This code runs the Pruned Exact Linear Time (PELT) CPD algorithm on the time series of features. These features are generated from the given set of wikipedia articles and 
                     their corresponding talk pages. The code computes precision, recall and coverage as the output of PELT algorithm.
		     
	The smaple dataset of articles is mentioned in the sample_dataset.json file
'''
from __future__ import division
import argparse
import numpy as np
import ruptures as rpt
import numpy as np
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
				count+=1
				c = y
				break
			temp_rem.append(rem_set[y])
		temp_rem = temp_rem + rem_set[c+1:]
		rem_set = temp_rem.copy()

	return count


# Command line arguments
parser = argparse.ArgumentParser(description='Read Arguments for running PELT algorithm')
parser.add_argument('--dataset_path', type=str, nargs='?', default='sample_dataset.json',
                                        help='path of the dataset')
parser.add_argument('--penalty', type=int, nargs='?', default=1,
                                        help='Penalty for PELT algorithm')
parser.add_argument('--initial_index',type=int, nargs='?', default=14,
                                        help='starting index from the list of features (FROM)')
parser.add_argument('--final_index',type=int, nargs='?', default=34,
                                        help='final index from the list of features (TO)')
args = parser.parse_args()

with open(args.dataset_path,'r') as f:
	dict_1 = json.load(f)
	
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
	old_feats = arr[:, args.initial_index:args.final_index]

	X = old_feats
	X = normalize(X, axis=0)
	y = arr[:, -1]
	data = np.array(X)

	model = "rbf"  # "l1", "rbf"
	algo = rpt.Pelt(model=model).fit(X)
	try:
		my_bkps = algo.predict(pen=args.penalty)
	except:
		continue
	
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
