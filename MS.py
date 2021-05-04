import multiprocessing as mp
from Final import (
    rundistance,
    rungps
    )
    
if(__name__=='__main__'):
    task_distance = mp.Process(target=rundistance)
    task_gps = mp.Process(target=rungps)
    
    task_distance.start()
    task_gps.start()


