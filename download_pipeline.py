from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Iterable, List, TypeVar

T = TypeVar("T")
R = TypeVar("R")


def run_parallel_jobs(jobs: Iterable[T], worker_fn: Callable[[T], R], max_workers: int = 4, on_error: Callable[[Exception], None] | None = None) -> List[R]:
    items = list(jobs)
    if not items:
        return []
    workers = max(1, min(max_workers, 8))
    out: List[R] = []
    if workers == 1 or len(items) <= 1:
        for job in items:
            out.append(worker_fn(job))
        return out

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = [ex.submit(worker_fn, j) for j in items]
        for fut in as_completed(futures):
            try:
                out.append(fut.result())
            except Exception as exc:
                if on_error:
                    on_error(exc)
    return out
