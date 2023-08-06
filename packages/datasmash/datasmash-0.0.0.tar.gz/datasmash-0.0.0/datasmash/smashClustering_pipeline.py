#!/usr/bin/python

from smashClustering import *
from utils import *
from sklearn import cluster


# Reading in data from deploy_scripts/examples/data.dat and setting dtype=np.int32
# because this input data is categorical
X = read_series("./data_/data.dat", delimiter=" ").values.astype(np.int32)

# instantiate clustering class to be used to cluster distance matrix data
# if not specified, default is cluster.KMeans
meanshift_cc = cluster.MeanShift()

# instantiate clustering class
# default cluster_class is sklearn.cluster.KMeans and numCluster default is 8
scc = SmashClustering(cluster_class=meanshift_cc)
# fit and return distance matrix of input timeseries data (repeat calculation 3 times)
scc.set_training_data(X)
scc.fit(nr=3)

# call clustering class predict method on fitted input data
print(scc.produce(nr=3))

# can switch clustering class; first need to initialize then set
KMeans_cc = cluster.KMeans(n_clusters=4)
scc = SmashClustering(cluster_class=KMeans_cc)

# can also call fit_predict for convenience (note: distance matrix will be recalculated)
scc.set_training_data(X)
print(scc.fit_predict(nr=3))

# second test on known dataset of 3 classes
X2 = read_series("./data_/COMBINED_TEST1", delimiter=" ").values
scc.set_training_data(X2)

# create the clustering classes to use (meanshift does not take param n_clusters, so reuse)
KMeans_cc2 = KMeans_cc = cluster.KMeans(n_clusters=3)

# compare
scc = SmashClustering(cluster_class=KMeans_cc2)
scc.set_training_data(X2)
print(scc.fit(nr=3))
print(scc.fit_predict(nr=3))
scc = SmashClustering(cluster_class=meanshift_cc)
scc.set_training_data(X2)
print(scc.fit(nr=3))
print(scc.fit_predict(nr=3))


# can switch clustering class; first need to initialize then set
# is_affinity=True implies we are usig an affinity matrix, so larger values
# imply more similarity, as opposed to a distance matrix
Spectral_cc = cluster.SpectralClustering(n_clusters=3,affinity='precomputed')
scc = SmashClustering(cluster_class=Spectral_cc)
print("spectral clustering: ", scc.fit_predict(nr=3,is_affinity=True))
