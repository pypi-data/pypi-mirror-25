from backtester.features.feature import Feature
import numpy as np


class DirectionFeature(Feature):

    @classmethod
    def computeForLookbackData(cls, featureParams, featureKey, currentFeatures, lookbackDataDf):
        data = lookbackDataDf[featureParams['featureName']]
        if len(data.index) < featureParams['period']:
            return 0
        return np.sign(currentFeatures[featureParams['featureName']] - data[-featureParams['period']])
