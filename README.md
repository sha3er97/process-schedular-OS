
# process-schedular-Simulator
>   simulates process scheduling in linux OS by graphs and calculations
> using python
## Prerequisites

  

#### python basic packages:

* numpy
* matplotlib
* sys


## Getting started

  

- run **process_generator.py** by command line :

```

python process_generator.py readFile.txt WriteFile.txt

```

### read file sample and format

![sample to in](/generator_in.png)

#### our random process generator work as follows:
```
First lineshould include the number of processes.
Second line should include μ and σ of arrival time distribution separated by a whitespace.
Third line should include μ and σ of burst time distribution separated by a whitespace.
Fourth line should include λ of prioritydistribution  
```
*N.B : you can implement your test cases yourself as you want

#### SCHEDULER SIMULATOR :
- run **scheduler.py** by command line as follows (or any other way):

```
python scheduler.py
```
#### you will be asked to enter 4 entries :
1. file to read (processes data)

![sample to test](/scheduler_in.png)
```
First line should include the number of processes.
Each line contains the parameters for one process only, separated by a white space, in the following order:
process number, arrival time, burst time andpriority.
```

2. context switching time (**if needed**).
3. scheduling mode :
```
 1. Non-Preemptive Highest Priority First.(HPF)
 2. First Come First Served. (FCFS)
 3. Round Robin with fixed time quantum.(RR)
 4. Preemptive Shortest Remaining Time Next.(SRTN)
```
4. quantum slice in case of (**RR**) mode.
# output
### graph:
 1. HPF :
 ![HPF](/HPF.png)
 2. FCFS :
 ![FCFS](/FCFS.png)
 3. RR :
 ![RR](/RR.png)
 4. SRTN :
 ![SRTN](/SRTN.png)

##### above graphs are with 0 time context switching for simplicity but you can add any number you want as this fig :
![FCFS_CSS](/FCFS_CS2.png)

### file output :
#### automatically created upon run with the following shape :
![out file](/out_file.png)
 


