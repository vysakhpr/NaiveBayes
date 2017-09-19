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
				


start=time.time()

f=open("/scratch/ds222-2017/assignment-1/DBPedia.full/full_train.txt",'r')
for line in f:
	parts=line.split("\t")
	labels=parts[0].replace(" ","").split(',')
	document=parts[1].split('"',1)[1].rsplit('"',1)[0].replace("\\u","").translate(None,string.punctuation).translate(None,string.digits)
	words=filter(None,document.split(" "))
	words=[word for  word in words if word.lower() not in months]
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
for line in f:
	label_probability_dict={}
	parts=line.split("\t")
	labels=parts[0].replace(" ","").split(',')
	document=parts[1].split('"',1)[1].rsplit('"',1)[0].replace("\\u","").translate(None,string.punctuation).translate(None,string.digits)
	words=filter(None,document.split(" "))
	words=[word for  word in words if word.lower() not in months]
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
for line in f:
	label_probability_dict={}
	parts=line.split("\t")
	labels=parts[0].replace(" ","").split(',')
	document=parts[1].split('"',1)[1].rsplit('"',1)[0].replace("\\u","").translate(None,string.punctuation).translate(None,string.digits)
	words=filter(None,document.split(" "))
	words=[word for  word in words if word.lower() not in months]
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
for line in f:
	label_probability_dict={}
	parts=line.split("\t")
	labels=parts[0].replace(" ","").split(',')
	document=parts[1].split('"',1)[1].rsplit('"',1)[0].replace("\\u","").translate(None,string.punctuation).translate(None,string.digits)
	words=filter(None,document.split(" "))
	words=[word for  word in words if word.lower() not in months]
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
		




