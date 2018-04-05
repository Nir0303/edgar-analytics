# Table of Contents
1. [Approach](README.md#Approach)
2. [Dependencies](README.md#Dependencies)
3. [Instructions](README.md#Instructions)
4. [Tests](README.md#Tests)

# Approach
1. Read input inactivity file to get details about inactivity session.
2. Read input log via python generator, so that you are not reading entire file.
3. Open output file for writing output data. when the record has become inactive, pass it via coroutine to write data.  
4. Iterate records via generator
     - for first record save check_time , create Record userdefined object , place it HashMap with ip address as key.
     - from next record check if current_record_timestamp matches with check_time.
     - if match (current_record_timestamp matches with check_time). check if record is already been tracked by HashMap , if been tracked, update metadata in HashMap. if not been tracked, place it HashMap with ip address as key.
     - if not match (current_record_timestamp not matches with check_time), update check_time and iterate HashMap keys iterate for pausible deletions and inserations in output file if inactivity time exceeds. check if existing record is already been tracked by HashMap , if been tracked, update metadata in HashMap. if not been tracked, place it HashMap with ip address as key.

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
usage: sessionization.py [-h] [--input INPUT]
                         [--inactivity_file INACTIVITY_FILE] [--output OUTPUT]
                         [--log_level LOG_LEVEL]

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        input files to process
  --inactivity_file INACTIVITY_FILE, -a INACTIVITY_FILE
                        inactivity file
  --output OUTPUT, -o OUTPUT
                        output file to write process data
  --log_level LOG_LEVEL, -l LOG_LEVEL
                        Set loglevel for debugging and analysis
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `./run.sh`

# Tests
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `cd insight_testsuite`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `./run_tests.sh`


