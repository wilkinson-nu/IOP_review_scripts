#!/bin/bash


INPUT_DIR="/pscratch/sd/c/cwilk/MC_IOP_review/\*/"
PLOT_DIR="/global/homes/c/cwilk/IOP_review_scripts/new_plots"

## List of plots I previously made sequentially
arg_sets=(
    "--input ${INPUT_DIR} --targ Ar40 --sample ccinc --output ${PLOT_DIR}"
    "--input ${INPUT_DIR} --targ O16 --sample cc0pi --output ${PLOT_DIR}"
    "--input ${INPUT_DIR} --targ O16 --sample ccinc --output ${PLOT_DIR}"
)


## Now submit them separately, one line at a time
for i in "${!arg_sets[@]}"; do
    args=${arg_sets[$i]}

    echo $args

    ## Construct a submission script
    job_script=double_ratio_comp_script_${i}.sh
    echo "#!/bin/bash" > ${job_script}
    echo "#SBATCH --image=wilkinsonnu/nuisance_project:genie_v340" >> ${job_script}
    echo "#SBATCH --qos=shared" >> ${job_script}
    echo "#SBATCH --constraint=cpu" >> ${job_script}
    echo "#SBATCH --time=240" >> ${job_script}
    echo "#SBATCH --nodes=1" >> ${job_script}
    echo "#SBATCH --ntasks=1" >> ${job_script}
    echo "#SBATCH --mem=4GB" >> ${job_script}

    echo "shifter --entrypoint python3 make_double_ratio_comp.py ${args}" >> ${job_script}
    
    ## Submit and $PROFIT
    sbatch ${job_script}
    rm ${job_script}    
done

