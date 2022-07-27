from matplotlib import pyplot as plt

import basic_sorts
import quick
from merg import mergesort
import general
from caching import update_required, prep, save, load_previous
prep()

SEED = 2
REPS = 16

def size_provider():
    yield 0  # required for benchmark to determine total size of datasets
    i = 1
    while 1:
        yield round(i)
        i *= 4/3
        if i > 10000:
            break

datasets = general.generate_testing_data(list(size_provider()), REPS, SEED, quiet=2)
edges = general.generate_edge_cases(list(size_provider()), quiet=2)

results = {}
edge_results = {}

def autorun_or_cache(f, fname, datasets, seed, quiet=1):
    if update_required(fname, seed):
        print(f'Cache missed for {fname}')
        result = general.bench(f, datasets, quiet=quiet)
        save(fname, seed, result)
        print(f'Saved {fname} to cache')
        return result
    else:
        print(f'Cache hit for {fname}')
        print(f'Retrieving {fname} from cache')
        return load_previous(fname, seed)

def run_edge_cases(f, fname, edges, seed, quiet=1):
    result = {}
    for k, v in edges.items():
        result[k] = autorun_or_cache(f, fname + "_edge_" + k, v, seed, quiet)
    print("Done!")
    return result

results['quicksort'] = autorun_or_cache(quick.quicksort, "quicksort", datasets, SEED, quiet=2)
edge_results['quicksort'] = run_edge_cases(quick.quicksort, "quicksort", edges, SEED, quiet=2)

fig, ax = plt.subplots()
ax.set_title("Quick Sort")
