import numpy as np
import sys
import matplotlib.pyplot as plt

read = input("please enter the file name to read:\n")
#read = 'test.txt'

#to be read from user by gui
write = "result.txt"
contextSwitch = float(input("please enter context switch time:\n"))
#contextSwitch = 0.5
mode = int(input("please enter the mode:\n1. Non-Preemptive Highest Priority First.(HPF)\n2. First Come First Served. (FCFS)\n3. Round Robin with fixed time quantum.(RR)\n4. Preemptive Shortest Remaining Time Next.(SRTN)\n"))
#mode = 2
if mode == 3:
    quantum = float(input("please enter quantum time:\n"))
else:
    quantum = 0.01 #least possible time slot for .1f 
    #quantum = 1   #if we used integers

'''
mode :
1. Non-Preemptive Highest Priority First.(HPF)
2. First Come First Served. (FCFS)
3. Round Robin with fixed time quantum.(RR)
4. Preemptive Shortest Remaining Time Next.(SRTN)
'''

r =  open(read,'r')
w_file= open(write,"w+")

#get processes number from file's first line.
line = r.readline()
data = line.split() #split string into a list
n=int(data[0])

processno=np.zeros(n)
arriv=np.zeros(n)
burst =np.zeros(n)
prio = np.zeros(n)

#get data for each process and store them
for i in range(n):
    line = r.readline()
    data = line.split() #split string into a list
    processno[i]=int(data[0])
    arriv[i]=float(data[1])
    burst[i]=float(data[2])
    prio[i]=float(data[3])

#close read file
r.close()
#########################################################################################

#set diagram dimensions and axis

s = 0
if mode == 3 and contextSwitch != 0 :
    for i in range(n):
        s += int(burst[i]/quantum)*0.4

totalTimeMax = np.sum(burst)+contextSwitch*n+s*contextSwitch+np.max(arriv)
w = 20
h = 4
d = 100
plt.figure(figsize=(w, h), dpi=d)
plt.axis([0, totalTimeMax*1.7, -1, n+1])
plt.xlabel('TimeStep')
plt.ylabel('Process')

waitingtime=np.zeros(n)
turnaroundtime=np.zeros(n)
finish_time=np.zeros(n)
finished=np.zeros(n)

from utility_funcs import *
#################################################################################################

#scheduling algorithms :

def FCFS_schedule():
    end_time=[]
    process_number_ended=[]
    process_id_list_FCFS =[]
    run_time_list_FCFS=[]
    totalTime=0
    process_id_list_FCFS.append(-1)
    run_time_list_FCFS.append(0)

    while (not check_if_all_finished(finished,n)):
        i = 0
        while(i<n):
            if(totalTime>arriv[i] and finished[i] == 0):
                break
            i += 1
        if i == n:
            process_id_list_FCFS.append(-1)
            totalTime+=quantum
            run_time_list_FCFS.append(totalTime)
            continue
        process_id_list_FCFS.append(processno[i])
        process_number_ended.append(processno[i])
        waitingtime[i]=totalTime #before adding burst time
        totalTime+=burst[i]
        run_time_list_FCFS.append(totalTime)
        end_time.append(totalTime)
        turnaroundtime[i]=totalTime-arriv[i]
        finished[i] = 1
        #add context switching TIME
        if (contextSwitch != 0 and isAnyoneNext(totalTime,finished,arriv,n)):
            process_id_list_FCFS.append(0)
            totalTime+=contextSwitch
            run_time_list_FCFS.append(totalTime)

    process_id_list_FCFS.append(-1)
    run_time_list_FCFS.append(totalTime)

    W_turnaroundtime=turnaroundtime/burst
    AVG = np.average(turnaroundtime)
    AVG_W = np.average(W_turnaroundtime)
    #write results to file
    w_file.write("# "+"waiting time "+" turn around time "+" weighted turn around time "+"\n")
    for i in range(n):
     w_file.write(str(i+1)
     +"  |"+str(float("{0:.1f}".format(waitingtime[i])))
     +"         | "+str(float("{0:.1f}".format(turnaroundtime[i])))
     +"                          | "+
     str(float("{0:.1f}".format(W_turnaroundtime[i])))+"\n")
    w_file.write("average turnaround time : "+str(float("{0:.2f}".format(AVG)))+"\n")
    w_file.write("average weighted turnaround time : "+str(float("{0:.2f}".format(AVG_W)))+"\n")
    #draw diagram
    plt.step(run_time_list_FCFS,process_id_list_FCFS,where='pre',label='FCFS')
    plt.plot(end_time,process_number_ended, 'C0o', alpha=0.5,label='end time')
    plt.plot(arriv,processno, 'ro', alpha=0.5,label='start time')
    plt.legend()
    plt.show()

