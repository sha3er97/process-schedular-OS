import numpy as np
import sys
read =  sys.argv[1]

#to be read from user by gui
write = "result.txt"
contextSwitch = 0
quantum = 1
mode = 3
'''
mode :
1. [15%] Non-Preemptive Highest Priority First.(HPF)
2. [15%] First Come First Served. (FCFS)
3. [20%] Round Robin with fixed time quantum.(RR)
4. [20%] Preemptive Shortest Remaining Time Next.(SRTN)
'''

r =  open(read,'r')
w_file= open(write,"w+")

line = r.readline()
data = line.split() #split string into a list
n=int(data[0])

processno=np.zeros(n)
arriv=np.zeros(n)
burst =np.zeros(n)
prio = np.zeros(n)
for i in range(n):
    line = r.readline()
    data = line.split() #split string into a list
    processno[i]=int(data[0])
    arriv[i]=float(data[1])
    burst[i]=float(data[2])
    prio[i]=float(data[3])

'''
print("process no",processno,"\n")
print("arriv",arriv,"\n")
print("burst",burst,"\n")
print("prio",prio,"\n")
'''

totalTimeMax = np.sum(burst)+contextSwitch*n
import matplotlib.pyplot as plt
w = 20
h = 4
d = 100
plt.figure(figsize=(w, h), dpi=d)
plt.axis([0, totalTimeMax*1.5, 0, n+1])
plt.xlabel('TimeStep')
plt.ylabel('Process')

waitingtime=np.zeros(n)
turnaroundtime=np.zeros(n)
remaining_time=np.copy(burst)
finish_time=np.zeros(n)
finished=np.zeros(n)

def FCFS_schedule():
    process_id_list_FCFS =[]
    run_time_list_FCFS=[]
    totalTime=0
    process_id_list_FCFS.append(processno[0])
    run_time_list_FCFS.append(0)

    for i in range(n):
        process_id_list_FCFS.append(processno[i])
        waitingtime[i]=totalTime #before adding burst time
        totalTime+=burst[i]
        run_time_list_FCFS.append(totalTime)
        turnaroundtime[i]=totalTime-arriv[i]
        #add context switching TIME
        process_id_list_FCFS.append(0)
        totalTime+=contextSwitch
        run_time_list_FCFS.append(totalTime)

    W_turnaroundtime=turnaroundtime/burst
    AVG = np.average(turnaroundtime)
    AVG_W = np.average(W_turnaroundtime)
    '''
    print("waitingtime",waitingtime,"\n")
    print("turnaroundtime",turnaroundtime,"\n")
    print("W_turnaroundtime",W_turnaroundtime,"\n")
    print("AVG : ",AVG,"\n")
    print("AVG_W : ",AVG_W,"\n")
    '''
    w_file.write("# "+"waiting time "+" turn around time "+" weighted turn around time "+"\n")
    for i in range(n):
     w_file.write(str(i+1)
     +"  |"+str(float("{0:.1f}".format(waitingtime[i])))
     +"         | "+str(float("{0:.1f}".format(turnaroundtime[i])))
     +"                          | "+
     str(float("{0:.1f}".format(W_turnaroundtime[i])))+"\n")
    
    w_file.write("average turnaround time : "+str(float("{0:.2f}".format(AVG)))+"\n")
    w_file.write("average weighted turnaround time : "+str(float("{0:.2f}".format(AVG_W)))+"\n")

    plt.step(run_time_list_FCFS,process_id_list_FCFS,where='pre')
    plt.plot(run_time_list_FCFS,process_id_list_FCFS, 'C0o', alpha=0.5,label='FCFS')
    plt.legend()
    plt.show()

def check_if_all_finished():
    for i in range(n):
        if (finished[i] == 0):
            return False
    
    return True

def RR_schedule():
    process_id_list_RR =[]
    run_time_list_RR=[]
    totalTime=0
    process_id_list_RR.append(processno[0])
    run_time_list_RR.append(0)
    i=0

    while(not check_if_all_finished()):
        if(not(arriv[i]>totalTime or finished[i]==1)):
            process_id_list_RR.append(processno[i])
            if(remaining_time[i]> quantum):
                totalTime+=quantum
                remaining_time[i]-=quantum
            else :
                totalTime+=remaining_time[i]
                remaining_time[i]=0
                finished[i]=1
                finish_time[i]=totalTime
            run_time_list_RR.append(totalTime)
            #add context switching TIME
            process_id_list_RR.append(0)
            totalTime+=contextSwitch
            run_time_list_RR.append(totalTime)
        i =(i+1) % (n)

    waitingtime=finish_time-burst
    turnaroundtime=finish_time-arriv
    W_turnaroundtime=turnaroundtime/burst
    AVG = np.average(turnaroundtime)
    AVG_W = np.average(W_turnaroundtime)
    '''
    print("waitingtime",waitingtime,"\n")
    print("turnaroundtime",turnaroundtime,"\n")
    print("W_turnaroundtime",W_turnaroundtime,"\n")
    print("AVG : ",AVG,"\n")
    print("AVG_W : ",AVG_W,"\n")
    '''
    w_file.write("# "+"waiting time "+" turn around time "+" weighted turn around time "+"\n")
    for i in range(n):
     w_file.write(str(i+1)
     +"  |"+str(float("{0:.1f}".format(waitingtime[i])))
     +"         | "+str(float("{0:.1f}".format(turnaroundtime[i])))
     +"                          | "+
     str(float("{0:.1f}".format(W_turnaroundtime[i])))+"\n")
    
    w_file.write("average turnaround time : "+str(float("{0:.2f}".format(AVG)))+"\n")
    w_file.write("average weighted turnaround time : "+str(float("{0:.2f}".format(AVG_W)))+"\n")
    
    plt.step(run_time_list_RR,process_id_list_RR,where='pre')
    plt.plot(run_time_list_RR,process_id_list_RR, 'C0o', alpha=0.5,label='RR')
    plt.legend()
    plt.show()

def HPF_schedule():
    process_id_list_HPF =[]
    run_time_list_HPF=[]
    totalTime=0
    process_id_list_HPF.append(processno[0])
    run_time_list_HPF.append(0)
    #ALGORITHM

def SRTN_schedule():
    process_id_list_SRTN =[]
    run_time_list_SRTN=[]
    totalTime=0
    process_id_list_SRTN.append(processno[0])
    run_time_list_SRTN.append(0)
    #ALGORITHM

if(mode == 1):
    #sort w.r.t priority
    prio, processno,burst,arriv = zip(*sorted(zip(prio, processno,burst,arriv)))
    HPF_schedule()
elif(mode == 2):
    #sort w.r.t arrival time
    arriv, processno,burst,prio = zip(*sorted(zip(arriv, processno,burst,prio)))
    FCFS_schedule()
elif(mode==3):
    #sort w.r.t arrival time
    arriv, processno,burst,prio = zip(*sorted(zip(arriv, processno,burst,prio)))
    RR_schedule()
elif(mode==4):
    #sort w.r.t burst time
    burst, processno,arriv,prio = zip(*sorted(zip(burst, processno,arriv,prio)))
    SRTN_schedule()

r.close()
w_file.close() 
