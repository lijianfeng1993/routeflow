#!/usr/bin/env python 
# -*- coding:utf-8 -*-

# 取多个列表的交集
def getAllElementsInSencodList(firstList ,secondList):
	list_c = [a for a in firstList if a in secondList]
	return list_c

def getIntersection(uinList):
	while len(uinList) > 1:
		list_a = []
		list_b = []
		list_a = uinList.pop()
		list_b = uinList.pop()
		list_c = getAllElementsInSencodList(list_a,list_b)
		if len(list_c) > 0:
			uinList.append(list_c)
	return uinList[0]

if __name__ == '__main__':
	print getIntersection([['a','b','c','d'],['a','b','c'],['a','b']])

