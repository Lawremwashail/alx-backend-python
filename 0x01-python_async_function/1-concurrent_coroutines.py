#!/usr/bin/env python3
"""Execute multiple coroutines at the same time with async"""

from typing import List
import asyncio
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    Spawns wait_random n times with specified max_delay,
    returns list of all delays (float values)
    """
    tasks = []

    for _ in range(n):
        task = wait_random(max_delay)
        tasks.append(task)

    results = []

    for task in asyncio.as_completed(tasks):
        results.append(task)

    delays = []

    for task in results:
        delay = await task
        delays.append(delay)

    return delays
