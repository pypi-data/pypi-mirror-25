import os
from pyDiamonds import UniformPrior, KmeansClusterer, MultiEllipsoidSampler, EuclideanMetric \
    , ExponentialLikelihood, PowerlawReducer, Results

import numpy as np
from numpy import ndarray

from pyDiamondsBackground.models import BackgroundModel
from pyDiamondsBackground.strings import *


class Background:
    """
    This class allows for backgroundfitting of a Powerspectraldensity of a star. Poviding the PSD and a Model to fit
    the data against, it will run a Nested Sampling algorithm provided by the PyDIAMONDS package
    (see https://github.com/muma7490/PyDIAMONDS) of the data.
    """
    def __init__(self, kicID: str, modelObject: type(BackgroundModel), data: ndarray = None, priors: ndarray = None,
                 nsmcConfiguringParameters: ndarray = None
                 , nyquistFrequency: float = None, xmeansConfiguringParameters: ndarray = None, rootPath: str = None):
        """
        The constructor of the class sets up the Nested Sampler. For this you need all the parameters of the
        constructor, namely the kicID of the star, the runID on which DIAMONDS should run, the Uniform Priors with
        which DIAMONDS will try to fit the data, the NSMC configuring parameters, which will setup the nested sampler,
        the XMeans configuring parameter which wil setup the Kmeans clusterer. See the documentation of the parameters
        for information on how the content has to look like.

        It is also possible, to read these values from files, which will occur if the rootPath parameter is set and
        any of the other parameters are not set. This assumes, that a data/ and results/ path are available at rootPath.
        The files are read in this locations:

        - data: root/data/KIC*KICID*.txt, where *KICID* is the kicID

        - priors: root/results/KIC*KICID*/background_hyperParameters_*modelName*.txt where *KICID* is the kicID and
                    *modelname* represents the Modelname, taken from the Model class

        - nyquistFrequency: root/results/KIC*KICID*/NyquistFrequency where *KICID* is the kicID. See the documentation
                            of the parameter for further information.

        -nsmcConfiguringParameters: root/results/KIC*KICID*/NSMC_configuringParameters.txt. *KICID* is the kicID.
                                    This is optional, a default configuration is provided

        -xmeansConfiguringParameters: root/results/KIC*KICID*/Xmeans_configuringParameters.txt. *KICID* is the kicID.
                                      This is optional, a default configuration is provided.

        Call the run method to start the analysis. Call getResults for direct results and writeResults to write the
        results to the filesystem.

        :param kicID: The KicID (name) of the star. This is needed for various files.
        :type kicID:str
        :param model: The model for which DIAMONDS performs the fitting. Pass here the class object, which should be
                        derived from BackgroundModel. The initialization of the object will be done within the
                        constructor
        :type model: BackgroundModel
        :param priors: The priors on which DIAMONDS will perform the fitting. In general this is a numpy array with
                        2xn values in it, where n represents the number of priors which depend on the model.
                        Background will check if the dimensions have the correct number of values, in accordance to
                        the dimensions property of the model.
                        The priors are assumed to be uniform. The first column describes the min values of the
                        priors, the second column describes the max values of the priors.
        :type priors:ndarray
        :param nyquistFrequency: The nyquist frequency of the dataset. This has to be computed outside of Background.
        :type nyquistFrequency: float
        :param nsmcConfiguringParameters: The NSMC configuring parameters for the DIAMONDS run. In general this doesn't
                                            need to be set, as default parameters are provided. For completeness here
                                            is a list of values which should be available:
                                            - Initial N live points
                                            - Minimum N live points
                                            - Maximum N live points
                                            - N inital Iterations without clustering
                                            - N iterations with same clustering
                                            - Initial enlargement fraction
                                            - Shrinking rate
                                            - Termination factor
        :type nsmcConfiguringParameters: ndarray
        :param xmeansConfiguringParameters: The Xmeans configuring parameters for the DIAMONDS run. In general this
                                            doesn't need to be set, as default parameters are provided. For completeness
                                            here is a list of values which should be available:
                                            - Minimum N clusters
                                            - Maximum N clusters
        :type xmeansConfiguringParameters: ndarray
        :param rootPath: The root path where the files are assumed. If this is set, it will try to find the files
                        according to the scheme above.
        :type rootPath:str
        """

        if rootPath is not None and os.path.exists(rootPath):
            rootPath = os.path.abspath(rootPath)+"/"
            self._dataPath = rootPath + "data/"
            self._resultsPath = rootPath + "results/KIC" + kicID + "/"
            if not os.path.exists(self._dataPath):
                raise IOError("Data Path "+self._dataPath+" does not exist!")

            if not os.path.exists(self._resultsPath):
                raise IOError("Results Path "+self._resultsPath+" does not exist!")
        else:
            self._dataPath = None
            self._resultsPath = None

        self._data = self._setupData(kicID,self._dataPath,data)
        self._nyquistFrequency = self._checkFileExistsAndRead(nyquistFrequency, self._resultsPath, "NyquistFrequency.txt")
        self._model = modelObject(self._data[0])
        self._model.nyquistFrequency = self._nyquistFrequency
        self._metric = EuclideanMetric()
        self._uniformPrior = self._setupPriors(kicID,self._resultsPath,priors)
        self._likelihood = ExponentialLikelihood(self._data[0].astype(float),self._model)
        self._kmeansClusterer = self._setupKmeans(self._resultsPath,xmeansConfiguringParameters)
        self._nestedSampler = self._setupNestedSampling(self._resultsPath,nsmcConfiguringParameters)
        # 2nd parameter -> tolerance, 3rd parameter -> exponent
        self._livePointsReducer = PowerlawReducer(self._nestedSampler, 1.e2, 0.4, self._terminationFactor)
        self.credibleInterval = 68.3

        if priors is None and nyquistFrequency is None and nsmcConfiguringParameters is None and \
                        xmeansConfiguringParameters is None and rootPath is None:
            raise ValueError("You need to set either the rootPath or all parameters")
        pass

    def _setupData(self, kicID: str, dataPath: str = None, data: ndarray = None):
        """
        This method sets up the data, checks its validity and returns it. Generally only used internally. Either
        dataPath or data have to be set. If both are set, data is used.
        :param kicID: the kicID of the star.
        :type kicID: str
        :param dataPath: The path where the data is found in the form of KIC*KICID*.txt.
        :type dataPath: str
        :param data: The data of the star. Has to be a powerspectraldensity with 2xn dimensions.
        :type data:ndarray
        :return:Returns the data of the star in form of a 2xn numpy array
        :rtype:ndarray
        """
        data = self._checkFileExistsAndRead(data, dataPath, "KIC" + kicID + ".txt")

        if len(data) != 2:
            raise ValueError("Data needs to have dimensions of 2xn. Actual dimensions are "+str(data.shape))

        return data

    def _setupPriors(self, kicID: str, dataPath: str = None, data: ndarray = None):
        """
        This method sets up the priors, checks their validity and returns a UniformPrior object. Generally only
        used internally. Either resultsPath or priors have to be set.
        :param kicID: the kicID of the star.
        :type kicID: str
        :param dataPath: the results path of the star where the prior file is found according to the scheme in
                            the constructor.
        :type dataPath: str
        :param data: The actual priors provided through the constructor. Has to be a 2xn numpy array. Will be checked
                        against the dimensions defined in the model.
        :type data: ndarray
        :return: The UniformPrior object, which will then be used in the analysis
        :rtype: UniformPrior
        """

        data = self._checkFileExistsAndRead(data, dataPath, "background_hyperParameters" +
                                            self._model.fileAppendix + ".txt")

        if len(data) != 2:
            raise ValueError("Priors need to have a dimension of 2. Actual dimension is "+str(len(data)))

        if data.shape != (2,self._model.dimension):
            raise ValueError("Priors need to have a shape of "+str((2,self._model.dimension))+", their actual shape "
                                                                                              "is "+str(data.shape))

        if len(data[0]) != len(data[1]):
            raise ValueError("Minimum and maxium Priors need to have the same dimensions. Minimum prior as "
                             ""+str(len(data[0]))+" dimensions ,maximum prior has "+str(len(data[1]))+" dimensions.")

        if not all(min<max for (min,max) in zip(data[0],data[1])):
            raise ValueError("Minima priors need to be smaller than maximum priors. Minimum priors are "
                             ""+str(data[0])+", maximum priors are "+str(data[1]))

        return UniformPrior(data[0].astype(float),data[1].astype(float))




    def _setupKmeans(self, dataPath: str = None, data: ndarray = None):
        """
        Sets up the KMeans parameters. Generally only used internally. If configuringParmeters is None and
        there is no Xmeans_configuringParameters.txt file available in resultsPath, default values will be used.
        Returns the KmeansClusterer object used for the analysis.
        :param dataPath: The path where Xmeans_configuringParameters.txt should be found.
        :type dataPath: str
        :param data: The configuringParameters. See constructor documentation for further information.
        :type data: ndarray
        :return: The KmeansClusterer object used for the analysis.
        :rtype: KmeansClusterer
        """
        try:
            data = self._checkFileExistsAndRead(data, dataPath, "Xmeans_configuringParameters.txt")
        except (IOError, AttributeError) as e:
            data = self._defaultxMeansParameters()

        if data.size != 2:
            raise ValueError("Priors need to have a dimension of 2. Actual dimension is "+str(data.size))

        if data[0] <= 0 or data[1] <= 0 or data[1] < data[0]:
            raise ValueError("Minimum or maximum number of clusters cannot be <=0 and minimum of clusters cannot be "
                             "larger than maximum number of clusters. Min is "+str(data[0])+", max is "+str(data[1]))

        Ntrials = 10
        relTolerance = 0.01

        return KmeansClusterer(self._metric,int(data[0]),int(data[1]),Ntrials,float(relTolerance))


    def _setupNestedSampling(self, dataPath: str = None, data: ndarray = None):
        """
        Sets up the Nested sampling parameters. Generally only used internally. If configuringParameters is None and
        there is no NSMC_configuringParameters.txt file available in resultsPath, default values will be used. Returns
        the MultiEllispoidSampler object used for the analysis
        :param dataPath: The path where NSMC_configuringParameters.txt should be found
        :type dataPath: str
        :param data: The configuringParameters. See constructor documentation for further information.
        :type data: ndarray
        :return: The MultiEllipsoidSampler used to run DIAMONDS.
        :rtype: MultiEllipsoidSampler
        """
        try:
            data = self._checkFileExistsAndRead(data, dataPath, "NSMC_configuringParameters.txt")
        except (IOError, AttributeError) as e:
            data = self._defaultNSMCParameters()

        if data.size != 8:
            raise ValueError("NSMC Parameters need to have a dimension of 8. Actual dimension is "+str(data.size))

        if data[6] > 1 or data[6] < 0:
            raise ValueError("Shrinking Rate for ellipsoids must be 0<x<1. Value is "+str(data[6]))

        printOnScreen = True
        initialNlivePoints = int(data[0])
        minNlivePoints = int(data[1])
        self._maxNdrawAttempts = data[2]
        self._nInitialIterationsWithoutClustering = data[3]
        self._nIterationsWithSameClustering = data[4]
        initialEnlargementFraction = 0.267*(self._model.dimension)**0.643
        shrinkingRate = data[6]
        self._terminationFactor = data[7]

        return MultiEllipsoidSampler(printOnScreen,[self._uniformPrior],self._likelihood,self._metric,self._kmeansClusterer
                                     ,initialNlivePoints,minNlivePoints,initialEnlargementFraction,shrinkingRate)


    def run(self):
        """
        Starts the process of fitting diamonds.
        """
        self._nestedSampler.run(self._livePointsReducer,int(self._nInitialIterationsWithoutClustering),
                                int(self._nIterationsWithSameClustering),int(self._maxNdrawAttempts),
                                float(self._terminationFactor),"")
        self._results = Results(self._nestedSampler)

    @property
    def parameters(self):
        """
        Property for the
        :return:
        :rtype:
        """
        return self._nestedSampler.getPosteriorSample()

    @property
    def logLikelihood(self):
        return self._nestedSampler.getLogLikelihood()

    @property
    def logWeights(self):
        return self._nestedSampler.getLogWeightOfPosteriorSample()

    @property
    def evidenceInformation(self):
        return {SkillingsLog:self._nestedSampler.getLogEvidence(),
                    SkillingsErrorLog:self._nestedSampler.getLogEvidenceError(),
                    SkillingsInformationGain:self._nestedSampler.getInformationGain()}

    @property
    def posteriorProbability(self):
        return self._results.posteriorProbability()

    @property
    def parameterSummary(self):
        return self._results.parameterEstimation(self.credibleInterval,False)

    @property
    def marginalDistributions(self):
        raise NotImplementedError("Not yet implemented")

    @property
    def credibleInterval(self):
        return self._credibleInterval

    @credibleInterval.setter
    def credibleInterval(self,value):
        self._credibleInterval = value

    def getResults(self):
        """
        Returns the results for diamonds. Work in progress.
        """
        raise NotImplementedError("Not yet implemented!")

    def writeResults(self, path: str, prefix: str = ""):
        """
        Writes the results to path.
        :param path: Path where the data is saved.
        :type path:str
        :param prefix: An optional prefix used for all files.
        :type prefix: str
        """
        self._nestedSampler.setOutputPathPrefix(os.path.abspath(path)+"/"+ prefix)
        self._results.writeParametersToFile("parameter","txt")
        self._results.writeLogLikelihoodToFile("logLikelihood.txt")
        self._results.writeLogWeightsToFile("logWeights.txt")
        self._results.writeEvidenceInformationToFile("evidenceInformation.txt")
        self._results.writePosteriorProbabilityToFile("posteriorDistribution.txt")
        self._results.writeParametersSummaryToFile("parameterSummary.txt",self.credibleInterval,True)

    def _checkFileExistsAndRead(self, data, dataPath, fileName):
        if dataPath is not None:
            try:
                fileName = dataPath + fileName
            except:
                raise TypeError("Cannot connotate type "+str(type(dataPath))+" with str!")
        else:
            fileName = None

        if data is None and fileName is not None:
            if os.path.exists(fileName):
                data = np.loadtxt(fileName).T
            else:
                raise IOError(fileName + " does not exist!")
        elif data is None and fileName is None:
            raise AttributeError("You need to set either data or fileName")
        return data

    def _defaultxMeansParameters(self):
        return np.array([1.0,10.0])

    def _defaultNSMCParameters(self):
        return np.array([500,500,50000,1500,50,2.1,0.01,0.1])

    @property
    def model(self):
        """
        :return: Property for the model used in the analysis. Must be derived from BackgroundModel
        :rtype: BackgroundModel
        """
        return self._model