def RR_schedule():
    end_time=[]
    process_number_ended=[]
    process_id_list_RR =[]
    run_time_list_RR=[]
    totalTime=0
    process_id_list_RR.append(-1)
    run_time_list_RR.append(0)
    i=0

    while(not check_if_all_finished(finished,n)):
        if(arriv[i]<totalTime and finished[i]==0):
            process_id_list_RR.append(processno[i])
            if(remaining_time[i]>quantum):
                totalTime+=quantum
                remaining_time[i]-=quantum
            else :
                totalTime+=remaining_time[i]
                remaining_time[i]=0
                finished[i]=1
                finish_time[i]=totalTime
                process_number_ended.append(processno[i])
                end_time.append(totalTime)
            run_time_list_RR.append(totalTime)
            #add context switching TIME
            if(contextSwitch != 0 and isAnyoneNext(totalTime,finished,arriv,n)):
                process_id_list_RR.append(0)
                totalTime+=contextSwitch
                run_time_list_RR.append(totalTime)
        else:
            if not isAnyoneNext(totalTime,finished,arriv,n):
                process_id_list_RR.append(-1)
                totalTime+=quantum
                run_time_list_RR.append(totalTime)
        i = (i+1) % (n)

    process_id_list_RR.append(-1)
    run_time_list_RR.append(totalTime)

    waitingtime=finish_time-burst
    turnaroundtime=finish_time-arriv
    W_turnaroundtime=turnaroundtime/burst
    AVG = np.average(turnaroundtime)
    AVG_W = np.average(W_turnaroundtime)
    #write results to file
    w_file.write("# "+"waiting time "+" turn around time "+" weighted turn around time "+"\n")
    for i in range(n):
     w_file.write(str(i+1)
     +"  |"+str(float("{0:.1f}".format(waitingtime[i])))
     +"         | "+str(float("{0:.1f}".format(turnaroundtime[i])))
     +"                          | "+
     str(float("{0:.1f}".format(W_turnaroundtime[i])))+"\n")
    w_file.write("average turnaround time : "+str(float("{0:.2f}".format(AVG)))+"\n")
    w_file.write("average weighted turnaround time : "+str(float("{0:.2f}".format(AVG_W)))+"\n")
    #draw diagram
    plt.step(run_time_list_RR,process_id_list_RR,where='pre',label='RR')
    plt.plot(end_time,process_number_ended, 'C0o', alpha=0.5,label='end time')
    plt.plot(arriv,processno, 'ro', alpha=0.5, label='arrival time')
    plt.legend()
    plt.show()

def HPF_schedule():
    end_time=[]
    process_number_ended=[]
    process_id_list_HPF =[]
    run_time_list_HPF=[]
    totalTime=0
    process_id_list_HPF.append(-1)
    run_time_list_HPF.append(0)

    #ALGORITHM
    while(not check_if_all_finished(finished,n)):
        i = 0
        while(i<n):
            if(totalTime>arriv[i] and finished[i] == 0):
                break
            i += 1
        if i == n:
            process_id_list_HPF.append(-1)
            totalTime+=quantum
            run_time_list_HPF.append(totalTime)
            continue
        process_id_list_HPF.append(processno[i])
        process_number_ended.append(processno[i])
        waitingtime[i]=totalTime #before adding burst time
        totalTime+=burst[i]
        run_time_list_HPF.append(totalTime)
        end_time.append(totalTime)
        turnaroundtime[i]=totalTime-arriv[i]
        finished[i] = 1
        #add context switching TIME
        if(contextSwitch != 0 and isAnyoneNext(totalTime,finished,arriv,n)):
            process_id_list_HPF.append(0)
            totalTime+=contextSwitch
            run_time_list_HPF.append(totalTime)

    process_id_list_HPF.append(-1)
    run_time_list_HPF.append(totalTime)
    W_turnaroundtime=turnaroundtime/burst
    AVG = np.average(turnaroundtime)
    AVG_W = np.average(W_turnaroundtime)
    #write results to file
    w_file.write("# "+"waiting time "+" turn around time "+" weighted turn around time "+"\n")
    for i in range(n):
     w_file.write(str(i+1)
     +"  |"+str(float("{0:.1f}".format(waitingtime[i])))
     +"         | "+str(float("{0:.1f}".format(turnaroundtime[i])))
     +"                          | "+
     str(float("{0:.1f}".format(W_turnaroundtime[i])))+"\n")
    w_file.write("average turnaround time : "+str(float("{0:.2f}".format(AVG)))+"\n")
    w_file.write("average weighted turnaround time : "+str(float("{0:.2f}".format(AVG_W)))+"\n")
    #draw diagram
    plt.step(run_time_list_HPF,process_id_list_HPF,where='pre',label='HPF')
    plt.plot(end_time,process_number_ended, 'C0o', alpha=0.5,label='end time')
    plt.plot(arriv,processno, 'ro', alpha=0.5,label='start time')
    plt.legend()
    plt.show()

