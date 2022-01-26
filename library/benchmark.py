"""
Library for measuring the execution time of a script

Author: Antonio Barbosa
E-mail: cunha.barbosa@gmail.com
Version: 2021-07-29
"""

import time
import sys
from datetime import datetime, timedelta

# How to use this library:
# Create folder "library" and copy this file into folder
# On the main script: from library import benchmark


# Start the benchmark in a script
# Input: None
# Output: Time in seconds since the epoch
# Execution: initial_time = benchmark.benchmark_ini()
# Help: https://docs.python.org/3/library/time.html#time.time
def benchmark_ini():
    """
    Start the benchmark in a script
    :return: Current time
    :rtype: float
    """
    # import time
    print("Current Time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  # Get current datetime
    return time.time()


# Stop the benchmark in a script and present the name of the script
# Input: initial time
# Output: none
# Execution: benchmark.benchmark_end(initial_time, sys.argv[0])
def benchmark_end(start, name_script):
    """
    Stop the benchmark in a script and present the name of the script
    :param float start: Initial datetime
    :param str name_script: The name of the script
    """
    # import time
    # shelf.name_script = name_script
    execute_time = round(time.time() - start, 0)
    print("done " + name_script + "! - Job took " + str(execute_time) + ' seconds = ' + str(
        timedelta(seconds=execute_time)) + "\n")


if __name__ == '__main__':
    # Only for debug:
    initial_time = benchmark_ini()  # Begin benchmark

    print("Do something...")

    benchmark_end(initial_time, sys.argv[0])  # End benchmark and end of script
