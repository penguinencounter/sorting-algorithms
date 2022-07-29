import general


# MIGRATED TO NOTEBOOK
# def selection(a: list):
#     chks = 0
#     swps = 0
#     data = copy.copy(a)
#     n = len(data)
#     for i in range(n):
#         m = i
#         for j in range(i+1, n):
#             chks += 1
#             if data[m] >= data[j]:
#                 m = j
#         swps += 1
#         general.swp(data, i, m)
#     return data, swps, chks


# MIGRATED TO NOTEBOOK
# def bubble(a: list):
#     # dont use this haha lol
#     chks = 0
#     swps = 0
#     data = copy.copy(a)
#     n = len(data)
#     while 1:
#         swapped = False
#         for i in range(n-1):
#             chks += 1
#             if data[i] > data[i+1]:
#                 general.swp(data, i, i+1)
#                 swapped = True
#                 swps += 1
#         if not swapped: break
#     return data, swps, chks


# def insertion(a: list):
#     chks = 0
#     swps = 0
#     data = copy.copy(a)
#     n = len(data)
#     v = None
#     j = None
#     for x in range(1, n):
#         v = data[x]
#         j = x
#         chks += 1
#         while data[j-1] > v and j > 0:
#             j -= 1
#             chks += 1
#         swps += 1
#         data.pop(x)
#         data.insert(j, v)
#     return data, swps, chks


# def shellsort(a: list):
#     chks = 0
#     swps = 0
#     data = copy.copy(a)
#     n = len(data)
#     h = 1
#     while h <= n/9:
#         h = int(3*h + 1)
#     while h > 0:
#         for i in range(h, n):
#             v = data[i]
#             j = i
#             chks += 1
#             while data[j-h] > v and j >= h:
#                 j -= h
#                 chks += 1
#             swps += 1
#             data.pop(i)
#             data.insert(j, v)
#         h = int(h/3)
#     return data, swps, chks


if __name__ == '__main__':
    trials = int(input("how many trials? "))
    reps = int(input("how many reps? "))
    seed = input("seed or default? ")
    if seed.strip() == '':
        seed = 1234567890
    else:
        seed = int(seed)
    datasets = general.generate_testing_data(list(range(30)), reps, seed)
    swaps, checks = general.bench(shellsort, datasets)
    general.dump(general.ExportType.LIST, swaps, checks, 'results.txt')
    print('done, check results.txt')
