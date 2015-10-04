#-*- coding: utf-8 -*-

import csv
from pymongo import MongoClient
from operator import itemgetter

import xml.etree.ElementTree as ET
import requests
import json
import sys

client = MongoClient()
db = client.snack
Fighting = db.result
wordcount=db.wordcount

def main():
    findAndInsert('protein')



def findAndInsert(word):
    
    if word is None:
        return 

    url2 = "http://openapi.ndsl.kr/itemsearch.do?keyValue=07712905&target=ARTI&searchField=BI&displayCount=10&startPosition=1&sortby=pubyear&returnType=xml&responseGroup=simple&query="+word

    absList = xmlURLToList(url2)
    #print abs word count Top 20
    #print absList
    listToMongo(absList, word)



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
    
    #print ifWordCount(sortedList, "bad")
    #insertMongo(string_dict, ing_name)
    
    #print sortedList 
    #print
    #print
    print sortedList[0:30]
    #print
    print "갯수 : "+str(len(sortedList))
    #print
    #Fighting.insert(string_dict)

def xmlURLToList(passedURL):
    
    dic={}

    r=requests.get(passedURL)
    text=str(r.text.encode('utf-8')) #.encode('utf-8')
    
    root = ET.fromstring(text)    
    
    abstract=root.findall(".//abstract")
    
    res = [i.text for i in abstract]

    return res


def insertMongo(dic, name):
    doc = {}
    doc["ing_name"] = str(name)
    doc["contents"] = dic
    wordcount.insert(doc)
    return "Insert Success!"


def ifWordCount(sortedList, word):
    count=0
    for a in sortedList:
        if a[0]==word:
            return a[1]
    return "No Such Word"

def stripWord(word):
    stripedword = word.strip(' (),:;.!@#$%^&*()_+=-0987654321')
    return stripedword


if __name__=="__main__":
    main()
