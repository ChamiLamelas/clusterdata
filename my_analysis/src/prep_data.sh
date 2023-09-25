#!/bin/bash

#
# Takes < 10 minutes total
#

cd ../../cluster-trace-gpu-v2020/data/
bash download_data.sh
mv *.tar.gz ../../my_analysis
cd ../../my_analysis
mkdir data
mv *.tar.gz data
cd data
for i in *.tar.gz; do tar -zxvf "$i" ;done
rm *.tar.gz

