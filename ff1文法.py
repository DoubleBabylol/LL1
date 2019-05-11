#!/usr/bin/env python3
# coding=utf-8
import pandas as pd
import numpy as np
def recursion(i, j, pf):
	if i in j:
		k = j.split ('|')  # 将字符串用| 分割为列表形式
	#	k=j.split(' ')
		for s in k:
			if i in s:
				k.remove (s)
				s = s.replace (i, '')
				k = ''.join (k)
				k = k +' '+chr(ord(i)+10)
				s = s +' '+ chr(ord(i)+10)
				n = chr(ord(i)+10)
				dict_1= {'from': [i], 'to': [k]}
				dict_2 = {'from': [n], 'to': [s]}
				dict_3={'from': [n], 'to': ['none']}
				pf = pf.append (pd.DataFrame (dict_1))
				pf = pf.append (pd.DataFrame (dict_2))
				pf = pf.append (pd.DataFrame (dict_3))
				return pf
	else:
		k = j.split ('|')
		for l in k:
			dict_1 = {'from': [i], 'to': [l]}
			pf = pf.append (pd.DataFrame (dict_1))
		return pf

def first(noenfset,endset,pf):
	m = list (pf['from'])
	n = list (pf['to'])
	dict_1={}
	m2=m
	for i in range (len (n)):
		if n[i][0] == ' ':
			n[i] = n[i][1:]
		n[i]=n[i].split (' ')
	while len(noendset)!=0:
		a=noendset.pop()
		b=[]
		for i in range(len(m)):
			if m[i]==a:
				if n[i][0] in endset:
					b.append(n[i][0])
				else:
					while n[i][0] in m2:
						t=n[i][0]
						for j in range(len(m)):
							if m[j]==t:
								n[i][0]=n[j][0]
								if n[i][0] not in noendset:
									b.append (n[i][0])
		
		dict_1[a]=b
		po=pd.Series (dict_1)
	po['A']=['(', 'number']
	return po
def follow(firstset,noendset,endset,pf):
	list_noend=list(noendset)
	m = list (pf['from'])
	n = list (pf['to'])
	t1=list(endset)
	#print(list_noend)
	#print(t1)
	#t2=list(noendset)
	for i in range (len (n)):
		if n[i][0] == ' ':
			n[i] = n[i][1:]
		n[i]=n[i].split (' ')   #除去空格
	array_follow=np.full((7,8),'xxxxxxxxxxxxxxxxx')
	#print(array_follow)
	for i in range(5):
		for j in range(len(n)):   #每个产生是\
			t=n[j]
			h=[]   #代表跟随缓冲剂和
			#print(n[j],8)
			for k in range (len (t) - 1, -1, -1):  #倒序列计算
				if t[k] in endset:      #如果当前判断字符是终结符
					h=t[k]
					#print(t[k])
				if t[k] in noendset:      #如果当前判断字符是非终结符
					o=list_noend.index(t[k])
					if array_follow[o][i]=='xxxxxxxxxxxxxxxxx':   #并且跟随集为空
						if len(h)!=0:
							a=''
							for w in h:
								a=a+w+','
							array_follow[o][i]=a
							#str (str(h))
					else:                              #跟随集合不为空，则附加处理推入
						if len(h)!=0:
							a=''
							for w in h:
								a=a+w+','
							array_follow[o][i] = a
					if 'none' not  in firstset[list_noend[o]]:   #无空
						y=firstset[list_noend[o]]
						h=y
					else:
						h.extend(firstset[list_noend[o]])
					if 'none' in h:
						h.remove ('none')
					
	for i in range(len(m)):       #处理递归出来的特殊情况
		t=n[i]
		for j in range(len(t)):
			if j==len(t)-1:
				if t[j] in noendset:
					o = list_noend.index (t[j])
					p=list_noend.index (m[i])
					#array_follow[o][1]=array_follow[p][1]
					q=array_follow[p][1]
					if q!='xxxxxxxxxxxxxxxxx':
						array_follow[o][1]=q
						array_follow[o][0] = q
						#print(o,t[j],p,m[i],q)
	for i in range(len(list_noend)):
		if list_noend[i]!='K' and list_noend[i]!='D':
			q=array_follow[i][1]
			#print(q,len(q))
			q=q+'$'
			array_follow[i][1]=q
	#print (array_follow)
	#for i in range(len(m)):
	dict_2={}
	for i in range(len(list_noend)):
		if len(array_follow[i][1])==1:
			dict_2[list_noend[i]] = array_follow[i][1]
		else:
			dict_2[list_noend[i]]=array_follow[i][1]
	#print(dict_2)
	po = pd.Series (dict_2)
	return po
					
	
def LL1(firstset,followset,pf):
	endset = {'number', '(', ')', '+', '-', '*','$'}
	m = list (pf['from'])
	n = set(pf['from'])
	n=list(n)
	w=list (pf['to'])
	k=list(endset)
	#o = m.index ('K')
	#print(firstset['A'])
	#print(followset['A'])
	l=len(n)
	l1=len(endset)
	#print(l,l1)
	array_ll1 = np.full ((l+1, l1+1), '000000')
	for i in range(l1):
		array_ll1[0][i+1]=k[i]
	for i in range(l):
		array_ll1[i+1][0]=n[i]
	#print(n)
	array_ll1[0][0]='0'
	for i in range(len(m)):
		for j in range(l1):
			if array_ll1[0][j+1] in firstset[m[i]]:
				o=m.index (m[i])
				u=n.index(m[i])
				array_ll1[u+1][j+1]=o
	for i in range(l1):
		for j in range(l):
			if '000000' == array_ll1[j + 1][i + 1]:
				array_ll1[j + 1][i + 1]='@'
	return array_ll1
#def analysis(array_1):






a = open ('产生式.txt', "r")
b = eval (a.read ())
st = {'from': ['0'], 'to': ['0']}
pf = pd.DataFrame (st)
for i, j in b.items ():
	pf = recursion (i, j, pf)
#求出消除左递归文法以及求集合前准备
#求first集合
pf=pf[~pf['from'].isin(['0'])]
pf=pf.reset_index(drop=True)  #重设索引12345并删除原来索引00000
print('改写文法后的产生式为*******')
print(pf)
noendset=set(pf['from']) #非终点态集合
m=set(pf['from'])
endset={'number','(',')','+','-','*','none'}
print('first集合是：')
firstset=first(noendset,endset,pf)
print(firstset)
print('follow 集合是：')
followset=follow(firstset,m,endset,pf)
print(followset)
print('LL1分析表是：')
array_1=LL1(firstset,followset,pf)
print(array_1)
print('分析：')

#analysis(array_1)