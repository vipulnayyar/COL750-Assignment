# foav-assignment
Foundations of Automatic Verification Assignment

## Setup
```
$ source .venv/bin/activate
$ pip3 install -r requirements.txt
```
## Input File for Q1-Q3
The input file should consist of a N X N array in the following format.

$ cat input

S.X..

.X.X.

...X.

XX...

...XG


## Q1 : SAT Solution
```
$ python3 sat.py -h

usage: sat.py [-h] [-i]

options:

  -h, --help         show this help message and exit
  
  -i, --incremental  run incrementally
  ```
```
$ python3 sat.py < input
```
## Q2 : SMT Solution
```
$ python3 smt.py < input
```
## Q3 : Incremental SAT Solution
```
$ python3 sat.py -i < input
```
## Q4 : NuSMV Model
```
$  ./NuSMV  model.smv
```
Note: Please use platform appropriate NuSMV binary present in the folder.
