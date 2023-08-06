import numpy as np

from background.models.BackgroundModel import BackgroundModel


class NoiseBackgroundModel(BackgroundModel):
    def __init__(self,covariates):
        self._covariates = covariates
        BackgroundModel.__init__(self,covariates,7,"noise")

    def predict(self,predictions,modelParameters):
        flatNoiseLevel = modelParameters[0]
        amplitudeHarvey1 = modelParameters[1]
        frequencyHarvey1 = modelParameters[2]
        amplitudeHarvey2 = modelParameters[3]
        frequencyHarvey2 = modelParameters[4]
        amplitudeHarvey3 = modelParameters[5]
        frequencyHarvey3 = modelParameters[6]

        zeta = 2*np.sqrt(2)/np.pi

        predictions = zeta*(amplitudeHarvey1**2)/(frequencyHarvey1*(1+(self._covariates/frequencyHarvey1)**4))

        predictions += zeta * (amplitudeHarvey2 ** 2) / (frequencyHarvey2*(1 + (self._covariates / frequencyHarvey2) ** 4))
        predictions += zeta * (amplitudeHarvey3 ** 2) / (frequencyHarvey3*(1 + (self._covariates / frequencyHarvey3) ** 4))

        predictions *=self._responseFunction
        predictions +=flatNoiseLevel
        return predictions

    def _calculateResponseFunction(self):
        sincFunctionArgument = np.pi * self._covariates / (2 * self._nyquistFrequency)
        self._responseFunction = (np.sin(sincFunctionArgument) / sincFunctionArgument) ** 2


    def parameterCount(self):
        return 7