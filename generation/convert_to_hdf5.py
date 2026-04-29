import uproot
import h5py
import numpy as np
import awkward as ak
import sys
from glob import glob

SCALAR_BRANCHES = {
    "Mode":         ("mode",    np.int32  ),
    "PDGnu":        ("pdg_nu",  np.int32  ),
    "tgt":          ("pdg_tgt", np.int32  ),
    "Enu_true":     ("Enu",     np.float32),
    "W":            ("W",       np.float32),
    "Q2":           ("Q2",      np.float32),
    "q0":           ("q0",      np.float32),
    "q3":           ("q3",      np.float32),
    "cc":           ("cc",      np.bool_  ),
    "fScaleFactor": ("wgt",     np.float32),
    "nfsp":         ("nfsp",    np.int32  ),
}

VLEN_BRANCHES = {
    "px":  ("px",  np.float32),
    "py":  ("py",  np.float32),
    "pz":  ("pz",  np.float32),
    "E":   ("E",   np.float32),
    "pdg": ("pdg", np.int32  ),
}


def convert_flattrees_to_hdf5(root_files,
                              hdf5_file,
                              tree_name="FlatTree_VARS"):
    if isinstance(root_files, str):
        root_files = [root_files]
    root_files = [f for pattern in root_files for f in sorted(glob(pattern))]
    if not root_files:
        raise FileNotFoundError("No files matched the given pattern(s)")

    print(f"Converting {len(root_files)} file(s)...")

    # --- First pass: read all data ---
    all_scalar_data = {root_name: [] for root_name in SCALAR_BRANCHES}
    all_vlen_data   = {root_name: [] for root_name in VLEN_BRANCHES}
    file_metadata   = []
    event_cursor    = 0
    particle_cursor = 0

    for path in root_files:
        with uproot.open(path) as f:
            tree = f[tree_name]
            n_events = tree.num_entries

            scalar_data = tree.arrays(list(SCALAR_BRANCHES.keys()), library="np")
            vlen_data   = tree.arrays(list(VLEN_BRANCHES.keys()), library="ak")
            nfsp        = scalar_data["nfsp"]
            n_particles = int(nfsp.sum())

            ## Unpick the per file normalization in the NUISANCE default
            scalar_data["fScaleFactor"] = (
                scalar_data["fScaleFactor"] * 1e38 * n_events
            )

            for root_name in SCALAR_BRANCHES:
                all_scalar_data[root_name].append(scalar_data[root_name])
            for root_name in VLEN_BRANCHES:
                all_vlen_data[root_name].append(vlen_data[root_name])
            
            file_metadata.append({
                "source_file":    path,
                "n_events":       n_events,
                "n_particles":    n_particles,
                "event_start":    event_cursor,
                "particle_start": particle_cursor,
            })
            event_cursor    += n_events
            particle_cursor += n_particles
            print(f"  Read {path}: {n_events} events, {n_particles} particles")

    # --- Concatenate ---
    scalar_data = {k: np.concatenate(v) for k, v in all_scalar_data.items()}
    vlen_data   = {k: ak.concatenate(v) for k, v in all_vlen_data.items()}
    nfsp        = scalar_data["nfsp"]
    n_events    = len(nfsp)
    n_particles = int(nfsp.sum())
    print(f"Total: {n_events} events, {n_particles} particles")

    # --- Write ---
    with h5py.File(hdf5_file, "w") as hf:

        # Top-level metadata
        hf.attrs["n_events"]    = n_events
        hf.attrs["n_particles"] = n_particles
        hf.attrs["tree_name"]   = tree_name
        hf.attrs["n_sources"]   = len(root_files)

        # Per-file metadata as a group of datasets
        meta_grp = hf.create_group("sources")
        meta_grp.create_dataset("source_file",    data=np.array([m["source_file"]    for m in file_metadata], dtype=h5py.string_dtype()))
        meta_grp.create_dataset("n_events",       data=np.array([m["n_events"]       for m in file_metadata], dtype=np.int64))
        meta_grp.create_dataset("n_particles",    data=np.array([m["n_particles"]    for m in file_metadata], dtype=np.int64))
        meta_grp.create_dataset("event_start",    data=np.array([m["event_start"]    for m in file_metadata], dtype=np.int64))
        meta_grp.create_dataset("particle_start", data=np.array([m["particle_start"] for m in file_metadata], dtype=np.int64))

        # Scalar events
        ev_grp = hf.create_group("events")
        for root_name, (hdf5_name, dtype) in SCALAR_BRANCHES.items():
            data = scalar_data[root_name]
            ev_grp.create_dataset(
                hdf5_name,
                data=data.astype(dtype),
                compression="gzip",
                compression_opts=4,
            )

        # Particle stack
        pt_grp = hf.create_group("particles")
        pt_grp.attrs["description"] = "Flat concatenated stack; use offsets to index events"

        offsets = np.concatenate([[0], np.cumsum(nfsp)]).astype(np.int64)
        pt_grp.create_dataset("offsets", data=offsets, compression="gzip")

        for root_name, (hdf5_name, dtype) in VLEN_BRANCHES.items():
            data = ak.to_numpy(ak.flatten(vlen_data[root_name]))
            pt_grp.create_dataset(
                hdf5_name,
                data=data.astype(dtype),
                compression="gzip",
                compression_opts=4,
            )

    print(f"Written to {hdf5_file}")


if __name__ == "__main__":
    convert_flattrees_to_hdf5(sys.argv[1:-1], sys.argv[-1])    

