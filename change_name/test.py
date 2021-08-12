import asyncio
import time


async def sleep1(delay):
    print(f'delay:{delay} time:{time.time()}')
    await asyncio.sleep(delay)
    print(f'await endtime: {time.time()}')
    return delay


async def main1():
    tasks = []
    for i in range(5):
       task = asyncio.create_task(sleep1(i))
       tasks.append(task)
    L = await asyncio.gather(*tasks)
    print(L)
start = time.time()
asyncio.run(main1())
end = time.time()
print(end-start)