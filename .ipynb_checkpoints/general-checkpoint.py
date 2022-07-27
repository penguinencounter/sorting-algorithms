import random
from time import time
import enum
import typing


def swp(l, ia, ib):
    l[ia], l[ib] = l[ib], l[ia]


def auto_time(seconds: int):
    result_hours = 0
    result_minutes = 0
    result_seconds = seconds
    if seconds >= 60:
        result_minutes = seconds // 60
        result_seconds %= 60
    if result_minutes >= 60:
        result_hours = result_minutes // 60
        result_minutes %= 60
    result = ''
    if result_hours > 0:
        result += f'{int(result_hours)}h '
    if result_minutes > 0:
        result += f'{int(result_minutes)}m '
    result += f'{round(result_seconds, 2)}s'
    return result


def generate_testing_data(sizes: typing.List[int], reps: int = 1, SEED: int = 1234567890, quiet=1):
    datasets = {}
    random.seed(SEED)
    print("Generating testing data. This may take a while.")
    print(f"Need to generate {len(sizes) * reps} total datasets")
    starttime = time()
    p = 0
    for i in sizes:
        datasets[i] = []
        for k in range(reps):
            p += 1
            if p % quiet == 0:
                print('\r', end='', flush=True)
                print(f'generating data for size {i}, rep {str(k+1).ljust(len(str(reps)))} of {reps}...'.ljust(80), end='', flush=True)
            l = list(range(i))
            random.shuffle(l)
            datasets[i].append(l)
    endtime = time()
    print('\r', end='')
    s = round(endtime - starttime, 2)
    print(f'generated {p} datasets in {auto_time(s)}'.ljust(100))
    return datasets


def bench(f, datasets: typing.Dict[int, typing.List[typing.List[int]]], quiet=1):
    resultss = {}
    resultsc = {}
    starttime = time()
    print("Running benchmark.")
    print(f"Need to run on {len(datasets) * len(datasets[0])} total datasets")
    o = 0
    for i, dss in datasets.items():
        s = []
        c = []
        for j, ds in enumerate(dss):
            o += 1
            if o % quiet == 0:
                print('\r', end='', flush=True)
                print(f'running benchmark with size {i}, dataset {j+1} of {len(dss)}, dataset total {o} of {len(dss)*len(datasets)}...'.ljust(100), end='', flush=True)
            result, swps, chks = f(ds)
            assert result == sorted(ds)
            s.append(swps)
            c.append(chks)
        avg_swps = sum(s) / len(s)
        avg_chks = sum(c) / len(c)
        resultss[i] = avg_swps
        resultsc[i] = avg_chks
    endtime = time()
    print('\r', end='')
    s = round(endtime - starttime, 2)
    print(f'benchmark finished in {auto_time(s)} seconds'.ljust(100))
    return resultss, resultsc


class ExportType(enum.Enum):
    LIST = 1
    DESMOS = 2


def dump(method: ExportType, swps: dict, chks: dict, fp: str = 'results.txt'):
    with open(fp, 'w') as f:
        if method == ExportType.LIST:
            f.write(str(list(swps.values())))
            f.write('\n')
            f.write(str(list(chks.values())))
            f.write('\n')
        elif method == ExportType.DESMOS:
            f.write(f'S_{"{waps}"}={list(swps.values())}\n')
            f.write(f'C_{"{hecks}"}={list(chks.values())}\n')
            f.write(f'S_{"{ize}"}={list(swps.keys())}\n')
            f.write('(S_{ize},S_{waps})\n(S_{ize},C_{hecks})\n')
