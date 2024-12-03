from WMCore.Configuration import Configuration
import os
config = Configuration()
config.section_("General")
config.General.requestName = 'VBF_SMEFTsim_topU3l_cdBIm'
config.General.workArea = "crab"
config.General.transferOutputs=True
config.General.transferLogs=True
config.section_("JobType")
config.JobType.scriptExe = 'setup_VBF_SMEFTsim_topU3l_cdBIm.sh'
config.JobType.pluginName = "PrivateMC"
config.JobType.psetName = "nanogen_cfg.py"
config.JobType.disableAutomaticOutputCollection = False
config.section_("Data")
config.Data.outputPrimaryDataset = 'VBF_SMEFTsim_topU3l_cdBIm'
config.Data.splitting = 'EventBased'
config.JobType.maxJobRuntimeMin = 600
config.Data.unitsPerJob = 5000
NJOBS = 200
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True
config.Data.ignoreLocality = False
config.Data.outLFNDirBase = '/store/user/jdickins/vbf-eft/el8/'
config.Data.publication = True
config.Data.outputDatasetTag = 'VBF_SMEFTsim_topU3l_cdBIm'

config.section_("Site")
config.Site.storageSite = 'T3_US_FNALLPC'
