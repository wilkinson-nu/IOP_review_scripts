import uproot
import h5py
import numpy as np
import awkward as ak
import sys

def convert_flattree_to_hdf5(root_file,
                             hdf5_file,
                             tree_name="FlatTree_VARS", 
                             chunk_size=10000):

    with uproot.open(root_file) as f:
        tree = f[tree_name]
        
        ## Scalar branches (one value per event)
        ## Some of these are mostly per file (fScaleFactor --> wgt, PDGnu, tgt --> PDGtgt), but not always, so has to be per event
        ## fScaleFactor is dangerous because this is often < 1E-39 and needs double precision. Solve by multiplying by a constant number
        ## Strictly speaking, nfsp isn't needed here because it's saved in offsets. The others all have the same length
        SCALAR_BRANCHES = {
            "Mode":         ("mode",    np.int32,    None),
            "PDGnu":        ("pdg_nu",  np.int32,    None),
            "tgt":          ("pdg_tgt", np.int32,    None),
            "Enu_true":     ("Enu",     np.float32,  None),
            "W":            ("W",       np.float32,  None),
            "Q2":           ("Q2",      np.float32,  None),
            "q0":           ("q0",      np.float32,  None),
            "q3":           ("q3",      np.float32,  None),
            "cc":           ("cc",      np.bool_,    None),
            "fScaleFactor": ("wgt",     np.float32, lambda x: x * 1e38),
            "nfsp":         ("nfsp",    np.int32,    None),
        }

        ## Variable-length branches (particle stacks)
        VLEN_BRANCHES = {
            "px":           ("px",      np.float32,  None),
            "py":           ("py",      np.float32,  None),
            "pz":           ("pz",      np.float32,  None),            
            "E":            ("E",       np.float32,  None),
            "pdg":          ("pdg",     np.int32,    None),
        }
        
        n_events = tree.num_entries
        print(f"Converting {n_events} events...")
        
        with h5py.File(hdf5_file, "w") as hf:
            ev_grp = hf.create_group("events")
            
            scalar_data = tree.arrays(list(SCALAR_BRANCHES.keys()), library="np")
            
            for root_name, (hdf5_name, dtype, transform) in SCALAR_BRANCHES.items():
                data = ak.to_numpy(scalar_data[root_name])
                if transform is not None:
                    data = transform(data)
                ev_grp.create_dataset(
                    hdf5_name,
                    data=data.astype(dtype),
                    compression="gzip",
                    compression_opts=4,
                )
            
            ## Store variable-length particle stack
            _convert_particle_stack(tree, hf, VLEN_BRANCHES, n_events, chunk_size)
            
            ## Include metadata
            ## Could include more info about how the file was produced, but it's not in the NUISANCE files
            hf.attrs["source_file"] = root_file
            hf.attrs["n_events"] = n_events
            hf.attrs["tree_name"] = tree_name

        print(f"Written to {hdf5_file}")

        
def _convert_particle_stack(tree, hf, VLEN_BRANCHES, n_events, chunk_size):
    nfsp = tree["nfsp"].array(library="np")
    arrays = tree.arrays(list(VLEN_BRANCHES.keys()), library="ak")

    flat_grp = hf.create_group("particles")
    flat_grp.attrs["description"] = "Flat concatenated stack; use offsets to index events"

    offsets = np.concatenate([[0], np.cumsum(nfsp)]).astype(np.int64)
    flat_grp.create_dataset("offsets", data=offsets, compression="gzip")

    for root_name, (hdf5_name, dtype, transform) in VLEN_BRANCHES.items():
        data = ak.to_numpy(ak.flatten(arrays[root_name]))
        if transform is not None:
            data = transform(data)
        flat_grp.create_dataset(
            hdf5_name,
            data=data.astype(dtype),
            compression="gzip",
            compression_opts=4,
        )

        
if __name__ == "__main__":
    convert_flattree_to_hdf5(sys.argv[1], sys.argv[2])
