import numpy as np
import pandas as pd
import os

#preprocessing the data#
with open('whole.dat','r') as old, open('whole1.dat', 'w') as new:
    lines = old.readlines()
    new.writelines(lines[5:-1])

df=pd.read_csv('whole1.dat',
                delim_whitespace=True,
                names=["JA","IX","IY","IZ","x","y","z"])
df.drop(['JA','x','y','z'],axis=1,inplace=True)
df.drop([0],axis=0,inplace=True)
np.savetxt(r'whole.txt', df.values,fmt='%s')
os.remove('whole1.dat')



with open('cap.dat','r') as oldcap, open('cap1.dat', 'w') as newcap:
    linescap = oldcap.readlines()
    newcap.writelines(linescap[5:-1])

dfcap=pd.read_csv('cap1.dat',
                delim_whitespace=True,
                names=["JA","IX","IY","IZ","x","y","z"])
dfcap.drop(['JA','x','y','z'],axis=1,inplace=True)
dfcap.drop([0],axis=0,inplace=True)
np.savetxt(r'cap.txt', dfcap.values,fmt='%s')
os.remove('cap1.dat')

# start main body #

with open('whole.txt') as c:
    wholestr=c.readlines()
    whole_str=(np.loadtxt(wholestr))
    whole=np.array(whole_str)
with open('cap.txt') as d:
    capstr=d.readlines()
    cap_str=(np.loadtxt(capstr))
    cap=np.array(cap_str)

# calculation of core coordinates #
core=list((set(wholestr)-set(capstr)))
with open('core.txt', 'w') as f:
    for x in range(len(core)):
        f.write(core[x])

# refinement of cap coordinates #
cap=list((set(wholestr)-set(core)))
with open('cap_refined.txt', 'w') as g:
    for n in range(len(cap)):
        g.write(cap[n])
        
# writing the cap coordinates #
data1 = pd.read_csv("cap_refined.txt",header=None, delimiter = '\s+')
data1.index=np.arange(1,len(data1)+1)
data1.to_csv('testcap.csv', index =int(1))

# writing the core coordinates #
data2 = pd.read_csv("core.txt",header=None, delimiter = '\s+')
data2.index = pd.RangeIndex(start=len(data1)+1, stop=len(data1)+1+len(core), step=1)
data2.to_csv('testcore.csv', index =int(1))

# refinement of the cap coordinates #
with open('cap_refined.txt') as a:
    f1=a.readlines()
with open('core.txt') as b:
    f2=b.readlines()
data=np.concatenate([f1, f2])

def intersection(wholestr,data): 
    return list(set(wholestr) & set(data)) 
com_cor=set(intersection(wholestr,data))
extra_points=set((set(data)-set(com_cor)))

core_mod=list((set(core)-set(extra_points)))
with open('core_ref.txt', 'w') as k:
    for i in range(len(core_mod)):
        k.write(core_mod[i])

# removal of common points from refined cap and core coordinates #
with open('core_ref.txt') as d:
    core_re=d.readlines()
    core_re_str=(np.loadtxt(core_re))
    core_ref=np.array(core_re_str)
with open('cap_refined.txt') as h:
    cap_re=h.readlines()
    cap_re_str=(np.loadtxt(cap_re))
    cap_ref=np.array(cap_re_str)
def intersection2(core_re, cap_re): 
    return list(set(core_re) & set(cap_re)) 
com_cor2=set(intersection2(core_re, cap_re))
core_mod2=list((set(core_re)-set(com_cor2)))
with open('core_refined.txt', 'w') as l:
    for m in range(len(core_mod2)):
        l.write(core_mod2[m])

# writing the modified core coordinates #
data3 = pd.read_csv("core_refined.txt",header=None, delimiter = '\s+')
data3.index = pd.RangeIndex(start=len(data1)+1, stop=len(data1)+1+len(core_mod), step=1)

# modification of cap data #
data1.insert(3, "D", 2)
data1.insert(4, "E", 2)
data1.insert(5, "F", 2)
data1.to_csv('test_cap.csv', index =int(1))

# modification of core data #
data3.insert(3, "D", 1)
data3.insert(4, "E", 1)
data3.insert(5, "F", 1)
data3.to_csv('test_core.csv', index =int(1))

# writing the whole structure file #
f3=pd.read_csv("test_cap.csv")
f4=pd.read_csv("test_core.csv")
data4=pd.concat([f3, f4])
data4.to_csv('test_full.csv', index = False)
