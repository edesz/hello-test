#!/bin/bash


ACTION=${1:-create}


if [[ $ACTION == "clone" ]]
then
    # (OPTION 1) clone a project containing requirements.txt
    git clone <repository url here>
if [[ $ACTION == "create" ]]
then
    # (OPTION 2) create requirements.txt
    cat > requirements.txt << EOF
    nb_black
    nodeenv
    jupyter_contrib_nbextensions
    jupyter_nbextensions_configurator
    numpy
    pandas
    scikit-learn
    matplotlib
    seaborn
    imbalanced-learn
    yellowbrick
    azure-storage-blob
    xgboost
    xlrd
    category_encoders
    EOF
fi

# Install Python packages
pip install -U -r requirements.txt
