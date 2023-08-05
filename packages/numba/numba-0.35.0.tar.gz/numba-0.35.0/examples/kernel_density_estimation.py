from numba import njit, prange
import numpy as np
import argparse
import time

@njit(parallel=True)
def kde(X):
    b = 0.5
    points = np.array([-1.0, 2.0, 5.0])
    N = points.shape[0]
    n = X.shape[0]
    exps = 0
    for i in prange(n):
        p = X[i]
        d = (-(p-points)**2)/(2*b**2)
        m = np.min(d)
        exps += m-np.log(b*N)+np.log(np.sum(np.exp(d-m)))
    return exps

def main():
    parser = argparse.ArgumentParser(description='Kernel-Density')
    parser.add_argument('--size', dest='size', type=int, default=1000000)
    args = parser.parse_args()
    size = args.size

    kde(np.random.ranf(10))
    print("size:", size)
    X = np.random.ranf(size)
    t1 = time.time()
    res = kde(X)
    t = time.time()-t1
    print("checksum:", res)
    print("SELFTIMED:", t)

if __name__ == '__main__':
    main()
