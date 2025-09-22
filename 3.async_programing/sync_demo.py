# Synchronous Programing Example
import time
from timeit import default_timer as timer

def run_task(name, seconds):
    print(f"{name} started at: {timer()}")
    time.sleep(seconds)
    print(f"{name} compleated at: {timer()}")


start = timer()
run_task('Task_1', 2)
run_task('Task_2', 1)
run_task('Tasl_3', 3)

print(f"\nTotal time taken: {timer() - start:.2f} sec.")