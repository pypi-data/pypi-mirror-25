from backtester.trading_system_parameters import TradingSystemParameters
from datetime import timedelta
from backtester.dataSource.quant_quest_data_source import QuantQuestDataSource
from backtester.executionSystem.QQ_execution_system import QQExecutionSystem
from backtester.orderPlacer.backtesting_order_placer import BacktestingOrderPlacer
from backtester.constants import *
from backtester.features.feature import Feature


class FairValueTradingParams(TradingSystemParameters):

    def __init__(self, problem1Solver):
        self.__problem1Solver = problem1Solver
        Problem1PredictionFeature.setProblemSolver(problem1Solver)
        super(FairValueTradingParams, self).__init__()

    def getStartingCapital(self):
        instrumentIds = self.__problem1Solver.getSymbolsToTrade()
        if instrumentIds and len(instrumentIds) > 0:
            return len(instrumentIds) * 10000
        return 1000000

    '''
    Returns an instance of class DataParser. Source of data for instruments
    '''

    def getDataParser(self):
        instrumentIds = self.__problem1Solver.getSymbolsToTrade()
        return QuantQuestDataSource(cachedFolderName='historicalData/',
                                    dataSetId=self.__problem1Solver.getTrainingDataSet(),
                                    instrumentIds=instrumentIds)

    '''
    Returns a timedetla object to indicate frequency of updates to features
    Any updates within this frequncy to instruments do not trigger feature updates.
    Consequently any trading decisions that need to take place happen with the same
    frequency
    '''

    def getFrequencyOfFeatureUpdates(self):
        return timedelta(0, 30)  # minutes, seconds

    def getBenchmark(self):
        return None

    '''
    This is a way to use any custom features you might have made.
    Returns a dictionary where
    key: featureId to access this feature (Make sure this doesnt conflict with any of the pre defined feature Ids)
    value: Your custom Class which computes this feature. The class should be an instance of Feature
    Eg. if your custom class is MyCustomFeature, and you want to access this via featureId='my_custom_feature',
    you will import that class, and return this function as {'my_custom_feature': MyCustomFeature}
    '''

    def getCustomFeatures(self):
        return dict(self.__problem1Solver.getCustomFeatures(), **{'problem1_prediction': Problem1PredictionFeature})

    '''
    Returns a dictionary with:
    key: string representing instrument type. Right now INSTRUMENT_TYPE_OPTION, INSTRUMENT_TYPE_STOCK, INSTRUMENT_TYPE_FUTURE
    value: Array of instrument feature config dictionaries
        feature config Dictionary has the following keys:
        featureId: a string representing the type of feature you want to use
        featureKey: {optional} a string representing the key you will use to access the value of this feature.
                    If not present, will just use featureId
        params: {optional} A dictionary with which contains other optional params if needed by the feature
    Example:
    positionConfigDict = {'featureId': 'position'}
    vwapConfigDict = {'featureKey': 'price',
                          'featureId': 'vwap'}
    movingAvg_30Dict = {'featureKey': 'mv_avg_30',
                          'featureId': 'moving_average',
                          'params': {'days': 30}}
    movingAvg_90Dict = {'featureKey': 'mv_avg_90',
                          'featureId': 'moving_average',
                          'params': {'days': 90}}
    return {INSTRUMENT_TYPE_FUTURE: [positionConfigDict, vwapConfigDict],
            INSTRUMENT_TYPE_STOCK: [positionConfigDict, movingAvg_30Dict, movingAvg_90Dict]}

    For each future instrument, you will have features keyed by position and price.
    For each stock instrument, you will have features keyed by position, mv_avg_30, mv_avg_90
    '''

    def getInstrumentFeatureConfigDicts(self):
        stockFeatureConfigs = self.__problem1Solver.getFeatureConfigDicts()
        fairValuePrediction = {'featureKey': 'prediction',
                               'featureId': 'problem1_prediction',
                               'params': {}}
        scoreDict = {'featureKey': 'score',
                     'featureId': 'prob1_score',
                     'params': {'predictionKey': 'prediction',
                                'price': 'FairValue'}}
        sdevDictForExec = {'featureKey': 'sdev_5_for_exec',
                           'featureId': 'moving_sdev',
                           'params': {'period': 5,
                                      'featureName': 'basis'}}
        return {INSTRUMENT_TYPE_STOCK: stockFeatureConfigs + [fairValuePrediction, sdevDictForExec, scoreDict]}

    '''
    Returns an array of market feature config dictionaries
        market feature config Dictionary has the following keys:
        featureId: a string representing the type of feature you want to use
        featureKey: a string representing the key you will use to access the value of this feature.this
        params: A dictionary with which contains other optional params if needed by the feature
    '''

    def getMarketFeatureConfigDicts(self):
        # ADD RELEVANT FEATURES HERE

        # customFeatureDict = {'featureKey': 'custom_mrkt_feature',
        #                      'featureId': 'my_custom_mrkt_feature',
        #                      'params': {'param1': 'value1'}}
        scoreDict = {'featureKey': 'score',
                     'featureId': 'prob1_score',
                     'params': {'price': 'FairValue',
                                'instrument_score_feature': 'score',
                                'benchmark_score_feature': 'benchmark_score'}}
        return [scoreDict]

    '''
    Returns the type of execution system we want to use. Its an implementation of the class ExecutionSystem
    It converts prediction to intended positions for different instruments.
    '''

    def getExecutionSystem(self):
        return QQExecutionSystem(basisEnter_threshold=0.5, basisExit_threshold=0.1,
                                 basisLongLimit=10000, basisShortLimit=10000,
                                 basisCapitalUsageLimit=0.05, basisLotSize=100,
                                 basisLimitType='L', basis_thresholdParam='sdev_5_for_exec',
                                 price=self.getPriceFeatureKey())

    '''
    Returns the type of order placer we want to use. its an implementation of the class OrderPlacer.
    It helps place an order, and also read confirmations of orders being placed.
    For Backtesting, you can just use the BacktestingOrderPlacer, which places the order which you want, and automatically confirms it too.
    '''

    def getOrderPlacer(self):
        return BacktestingOrderPlacer()

    '''
    Returns the amount of lookback data you want for your calculations. The historical market features and instrument features are only
    stored upto this amount.
    This number is the number of times we have updated our features.
    '''

    def getLookbackSize(self):
        return 90

    def getPriceFeatureKey(self):
        return 'basis'


class Problem1PredictionFeature(Feature):
    problem1Solver = None

    @classmethod
    def setProblemSolver(cls, problem1Solver):
        Problem1PredictionFeature.problem1Solver = problem1Solver

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        return Problem1PredictionFeature.problem1Solver.getFairValue(updateNum, time, instrumentManager)
