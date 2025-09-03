import asyncio
from timeit import default_timer as timer


async def run_task(name, seconds):
    print(f"{name} started at; {timer()}")
    await asyncio.sleep(seconds)
    print(f"{name} completed at: {timer()}")

async def main():
    start = timer()
    await asyncio.gather(
    run_task('Task_1', 2),
    run_task('Task_2', 1),
    run_task('Task_3', 3)
    )
    print(f'\n Total time taken: {timer() - start:.2f} sec.')

asyncio.run(main())