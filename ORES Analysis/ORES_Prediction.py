''' This code extracts the ORES predictions for all the revisions of all the articles by its revision ids
	using an online ORES predictor

	The sample_article_rev_ids.json file contains the rev ids for sample set of pages
	The revision ids for each article is extracted from the textpage history (refer to "Extract Revision History" folder)
'''
import ores
import os
import json
import argparse


# Command line arguments
parser = argparse.ArgumentParser(description='Read Arguments for extracting the ORES predictions for all the revision articles')
parser.add_argument('--batch_size', type=int, nargs='?', default=50,
										help='Batch size for running the ORES predictor')
parser.add_argument('--mail_id', type=str, nargs='?', default='sample_mail@gmail.com',
										help='same sample mail id for running the ORES predictor')
parser.add_argument('--articles_revids_path', type=str, nargs='?', default='sample_articles_rev_ids.json',
										help='path of the article rev ids json file')
rgs = parser.parse_args()


def assign_newlabel(label):
	if(label.lower() == 'fa'):
		return 'FA'
	elif(label.lower() == 'ga'):
		return 'AGA'
	elif(label.lower() == 'b'):
		return 'BC'
	elif(label.lower() == 'c'):
		return 'BC'
	elif(label.lower() == 'start'):
		return 'SS'
	else:
		return 'SS'

# rev ids of each revision of all articles with timestamp indexed as key for each revision of an article
with open(args.articles_revids_path,'r') as f:
	g = json.load(f)

articles_list = list(g.keys())


				
batch_size = args.batch_size
dict_all_art = {}
for i in articles_list:
	dict1 = g[i]
	# l2 is the list of timestamps
	l2 = list(dict1.keys())
	# l3 is the list of revision ids for an article
	l3 = []
	for j in l2:
		l3.append(str(dict1[j]))
	if(len(l3)>0):
		str1 = 'echo -e '
		str3 = ' | ores score_revisions https://ores.wikimedia.org/ '+args.mail_id+' enwiki articlequality --batch-size='+str(batch_size)+' --parallel-requests=40 --output=temp.txt'
		if(len(l3)<=batch_size):
			s1 = """'{"rev_id": """
			s2 = str(l3[0])
			s3 = """}"""
			str2 = s1+s2+s3
			for j in range(1,len(l3)):
				str2 += """\n"""
				s1 = """{"rev_id": """
				s2 = str(l3[j])
				s3 = """}"""
				s4 = s1+s2+s3
				str2 += s4
			str2 += """'"""
				
			str4 = str1+str2+str3
			exec_run = os.system(str4)
			f11 = open('temp.txt','r')
			g11 = f11.readlines()
			dict_each_art = {}
			for j in range(len(l3)):
				js = json.loads(g11[j])
				if(js['rev_id'] == int(l3[j])):
					try:
						dict_each_art[l2[j]] = assign_newlabel(js['score']['articlequality']['score']['prediction'])
					except:
						temp_ = 1

			os.remove('temp.txt')

			dict_all_art[i] = dict_each_art

			with open('ores_preds/'+i+'__preds.json', 'w',encoding='utf-8') as fp:
				json.dump(dict_each_art, fp)
		else:
			# if number of revisions are more than batch_size then divide into batches where each batch is of size batch_size
			k = int(len(l3)/batch_size)
			dict_each_art = {}
			# for all the batches except last batch
			for l in range(k):
				s1 = """'{"rev_id": """
				s2 = str(l3[l*batch_size])
				s3 = """}"""
				str2 = s1+s2+s3
				for j in range(1+l*batch_size,(l+1)*batch_size):
					str2 += """\n"""
					s1 = """{"rev_id": """
					s2 = str(l3[j])
					s3 = """}"""
					s4 = s1+s2+s3
					str2 += s4
				str2 += """'"""
				str4 = str1+str2+str3
				exec_run = os.system(str4)
				f11 = open('temp.txt','r')
				g11 = f11.readlines()
				co = 0
				for j in range(l*batch_size,(l+1)*batch_size):
					js = json.loads(g11[co])
					co+=1
					if(js['rev_id'] == int(l3[j])):
						try:
							dict_each_art[l2[j]] = assign_newlabel(js['score']['articlequality']['score']['prediction'])
						except:
							temp_ = 1
						
				os.remove('temp.txt')
			# for the last batch		
			if((k)*batch_size!= len(l3)):
				s1 = """'{"rev_id": """
				s2 = str(l3[k*batch_size])
				s3 = """}"""
				str2 = s1+s2+s3
				for j in range(1+k*batch_size,len(l3)):
					str2 += """\n"""
					s1 = """{"rev_id": """
					s2 = str(l3[j])
					s3 = """}"""
					s4 = s1+s2+s3
					str2 += s4
				str2 += """'"""
				str4 = str1+str2+str3
				exec_run = os.system(str4)
				f11 = open('temp.txt','r')
				g11 = f11.readlines()
				co = 0
				for j in range(k*batch_size,len(l3)):
					js = json.loads(g11[co])
					co+=1
					if(js['rev_id'] == int(l3[j])):
						try:
							dict_each_art[l2[j]] = assign_newlabel(js['score']['articlequality']['score']['prediction'])
						except:
							temp_ = 1
						
				os.remove('temp.txt')
			
			dict_all_art[i] = dict_each_art

			# save for each article in a json file in ores_preds folder for saving time in case the code has stopped in middle
			with open('ores_preds/'+i+'__preds.json', 'w',encoding='utf-8') as fp:
				json.dump(dict_each_art, fp)



# if the code execution is successful without stopping then save for all articles together
with open('all_articles_ores_preds.json', 'w',encoding='utf-8') as fp:
	json.dump(dict_all_art, fp)