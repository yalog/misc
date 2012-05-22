#!/bin/bash
#This is a script that provide easy method to generate predict script

#gernerate train data by even line
cat DNA.A | awk '{if (NR % 2 == 0) print $0}' | ./feature.py 1 > train.tmp
cat DNA.B | awk '{if (NR % 2 == 0) print $0}' | ./feature.py -1 >> train.tmp

#gernerate test data by odd line
cat DNA.A | awk '{if (NR % 2 == 1) print $0}' | ./feature.py 1 > test.tmp
cat DNA.B | awk '{if (NR % 2 == 1) print $0}' | ./feature.py -1 >> test.tmp

#scale all data by [0, 1]
./scale.py train.tmp > train.scale.tmp
./scale.py train.tmp > test.scale.tmp
