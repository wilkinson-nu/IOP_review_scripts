import h5py
import numpy as np
import sys

def report_sizes(hdf5_file):
    with h5py.File(hdf5_file, "r") as f:
        total_compressed   = 0
        total_uncompressed = 0

        def visitor(name, obj):
            if isinstance(obj, h5py.Dataset):
                compressed   = obj.id.get_storage_size()
                uncompressed = obj.dtype.itemsize * np.prod(obj.shape)
                print(f"{name:<40} {uncompressed/1e6:8.2f} MB  ->  {compressed/1e6:8.2f} MB  ({100*compressed/uncompressed:.1f}%)")
                nonlocal total_compressed, total_uncompressed
                total_compressed   += compressed
                total_uncompressed += uncompressed

        f.visititems(visitor)
        print("-" * 75)
        print(f"{'TOTAL':<40} {total_uncompressed/1e6:8.2f} MB  ->  {total_compressed/1e6:8.2f} MB  ({100*total_compressed/total_uncompressed:.1f}%)")

if __name__ == "__main__":
    report_sizes(sys.argv[1])
