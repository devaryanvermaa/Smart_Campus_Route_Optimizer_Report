"""
Smart Campus Parking & Route Optimizer
Module: sorting_searching.py
Author: Aryan (MCA DAA Project)
Description:
    Manual implementation of fundamental sorting and searching algorithms:
    - Merge Sort (Divide and Conquer)
    - Linear Search (Sequential Scan)
    - Binary Search (Logarithmic Halving)
    - Empirical benchmarking comparing manual Merge Sort vs Python's Timsort.

DAA Theoretical Analysis:
    1. Merge Sort:
       - Strategy: Divide and Conquer
       - Recurrence Relation: T(n) = 2 T(n/2) + O(n)
       - By Master Theorem: T(n) = O(n log n) in Best, Average, and Worst cases.
       - Space Complexity: O(n) auxiliary memory for merge buffer.
       - Stability: Preserved (equal elements maintain relative original order).

    2. Linear Search:
       - Best Case: O(1) when element is at index 0.
       - Worst Case: O(n) when element is at last position or absent.
       - Average Case: O(n/2) = O(n).
       - Space Complexity: O(1).
       - Precondition: None (works on unsorted collections).

    3. Binary Search:
       - Recurrence Relation: T(n) = T(n/2) + O(1)
       - Time Complexity: O(log n) in average and worst cases; O(1) best case.
       - Space Complexity: O(1) iterative implementation.
       - Precondition: Collection must already be sorted by target key.
"""

import time
import random
from typing import List, Any, Callable, Optional, Tuple, Dict


# ==========================================
# 1. MERGE SORT IMPLEMENTATION
# ==========================================

def merge_sort(arr: List[Any], key: Callable[[Any], Any] = lambda x: x, reverse: bool = False) -> List[Any]:
    """
    Sorts a list of items using the recursive Merge Sort algorithm.

    Args:
        arr: The list of items to sort.
        key: A function that extracts a comparison key from each element.
        reverse: If True, sort in descending order; otherwise ascending.

    Returns:
        A new sorted list (leaves original unmodified).
    """
    # Base case: lists of size 0 or 1 are already sorted
    if len(arr) <= 1:
        return list(arr)

    # Divide: Split list into two halves
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid], key=key, reverse=reverse)
    right_half = merge_sort(arr[mid:], key=key, reverse=reverse)

    # Conquer & Combine: Merge the two sorted halves
    return _merge(left_half, right_half, key=key, reverse=reverse)


def _merge(left: List[Any], right: List[Any], key: Callable[[Any], Any], reverse: bool) -> List[Any]:
    """
    Helper function to merge two sorted lists in O(len(left) + len(right)) time.
    Maintains algorithmic stability by favoring the left element on equality.
    """
    merged = []
    i = 0
    j = 0
    len_left = len(left)
    len_right = len(right)

    while i < len_left and j < len_right:
        k_left = key(left[i])
        k_right = key(right[j])

        # If reverse=False (ascending): choose left if k_left <= k_right
        # If reverse=True (descending): choose left if k_left >= k_right
        if not reverse:
            condition = (k_left <= k_right)
        else:
            condition = (k_left >= k_right)

        if condition:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Append any remaining elements
    while i < len_left:
        merged.append(left[i])
        i += 1
    while j < len_right:
        merged.append(right[j])
        j += 1

    return merged


# ==========================================
# 2. SEARCHING ALGORITHMS
# ==========================================

def linear_search(arr: List[Any], target: Any, key: Callable[[Any], Any] = lambda x: x) -> Tuple[Optional[int], int]:
    """
    Searches sequentially for a target in an array.

    Args:
        arr: Collection of items.
        target: Target value to match.
        key: Function extracting the value to compare against target.

    Returns:
        (index_of_item_or_None, comparisons_count)
    """
    target_str = str(target).strip().lower()
    comparisons = 0

    for idx, item in enumerate(arr):
        comparisons += 1
        item_val = str(key(item)).strip().lower()
        if item_val == target_str:
            return idx, comparisons

    return None, comparisons


def is_sorted(arr: List[Any], key: Callable[[Any], Any] = lambda x: x) -> bool:
    """Check if an array is sorted in ascending order according to key."""
    for i in range(len(arr) - 1):
        if key(arr[i]) > key(arr[i + 1]):
            return False
    return True


def binary_search(sorted_arr: List[Any], target: Any, key: Callable[[Any], Any] = lambda x: x) -> Tuple[Optional[int], int]:
    """
    Performs Binary Search on an array assumed to be sorted in ascending order.

    Args:
        sorted_arr: Array sorted in ascending order.
        target: Target value to find.
        key: Function extracting the value to compare against target.

    Returns:
        (index_of_item_or_None, comparisons_count)

    Raises:
        ValueError: If input array is not sorted by key.
    """
    # Verify precondition
    if not is_sorted(sorted_arr, key):
        raise ValueError("Binary Search requires the collection to be sorted in ascending order prior to searching.")

    low = 0
    high = len(sorted_arr) - 1
    comparisons = 0
    target_str = str(target).strip().lower()

    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        mid_val = str(key(sorted_arr[mid])).strip().lower()

        if mid_val == target_str:
            return mid, comparisons
        elif mid_val < target_str:
            low = mid + 1
        else:
            high = mid - 1

    return None, comparisons


# ==========================================
# 3. EMPIRICAL BENCHMARKING
# ==========================================

def benchmark_sorting_algorithms(sizes: Optional[List[int]] = None) -> List[Dict[str, Any]]:
    """
    Conducts empirical execution-time comparison between manual Merge Sort
    and Python's built-in Timsort (sorted()) across various array sizes.

    Uses time.perf_counter() for high-precision measurement.

    Returns:
        List of benchmark records containing:
        - size: Integer elements count
        - merge_sort_time_sec: Time in seconds
        - builtin_sort_time_sec: Time in seconds
        - speedup_factor: Built-in speedup ratio
    """
    if sizes is None:
        sizes = [100, 500, 1000, 2500, 5000, 10000]

    results = []

    for size in sizes:
        # Generate reproducible random list of integers
        random.seed(42 + size)
        test_data = [random.randint(1, 100000) for _ in range(size)]

        # 1. Benchmark Manual Merge Sort
        data_copy1 = list(test_data)
        start_ms = time.perf_counter()
        _ = merge_sort(data_copy1)
        end_ms = time.perf_counter()
        merge_duration = end_ms - start_ms

        # 2. Benchmark Built-in Timsort
        data_copy2 = list(test_data)
        start_bi = time.perf_counter()
        _ = sorted(data_copy2)
        end_bi = time.perf_counter()
        builtin_duration = end_bi - start_bi

        # Calculate practical speedup factor
        speedup = merge_duration / builtin_duration if builtin_duration > 0 else 0.0

        results.append({
            "size": size,
            "merge_sort_time_sec": merge_duration,
            "builtin_sort_time_sec": builtin_duration,
            "speedup_factor": speedup
        })

    return results
