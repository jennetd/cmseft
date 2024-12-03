samplename=$1

cp crab_submit_TEMPLATE.py crab_submit_${samplename}.py
sed -i -e 's/TEMPLATE/'${samplename}'/g' crab_submit_${samplename}.py

cp setup_TEMPLATE.sh setup_${samplename}.sh
sed -i -e 's/TEMPLATE/'${samplename}'/g' setup_${samplename}.sh

crab submit crab_submit_${samplename}.py
