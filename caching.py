import os
import pickle

PREPPED = False


def prep():
    global PREPPED
    PREPPED = True
    if not os.path.exists(".run_cache"):
        os.mkdir(".run_cache")


def _rp():
    if not PREPPED:
        raise RuntimeError("You must call prep() before using the rest of this module.")


def update_required(f_name, seed):
    _rp()
    return not os.path.exists(f'.run_cache/{f_name}_{seed}.pkl')


def save(f_name, seed, data):
    _rp()
    with open(f'.run_cache/{f_name}_{seed}.pkl', 'wb') as f:
        pickle.dump(data, f)


def load_previous(f_name, seed):
    _rp()
    with open(f'.run_cache/{f_name}_{seed}.pkl', 'rb') as f:
        return pickle.load(f)