def SRTN_schedule():
    global remaining_time
    global processno
    global arriv
    global prio
    end_time=[]
    process_number_ended=[]
    process_id_list_SRTN =[]
    run_time_list_SRTN=[]
    totalTime=0
    previous = -1
    process_id_list_SRTN.append(-1)
    run_time_list_SRTN.append(0)
    idle = 0
    #ALGORITHM
    while(not check_if_all_finished(finished,n)):
        i=0
        while i < n:
            if (arriv[i] <= totalTime and finished[i] == 0):
                break
            i+=1
        if i == n:
            process_id_list_SRTN.append(-1)
            totalTime+=quantum
            run_time_list_SRTN.append(totalTime)
            idle = 1
            continue
        if (previous != processno[i]):
            if(contextSwitch != 0 and previous != -1 and idle != 1):
                process_id_list_SRTN.append(0)
                totalTime+=contextSwitch
                run_time_list_SRTN.append(totalTime)
            previous = processno[i]
        process_id_list_SRTN.append(processno[i])
        if(remaining_time[i]> quantum):
            totalTime+=quantum
            remaining_time[i]-=quantum
        else :
            totalTime+=remaining_time[i]
            remaining_time[i]=0
            finished[i]=1
            finish_time[i]=totalTime
            process_number_ended.append(processno[i])
            end_time.append(totalTime)
        run_time_list_SRTN.append(totalTime)
        #add context switching TIME
        remaining_time,processno,arriv, prio = zip(*sorted(zip(remaining_time, processno,arriv,prio)))
        remaining_time = list(remaining_time)
        processno = list(processno)
        arriv = list(arriv)
        prio = list(prio)
        idle = 0
    process_id_list_SRTN.append(-1)
    run_time_list_SRTN.append(totalTime)
    W_turnaroundtime=turnaroundtime/burst
    AVG = np.average(turnaroundtime)
    AVG_W = np.average(W_turnaroundtime)
    #write results to file
    w_file.write("# "+"waiting time "+" turn around time "+" weighted turn around time "+"\n")
    for i in range(n):
     w_file.write(str(i+1)
     +"  |"+str(float("{0:.1f}".format(waitingtime[i])))
     +"         | "+str(float("{0:.1f}".format(turnaroundtime[i])))
     +"                          | "+
     str(float("{0:.1f}".format(W_turnaroundtime[i])))+"\n")
    w_file.write("average turnaround time : "+str(float("{0:.2f}".format(AVG)))+"\n")
    w_file.write("average weighted turnaround time : "+str(float("{0:.2f}".format(AVG_W)))+"\n")

    #draw diagram
    plt.step(run_time_list_SRTN,process_id_list_SRTN,where='pre',label='SRTN')
    plt.plot(end_time,process_number_ended, 'C0o', alpha=0.5,label='end time')
    plt.plot(arriv,processno, 'ro', alpha=0.5,label='arrival time')
    plt.legend()
    plt.show()


#call function based on user choice
if(mode == 1):
    #sort w.r.t priority descendingly
    prio, processno,burst,arriv = zip(*sorted(zip(prio, processno,burst,arriv),reverse = True))
    remaining_time=np.copy(burst)
    HPF_schedule()
elif(mode == 2):
    #sort w.r.t arrival time
    arriv, processno,burst,prio = zip(*sorted(zip(arriv, processno,burst,prio)))
    remaining_time=np.copy(burst)
    FCFS_schedule()
elif(mode==3):
    #sort w.r.t arrival time
    arriv, processno,burst,prio = zip(*sorted(zip(arriv, processno,burst,prio)))
    remaining_time=np.copy(burst)
    RR_schedule()
elif(mode==4):
    #sort w.r.t burst time
    burst, processno,arriv,prio = zip(*sorted(zip(burst, processno,arriv,prio)))
    remaining_time=np.copy(burst)
    SRTN_schedule()

print("your results are saved in "+write+ " file")

#close write file
w_file.close() 

