"""Async utilities for parallel processing of LLM and API calls."""

import asyncio
from typing import List, Dict, Optional, Any, Callable, TypeVar, Awaitable
from concurrent.futures import ThreadPoolExecutor
import time
from functools import wraps

T = TypeVar("T")


class AsyncProcessor:
    """Handles parallel processing of tasks."""

    def __init__(self, max_workers: int = 4):
        """
        Initialize async processor.

        Args:
            max_workers: Maximum number of concurrent workers
        """
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    async def map_async(
        self, async_fn: Callable[[T], Awaitable[Any]], items: List[T]
    ) -> List[Any]:
        """
        Execute async function on all items in parallel.

        Args:
            async_fn: Async function to apply
            items: Items to process

        Returns:
            List of results in same order as items
        """
        tasks = [async_fn(item) for item in items]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def batch_async(
        self, async_fn: Callable[[T], Awaitable[Any]], items: List[T], batch_size: int = 3
    ) -> List[Any]:
        """
        Execute async function with batching for rate limiting.

        Args:
            async_fn: Async function to apply
            items: Items to process
            batch_size: Max concurrent operations

        Returns:
            List of results
        """
        results = []
        for i in range(0, len(items), batch_size):
            batch = items[i : i + batch_size]
            batch_results = await self.map_async(async_fn, batch)
            results.extend(batch_results)
            if i + batch_size < len(items):
                await asyncio.sleep(0.1)  # Small delay between batches
        return results

    def run_sync(self, async_fn: Callable[..., Awaitable[T]], *args, **kwargs) -> T:
        """
        Run async function from sync context.

        Args:
            async_fn: Async function to run
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Function result
        """
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # We're already in an async context, use thread executor
                future = loop.run_in_executor(
                    self.executor, lambda: asyncio.run(async_fn(*args, **kwargs))
                )
                return asyncio.wait(future)
            else:
                return loop.run_until_complete(async_fn(*args, **kwargs))
        except RuntimeError:
            # No event loop exists, create one
            return asyncio.run(async_fn(*args, **kwargs))

    def shutdown(self) -> None:
        """Shutdown executor."""
        self.executor.shutdown(wait=True)


class RateLimiter:
    """Simple rate limiter for API calls."""

    def __init__(self, calls_per_second: float = 1.0):
        """
        Initialize rate limiter.

        Args:
            calls_per_second: Maximum calls per second
        """
        self.calls_per_second = calls_per_second
        self.min_interval = 1.0 / calls_per_second
        self.last_call = 0.0
        self.lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Wait until it's safe to make another call."""
        async with self.lock:
            now = time.time()
            time_since_last_call = now - self.last_call

            if time_since_last_call < self.min_interval:
                await asyncio.sleep(self.min_interval - time_since_last_call)

            self.last_call = time.time()

    def __call__(self, func: Callable) -> Callable:
        """Decorator to apply rate limiting to a function."""

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            await self.acquire()
            return await func(*args, **kwargs)

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            asyncio.run(self.acquire())
            return func(*args, **kwargs)

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper


class ParallelLLMProcessor:
    """Process multiple LLM requests in parallel with rate limiting."""

    def __init__(self, client, max_concurrent: int = 2):
        """
        Initialize parallel LLM processor.

        Args:
            client: OllamaClient instance
            max_concurrent: Maximum concurrent LLM requests
        """
        self.client = client
        self.rate_limiter = RateLimiter(calls_per_second=max_concurrent)
        self.processor = AsyncProcessor(max_workers=max_concurrent)

    async def generate_multiple(
        self,
        model: str,
        prompts: List[str],
        system: Optional[str] = None,
        temperature: float = 0.2,
    ) -> List[str]:
        """
        Generate text for multiple prompts in parallel.

        Args:
            model: LLM model name
            prompts: List of prompts
            system: System message
            temperature: Temperature setting

        Returns:
            List of generated responses
        """

        async def generate_one(prompt: str) -> str:
            await self.rate_limiter.acquire()
            return self.client.generate(
                model, prompt, system=system, temperature=temperature
            )

        tasks = [generate_one(prompt) for prompt in prompts]
        return await asyncio.gather(*tasks, return_exceptions=True)


def async_timed(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
    """Decorator to measure async function execution time."""

    @wraps(func)
    async def wrapper(*args, **kwargs) -> T:
        start = time.time()
        result = await func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"[Timing] {func.__name__} took {elapsed:.2f}s")
        return result

    return wrapper
