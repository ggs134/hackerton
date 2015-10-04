#-*- coding: utf-8 -*-

import csv
from pymongo import MongoClient
from operator import itemgetter

import xml.etree.ElementTree as ET
import requests
import json
import sys

#몽고 관련 설정
client = MongoClient()
db = client.snack
Fighting = db.result
wordcount=db.wordcount


#파라미터 : api로부터 검색할 단어    
def findAndInsert(word):
    
    if word is None:
        return 

    url2 = "http://openapi.ndsl.kr/itemsearch.do?keyValue=07712905&target=ARTI&searchField=BI&displayCount=10&startPosition=1&sortby=pubyear&returnType=xml&responseGroup=simple&query="+word

    absList = xmlURLToList(url2)
    #print abs word count Top 20
    #print absList
    listToMongo(absList, word)


# 파라미터 : 추출된 단어의 배열, 몽고에 입력할 성분명
def  listToMongo(arr, ing_name):
    string_dict = {}

    for arr in arr:
        string_list = arr.split()
        for _word in string_list:
            stripedWord = stripWord(_word)
            if stripedWord in string_dict:
                string_dict[stripedWord] += 1
                continue
            else:
                string_dict[stripedWord] = 1
        #with open('output.txt','w') as output:
        #    output.write(str(string_dict))
    #print len(string_dict)
    #print type(string_dict)
    #print type(string_dict['and'])
    #print (string_dict['and'])
    
    item=string_dict.items()
    sortedList=sorted(item, key=itemgetter(1), reverse=True)
    
    #몽고에 입력
    insertMongo(string_dict, ing_name)


#전달받은 url을 배열로 비꿔줌
def xmlURLToList(passedURL):
    
    dic={}

    r=requests.get(passedURL)
    text=str(r.text.encode('utf-8')) #.encode('utf-8')
    
    root = ET.fromstring(text)    
    
    abstract=root.findall(".//abstract")
    
    res = [i.text for i in abstract]

    return res

#입력받은 딕셔너리를 name이라는 키를 붙여서 몽고에 삽입
#입력 예시 
#{"ing_name" : name , "contents"  : ... }
def insertMongo(dic, name):
    doc = {}
    doc["ing_name"] = str(name)
    doc["contents"] = dic
    wordcount.insert(doc)
    return "Insert Success!"


#정렬된 결과에서 word의 숫자를 세어 주는 모듈
def ifWordCount(sortedList, word):
    count=0
    for a in sortedList:
        if a[0]==word:
            return a[1]
    return "No Such Word"

#텍스트 필터링, 전달받은 단어에서 불필요한 부분을 제거
def stripWord(word):
    # (),:;.!@#$%^&*()_+=-0987654321 를 단어에서 제거함
    stripedword = word.strip(' (),:;.!@#$%^&*()_+=-0987654321')
    return stripedword
