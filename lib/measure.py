import time


def print_runtime(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"[took {(end - start) * 1000:.4f}ms.]")
        return result

    return wrapper
