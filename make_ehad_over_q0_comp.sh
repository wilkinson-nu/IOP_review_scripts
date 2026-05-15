#!/bin/bash


INPUT_DIR="/pscratch/sd/c/cwilk/MC_IOP_review/\*/"
PLOT_DIR="/global/homes/c/cwilk/IOP_review_scripts/new_plots"

## List of plots I previously made sequentially
arg_sets=(
    "--input ${INPUT_DIR} --det=T2K --flux=FHC_numu --targ=H2O --output ${PLOT_DIR}"
    "--input ${INPUT_DIR} --det=T2K --flux=RHC_numubar --targ=H2O --output ${PLOT_DIR}"
    "--input ${INPUT_DIR} --det=DUNE --flux=FHC_numu --targ=Ar40 --output ${PLOT_DIR}"
    "--input ${INPUT_DIR} --det=DUNE --flux=RHC_numubar --targ=Ar40 --output ${PLOT_DIR}"
)


## Now submit them separately, one line at a time
for i in "${!arg_sets[@]}"; do
    args=${arg_sets[$i]}

    echo $args

    ## Construct a submission script
    job_script=ehad_over_q0_comp_script_${i}.sh
    echo "#!/bin/bash" > ${job_script}
    echo "#SBATCH --image=wilkinsonnu/nuisance_project:genie_v340" >> ${job_script}
    echo "#SBATCH --qos=shared" >> ${job_script}
    echo "#SBATCH --constraint=cpu" >> ${job_script}
    echo "#SBATCH --time=180" >> ${job_script}
    echo "#SBATCH --nodes=1" >> ${job_script}
    echo "#SBATCH --ntasks=1" >> ${job_script}
    echo "#SBATCH --mem=4GB" >> ${job_script}

    echo "shifter --entrypoint python3 make_ehad_over_q0_comp.py ${args}" >> ${job_script}
    
    ## Submit and $PROFIT
    sbatch ${job_script}
    rm ${job_script}    
done

