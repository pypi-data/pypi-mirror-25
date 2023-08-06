#!/usr/bin/python

# import necessary libraries and utility files
from smashDistanceMetricLearning import *
from utils import *

# declare bin location relative to script path
bin_path = "./bin/"

# Reading in data from deploy_scripts/examples/data.dat and setting dtype=np.int32
# because this input data is categorical
X = read_series("./data/data.dat", delimiter=" ").values.astype(np.int32)

# create SmashDistanceMatrixLearning class to run methods
dmlc = SmashDistanceMetricLearning()

# return distance matrix of input timeseries data (repeat calculation 3 times)
dmlc.set_training_data(X)
print(dmlc.produce(nr=3))
