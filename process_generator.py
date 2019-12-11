import numpy as np
import sys
read =  sys.argv[1]
write =  sys.argv[2]

r =  open(read,'r')

w= open(write,"w+")

line = r.readline()
data = line.split() #split string into a list
n=int(data[0])

line = r.readline()
data = line.split() #split string into a list
mu=float(data[0]) 
sigma =float(data[1])
arriv = np.random.normal(mu, sigma, n)
arriv=abs(arriv)

line = r.readline()
data = line.split() #split string into a list
mu2=float(data[0])
sigma2 = float(data[1])
burst = np.random.normal(mu2, sigma2, n)
burst=abs(burst)

line = r.readline()
data = line.split() #split string into a list
lambda0=float(data[0])
prio = np.random.poisson(lambda0, n)

w.write(str(n)+"\n")
for i in range(n):
     w.write(str(i+1)
     +" "+str(float("{0:.2f}".format(arriv[i])))
     +" "+str(float("{0:.2f}".format(burst[i])))
     +" "+str(float("{0:.2f}".format(prio[i])))+"\n")
	 
r.close()
w.close() 

	 