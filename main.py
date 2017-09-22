import string 
import time
import math
import operator

label_count=0
label_dict={}
word_label_dict={}
label_anyword_dict={}
predictions=[]
truth=[]
months=["january","february", "march","april","may","june","july","august","september","october","november","december"]
stopwords=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]
				


start=time.time()

f=open("/scratch/ds222-2017/assignment-1/DBPedia.full/full_train.txt",'r')
# f=open("/scratch/ds222-2017/assignment-1/DBPedia.verysmall/verysmall_train.txt",'r')
for line in f:
	if "\t" not in line:
		continue
	parts=line.split("\t")
	labels=parts[0].replace(" ","").split(',')
	document=parts[1].split('"',1)[1].rsplit('"',1)[0].replace("\\u","").translate(None,string.punctuation).translate(None,string.digits)
	words=filter(None,document.split(" "))
	words=[word for  word in words if word.lower() not in months]
	words=[word for  word in words if word.lower() not in stopwords]
	for label in labels:
		label_count = label_count + 1
		if label not in label_dict:
			label_dict[label]=1
		else:
			label_dict[label]=label_dict[label]+1
		if label not in label_anyword_dict:
			label_anyword_dict[label] = 0
	for word in words:
		if word not in word_label_dict:
			word_label_dict[word]={}
		for label in labels:
			if label not in word_label_dict[word]: 
				word_label_dict[word][label]=1
			else:
				word_label_dict[word][label]=word_label_dict[word][label]+1
			label_anyword_dict[label]=label_anyword_dict[label]+1
qx=1.0/len(word_label_dict)
qy=1.0/len(label_dict)
m=1
# for label in label_dict:
# 	print label,len(label)
for word in word_label_dict:
	for label in label_dict:
		if label not in word_label_dict[word]:
			word_label_dict[word][label]=0

end = time.time()
print "Time Taken for Training: ",(end - start)

start=time.time()

f=open("/scratch/ds222-2017/assignment-1/DBPedia.full/full_train.txt",'r')
# f=open("/scratch/ds222-2017/assignment-1/DBPedia.verysmall/verysmall_train.txt",'r')
for line in f:
	if "\t" not in line:
		continue
	label_probability_dict={}
	parts=line.split("\t")
	labels=parts[0].replace(" ","").split(',')
	document=parts[1].split('"',1)[1].rsplit('"',1)[0].replace("\\u","").translate(None,string.punctuation).translate(None,string.digits)
	words=filter(None,document.split(" "))
	words=[word for  word in words if word.lower() not in months]
	words=[word for  word in words if word.lower() not in stopwords]

	for label in label_dict:
		sum=0
		for word in words:
			t=(word_label_dict[word][label]+m*qx)/(label_anyword_dict[label]+m)
			sum=sum+math.log(t)
		label_probability_dict[label]=sum+math.log((label_dict[label]+m*qy)/(label_count+m))
	max_label=max(label_probability_dict.iteritems(),key=operator.itemgetter(1))[0]
	predictions.append(max_label)
	truth.append(parts[0].replace(" ",""))

end = time.time()
print "Time Taken for Testing on Train Data: ",(end - start)
sum = 0
for i in range(0,len(predictions)):
	x=truth[i].split(',')
	if predictions[i] in x:
		sum=sum+1
print "Accuracy :", sum*100.0/len(predictions), "%"
predictions=[]
truth=[]

start=time.time()
f=open("/scratch/ds222-2017/assignment-1/DBPedia.full/full_test.txt",'r')
# f=open("/scratch/ds222-2017/assignment-1/DBPedia.verysmall/verysmall_test.txt",'r')
for line in f:
	if "\t" not in line:
		continue
	label_probability_dict={}
	parts=line.split("\t")
	labels=parts[0].replace(" ","").split(',')
	document=parts[1].split('"',1)[1].rsplit('"',1)[0].replace("\\u","").translate(None,string.punctuation).translate(None,string.digits)
	words=filter(None,document.split(" "))
	words=[word for  word in words if word.lower() not in months]
	words=[word for  word in words if word.lower() not in stopwords]
	for label in label_dict:
		sum=0
		for word in words:
			t=(word_label_dict[word][label]+m*qx)/(label_anyword_dict[label]+m)
			sum=sum+math.log(t)
		label_probability_dict[label]=sum+math.log((label_dict[label]+m*qy)/(label_count+m))
	max_label=max(label_probability_dict.iteritems(),key=operator.itemgetter(1))[0]
	predictions.append(max_label)
	truth.append(parts[0].replace(" ",""))

end = time.time()
print "Time Taken for Testing on Test Data: ",(end - start)
sum = 0
for i in range(0,len(predictions)):
	x=truth[i].split(',')
	if predictions[i] in x:
		sum=sum+1
print "Accuracy :", sum*100.0/len(predictions), "%"
predictions=[]
truth=[]

start=time.time()
f=open("/scratch/ds222-2017/assignment-1/DBPedia.full/full_devel.txt",'r')
# f=open("/scratch/ds222-2017/assignment-1/DBPedia.verysmall/verysmall_devel.txt",'r')
for line in f:
	if "\t" not in line:
		continue
	label_probability_dict={}
	parts=line.split("\t")
	labels=parts[0].replace(" ","").split(',')
	document=parts[1].split('"',1)[1].rsplit('"',1)[0].replace("\\u","").translate(None,string.punctuation).translate(None,string.digits)
	words=filter(None,document.split(" "))
	words=[word for  word in words if word.lower() not in months]
	words=[word for  word in words if word.lower() not in stopwords]
	for label in label_dict:
		sum=0
		for word in words:
			t=(word_label_dict[word][label]+m*qx)/(label_anyword_dict[label]+m)
			sum=sum+math.log(t)
		label_probability_dict[label]=sum+math.log((label_dict[label]+m*qy)/(label_count+m))
	max_label=max(label_probability_dict.iteritems(),key=operator.itemgetter(1))[0]
	predictions.append(max_label)
	truth.append(parts[0].replace(" ",""))

end = time.time()
print "Time Taken for Testing on Development data: ",(end - start)
sum = 0
for i in range(0,len(predictions)):
	x=truth[i].split(',')
	if predictions[i] in x:
		sum=sum+1
print "Accuracy :", sum*100.0/len(predictions), "%"
		




