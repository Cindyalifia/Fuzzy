#!/usr/bin/env python
# coding: utf-8

# # Data Pendapatan dan Hutang 

# In[59]:


#import csv with numpy
import pandas as pds
import numpy as np

fileCsv = np.genfromtxt('DataTugas2.csv', delimiter=',')

fileCsv = np.delete(fileCsv, (0), axis=0)


# # Fuzzification Pendapatan dan Hutang 

# In[60]:


#Kurva pendapatan 

import matplotlib.pyplot as pplt

pplt.plot([0, 0.5, 1], [1,1,0])
pplt.plot([0.5, 1, 1.5, 2], [0, 1, 1, 0])
pplt.plot([1.5, 2, 2.5] , [0, 1, 1])

pplt.xlabel('Pendapatan')
pplt.show()

def hitungPendapatan(pendapatan) :
    result = []
    if (pendapatan >= 0 and pendapatan <= 0.5) :
        result.append(1)
        result.append(0)
        result.append(0)
    elif (pendapatan > 0.5 and pendapatan <= 1) :
        result.append((1 - pendapatan) / 0.5)
        result.append((pendapatan - 0.5) / 0.5)
        result.append(0)
    elif (pendapatan > 1 and pendapatan <= 1.5) :
        result.append(0)
        result.append(1)
        result.append(0)
    elif (pendapatan > 1.5 and pendapatan <= 2) :
        result.append(0)
        result.append((2 - pendapatan)/0.5)
        result.append((pendapatan - 1.5)/0.5)
    elif (pendapatan > 2) :
        result.append(0)
        result.append(0)
        result.append(1)
    return result


# In[61]:


#fuzzification Hutang 

pplt.plot([0, 25, 50], [1,1,0])
pplt.plot([25, 50, 75, 100], [0, 1, 1, 0])
pplt.plot([75, 100, 125] , [0, 1, 1])

pplt.xlabel('Hutang')
pplt.show()

def hitungHutang(hutang):
    result = []
    if (hutang >= 0 and hutang <= 25) :
        result.append(1)
        result.append(0)
        result.append(0)
    elif (hutang > 25 and hutang <= 50) :
        result.append((50 - hutang) / 25)
        result.append((hutang - 25) / 25)
        result.append(0)
    elif (hutang > 50 and hutang <= 75) :
        result.append(0)
        result.append(1)
        result.append(0)
    elif (hutang > 75 and hutang <= 100) :
        result.append(0)
        result.append((100 - hutang)/25)
        result.append((hutang - 75)/25)
    elif (hutang > 100) :
        result.append(0)
        result.append(0)
        result.append(1)
    return result


# # Inference Pendapatan dan Hutang

# In[84]:


#Nomor orang dan Pendapatan

arrPendapatan = []
arrHutang = []
data = []
for item in range (100) :
    data.append(item + 1)
    data.append(fileCsv[item,1])
    
    arrPendapatan.append(data)
    data = []

pds.DataFrame(arrPendapatan, columns=["Orang ke- ","Pendapatan"])


# In[63]:


#Nomor orang dan hutang 

for item in range (100) :
    data.append(item + 1)
    data.append(fileCsv[item,2])
    
    arrHutang.append(data)
    data = []

pds.DataFrame(arrHutang, columns=["Orang ke- ","Hutang"])
# # print (arrPendapatan[2])
# # print (arrPendapatan[2][1])


# In[64]:


#Inference Pendapatan 
arrPendapatanInference = []
temp = []

# print (hitungPendapatan(arrPendapatan[7][1]))
for item in range (100) :
    arrPendapatanInference.append(hitungPendapatan(arrPendapatan[item][1]))

# arrPendapatanInference
pds.DataFrame(arrPendapatanInference, columns=["Kecil", "Menengah","Besar"])


# In[65]:


#Inference Hutang
arrHutangInference = []
temp = []
for item in range (100) :
    arrHutangInference.append(hitungHutang(arrHutang[item][1]))
    
# arrHutangInference
pds.DataFrame(arrHutangInference, columns=["Sedikit", "Sedang","Banyak"])


# # Fuzzy Rule

# In[66]:



data = [['Kecil','Banyak','Layak'], ['Kecil', 'Sedang','Layak'],['Kecil','Sedikit','Dipertimbangkan'],
        ['Menengah','Banyak','Layak'],['Menengah','Sedang','Dipertimbangkan'],['Menengah','Sedikit','Tidak Layak'],
        ['Besar','Banyak','Dipertimbangkan'],['Besar','Sedang','Tidak Layak'],['Besar','Sedikit','Tidak Layak']] 
pds.DataFrame(data, columns=["Pendapatan", "Hutang","Hasil"])


