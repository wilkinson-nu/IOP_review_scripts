#!/bin/bash

## If I want to pile more on later
FIRST_JOB=0
LAST_JOB=10

## Loop over these configs (max 23)
FIRST_CONFIG=0
LAST_CONFIG=23

## (Omit the last two here)

name_arr=( "T2KSK_osc_FHC_numu_H2O" "T2KSK_osc_RHC_numubar_H2O" \
           "T2KSK_osc_FHC_numubar_H2O" "T2KSK_osc_RHC_numu_H2O" \
	   "T2KND_FHC_numu_C8H8" "T2KND_RHC_numubar_C8H8" \
	   "T2KND_FHC_numu_H2O" "T2KND_RHC_numubar_H2O" \
	   "DUNEND_FHC_numu_Ar40" "DUNEND_RHC_numubar_Ar40" \
	   "DUNEFD_osc_FHC_numu_Ar40" "DUNEFD_osc_RHC_numubar_Ar40" \
	   "flat_0-10GeV_numu_H2O" "flat_0-10GeV_numubar_H2O" \
	   "flat_0-10GeV_numu_C8H8" "flat_0-10GeV_numubar_C8H8" \
	   "flat_0-10GeV_numu_Ar40" "flat_0-10GeV_numubar_Ar40" \
	   "flat_0-10GeV_nue_H2O" "flat_0-10GeV_nuebar_H2O" \
           "flat_0-10GeV_nue_C8H8" "flat_0-10GeV_nuebar_C8H8" \
           "flat_0-10GeV_nue_Ar40" "flat_0-10GeV_nuebar_Ar40" \
	   "NuMIME_FHC_numu_Ar40" "NuMIME_RHC_numubar_Ar40" )

nu_pdg_arr=( 14 -14 \
            -14  14 \
	     14 -14 \
	     14 -14 \
	     14 -14 \
	     14 -14 \
	     14 -14 \
	     14 -14 \
             14 -14 \
	     12 -12 \
	     12 -12 \
	     12 -12 \
	     14 -14 \
	   )

emin_arr=( 0.1 0.15 \
           0.15 0.1 \
           0.1 0.15 \
           0.1 0.15 \
           0.1 0.1 \
           0.1 0.1 \
           0.1 0.1 \
           0.1 0.1 \
           0.1 0.1 \
           0.1 0.1 \
           0.1 0.1 \
           0.1 0.1 \
           0.1 0.1 \
         )

emax_arr=( 10 10 \
	   10 10 \
           10 10 \
	   10 10 \
	   50 50 \
	   50 50 \
	   10 10 \
	   10 10 \
	   10 10 \
	   10 10 \
           10 10 \
           10 10 \
	   50 50 \
	 )

targ_arr=( "1000080160[0.8889],1000010010[0.1111]" "1000080160[0.8889],1000010010[0.1111]" \
           "1000080160[0.8889],1000010010[0.1111]" "1000080160[0.8889],1000010010[0.1111]" \
	   "1000060120[0.9231],1000010010[0.0769]" "1000060120[0.9231],1000010010[0.0769]" \
 	   "1000080160[0.8889],1000010010[0.1111]" "1000080160[0.8889],1000010010[0.1111]" \
	   "1000180400[1.00]" "1000180400[1.00]" \
	   "1000180400[1.00]" "1000180400[1.00]" \
	   "1000080160[0.8889],1000010010[0.1111]" "1000080160[0.8889],1000010010[0.1111]" \
           "1000060120[0.9231],1000010010[0.0769]" "1000060120[0.9231],1000010010[0.0769]" \
	   "1000180400[1.00]" "1000180400[1.00]" \
	   "1000080160[0.8889],1000010010[0.1111]" "1000080160[0.8889],1000010010[0.1111]" \
           "1000060120[0.9231],1000010010[0.0769]" "1000060120[0.9231],1000010010[0.0769]" \
           "1000180400[1.00]" "1000180400[1.00]" \
	   "1000180400[1.00]" "1000180400[1.00]" )

