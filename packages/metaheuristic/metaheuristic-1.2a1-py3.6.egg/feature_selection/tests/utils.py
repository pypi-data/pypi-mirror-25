import numpy as np
from sklearn.utils.estimator_checks import check_estimator
from sklearn.utils.testing import assert_array_equal
from sklearn.datasets import load_breast_cancer
from sklearn.svm import SVC
from feature_selection import HarmonicSearch, GeneticAlgorithm, RandomSearch, BinaryBlackHole, SimulatedAnneling
from sklearn.utils.testing import assert_raises
from sklearn.utils.testing import assert_warns
from six.moves import cPickle
import pickle
from os import listdir
from os.path import isfile, join

if __name__ == "__main__":
    
    dataset_name = "data_path" 
    dataset = load_breast_cancer()
    X, y = dataset['data'], dataset['target_names'].take(dataset['target'])
    
    # Classifier to be used in the metaheuristic
    clf = SVC()
    
    hs = HarmonicSearch(number_gen=500, verbose=1, random_state=0,
                        make_logbook=True)
    
    param = hs.get_params()
    
    hs.fit(X,y, normalize=True)
    
    file = "HarmonicSearch_"
    for i, value in param.items():
        file = file + i + "_" + str(value) + "_"

    onlyfiles = [f for f in listdir(".") if isfile(join(("."), f))]


    f = open(file +'.save', 'wb')
    #for obj in [hs.logbook, hs.best_mask_, hs.fitness_, hs.mask_, hs.classes_]
    cPickle.dump(hs, f, protocol=cPickle.HIGHEST_PROTOCOL)
    f.close()
    
    
    