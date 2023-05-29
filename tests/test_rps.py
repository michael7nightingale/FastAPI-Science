import asyncio
import aiohttp
import requests
from matplotlib import pyplot as plt
import time
import numpy as np


times_range = [100, 250, 500, 750, 1000, 1500, 2000, 2500, 3000, 3500, 4000]
urls = [
    'http://localhost:8000/science/physics/formula/impulse/', 
    'http://localhost:8000/science/physics', 
     'http://localhost:8000/', 
     'http://localhost:8000/accounts/login/', 
     'http://localhost:8000/accounts/register/', 


]


async def test_rps_async(url: str, n_times: int) -> tuple[float, float]:
    async with aiohttp.ClientSession() as session:
        time0 = time.perf_counter()

        for _ in range(n_times):
            async with session.get(url) as resp:
                await resp.text()

        elapsed_time = time.perf_counter() - time0
        return elapsed_time, n_times/elapsed_time


def test_rps_sync(url: str, n_times: int) -> tuple[float, float]:
    time0 = time.perf_counter()

    for _ in range(n_times):
        print(_)
        resp = requests.get(url)

    elapsed_time = time.perf_counter() - time0
    return elapsed_time, n_times/elapsed_time


async def main_async():
    results = await asyncio.gather(
        *(test_rps_async(urls[0], n) for n in times_range)
    )
    return results


def main_sync():
    results = [test_rps_sync(urls[0], n) for n in times_range]
    return results


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    results1 = loop.run_until_complete(main_async())
    plt.plot(times_range, [i[1] for i in results1], marker='*', color='b', label='Асинхронно')

    # results2 = main_sync()
    # plt.plot(times_range, [i[1] for i in results2], marker='*', color='r', label='Синхронно')

    plt.grid()
    plt.legend()
    plt.show()





