import h5py
import numpy as np
import matplotlib.pyplot as plt
import sys
from glob import glob

def validate_hdf5(hdf5_files):

    if isinstance(hdf5_files, str):
        hdf5_files = [hdf5_files]
    hdf5_files = [f for pattern in hdf5_files for f in sorted(glob(pattern))]
    if not hdf5_files:
        raise FileNotFoundError("No files matched the given pattern(s)")

    print(hdf5_files)
    
    ## Load and concatenate across all files
    offsets_list, pdg_list, E_list = [], [], []
    ev_data = {}  # name -> list of arrays
    
    event_cursor = 0
    for path in hdf5_files:
        with h5py.File(path, "r") as f:
            ev_grp = f["events"]
            pt_grp = f["particles"]

            # Scalars
            for name in ev_grp:
                if name not in ev_data:
                    ev_data[name] = []
                ev_data[name].append(ev_grp[name][:])

            ## Particle stack — shift offsets by current particle cursor
            offsets = pt_grp["offsets"][:]
            if offsets_list:
                ## Drop the leading 0 to avoid duplicates, shift by last offset
                offsets = offsets[1:] + offsets_list[-1][-1]
            offsets_list.append(offsets)
            pdg_list.append(pt_grp["pdg"][:])
            E_list.append(pt_grp["E"][:])

    ## Concatenated objects (everything in memory)
    offsets   = np.concatenate(offsets_list)
    pdg       = np.concatenate(pdg_list)
    E         = np.concatenate(E_list)
    n_events  = len(offsets) - 1
    ev_data   = {name: np.concatenate(arrays) for name, arrays in ev_data.items()}

    ## Make scalar histograms
    for name in ev_data:
        data = ev_data[name][:]
        fig, ax = plt.subplots()
        if data.dtype == np.bool_:
            # Boolean flag: just show counts of True/False
            counts = [np.sum(~data), np.sum(data)]
            ax.bar(["False", "True"], counts)
        else:
            ax.hist(data, bins=100)
        ax.set_xlabel(name)
        ax.set_ylabel("N. Events")
        ax.set_yscale('log')
        fig.tight_layout()
        fig.savefig(f"scalar_{name}.png")
        plt.close(fig)

    ## List of pdg codes to make plots for
    PDG_CODES = {
        "2112":   lambda p: p == 2112,
        "2212":   lambda p: p == 2212,
        "211":    lambda p: np.abs(p) == 211,
        "111":    lambda p: p == 111,
    }

    ## Loop over pdg codes to check
    for label, mask_fn in PDG_CODES.items():

        ## Start with energy
        fig, axes = plt.subplots(1, 2, figsize=(4*2, 4))
        mask = mask_fn(pdg)
        axes[0].hist(E[mask], bins=100, label=label)
        axes[0].set_xlabel("E (GeV)")
        axes[0].set_ylabel("N. "+label)
        axes[0].set_yscale('log')

        ## Add multiplicity
        counts = np.zeros(n_events, dtype=np.int32)
        for i in range(n_events):
            sl = slice(offsets[i], offsets[i + 1])
            counts[i] = np.sum(mask_fn(pdg[sl]))
        axes[1].hist(counts, bins=np.arange(counts.max() + 2) - 0.5)
        axes[1].set_xlabel("N. "+label)
        axes[1].set_ylabel("N. Events")
        
        fig.tight_layout()
        fig.savefig(f"energy_multiplicity_{label}.png")
        plt.close(fig)

        
if __name__ == "__main__":
    validate_hdf5(sys.argv[1])
