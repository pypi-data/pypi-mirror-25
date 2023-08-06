from pyDiamonds import Model
import numpy as np
from numpy import ndarray

class BackgroundModel(Model):
    """
    The Background model is an abstract class, that provides the necessary methods to compute a bayesian analysis with
    PyDIAMONDS. It inherits multiple methods already from the Model class from PyDIAMONDS, naming the predict method and
    it provides said Models class with the covariates, the frequential axis of the data.
    """
    def __init__(self, covariates: ndarray, dimension: int, name: str, fileAppendix: str = ""):
        """
        The constructor of the class sets up the class. It sets the names, dimensions, as well as the fileAppendix.
        The Nyquist frequency must be set at a later point in using the code using the property for the Nyquist
        frequency.
        :param covariates: The frequential axis of the dataset.
        :type covariates: ndarray
        :param dimension: The dimension of the priors. Will be used for a check within Background to check the length of
                            the priors
        :type dimension: int
        :param name: The name of the model.
        :type name: str
        :param fileAppendix: The appendix for the filename, used for the priors (i.e. hyperparameters*fileAppendix*.txt
        :type fileAppendix: str
        """
        covariates = covariates.astype(float)
        Model.__init__(self,covariates)
        self._dimension = dimension
        self._name = name
        self._fileAppendix = fileAppendix
        self._nyquistFrequency = None
        self._responseFunction = None
        pass

    def getResponseFunction(self):
        """
        :return: The response function. Multiplied with the prediction to create an initial sampling
        :rtype: ndarray
        """
        if self._responseFunction is None:
            raise ValueError("Nyquist frequency must be set!")

        return self._responseFunction

    def getNyquistFrequency(self):
        """
        :return: The Nyquist frequency. Must have been set previously using the setter property.
        :rtype: float
        """
        return self._nyquistFrequency

    def readNyquistFrequencyFromFile(self, fileName: str):
        """
        Reads the Nyquist frequency from a file and sets it as the used Nyquist frequency
        :param: fileName: Name of the file containing the nyquist frequency. Must contain only one item!
        :type: fileName: str
        """
        self._nyquistFrequency = np.loadtxt(fileName).T

    @property
    def nyquistFrequency(self):
        """
        Property of the Nyquist frequency. Raises a ValueError if the Nyquist frequency was not set previously.
        :return: The Nyquist frequency
        :rtype: float
        """
        if self._nyquistFrequency is None:
            raise ValueError("Nyquist frequency must be set before accessing it!")
        return self._nyquistFrequency

    @nyquistFrequency.setter
    def nyquistFrequency(self, value: float):
        """
        Setter property for the Nyquist frequency. Also triggers the calculation of the response Function
        :param: value: Value for the Nyquist frequency.
        :type: value: float
        """
        self._nyquistFrequency = value
        self._calculateResponseFunction()

    def predict(self, predictions: ndarray, modelParameters: ndarray):
        """
        Predict method, called by PyDIAMONDS to sample an initial value set. Must be implemented in the class
        derived from this class. Here one can calculate the model using the modelParameters as an input from DIAMONDS.
        Must return the predictions after finishing the calculation.
        :param predictions: The predictions for the dataset
        :type predictions: ndarray
        :param modelParameters: The parameters for the model, representing the priors. Determined by PyDIAMONDS
        :type modelParameters: ndarray
        :return: The predictions for the dataset using the covariates.
        :rtype: ndarray
        """
        raise NotImplementedError("You need to implement predict if you derive from BackgroundModel")

    @property
    def dimension(self):
        """
        Property for the dimensions of the priors
        :return: Size of Priors
        :rtype: int
        """
        return self._dimension

    @property
    def name(self):
        """
        Property for the name of the model
        :return: Name of the model
        :rtype: str
        """
        return self._name

    @property
    def fileAppendix(self):
        """
        Property for the fileAppendix. Used in Background.
        :return: Text for the fileAppendix
        :rtype: str
        """
        return self._fileAppendix

    def _calculateResponseFunction(self):
        """
        This method calculates the response function, used for the first sampling of the dataset. Backgroundmodel
        implements a default implementation, but this could be different for different applications.
        :return: The response function using the covariates
        :rtype: ndarray
        """
        try:
            sincFunctionArgument = np.pi * self._covariates / (2 * self._nyquistFrequency)
            self._responseFunction = (np.sin(sincFunctionArgument) / sincFunctionArgument) ** 2
        except:
            raise ValueError("Nyquist frequency was not set before calculating response Function. Set the Nyquist "
                             "frequency before performing analysis")