# # Nilai Fuzzy

# In[67]:



listNilai = []
temp = []
for item in range (100) :
    for i in range (3) :
        for n in range (2,-1,-1) : 
            if (arrPendapatanInference[item][i] <= arrHutangInference[item][n]) :
                temp.append(arrPendapatanInference[item][i])
            elif (arrPendapatanInference[item][i] > arrHutangInference[item][n]) :
                temp.append(arrHutangInference[item][n])
        listNilai.append(temp)
        temp = []

# listNilaiFuzzy
pds.DataFrame(listNilai) #, columns=["Layak","Dipertimbangkan","Tidak Layak"]

    


# In[68]:


listNilaiFuzzy = []
nilaiFuzzy = []
temp = []
item = 0
while item < 300 :
    #List Layak menerima bantuan
    if (listNilai[item][0] >= listNilai[item][1]) and (listNilai[item][0] >= listNilai[item+i][0]) :
        temp.append(listNilai[item][0])
    elif (listNilai[item][1] >= listNilai[item][0]) and (listNilai[item][1] >= listNilai[item+1][0]) :
        temp.append(listNilai[item][1])
    elif (listNilai[item+1][0] >= listNilai[item][0]) and (listNilai[item+1][0] >= listNilai[item][1]) :
        temp.append(listNilai[item+1][0])

    #List dipertimbangkan
    if (listNilai[item][2] >= listNilai[item+1][1]) and (listNilai[item][2] >= listNilai[item+2][0]) :
        temp.append(listNilai[item][2])
    elif (listNilai[item+1][1] >= listNilai[item][2]) and (listNilai[item+1][1] >= listNilai[item+2][0]) :
        temp.append(listNilai[item+1][1])
    elif (listNilai[item+2][0] >= listNilai[item][2]) and (listNilai[item+2][0] >=listNilai[item+1][1]) :
        temp.append(listNilai[item+2][0])

    #List ditolak 
    if (listNilai[item+1][2] >= listNilai[item+2][1]) and (listNilai[item+1][2] >= listNilai[item+2][2]) :
        temp.append(listNilai[item+1][2])
    elif (listNilai[item+2][1] >= listNilai[item+1][2]) and (listNilai[item+2][1] >= listNilai[item+2][2]) :
        temp.append(listNilai[item+2][1])
    elif (listNilai[item+2][2] >= listNilai[item+1][2]) and (listNilai[item+2][2] >= listNilai[item+2][1]) :
        temp.append(listNilai[item+2][2])

    item = item + 3
    listNilaiFuzzy.append(temp)
    temp = []
    
pds.DataFrame(listNilaiFuzzy, columns=["Terima","Pertimbangkan","Tolak"])


# # Defuzzyfikasi

# In[69]:


def hitungDefuzzySugeno(a, b, c) : 
    return (((a*100) + (b*75) + (c*50))/(a + b + c))

x = [0,25,50,75,100]
y = [0,0,1,1,1]
pplt.bar(x,y)
pplt.show()


# In[70]:


nilaiAkhir = []
temp = []

for item in range (100) : 
    temp.append(item+1)
    temp.append(hitungDefuzzySugeno(listNilaiFuzzy[item][0], listNilaiFuzzy[item][1], listNilaiFuzzy[item][2]))
    nilaiAkhir.append(temp)
    temp = []

pds.DataFrame(nilaiAkhir, columns=["Orang ke - ","Output"])


# In[71]:


# Distribusi Persebaran nomor orang yang menerima blt

pplt.scatter([x[0] for x in nilaiAkhir], [x[1] for x in nilaiAkhir])
pplt.xlabel('Nomor penduduk')
pplt.ylabel('Output fuzzy')
pplt.show()


# In[72]:


from operator import itemgetter
nilaiAkhirSort = sorted(nilaiAkhir, key=itemgetter(1))
pds.DataFrame(nilaiAkhirSort, columns=["orang ke -", "nilai"])


# # Pengambilan 20 orang yang layak menerima BLT 

# In[83]:


listTerimaBantuan = []
for item in range (99, 79, -1) :
    listTerimaBantuan.append(nilaiAkhirSort[item])
    
listTerimaBantuan = sorted(listTerimaBantuan, key=itemgetter(0))
# pds.DataFrame(listTerimaBantuan, columns=["Orang ke-","nilai"])

pplt.scatter([x[0] for x in listTerimaBantuan], [x[1] for x in listTerimaBantuan])
pplt.xlabel('Penduduk ke - ')
pplt.ylabel('Output fuzzy')
pplt.show()


# In[78]:


np.savetxt("neww.csv",[x[0] for x in listTerimaBantuan],delimiter=" ")

