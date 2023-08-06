""" test ltsa package imports """

import ltsa
import h5py
import numpy as np
import scipy.io as spio

if __name__ == "__main__":

    switch = 0
    if switch:
        print "Darcy example"
        fTr = spio.loadmat('baseline/KLRF_train75.mat')
        Output = fTr['output']
    else:
        print "Richards example"
        fTr = h5py.File('baseline/Train_N400.mat')
        Output = np.reshape(fTr['output'].value.T, [400, 26 * 26 * 26])

    OutputR, dictOut = ltsa.utils.preprocessing.pre(Output)
    OutputF = ltsa.utils.preprocessing.post(OutputR, dictOut)

    k = 25
    d = 5

    errors = []
    delta = 0.1  # this will have higher error as it is normalised.
    # This also depends on the quality of the data.

    manifold_model = ltsa.LocalTangentSpaceAlignment(OutputR, k, d)
    print "output reduced"
    print OutputR
    manifold_model.solve()
    print "latent"
    print manifold_model.t

    y_r = manifold_model.pre_image(manifold_model.t)
    print "output recovered"
    print y_r

    # test the preimage by comparing training features and features from pre-image of raw LTSA latent points
    mat1 = OutputR
    mat2 = y_r
    error = np.mean(np.linalg.norm((mat1 - mat2) / np.linalg.norm(mat1))**2)
    print error
    if error > delta:
        errors.append('test_preimage1, error: {0}'.format(error))

