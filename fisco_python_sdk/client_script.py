import os                                                                       
from multiprocessing import Pool                                                
                                                                                                                                     
processes = ('client.py worker1 server 4000,4000,4000,3000,10,10,10,10,4000,10 contractaddr', 'client.py worker2 server 0,10,10,10,4000,3000,4000,5000,10,4500 contractaddr')                                    
                                                  
                                                                                
def run_process(process):                                                             
    os.system('python {}'.format(process))                                       
                                                                                
                                                                                
pool = Pool(processes=2)                                                        
pool.map(run_process, processes) 