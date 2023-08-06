#!/usr/bin/python

from smashFeaturization import *
from utils import *
from sklearn import manifold


# Reading in data from deploy_scripts/examples/data.dat and setting dtype=np.int32
# because this input data is categorical
X = read_series("./data/data.dat", delimiter=" ").values.astype(np.int32)

# decide on number of dimensions to use (default is 2)
num_dim = 2

# instantiate another embedding class if desired
# e.g. sklearn.manifold.MDS
mds_emb = manifold.MDS(n_components=num_dim, dissimilarity="precomputed")

# create SmashEmbedding class to run methods (require 2 dimensions in embedding)
sfc = SmashFeaturization(n_dim=num_dim, embed_class=mds_emb)

# return distance matrix of input timeseries data (repeat calculation 3 times)
# NOTE: fits both default Sippl Embedding and user-defined custom embedding class
sfc.set_training_data(X)

# return embedded coordinates using Sippl embedding (default) on distance matrix
print(sfc.produce(nr=3, embedder='default'))

# return embedded coordinates using Sippl embedding (default) on distance matrix
print(sfc.produce(nr=3, embedder='custom'))
