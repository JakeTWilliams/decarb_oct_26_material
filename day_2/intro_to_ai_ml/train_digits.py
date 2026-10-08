"""Hyperparameter search for a small neural network, run as a batch job.

The same grid search runs twice: first on 1 CPU core, then on every core
Slurm allocated to the job. A grid search is embarrassingly parallel (every
combination is an independent fit), so the search itself speeds up almost
linearly. Starting the parallel worker processes has a fixed cost, which is
timed separately.

Usage (normally via train_digits.slurm):
    python train_digits.py --n-jobs 16
"""

import argparse
import itertools
import os
import time
import warnings

import pandas as pd
from joblib import Parallel, delayed
from sklearn.datasets import load_digits
from sklearn.exceptions import ConvergenceWarning
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.neural_network import MLPClassifier

PARAM_GRID = {
    "hidden_layer_sizes": [(32,), (64,), (128,), (64, 64)],
    "alpha": [1e-4, 1e-2, 1.0],
    "learning_rate_init": [1e-3, 1e-2],
}


def _import_in_worker():
    import sklearn.neural_network  # noqa: F401  (the import is the point)
    return os.getpid()


def start_workers(n_jobs):
    """Start the worker processes. Each one imports NumPy, SciPy and scikit-learn,
    which takes seconds when the software lives on a shared file system.
    The grid search afterwards reuses these workers."""
    start = time.perf_counter()
    Parallel(n_jobs=n_jobs)(delayed(_import_in_worker)() for _ in range(n_jobs))
    return time.perf_counter() - start


def search(X, y, n_jobs):
    grid = GridSearchCV(
        MLPClassifier(max_iter=200, random_state=0),
        PARAM_GRID,
        cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=0),
        n_jobs=n_jobs,
    )
    start = time.perf_counter()
    grid.fit(X, y)
    return grid, time.perf_counter() - start


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--n-jobs", type=int, default=int(os.environ.get("SLURM_CPUS_PER_TASK", 1)))
    args = parser.parse_args()

    # Some small configurations stop at max_iter before converging; that is expected here.
    warnings.filterwarnings("ignore", category=ConvergenceWarning)
    os.environ["PYTHONWARNINGS"] = "ignore::UserWarning"  # the same for worker processes (ConvergenceWarning is a UserWarning)

    digits = load_digits()
    X_train, X_test, y_train, y_test = train_test_split(
        digits.data / 16.0, digits.target, test_size=0.25, stratify=digits.target, random_state=0
    )
    n_fits = 5 * len(list(itertools.product(*PARAM_GRID.values())))
    print(f"host {os.uname().nodename}: {n_fits} model fits per search\n")

    n = args.n_jobs
    _, t_serial = search(X_train, y_train, n_jobs=1)
    print(f"search on  1 core           : {t_serial:6.1f} s")
    t_start = start_workers(n)
    print(f"starting {n:>2} worker processes: {t_start:6.1f} s")
    grid, t_parallel = search(X_train, y_train, n_jobs=n)
    print(f"search on {n:>2} cores          : {t_parallel:6.1f} s")
    print(f"speed-up of the search      : {t_serial / t_parallel:6.1f}x")
    print(f"speed-up including start-up : {t_serial / (t_start + t_parallel):6.1f}x\n")

    results = pd.DataFrame(grid.cv_results_)
    table = results[["param_hidden_layer_sizes", "param_alpha", "param_learning_rate_init",
                     "mean_test_score", "std_test_score"]].sort_values("mean_test_score", ascending=False)
    print("top 5 configurations (5-fold cross-validation accuracy):")
    print(table.head().to_string(index=False), "\n")
    print("best hyperparameters:", grid.best_params_)
    print(f"test accuracy of the best model: {grid.score(X_test, y_test):.3f}")

    out = f"digits_search_{os.environ.get('SLURM_JOB_ID', 'local')}.csv"
    table.to_csv(out, index=False)
    print(f"full results written to {out}")


if __name__ == "__main__":
    main()
