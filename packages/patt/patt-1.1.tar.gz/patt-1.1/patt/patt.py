import numpy

def getNp_array(tup):
    return numpy.array(list(tup))
    
def getDistance(np_a1,np_a2):
    np_a1 = getNp_array(np_a1)
    np_a2 = getNp_array(np_a2)
    return numpy.linalg.norm(np_a1 - np_a2)

def getCluster(X,Z1,Z2):
    Y = iter(X)
    tmp = next(Y)
    Z=[[],[]]
    while tmp:
        if getMinlength(X[tmp],Z1,Z2): Z[0].append(tmp)
        else: Z[1].append(tmp)
        tmp = next(Y,0)
    return Z

#一个坐标点，两个聚类中心，得到离坐标点最近的聚类中心
def getMinlength(p,Z1,Z2):
    p=getNp_array(p)
    Z1=getNp_array(Z1)
    Z2=getNp_array(Z2)
    return getDistance(p,Z1) < getDistance(p,Z2)

def getMidpoint(X,Zk):
    return sum([getNp_array(X[n]) for n in Zk])/len(Zk)

def getMatlength(X,tmp,Z):
    print([getDistance(X[tmp],getMidpoint(X,x)) for x in Z])
    print(numpy.min([getDistance(X[tmp],getMidpoint(X,x)) for x in Z]))
    return numpy.min([getDistance(X[tmp],getMidpoint(X,x)) for x in Z])

def getArg(X,Zi,Zk):
    #X:以字典保存的所有的数据集
    #Zi：指代聚类中心
    #Zk：每个聚类
    return sum([getDistance(X[n],Zi) for n in Zk]) / len(Zk)

def mCont(p1,p2,T):
    return getDistance(p1,p2) <= T
