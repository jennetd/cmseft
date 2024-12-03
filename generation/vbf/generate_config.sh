cmsDriver.py Configuration/GenProduction/python/pythia_fragment.py \
    --python_filename nanogen_cfg.py --eventcontent NANOAODGEN \
    --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAOD     --customise_commands "process.RandomNumberGeneratorService.externalLHEProducer.initialSeed=123" \
    --fileout file:nanogen_123.root --conditions 102X_upgrade2018_realistic_v15 \
    --beamspot Realistic25ns13TeVEarly2018Collision \
    --step LHE,GEN,NANOGEN --geometry DB:Extended --era Run2_2018 --no_exec --mc -n 100
