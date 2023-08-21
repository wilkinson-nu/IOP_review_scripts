#!/bin/bash
#SBATCH --image=docker:wilkinsonnu/nuisance_project:gibuu_2021
#SBATCH --qos=shared
#SBATCH --constraint=cpu
#SBATCH --time=1200
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=4GB

## These change for each job
THIS_SEED=__THIS_SEED__
FILE_NUM=__FILE_NUM__
outDir=__THIS_OUTDIR__
nuType=__THIS_FLAV__

## Place for storing common inputs
inDir=${PWD}/MC_inputs
inCard=dune_Ar40_${nuType}_GiBUU.job

## Output file name
outFile="dune_Ar40_${nuType}_GiBUU_1M_${FILE_NUM}.root"

## Fluxfile
fluxFile=dune_numu_NDFHC_flux.dat; if [[ "$nuType" == "-14" || "$nuType" == "-12" ]]; then fluxFile=dune_numubar_NDRHC_flux.dat; fi;

## Where to temporarily save files
tempDir=${SCRATCH}/${outFile/.root/}_${THIS_SEED}

echo "Moving to SCRATCH: ${tempDir}"
mkdir ${tempDir}
cd ${tempDir}

## Sort out the inputs
cp ${inDir}/${fluxFile} .
cp ${inDir}/${inCard} .
sed -i "s/_THIS_SEED_/${THIS_SEED}/g" ${inCard}
sed -i "s/_THIS_FLUX_FILE_/${fluxFile}/g" ${inCard}

## No option to change the GiBUU output file name...
shifter -V ${PWD}:/output --entrypoint /opt/generators/GiBUU/GiBUU.x < ${inCard}
shifter -V ${PWD}:/output --entrypoint PrepareGiBUU -i EventOutput.Pert.00000001.root -f ${fluxFile} -o ${outFile}
shifter -V ${PWD}:/output --entrypoint nuisflat -f GenericVectors -i GiBUU:${outFile} -o ${outFile/.root/_NUISFLAT.root} -q "nuisflat_SaveSignalFlags=false"
echo "Complete"

## Copy back the important files
cp ${tempDir}/${outFile} ${outDir}/.
cp ${tempDir}/${outFile/.root/_NUISFLAT.root} ${outDir}/.

## Clean up
rm -r ${tempDir}
