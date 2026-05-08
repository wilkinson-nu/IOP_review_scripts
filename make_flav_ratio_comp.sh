#!/bin/bash


INPUT_DIR="/pscratch/sd/c/cwilk/MC_IOP_review/\*/"
PLOT_DIR="/global/homes/c/cwilk/IOP_review_scripts/new_plots"

## List of plots I previously made sequentially
arg_sets=(
    "--input ${INPUT_DIR} --flav1 12 --flav2 14 --targ Ar40 --sample ccinc --y_limits 1 1.9 --y_rat_limits 0.75 1.15 --leg_dim 0.65 0.51 0.93 0.90 --lowe 1 --output ${PLOT_DIR}"
    "--input ${INPUT_DIR} --flav1 -12 --flav2 -14 --targ Ar40 --sample ccinc --y_limits 1 1.9 --y_rat_limits 0.75 1.15 --leg_dim 0.65 0.51 0.93 0.90 --lowe 1 --output ${PLOT_DIR}"
    ## "--input ${INPUT_DIR} --flav1 -12 --flav2 12 --targ Ar40 --sample ccinc --y_limits 0 0.65 --y_rat_limits 0.75 1.5 --leg_dim 0.65 0.06 0.93 0.45 --output ${PLOT_DIR}"
    ## "--input ${INPUT_DIR} --flav1 -14 --flav2 14 --targ Ar40 --sample ccinc --y_limits 0 0.65 --y_rat_limits 0.75 1.5 --leg_dim 0.65 0.06 0.93 0.45 --output ${PLOT_DIR}"
    "--input ${INPUT_DIR} --flav1 12 --flav2 14 --targ O16 --sample cc0pi --y_limits 1 1.9 --y_rat_limits 0.75 1.15 --leg_dim 0.65 0.51 0.93 0.90 --lowe 1 --output ${PLOT_DIR}"
    "--input ${INPUT_DIR} --flav1 -12 --flav2 -14 --targ O16 --sample cc0pi --y_limits 1 1.9 --y_rat_limits 0.75 1.15 --leg_dim 0.65 0.51 0.93 0.90 --lowe 1 --output ${PLOT_DIR}"
    ## "--input ${INPUT_DIR} --flav1 -12 --flav2 12 --targ O16 --sample cc0pi --y_limits 0 0.85 --y_rat_limits 0.75 1.5 --leg_dim 0.65 0.06 0.93 0.45 --output ${PLOT_DIR}"
    ## "--input ${INPUT_DIR} --flav1 -14 --flav2 14 --targ O16 --sample cc0pi --y_limits 0 0.85 --y_rat_limits 0.75 1.5 --leg_dim 0.65 0.06 0.93 0.45 --output ${PLOT_DIR}"
)


## Now submit them separately, one line at a time
for i in "${!arg_sets[@]}"; do
    args=${arg_sets[$i]}

    echo $args

    ## Construct a submission script
    job_script=flav_ratio_comp_script_${i}.sh
    echo "#!/bin/bash" > ${job_script}
    echo "#SBATCH --image=wilkinsonnu/nuisance_project:genie_v340" >> ${job_script}
    echo "#SBATCH --qos=shared" >> ${job_script}
    echo "#SBATCH --constraint=cpu" >> ${job_script}
    echo "#SBATCH --time=120" >> ${job_script}
    echo "#SBATCH --nodes=1" >> ${job_script}
    echo "#SBATCH --ntasks=1" >> ${job_script}
    echo "#SBATCH --mem=4GB" >> ${job_script}

    echo "shifter --entrypoint python3 make_flav_ratio_comp.py ${args}" >> ${job_script}
    
    ## Submit and $PROFIT
    sbatch ${job_script}
    rm ${job_script}    
done

