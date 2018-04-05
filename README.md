# Table of Contents
1. [Approach](README.md#Approach)
2. [Dependencies](README.md#Dependencies)
3. [Instructions](README.md#Instructions)
4. [Tests](README.md#Tests)

# Approach
1. 
2.
3.
4.

# Dependencies
1. python3
2. csv
3. mock
4. pytest
5. argparse
6. pytest

# Instructions
1. Clone the github repo and change directory

2. Install required packages

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `pip install -r requirements.txt`

3. Check python style or static checks (>8.5 score)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `pylint src/*.py`

4. Run python unit testcases

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `pytest`

5. Run shell script to start streaming application

```
usage: sessionization.py [-h] [--input INPUT] [--output OUTPUT] [--log_level LOG_LEVEL]

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        input files to process
  --output OUTPUT, -o OUTPUT
                        output file to write process data
  --log_level LOG_LEVEL, -l LOG_LEVEL
                        Set loglevel for debugging and analysis


```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `./run.sh`

# Tests
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `cd insight_testsuite`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `./run_tests.sh`


