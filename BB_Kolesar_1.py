import numpy as np

def h2l_uvm(n,v,w):
    # High to low unit value matrix
    h2l_mat = np.arange(n*5, dtype=float).reshape(n,5)
    for i in range(n):
        h2l_mat[i][0] = (v[i][0]/w[i][0])
        h2l_mat[i][1] = v[i][0]
        h2l_mat[i][2] = w[i][0]
        h2l_mat[i][3] = i
        h2l_mat[i][4] = 1
    # Sort 2D numpy array by 1st Column
    columnIndex = 0
    h2l_mat = h2l_mat[h2l_mat[:,columnIndex].argsort()][::-1]
    return h2l_mat

# Function to compute bound
def nodebound(K,n,i,h2l_mat,maxboundval) :
    for x in range(0,2):
        if x == 0: # test for 0 at current index
            maxboundval_0 = 0.0
            residweight = K
            # do not include the value of the current index
            h2l_mat[i][4] = 0
            for iter in range(n):
                #Look up for the value of the weight
                ww = h2l_mat[iter][2]
                # Look up for the value of the "value"
                vv = h2l_mat[iter][1]
                # Index value (0 or 1)
                ii = h2l_mat[iter][4]
                #print("RW",residweight,ii,ww)
                if residweight>ww :
                    maxboundval_0 = maxboundval_0 + vv*ii
                    residweight = residweight-ww*ii
                elif residweight>0:
                    maxboundval_0 = maxboundval_0 + (residweight/ww)*vv*ii
                    residweight = residweight*(1-ii)
                #print("MB",maxboundval_0)

        if x == 1: # test for 0 at current index
            maxboundval_1 = 0.0
            residweight = K
            # do include the value of the current index
            h2l_mat[i][4] = 1
            for iter in range(-1,i+1):
                if iter > -1:
                    maxboundval_1 = maxboundval_1 + h2l_mat[iter][1]*h2l_mat[iter][4]
                    residweight = residweight-h2l_mat[iter][2]*h2l_mat[iter][4]
            #print("RWx",residweight)
            if residweight < 0:
                maxboundval_1 = -999.0
                continue
            for iter in range(i+1,n):
                ww = h2l_mat[iter][2]
                vv = h2l_mat[iter][1]
                ii = h2l_mat[iter][4]
                if residweight>ww :
                    maxboundval_1 = maxboundval_1 + vv*ii
                    residweight = residweight-ww*ii
                elif residweight>0:
                    maxboundval_1 = maxboundval_1 + (residweight/ww)*vv*ii
                    residweight = 0

    # Compare bounds
    if maxboundval_0 > maxboundval_1:
        maxboundval[i] = maxboundval_0
        h2l_mat[i][4] = 0
    else:
        maxboundval[i] = maxboundval_1
        h2l_mat[i][4] = 1
    print("***********")
    print(i,maxboundval_0)
    print(i,maxboundval_1)
    #print(maxboundval[i])
    print(h2l_mat[:,4])
    #print("-----------")
    #print("ok", iter)
    #print(maxboundval_0, maxboundval_1)
    return h2l_mat, maxboundval

#---------------------------------------------------------------------

name = input("Enter file:")
if len(name) < 1 : fname = "test_dp_2.txt"
try:
    fh = open(fname)
except:
    print('File not found')
    quit()
print("done")

i = -1
for lines in fh:
    linesplit = lines.split()
    if i == -1:
        n = int(linesplit[0])
        #print("n",n)
        K = float(linesplit[1])
        i = 0
        v = np.arange(n*2,dtype=float).reshape(n,2)
        w = np.arange(n*2,dtype=float).reshape(n,2)
        x = np.arange(n*2,dtype=float).reshape(n,2)
        y = np.arange(n*2,dtype=float).reshape(n,2)
        maxboundval = np.arange(n)
    else:
        # populate column 0
        v[i][0] = (float(linesplit[0]))
        w[i][0] = (float(linesplit[1]))
        x[i][0] = 1
        y[i][0] = 0
        # populate column 1
        v[i][1] = i
        w[i][1] = i
        x[i][1] = i
        y[i][1] = i
        # completed lines
        i = i + 1

#print(v)
h2l_mat = h2l_uvm(n,v,w)
#print(huvm1)
for iter in range(0,7):
   test = nodebound(K,n,iter,h2l_mat,maxboundval)
   #print(maxboundval[ii])
#print(h2l_mat)
print("***********")
#print(i,maxboundval_0)
#print(i,maxboundval_1)
#print(maxboundval[i])
#print(maxboundval[0:7])
#print(h2l_mat[:,0])
print("-----------")
