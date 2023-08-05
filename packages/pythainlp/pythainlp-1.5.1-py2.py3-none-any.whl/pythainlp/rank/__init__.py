# -*- coding: utf-8 -*-
from __future__ import absolute_import,print_function,unicode_literals
import nltk
from pythainlp.corpus import stopwords
#เรียงจำนวนคำของประโยค
def rank(data,stopword=False):
	"""เรียงจำนวนคำของประโยค
	รับค่าเป็น ''list'' คืนค่าเป็น ''dict'' [ข้อความ,จำนวน]"""
	if stopword==False:
		rankdata = nltk.FreqDist(data)
	else:
		data = [word for word in data if word not in stopwords.words('thai')]
		rankdata = nltk.FreqDist(data)
	return dict(rankdata)
if __name__ == "__main__":
	text = ['แมว','ชอบ','ปลา','และ','แมว','ชอบ','นอน','มาก','เลย','คน','เลี้ยง','กลาย','เป็น','ทาส','แมว']
	print(rank(text))
