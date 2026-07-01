#!/bin/bash


INPUT_DIR="/pscratch/sd/c/cwilk/MC_IOP_review/\*/"
PLOT_DIR="/global/homes/c/cwilk/IOP_review_scripts/new_plots"

## List of plots I previously made sequentially
arg_sets=(
    "--input ${INPUT_DIR} --targ Ar40 --flav_num 14 --flav_den 14 --sample_num nc1pip --sample_den cc1pip --y_limits 0.0 0.4 --y_rat_limits 0.5 1.5 --output ${PLOT_DIR}"
    "--input ${INPUT_DIR} --targ O16  --flav_num 14 --flav_den 14 --sample_num nc1pip --sample_den cc1pip --y_limits 0.0 0.4 --y_rat_limits 0.5 1.5 --output ${PLOT_DIR}"
    "--input ${INPUT_DIR} --targ Ar40 --flav_num 14 --flav_den 14 --sample_num nc1pi0 --sample_den cc1pip --y_limits 0.2 0.6 --y_rat_limits 0.5 1.5 --output ${PLOT_DIR}"
    "--input ${INPUT_DIR} --targ O16  --flav_num 14 --flav_den 14 --sample_num nc1pi0 --sample_den cc1pip --y_limits 0.2 0.6 --y_rat_limits 0.5 1.5 --output ${PLOT_DIR}"
    "--input ${INPUT_DIR} --targ Ar40 --flav_num 14 --flav_den 14 --sample_num ncnpi0 --sample_den cc1pip --y_limits 0.4 2.2 --y_rat_limits 0.5 1.5 --output ${PLOT_DIR}"
    "--input ${INPUT_DIR} --targ O16  --flav_num 14 --flav_den 14 --sample_num ncnpi0 --sample_den cc1pip --y_limits 0.4 2.2 --y_rat_limits 0.5 1.5 --output ${PLOT_DIR}"
    "--input ${INPUT_DIR} --targ Ar40 --flav_num 14 --flav_den 14 --sample_num cc1pi0 --sample_den cc1pip --y_limits 0 1.0 --y_rat_limits 0.5 1.5 --output ${PLOT_DIR}"
    "--input ${INPUT_DIR} --targ O16  --flav_num 14 --flav_den 14 --sample_num cc1pi0 --sample_den cc1pip --y_limits 0 1.0 --y_rat_limits 0.5 1.5 --output ${PLOT_DIR}"
    "--input ${INPUT_DIR} --targ Ar40 --flav_num -14 --flav_den 14 --sample_num cc1pim --sample_den cc1pip --y_limits 0 0.5 --y_rat_limits 0.5 1.5 --output ${PLOT_DIR}"
    "--input ${INPUT_DIR} --targ O16  --flav_num -14 --flav_den 14 --sample_num cc1pim --sample_den cc1pip --y_limits 0 0.5 --y_rat_limits 0.5 1.5 --output ${PLOT_DIR}"
)


## Now submit them separately, one line at a time
for i in "${!arg_sets[@]}"; do
    args=${arg_sets[$i]}

    echo $args

    ## Construct a submission script
    job_script=nc_over_ccrpp_ratio_comp_script_${i}.sh
    echo "#!/bin/bash" > ${job_script}
    echo "#SBATCH --image=wilkinsonnu/nuisance_project:genie_v340" >> ${job_script}
    echo "#SBATCH --qos=shared" >> ${job_script}
    echo "#SBATCH --constraint=cpu" >> ${job_script}
    echo "#SBATCH --time=180" >> ${job_script}
    echo "#SBATCH --nodes=1" >> ${job_script}
    echo "#SBATCH --ntasks=1" >> ${job_script}
    echo "#SBATCH --mem=4GB" >> ${job_script}

    echo "shifter --entrypoint python3 make_rpp_ratio_comp.py ${args}" >> ${job_script}
    
    ## Submit and $PROFIT
    sbatch ${job_script}
    rm ${job_script}    
done

