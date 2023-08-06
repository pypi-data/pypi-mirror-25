import h5py
import scipy.io as spio
import unittest
from nose.tools import with_setup, nottest
import numpy as np

import ltsa



class PreImageTestCase(unittest.TestCase):
    """
    Test pre-image from LocalTangentSpaceAlignment.
    """
    def setUp(self):

        switch = 0
        if switch:
            fTr = spio.loadmat('ltsa/testing/baseline/KLRF_train75.mat')
            Output = fTr['output']
        else:
            fTr = h5py.File('ltsa/testing/baseline/Train_N400.mat')
            Output = np.reshape(fTr['output'].value.T, [400, 26 * 26 * 26])

        OutputR, dictOut = ltsa.utils.preprocessing.pre(Output)
        OutputF = ltsa.utils.preprocessing.post(OutputR, dictOut)

        self.Output = Output
        self.OutputR = OutputR
        self.OutputF = OutputF

        self.k = 25
        self.d = 7

        self.fun = self.error_temp

    def tearDown(self):
        self.Output = None
        self.OutputR = None
        self.OutputF = None

    @nottest
    def error(self, mat1, mat2, fun):
        assert(mat1.shape == mat2.shape)
        return fun(mat1, mat2)

    @nottest
    def MAPEerror(self, mat1, mat2):
        """ mean absolute percentage error
        """
        assert(mat1.shape == mat2.shape)
        n, _ = mat1.shape
        ape = 0
        for i in range(n):
            ape += np.linalg.norm((mat1[i, :] - mat2[i, :]) / mat1[i, :])
        return ape / n

    @nottest
    def error_temp(self, mat1, mat2):
        #print np.mean(np.linalg.norm((mat1 - mat2) / np.linalg.norm(mat1))**2)
        return np.mean(np.linalg.norm((mat1 - mat2) / np.linalg.norm(mat1))**2)


    @with_setup(setUp, tearDown)
    def test_util(self):
        """
        Test the utils normalising for the features
        """
        print "test_util()"
        errors = []
        delta = 1e-10

        # test utils when normalising (and removing constant dimensions)
        error = self.error(self.Output, self.OutputF, self.fun)
        if error > delta:
            errors.append('Error in normalising and reconstructing using utils module. mnae: {}'.format(error))

        # assert no error message has been registered, else print messages
        self.assertTrue(not errors, "errors occured:\n{}".format("\n".join(errors)))

    @with_setup(setUp, tearDown)
    def test_util_usecase(self):
        """
        Test the utils normalising in a use case by comparing a normalised, then recovered latent variables from an LTSA
        model to its raw value.
        """
        print "test_util_usecase()"
        errors = []
        delta = 1e-10

        manifold_model = ltsa.LocalTangentSpaceAlignment(self.Output, self.k, self.d)
        manifold_model.solve()
        self.ManifoldModel = manifold_model

        latent = self.ManifoldModel.t
        latent_r, dictLat = ltsa.utils.preprocessing.pre(latent)
        latent_f = ltsa.utils.preprocessing.post(latent_r, dictLat)

        # test utils when normalising (and removing constant dimensions) by seeing if error of original and
        # reconstructed is sufficiently small
        error = self.error(latent, latent_f, self.fun)
        if error > delta:
            errors.append('Error in normalising and reconstructing using utils module. mnae: {}'.format(error))

        # assert no error message has been registered, else print messages
        self.assertTrue(not errors, "errors occured:\n{}".format("\n".join(errors)))

    @with_setup(setUp, tearDown)
    def test_train_preimage1(self):
        """
        Test the pre-image map of our LTSA model by comparing the raw features (normalised) to the pre-image
        predictions.
        """
        print "test_train_preimage1()"
        errors = []
        delta = 0.1         # this will have higher error as it is normalised.
                            # This also depends on the quality of the data.

        manifold_model = ltsa.LocalTangentSpaceAlignment(self.OutputR, self.k, self.d)
        manifold_model.solve()
        self.ManifoldModel = manifold_model

        y_r = self.ManifoldModel.pre_image(self.ManifoldModel.t)

        # test the preimage by comparing training features and features from pre-image of raw LTSA latent points
        error = self.error(self.OutputR, y_r, self.fun)
        if error > delta:
            errors.append('test_preimage1, error: {0}'.format(error))

        # assert no error message has been registered, else print messages
        self.assertTrue(not errors, "errors occured:\n{}".format("\n".join(errors)))

    @with_setup(setUp, tearDown)
    def test_train_preimage2(self):
        """
        Test the pre-image map for numerical instability from numerical errors introduced by normalising. We check the
         pre-image of the raw latent against the pre-image of the normalised, then recovered latent.
        """
        print "test_train_preimage2()"
        errors = []
        delta = 0.05

        manifold_model = ltsa.LocalTangentSpaceAlignment(self.Output, self.k, self.d)
        manifold_model.solve()
        self.ManifoldModel = manifold_model

        latent_r, dictLat = ltsa.utils.preprocessing.pre(self.ManifoldModel.t)
        latent_f = ltsa.utils.preprocessing.post(latent_r, dictLat)

        y_norm = self.ManifoldModel.pre_image(latent_f)
        y_raw = self.ManifoldModel.pre_image(self.ManifoldModel.t)

        # test the previous two against each other (without raw LTSA latent points)
        error = self.error(y_raw, y_norm, self.fun)
        if error > delta:
            errors.append('test_preimage2, error: {0}'.format(error))

        # assert no error message has been registered, else print messages
        self.assertTrue(not errors, "errors occured:\n{}".format("\n".join(errors)))

if __name__ == '__main__':
    print "Running unit tests for PreImageTestCase (this may take a while)"
    unittest.main()