flux_file_arr=( "T2KSK_FHC_NuFit5NO.root" "T2KSK_RHC_NuFit5NO.root" \
		"T2KSK_FHC_NuFit5NO.root" "T2KSK_RHC_NuFit5NO.root" \
		"t2kflux_2016_plus250kA.root" "t2kflux_2016_minus250kA.root" \
		"t2kflux_2016_plus250kA.root" "t2kflux_2016_minus250kA.root" \
		"DUNE_OptimizedEngineeredNov2017_REGULAR.root" "DUNE_OptimizedEngineeredNov2017_REGULAR.root" \
		"DUNE_numu_osc_NuFit5NO.root" "DUNE_numu_osc_NuFit5NO.root" \
		"flat_flux_10GeV.root" "flat_flux_10GeV.root" \
		"flat_flux_10GeV.root" "flat_flux_10GeV.root" \
		"flat_flux_10GeV.root" "flat_flux_10GeV.root" \
		"flat_flux_10GeV.root" "flat_flux_10GeV.root" \
                "flat_flux_10GeV.root" "flat_flux_10GeV.root" \
                "flat_flux_10GeV.root" "flat_flux_10GeV.root" \
		"MINERvA_flux_ME1F.root" "MINERvA_flux_ME5ARHC.root" )

flux_hist_arr=( "sk_numu_osc" "sk_numubar_osc" \
		"sk_numubar_osc" "sk_numu_osc" \
		"enu_nd280_numu" "enu_nd280_numub" \
		"enu_nd280_numu" "enu_nd280_numub" \
		"numu_NDFHC_flux" "numubar_NDRHC_flux" \
		"numu_FDFHC_flux_osc" "numubar_FDRHC_flux_osc" \
		"flat_flux" "flat_flux" \
	        "flat_flux" "flat_flux" \
                "flat_flux" "flat_flux" \
		"flat_flux" "flat_flux" \
                "flat_flux" "flat_flux" \
                "flat_flux" "flat_flux" \
		"flux_E_cvweighted_CV_WithStatErr" "flux_E_cvweighted_CV_WithStatErr" )

## Loop over templates
for GENERATOR in GENIEv3_G18_10X_00_000 GENIEv3_G18_10a_00_000 GENIEv3_G18_10b_00_000 \
		 GENIEv3_G18_10c_00_000 GENIEv3_CRPA21_04a_00_000 GENIEv3_G21_11a_00_000 \
		 NUWRO_LFGRPA NUWRO_SF NEUT562 GENIEv3_AR23_20i_00_000
do
    for i in $(seq ${FIRST_CONFIG} ${LAST_CONFIG}); do
	
	OUTDIR="${CFS}/dune/users/cwilk/MC_IOP_review/${GENERATOR}"
	
	if [ ! -d "${OUTDIR}" ]; then
	    mkdir -p ${OUTDIR}
	fi
	
	TEMPLATE=batch_${GENERATOR}_TEMPLATE.sh

	for JOB in $(seq ${FIRST_JOB} ${LAST_JOB}); do
	    
	    printf -v PADJOB "%04d" $JOB
	    
	    OUTFILE="${name_arr[$i]}_${GENERATOR}_1M_${PADJOB}.root"
	    
	    ## Check if file has already been processed
	    if [ -f "${OUTDIR}/${OUTFILE/.root/_NUISFLAT.root}" ]; then
                continue
	    fi
	    echo "Processing ${OUTFILE}"
	    
	    ## Copy the template
	    THIS_TEMP=${TEMPLATE/_TEMPLATE/_${name_arr[$i]}_${PADJOB}}
	    cp ${TEMPLATE} ${THIS_TEMP}
	    
	    ## Set everything important...
	    sed -i "s/__THIS_SEED__/${RANDOM}/g" ${THIS_TEMP}
	    sed -i "s/__FILE_NUM__/${PADJOB}/g" ${THIS_TEMP}
	    sed -i "s/__NU_PDG__/${nu_pdg_arr[$i]}/g" ${THIS_TEMP}
	    sed -i "s/__OUTDIR__/${OUTDIR//\//\\/}/g" ${THIS_TEMP}
	    sed -i "s/__OUTFILE__/${OUTFILE}/g" ${THIS_TEMP}
	    sed -i "s/__FLUX_FILE__/${flux_file_arr[$i]}/g" ${THIS_TEMP}
	    sed -i "s/__FLUX_HIST__/${flux_hist_arr[$i]}/g" ${THIS_TEMP}
            sed -i "s/__TARG__/${targ_arr[$i]}/g" ${THIS_TEMP}
            sed -i "s/__ROOT_NAME__/${name_arr[$i]}/g" ${THIS_TEMP}
	    sed -i "s/__E_MAX__/${emax_arr[$i]}/g" ${THIS_TEMP}
            sed -i "s/__E_MIN__/${emin_arr[$i]}/g" ${THIS_TEMP}
	    echo "Submitting ${THIS_TEMP}"
	    
	    ## Submit the template
	    sbatch ${THIS_TEMP}
	    
	    ## No need to delete, so done
	    rm ${THIS_TEMP}
	done
    done
done
