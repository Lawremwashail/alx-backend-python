#!/usr/bin/env python3
"""Create an asyncio to wait for tasks"""

import asyncio
wait_random = __import__('0-basic_async_syntax')


def task_wait_random(max_delay: int) -> asyncio.Task:
    """Creates and returns asyncio task"""
    return asyncio.create_task(wait_random(max_delay))
