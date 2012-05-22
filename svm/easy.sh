#!/bin/bash
#This is a script that provide easy method to generate predict script

#gernerate train data by even line
cat DNA.A | awk '{if (NR % 2 == 0) print $0}' | ./feature.py 1 > .train.tmp
cat DNA.B | awk '{if (NR % 2 == 0) print $0}' | ./feature.py -1 >> .train.tmp

#gernerate test data by odd line
cat DNA.A | awk '{if (NR % 2 == 1) print $0}' | ./feature.py 1 > .test.tmp
cat DNA.B | awk '{if (NR % 2 == 1) print $0}' | ./feature.py -1 >> .test.tmp

#scale all data by [0, 1]
./scale.py .train.tmp > .train.scale.tmp
./scale.py .test.tmp  > .test.scale.tmp

#train sample data
./train.py .train.scale.tmp > train.model
cat train.model

#predict known test data
echo 
echo '>>>>>known data result<<<<<'
echo 
./predict.py train.model -k .test.scale.tmp

#predict unknown test data
echo 
echo '>>>>>unknown data result<<<<<'
echo 
./feature.py 0 DNA.none > .none.tmp
./scale.py .none.tmp > .none.scale.tmp
./predict.py train.model .none.scale.tmp
