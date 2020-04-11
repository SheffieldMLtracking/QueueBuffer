from multiprocessing import Process
from QueueBuffer import QueueBuffer as QB
import numpy as np
import time

class Other:
    def __init__(self):
        print("Other class initialised")
        self.q = QB(5)
    
    def worker(self):
        i = 0
        while True:
            time.sleep(2)
            print("putting item on queue")
            self.q.put(i)
            i+=1

class Trigger:
    def __init__(self,q):
        print("Trigger class initialised")
        self.q = q
    
    def worker(self):
        while True:
            print("waiting for queue")
            v = self.q.pop()
            print(v)
            print("Try reading from queue")
            print(self.q.read(0),self.q.len(),self.q.read(self.q.len()-1))
            
other = Other()
t = Process(target=other.worker)
t.start()

trigger = Trigger(other.q)        
t = Process(target=trigger.worker)
t.start()
