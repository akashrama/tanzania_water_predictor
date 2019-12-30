#!/bin/bash

echo "Start downloading data and documentation"

# bash function used to retrieve the absolute file path of a file as a string
# note: thank you to peterh's answer on SO 
#       https://stackoverflow.com/a/21188136
get_str_abs_filename() {
  # $1 : relative filename
  echo "'$(cd "$(dirname "$1")" && pwd)/$(basename "$1")'"
}

# download the Submission Format .csv file 
wget -P data/raw/ https://s3.amazonaws.com/drivendata/data/7/public/SubmissionFormat.csv

# download the the independent variables that need predictions (test set)
wget -P data/raw/ https://s3.amazonaws.com/drivendata/data/7/public/702ddfc5-68cd-4d1d-a0de-f5f566f76d91.csv

# download the dependent variable (status_group) for each of the rows in training set values (training set labels)
wget -P data/raw/ https://s3.amazonaws.com/drivendata/data/7/public/0bf8bc6e-30d0-4c50-956a-603fc693d966.csv

# download the independent variables for the training set (training set predictors)
wget -P data/raw/ https://s3.amazonaws.com/drivendata/data/7/public/4910797b-ee55-40a7-8668-10efd5c1b960.csv


echo "Finished downloading data and documentation"
