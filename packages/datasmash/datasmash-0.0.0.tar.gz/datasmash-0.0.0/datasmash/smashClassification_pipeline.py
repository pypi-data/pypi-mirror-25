#!/usr/bin/python
# start from working directory of where SmashClassification is located
from smashClassification import *
from utils import condense, read_series

# create instance of the SmashClassification with the given quantization and force vectorization
# note: force_vect_preproc == True by default, unless input quantizer is vectorized,
# then need to set as False
clf = SmashClassification()

# quantize and read in library files as pd.DataFrame
lib0 = read_series("./data/LIB0", delimiter=" ")
lib1 = read_series("./data/LIB1", delimiter=" ")
lib2 = read_series("./data/LIB2", delimiter=" ")

# map library files to class/label numbers
# i.e. all timeseries in lib0 are of class 0, etc.
maps = [(lib0, 0), (lib1, 1), (lib2, 2)]

# set training data from mappings to be fit into SmashMatchClassification
#clf.set_training_data(maps)
#X, y = condense(maps)
clf.set_training_data(maps)

# fit the formatted examples and labels
# since when reading in the libraries we had alreaady performed quantization,
# we do not need to quantize again
clf.fit()

# quantize and read in the timeseries data to be classified as pd.DataFrame
data = read_series("./data/TEST0", delimiter=" ")

# run algorithm twice, and print the results
print(clf.produce(data, nr=2))

# get the log probabilities for each timeseries to fall in each class,
# and force rerun of the SmashMatch algorithm
print(clf.produce_log_proba(data, nr=2, force=True))

