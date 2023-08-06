import os
import pdb
import uuid
import atexit
import sys
import subprocess as sp
import numpy as np
from numpy import nan
import pandas as pd
from sklearn import cluster
from datasmash.utils import write_series, preprocess_map, quantizer
from datasmash.primitive_interfaces.unsupervised_learning import UnsupervisedLearnerPrimitiveBase
from datasmash.config import CWD, TEMP_DIR, BIN_PATH


class SmashClustering(UnsupervisedLearnerPrimitiveBase):
    '''
    Object for running Data Smashing to calculate the distance matrix between n
        timeseries and using sklearn.cluster classes to cluster;
        inherits from UnsupervisedSeriesLearningBase API

    Inputs -
        bin_path(string): Path to Smash binary as a string
        quantiziation (function): quantization function for input timeseries
            data

    Attributes:
        bin_path (string): path to bin/smash
        quantizer (function): function to quantify input data
        num_dimensions (int): number of dimensions used for clustering

        (Note: bin_path and num_dimensions can be set by assignment,
        input and quantizer must be set using custom method)
    '''

    def __init__(self, bin_path=BIN_PATH, n_clus=8, cluster_class=None) -> None:
        self.__bin_path = os.path.abspath(bin_path)
        if cluster_class is None:
            self.__cluster_class = cluster.KMeans(n_clusters=self.__num_clusters)
        else:
            self.__cluster_class = cluster_class
        prev_wd = os.getcwd()
        os.chdir(CWD)
        sp.Popen("mkdir "+ TEMP_DIR, shell=True, stderr=sp.STDOUT).wait()
        self.__file_dir = CWD + "/" + TEMP_DIR
        os.chdir(prev_wd)
        self.__input_dm_fh = None
        self.__input_dm_fname = None
        self.__output_dm_fname = None
        self.__command = (self.__bin_path + "/smash")
        self.__input_e = None
        self.fitted = False

    def set_training_data(self, data) -> None:
        self._data = data
        self.__quantized_data = preprocess_map(quantizer, self._data)
        self.fitted = False

    def _get_dm(self, first_run, max_len=None, num_get_dms=5, details=False):
        '''
        Helper function:
        Calls bin/smash to compute the distance matrix on the given input
        timeseries and write I/O files necessary for Data Smashing

        Inputs -
            max_len (int): max length of data to use
            num_get_dms (int): number of runs of Smash to compute distance
                matrix (refines results)
            details (boolean): do (True) or do not (False) show cpu usage of
                Data Smashing algorithm

        Outuputs -
            (numpy.ndarray) distance matrix of the input timeseries
            (shape n_samples x n_samples)
        '''

        if not first_run:
            os.unlink(self.__input_dm_fh.name)
            self.__command = (self.__bin_path + "/smash")

        self.__input_dm_fh, self.__input_dm_fname = write_series(input_data=self.__quantized_data,\
                                                                    file_dir=self.__file_dir)

        self.__command += " -f " + self.__input_dm_fname + " -D row -T symbolic"

        if max_len is not None:
            self.__command += (" -L " + str(max_len))
        if num_get_dms is not None:
            self.__command += (" -n " + str(num_get_dms))
        if not details:
            self.__command += (" -t 0")

        self.__output_dm_fname = str(uuid.uuid4())
        self.__output_dm_fname = self.__output_dm_fname.replace("-", "")
        self.__command += (" -o " + self.__output_dm_fname)

        prev_wd = os.getcwd()
        os.chdir(self.__file_dir)
        sp.Popen(self.__command, shell=True, stderr=sp.STDOUT).wait()
        os.chdir(prev_wd)

        try:
            results = np.loadtxt(\
            fname=(self.__file_dir+"/"+self.__output_dm_fname), dtype=float)
            return results
        except IOError:
            print("Error: Smash calculation unsuccessful. Please try again.")

    def fit(self, ml=None, nr=None, d=False, y=None, is_affinity=False):
        '''
        Uses Data Smashing to compute the distance matrix of the input time
        series and fit Data Smashing output to clustering class

        Inputs -
            ml (int): max length of data to use
            nr (int): number of runs of Smash to compute distance matrix
                (refines results)
            d (boolean): do (True) or do not (False) show cpu usage of Smash
                algorithm
            y (numpy.ndarray): labels for fit method of user-defined
                clustering_class

        Outuputs -
            (numpy.ndarray) distance matrix of the input timeseries
            (shape n_samples x n_samples)
        '''

        if self.__input_dm_fh is None:
            self._output = self._get_dm(True, ml, nr, d)
            self._output = self._output+self._output.T
            self.__cluster_class.fit(self._output)
            if is_affinity:
                self._output =np.reciprocal(self._output+1e-10)
            return self._output
        else:
            self._output = self._get_dm(False, ml, nr, d)
            self._output = self._output+self._output.T
            self.__cluster_class.fit(self._output)
            if is_affinity:
                self._output =np.reciprocal(self._output+1e-10)
            return self._output

    def fit_predict(self, ml=None, nr=None, d=False, y=None, is_affinity=False):
        '''
        Returns output sklearn/clustering_class' fit_predict on distance matrix
        computed by Data Smashing algorithm and input y

        Inputs -
            ml (int): max length of data to use
            nr (int): number of runs of Smash to compute distance matrix
                (refines results)
            d (boolean): do (True) or do not (False) show cpu usage of Smash
                algorithm

        Returns -
            (np.ndarray) Computed cluster centers and predict cluster index
                from the input  using Data Smashing and sklearn cluster_class
        '''

        self.__input_e = self.fit(ml, nr, d,y=None,is_affinity=is_affinity)
        self._output = self.__cluster_class.fit_predict(self.__input_e, y)
        return self._output

    def produce(self, ml=None, nr=None, d=False):
        '''
        Returns output sklearn/clustering_class' predict on distance matrix
        computed by Data Smashing algorithm

        Inputs -
            ml (int): max length of data to use
            nr (int): number of runs of Smash to compute distance matrix
                (refines results)
            d (boolean): do (True) or do not (False) show cpu usage of Smash
                algorithm

        Returns -
            (np.ndarray) Computed cluster centers and predict cluster index
                from the input data using data smashing and
                sklearn cluster_class
        '''

        self.__input_e = self.fit(ml, nr, d)
        self._output = self.__cluster_class.predict(self.__input_e)
        return self._output

    def get_params(self):
        pass

    def set_params(self):
        pass


def cleanup():
    '''
    Maintenance method:
    Clean up library files before closing the script; no I/O
    '''

    prev_wd = os.getcwd()
    os.chdir(CWD)
    if os.path.exists(CWD + "/" + TEMP_DIR):
        command = "rm -r " + CWD + "/" + TEMP_DIR
        sp.Popen(command, shell=True, stderr=sp.STDOUT).wait()
    os.chdir(prev_wd)



atexit.register(cleanup)
