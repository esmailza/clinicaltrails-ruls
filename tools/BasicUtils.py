from time import sleep
from typing import Iterable, List
import numpy as np
from heapq import nlargest, nsmallest
from multiprocessing import Pool
from threading import Thread
from math import ceil
import subprocess
import json
import pickle
import csv
import tqdm
import time
from collections import defaultdict


def calculate_time(func):
     
    # added arguments inside the inner1,
    # if function takes any arguments,
    # can be added like this.
    def inner1(*args, **kwargs):
 
        # storing time before function execution
        begin = time.time()
         
        data = func(*args, **kwargs)
 
        # storing time after function execution
        end = time.time()
        print("Total time taken in : ", func.__name__, end - begin)
        return data

class MyMultiProcessing:
    def __init__(self, thread_num:int=1):
        self.thread_num = thread_num

    @calculate_time
    def run(self, func, input_list:list):
        print('Number of lines is %d' % len(input_list))
        with Pool(self.thread_num) as pool:
            print('Start assigning jobs')
            jobs = [pool.apply_async(func=func, args=(*argument,)) if isinstance(argument, tuple) else pool.apply_async(func=func, args=(argument,)) for argument in input_list]
            pool.close()
            print('Jobs are assigned, start getting results')
            return [job.get() for job in tqdm.tqdm(jobs)]

def my_write(file_name:str, content:dict):
    with open(file_name, 'w') as f_out:
        f_out.write('\n'.join(content))