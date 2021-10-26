''' This code extracts the entire revision history of the selected list of talk pages from wikipedia dumps.
	
	The sample wikipedia dumps are in 7z_names.txt file.
	For latest wikipedia dumps please refer to    https://dumps.wikimedia.org/enwiki/ 

	We have extracted the talk page history of 30826 pages. To extract the entire talk page history
	of only selected pages, keep the list of selected pages in a json file (titles.json)

	The sample titles.json file has only a subset of 30826 pages.
'''
import argparse
import pickle as pk
import os
import json
import xmltodict

# Command line arguments
parser = argparse.ArgumentParser(description='Read Arguments for extracting the entire history of talk pages')
parser.add_argument('--wikidumps_path', type=str, nargs='?', default='7z_names.txt',
                                        help='path of the wikipedia dump links file')
parser.add_argument('--pagenames_list_path', type=str, nargs='?', default='titles.json',
                                        help='path of the list of page names json file')
parser.add_argument('--destination_path', type=str, nargs='?', default='./',
                                        help='path of the talk pages to be saved')
args = parser.parse_args()

# list of wikidump links
f = open(args.wikidumps_path,'r')
g = f.readlines()
links = [i.strip() for i in g]

# list of talk pages to be extracted
with open('titles.json', 'r') as fp:
	titles = json.load(fp)

titles = ['Talk:'+i for i in titles]

# Extracting the entire talk page history of the given list of pages
for link in links:
	# Download the dump
	os.system('wget '+link)
	dump_name = link[44:]
	# Decompress the dump
	os.system('7z x '+dump_name)
	'''Save the starting and ending line of the entire revision history
	   of all the pages present in the dump in one scan in sample_file.txt (for saving time)
	'''
	os.system('cat '+dump_name[:-3]+' | grep -n "<page>\|<title>\|</page>" > sample_file.txt')

	# Check only for your list of talk pages to be extracted
	dict1 = {}
	names = []
	f = open('sample_file.txt','r')
	g = f.readlines()
	g = [i.strip() for i in g]
	for i in range(int(len(g)/3)):
		j = i*3
		name = g[j+1].split()[1:]
		name[0] = name[0][7:]
		name[-1] = name[-1][:-8]
		name = ' '.join(name)
		# consider only talk pages
		if(name.find('Talk:') != -1):
			dict1[name] = [g[j].split()[0][:-1],g[j+2].split()[0][:-1]]
			names.append(name)
	ranges = []
	names2 = []
	for i in titles:
		if i in names:
			ll = dict1[i][0]
			ul = dict1[i][1]
			ranges.append((int(ll), int(ul)))
			names.remove(i)
			names2.append(i)
			titles.remove(i)

	if(len(ranges) == 0):
		print("NO REQUIRED PAGES IN THIS DUMP")
	else:
		# Sort all the start and end lines of the required pages and extract them in one scan of the dump
		ranges = sorted(ranges, key=lambda x:x[0])
		extractor = " "
		for x in ranges:
			extractor += "-e %d,%dp "%(x[0], x[1])
		# After this check if all the required lines are there or not as in if page 1 is in lines 1-3 and page 2 is in lines 9-15 then this should print -e 1,3p -e 9,15p.
		if(extractor != " "):
			os.system('sed -n '+extractor+dump_name[:-3]+' > pages.xml')
			os.system('(echo "<document>" && cat pages.xml) > pages1.xml')
			os.system('(cat pages1.xml && echo "</document>" ) > pages.xml')

			# convert from xml to dict
			with open('pages.xml','rb') as n:
				a = xmltodict.parse(n)
			# If this dump has more than one of the required talk pages	
			if(len(names2) > 1):
				for x in a["document"]["page"]:
					b = dict(x)
					c = json.loads(json.dumps(b))
					ttl = b["title"] # check this if this one from the wikipedia dump and the title list are same or not.
					page_name = ttl
					page_name = page_name.replace("(","_")
					page_name = page_name.replace(")","_")
					page_name = page_name.replace("\'","_")
					if ttl in names2:
						with open(args.destination_path+page_name.replace(" ","_")+'1.pkl','wb') as fi:
							pk.dump(c,fi)
			else:
				# if the dump has only one of the required talk page
				x = a["document"]["page"]
				b = dict(x)
				c = json.loads(json.dumps(b))
				ttl = b["title"] # check this if this one from the wikipedia dump and the title list are same or not.
				page_name = ttl
				page_name = page_name.replace("(","_")
				page_name = page_name.replace(")","_")
				page_name = page_name.replace("\'","_")
				if ttl in names2:
					with open(args.destination_path+page_name.replace(" ","_")+'1.pkl','wb') as fi:
						pk.dump(c,fi)

			os.system('rm pages.xml pages1.xml')
			
	os.system('rm sample_file.txt')
	os.system('rm '+dump_name)
	os.system('rm -rfv '+dump_name[:-3])
