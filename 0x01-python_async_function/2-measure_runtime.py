#!/usr/bin/env python3
"""Measure the Time"""

import time
wait_n = __import__('2-measure_runtime.py').wait_n


async def measure_time(n: int, max_delay: int) -> float:
    """Measures and returns total execution time"""
    start_time = time.perf_counter()
    await wait_n(n, max_delay)
    end_time = time.perf_counter()

    total_time = (end_time - start_time) / n
    return total_time
