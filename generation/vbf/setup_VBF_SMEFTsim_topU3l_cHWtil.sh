#!/bin/bash

xrdcp root://cmseos.fnal.gov//store/user/jdickins/vbf-eft/el8/VBF_SMEFTsim_topU3l_cHWtil_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz gridpack.xz

p=`pwd`
cmsDriver.py Configuration/GenProduction/python/pythia_fragment.py \
	     --python_filename nanogen_cfg.py --eventcontent NANOAODGEN \
	     --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAOD \
	     --customise_commands='process.RandomNumberGeneratorService.externalLHEProducer.initialSeed='$RANDOM'\nprocess.externalLHEProducer.args = cms.vstring("'$p'/gridpack.xz")'\
	     --fileout file:nanogen_123.root \
	     --conditions 130X_mcRun3_2023_realistic_v14 --beamspot Realistic25ns13p6TeVEarly2023Collision \
	     --step LHE,GEN,NANOGEN --geometry DB:Extended --era Run3 --no_exec --mc -n 100
#CRAB wasn't randomizing the seed, so using $RANDOM now

# Add weights to cfg file
echo "named_weights = [" >> nanogen_cfg.py
tar xf ttgamma_gridpack.xz InputCards
cat InputCards/*reweight_card.dat | grep launch | sed 's/launch --rwgt_name=/"/' | sed 's/$/",/' >> nanogen_cfg.py
echo -e "]\nprocess.genWeightsTable.namedWeightIDs = named_weights\nprocess.genWeightsTable.namedWeightLabels = named_weights" >> nanogen_cfg.py

cmsRun -j FrameworkJobReport.xml nanogen_cfg.py
