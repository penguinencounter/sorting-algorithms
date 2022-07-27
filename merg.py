import general


# migrated
def merge(a: list, b: list):
    result = []
    checks = 0
    swaps = 0
    while len(a) > 0 and len(b) > 0:
        checks += 1
        if a[0] < b[0]:
            result.append(a.pop(0))
        else:
            result.append(b.pop(0))
        swaps += 1

    # Consume rest
    while len(a) > 0:
        result.append(a.pop(0))
        swaps += 1
    while len(b) > 0:
        result.append(b.pop(0))
        swaps += 1
    return result, checks, swaps


def mergesort(m: list):
    if len(m) <= 1:
        return m, 0, 0

    left = []
    right = []
    for i, x in enumerate(m):
        if i < len(m) // 2:
            left.append(x)
        else:
            right.append(x)

    left, c1, s1 = mergesort(left)
    right, c2, s2 = mergesort(right)

    r, c3, s3 = merge(left, right)

    checks = c1 + c2 + c3
    swaps = s1 + s2 + s3
    return r, checks, swaps


if __name__ == '__main__':
    trials = int(input("how many trials? "))
    reps = int(input("how many reps? "))
    seed = input("seed or default? ")
    if seed.strip() == '':
        seed = 1234567890
    else:
        seed = int(seed)
    datasets = general.generate_testing_data(list(range(30)), reps, seed)
    swaps, checks = general.bench(mergesort, datasets)
    general.dump(general.ExportType.LIST, swaps, checks, 'results.txt')
    print('done, check results.txt')
