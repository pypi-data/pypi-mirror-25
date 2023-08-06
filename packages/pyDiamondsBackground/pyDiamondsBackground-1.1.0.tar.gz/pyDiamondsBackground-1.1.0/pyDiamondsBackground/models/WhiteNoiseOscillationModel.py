import numpy as np

from pyDiamondsBackground.models.BackgroundModel import BackgroundModel


class WhiteNoiseOscillationModel(BackgroundModel):
    """
    This implementation of the Background model implements a solar like oscillator including granular components as
    well as the white noise component.
    """
    def __init__(self, covariates):
        """
        The constructor for this implementation calls the super of the Backgroundmodel and sets the dimension as
        well as the name of the model and the covariates, which are passed as a parameter
        :param covariates: The frequential axis of the data set
        :type covariates: ndarray
        """
        self._covariates = covariates
        BackgroundModel.__init__(self, covariates, 10, "White noise oscillation model")

    def predict(self, predictions, modelParameters):
        """
        The predict method for this implementation computes a model for a solar like oscillator with white background
        noise.
        :param predictions: The predictions for the sampling of the initial dataset
        :type predictions: ndarray
        :param modelParameters: The model parameters used to compute the initial sampling of the dataset, basically
        representing the priors.
        :return: The predictions of the dataset
        :type modelParameters: ndarray
        """
        flatNoiseLevel = modelParameters[0]
        amplitudeHarvey1 = modelParameters[1]
        frequencyHarvey1 = modelParameters[2]
        amplitudeHarvey2 = modelParameters[3]
        frequencyHarvey2 = modelParameters[4]
        amplitudeHarvey3 = modelParameters[5]
        frequencyHarvey3 = modelParameters[6]
        heightOscillation = modelParameters[7]
        nuMax = modelParameters[8]
        sigma = modelParameters[9]

        zeta = 2 * np.sqrt(2) / np.pi
        predictions = zeta * amplitudeHarvey1 ** 2 / (
            frequencyHarvey1 * (1 + np.power(self._covariates / frequencyHarvey1, 4)))

        predictions += zeta * amplitudeHarvey2 ** 2 / (
            frequencyHarvey2 * (1 + np.power(self._covariates / frequencyHarvey2, 4)))

        predictions += zeta * amplitudeHarvey3 ** 2 / (
            frequencyHarvey3 * (1 + np.power(self._covariates / frequencyHarvey3, 4)))

        predictions += heightOscillation * np.exp(-1*np.power(nuMax-self._covariates,2)/(2*sigma**2))

        predictions *= self._responseFunction

        predictions += flatNoiseLevel

        return predictions
