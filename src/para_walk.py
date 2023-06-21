from multiprocessing import Queue, Process
from tqdm import tqdm
from typing import Union, Callable, Generator, TypedDict, List
import pathlib
import os
import sys


# annotation types
PathLike = Union[str, os.PathLike]

class OsWalkParam(TypedDict):
    topdown: bool
    onerror: Union[None, Callable]
    followlinks: bool
    

def pwalk(top_directory: PathLike,
          parallel: int=4,
          **kwargs: OsWalkParam) -> Generator[str, List[str], List[str]]:
    """
    a parallel version of os.walk

    :param str top_directory: directory to walk
    :param int parallel: multiple process number
    :param optional kwargs: arguments pass to os.walk
    """
    # create two queue, one for processing, one for result
    process_queue = Queue()
    result_queue = Queue()

    # create process
    for i in range(parallel):
        process = Process(target=one_step_walk,
                          args=(process_queue, result_queue, kwargs))
        process.start()
        
    # put init data in process_queue
    process_queue.put(top_directory)

    # get result from result_queue
    while True:
        try:
            res = result_queue.get(timeout=100)
            yield res
        except Exception as exp:
            break


def one_step_walk(process_queue: Queue, result_queue: Queue,
                  kwargs: OsWalkParam) -> None:
    """
    walk worker, recieve data from process_queue and put data back to both
    process_queue and result_queue
    :param Queue process_queue: process queue for distribute jobs
    :param Queue result_queue: process queue for collect result
    :param Optional kwargs: arguments pass to os.walk
    """
    while True:
        try:
            # set a timeout, otherwise wait for queue is too slow            
            top_directory = process_queue.get(timeout=100) 
        
            # get all sub directories
            walk = next(os.walk(top_directory, **kwargs))

            # put result to result_queue
            result_queue.put(walk)

            # put sub directories to process queue
            prefix, sub_dirs, files = walk
            for sd in sub_dirs:
                process_queue.put(os.path.join(prefix, sd))

        except Exception as exp:
            break
        
