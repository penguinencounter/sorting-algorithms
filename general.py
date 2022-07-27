import random
from collections import defaultdict
from time import time, sleep
import enum
import typing


def swp(l, ia, ib):
    l[ia], l[ib] = l[ib], l[ia]


def auto_time(seconds: float):
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
                print(f'generating data for size {i}, rep {str(k + 1).ljust(len(str(reps)))} of {reps}...'.ljust(80),
                      end='', flush=True)
            l = list(range(i))
            random.shuffle(l)
            datasets[i].append(l)
    endtime = time()
    print('\r', end='')
    s = round(endtime - starttime, 2)
    print(f'generated {p} datasets in {auto_time(s)}'.ljust(100))
    return datasets


def generate_edge_cases(sizes: typing.List[int],
                        quiet: typing.Optional[int] = 1,
                        disable: typing.Optional[typing.List[str]] = None):
    if disable is None:
        disable = []
    datasets = {}
    types_to_use = {
        'sorted': lambda x: list(range(x)),
        'reversed': lambda x: list(range(x))[::-1],
        'all_eq': lambda x: [1 for _ in range(x)]
    }
    for to_remove in disable:
        del types_to_use[to_remove]
    print("Generating edge cases.")
    print("Generators:")
    for k in types_to_use.keys():
        print(f"   - {k}")
    for k in disable:
        print(f"   - {k} (disabled)")

    starttime = time()
    i = 0
    for name, gen in types_to_use.items():
        datasets[name] = defaultdict(list)
        for size in sizes:
            if i % quiet == 0:
                spinner_i = (i % (4*quiet)) // quiet
                if spinner_i == 0:
                    spinner = '/'
                elif spinner_i == 1:
                    spinner = '-'
                elif spinner_i == 2:
                    spinner = '\\'
                else:
                    spinner = '|'
                print("\r", end='', flush=True)
                print(f'{spinner} {size} {name}...'.ljust(100), end='', flush=True)
            datasets[name][size].append(gen(size))
            i += 1
    endtime = time()
    s = round(endtime - starttime, 2)
    print('\r', end='')
    print(f'done, took {auto_time(s)}'.ljust(100))
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
                print(
                    f'running benchmark with size {i}, dataset {j + 1} of {len(dss)}, dataset total {o} of {len(dss) * len(datasets)}...'.ljust(
                        100), end='', flush=True)
            try:
                result, swps, chks = f(ds)
                assert result == sorted(ds)
                s.append(swps)
                c.append(chks)
            except RecursionError:
                print(f'RecursionError on size {i}, dataset {j + 1} of {len(dss)}, dataset total {o} of {len(dss) * len(datasets)}, skipping...')
        print('\r', end='', flush=True)
        print(f'processing data (size {i}, dataset {o}/{len(dss) * len(datasets)})...'.ljust(100), end='', flush=True)
        avg_swps = sum(s) / len(s) if len(s) > 0 else 0
        avg_chks = sum(c) / len(c) if len(c) > 0 else 0
        resultss[i] = avg_swps
        resultsc[i] = avg_chks
    endtime = time()
    print('\r', end='', flush=True)
    print(f'finishing up'.ljust(100), end='', flush=True)
    s = round(endtime - starttime, 2)
    print('\r', end='')
    print(f'benchmark finished in {auto_time(s)}'.ljust(100))
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


if __name__ == '__main__':
    a = list(range(128))
    b = generate_edge_cases(a)
