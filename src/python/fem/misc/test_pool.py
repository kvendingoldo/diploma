from multiprocessing import Process
import time


def print_something(ind):
    print(ind)
    time.sleep(1)

elements = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']



max_tasks = 0
elements_copy = elements.copy()

if max_tasks > 0:
    while len(elements_copy) > 0:
        tasks = []
        cur_len = len(elements_copy)

        for ind in range(0, max_tasks):
            if ind < cur_len:
                process = Process(target=print_something, args=(elements_copy[ind]))
            else:
                continue
            tasks.append(process)

        for task in tasks:
            task.start()

        for task in tasks:
            task.join()

        if max_tasks < cur_len:
            elements_copy = elements_copy[max_tasks:]
        else:
            break
