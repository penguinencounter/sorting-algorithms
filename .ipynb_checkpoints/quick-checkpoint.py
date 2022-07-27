import sys

from general import swp


def quicksort(a: list, left: int = 0, right: int = None, depth: int = 0):
    if depth * 2 > 2000:
        raise RecursionError(f'Recursion limit will be exceeded ({depth} branch depth) halting before crash')
    n = len(a)
    if right is None:
        right = n - 1
    chks = 0
    swps = 0

    chks += 1
    if right - left < 1:
        # Do we even need to do work here?
        return a, swps, chks

    # partitioning
    pivot = a[right]
    q = left
    j = left
    for _ in range(left, right):
        target = a[j]
        chks += 1
        if target <= pivot:
            swp(a, j, q)
            swps += 1
            q += 1
        j += 1
        if j == right:
            break

    swp(a, right, q)
    # Q is the partition point.

    # Recursively apply quicksort to the left and right partitions
    a, _1, _2 = quicksort(a, left, q - 1, depth + 1)
    a, _3, _4 = quicksort(a, q + 1, right, depth + 1)
    chks += _1
    chks += _3
    swps += _2
    swps += _4
    return a, swps, chks


if __name__ == '__main__':
    test_data = [8, 1, 7, 2, 6, 3, 5, 4]
    print(quicksort(test_data))
