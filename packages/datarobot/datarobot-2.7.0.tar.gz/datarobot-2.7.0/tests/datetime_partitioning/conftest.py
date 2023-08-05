import pytest

from datarobot import (BacktestSpecification, DatetimeModel, DatetimePartitioning,
                       DatetimePartitioningSpecification, Project, enums)
from datarobot.utils import parse_time


@pytest.fixture
def holdout_start_date():
    return parse_time('2015-12-10T19:00:00.000000Z')


@pytest.fixture
def datetime_partition_without_holdout_server_data(project_id):
    return {
        'primaryTrainingEndDate': None,
        'holdoutRowCount': 0,
        'backtests': [
            {
                'index': 0,
                'validationRowCount': 108,
                'primaryTrainingDuration': 'P0Y0M48DT0H5M36S',
                'primaryTrainingEndDate': '2014-01-07T22:44:23.000000Z',
                'availableTrainingStartDate': '2013-11-20T22:38:47.000000Z',
                'primaryTrainingStartDate': '2013-11-20T22:38:47.000000Z',
                'validationEndDate': '2014-01-12T22:44:23.000000Z',
                'availableTrainingDuration': 'P0Y0M48DT0H5M36S',
                'availableTrainingRowCount': 4168,
                'gapEndDate': '2014-01-07T22:44:23.000000Z',
                'validationDuration': 'P5D',
                'gapStartDate': '2014-01-07T22:44:23.000000Z',
                'availableTrainingEndDate': '2014-01-07T22:44:23.000000Z',
                'primaryTrainingRowCount': 4168,
                'validationStartDate': '2014-01-07T22:44:23.000000Z',
                'totalRowCount': 4276,
                'gapRowCount': 0,
                'gapDuration': 'P0Y0M0D'
            }
        ],
        'availableTrainingDuration': 'P0Y0M53DT0H5M36S',
        'availableTrainingRowCount': 4276,
        'gapEndDate': None,
        'partitioningWarnings': [],
        'primaryTrainingRowCount': 0,
        'holdoutStartDate': None,
        'datetimePartitionColumn': 'Timestamp',
        'dateFormat': '%Y-%m-%d %H:%M:%S',
        'numberOfBacktests': 1,
        'availableTrainingStartDate': '2013-11-20T22:38:47.000000Z',
        'primaryTrainingStartDate': None,
        'holdoutEndDate': None,
        'gapStartDate': None,
        'totalRowCount': 4276,
        'gapRowCount': 0,
        'primaryTrainingDuration': 'P0Y0M0D',
        'holdoutDuration': 'P0Y0M0D',
        'gapDuration': 'P0Y0M0D',
        'autopilotDataSelectionMethod': 'duration',
        'validationDuration': 'P5D',
        'projectId': project_id,
        'availableTrainingEndDate': '2014-01-12T22:44:23.000000Z'
    }


@pytest.fixture
def datetime_partition_server_data(project_id, holdout_start_date):
    return {
        'primaryTrainingEndDate': '2015-12-10T19:00:00.000000Z',
        'primaryTrainingDuration': 'P0Y1M0D',
        'backtests': [
            {
                'primaryTrainingEndDate': '2015-11-26T19:00:00.000000Z',
                'primaryTrainingDuration': 'P0Y1M0D',
                'index': 0,
                'availableTrainingStartDate': '2015-06-08T20:00:00.000000Z',
                'primaryTrainingStartDate': '2015-10-26T19:00:00.000000Z',
                'validationEndDate': '2015-12-10T19:00:00.000000Z',
                'availableTrainingDuration': 'P0Y0M170DT23H0M0S',
                'validationDuration': 'P14D',
                'gapStartDate': '2015-11-26T19:00:00.000000Z',
                'availableTrainingEndDate': '2015-11-26T19:00:00.000000Z',
                'validationStartDate': '2015-11-26T19:00:00.000000Z',
                'gapEndDate': '2015-11-26T19:00:00.000000Z',
                'gapDuration': 'P0Y0M0D'
            }
        ],
        'datetimePartitionColumn': 'dates',
        'dateFormat': '%Y-%m-%d %H:%M:%S',
        'projectId': project_id,
        'availableTrainingStartDate': '2015-06-08T20:00:00.000000Z',
        'primaryTrainingStartDate': '2015-11-10T19:00:00.000000Z',
        'holdoutEndDate': '2015-12-24T19:00:00.000000Z',
        'validationDuration': 'P14D',
        'availableTrainingDuration': 'P0Y0M184DT23H0M0S',
        'numberOfBacktests': 1,
        'gapStartDate': '2015-12-10T19:00:00.000000Z',
        'availableTrainingEndDate': '2015-12-10T19:00:00.000000Z',
        'holdoutStartDate': holdout_start_date.isoformat(),
        'gapEndDate': '2015-12-10T19:00:00.000000Z',
        'holdoutDuration': 'P14D',
        'gapDuration': 'P0Y0M0D',
        'autopilotDataSelectionMethod': 'rowCount'
    }


@pytest.fixture
def datetime_partition_after_target_server_data(project_id, holdout_start_date):
    return {
        'primaryTrainingEndDate': '2015-12-10T19:00:00.000000Z',
        'primaryTrainingDuration': 'P0Y1M0D',
        'primaryTrainingRowCount': 100,
        'backtests': [
            {
                'primaryTrainingEndDate': '2015-11-26T19:00:00.000000Z',
                'primaryTrainingDuration': 'P0Y1M0D',
                'primaryTrainingRowCount': 100,
                'index': 0,
                'availableTrainingStartDate': '2015-06-08T20:00:00.000000Z',
                'primaryTrainingStartDate': '2015-10-26T19:00:00.000000Z',
                'validationEndDate': '2015-12-10T19:00:00.000000Z',
                'availableTrainingDuration': 'P0Y0M170DT23H0M0S',
                'availableTrainingRowCount': 100,
                'validationDuration': 'P14D',
                'validationRowCount': 100,
                'gapStartDate': '2015-11-26T19:00:00.000000Z',
                'availableTrainingEndDate': '2015-11-26T19:00:00.000000Z',
                'validationStartDate': '2015-11-26T19:00:00.000000Z',
                'gapEndDate': '2015-11-26T19:00:00.000000Z',
                'gapDuration': 'P0Y0M0D',
                'gapRowCount': 100,
                'totalRowCount': 100
            }
        ],
        'datetimePartitionColumn': 'dates',
        'dateFormat': '%Y-%m-%d %H:%M:%S',
        'projectId': project_id,
        'availableTrainingStartDate': '2015-06-08T20:00:00.000000Z',
        'primaryTrainingStartDate': '2015-11-10T19:00:00.000000Z',
        'holdoutEndDate': '2015-12-24T19:00:00.000000Z',
        'validationDuration': 'P14D',
        'availableTrainingDuration': 'P0Y0M184DT23H0M0S',
        'availableTrainingRowCount': 100,
        'numberOfBacktests': 1,
        'gapStartDate': '2015-12-10T19:00:00.000000Z',
        'availableTrainingEndDate': '2015-12-10T19:00:00.000000Z',
        'holdoutStartDate': holdout_start_date.isoformat(),
        'gapEndDate': '2015-12-10T19:00:00.000000Z',
        'holdoutDuration': 'P14D',
        'holdoutRowCount': 100,
        'gapDuration': 'P0Y0M0D',
        'gapRowCount': 100,
        'totalRowCount': 100,
        'autopilotDataSelectionMethod': 'rowCount'
    }


@pytest.fixture
def datetime_partition(datetime_partition_server_data):
    return DatetimePartitioning.from_server_data(datetime_partition_server_data)


@pytest.fixture
def datetime_partition_spec(datetime_partition_server_data, holdout_start_date):
    backtest_data = datetime_partition_server_data['backtests'][0]
    return DatetimePartitioningSpecification(
        datetime_partition_server_data['datetimePartitionColumn'],
        autopilot_data_selection_method=enums.DATETIME_AUTOPILOT_DATA_SELECTION_METHOD.ROW_COUNT,
        validation_duration=datetime_partition_server_data['validationDuration'],
        holdout_start_date=holdout_start_date,
        holdout_duration=datetime_partition_server_data['holdoutDuration'],
        gap_duration=datetime_partition_server_data['gapDuration'],
        number_of_backtests=datetime_partition_server_data['numberOfBacktests'],
        backtests=[BacktestSpecification(backtest_data['index'], backtest_data['gapDuration'],
                                         parse_time(backtest_data['validationStartDate']),
                                         backtest_data['validationDuration']
                                         )]
    )


@pytest.fixture
def datetime_project_server_data(project_id):
    return {
        'id': project_id,
        'projectName': 'Untitled Project',
        'fileName': 'special_date_kickcars.csv',
        'stage': 'modeling',
        'autopilotMode': 0,
        'created': '2017-01-05T17:13:51.257353Z',
        'target': 'y',
        'metric': 'LogLoss',
        'partition': {
            'datetimeCol': None,
            'cvMethod': 'datetime',
            'datetimePartitionColumn': 'Purch\xc3\xa4Date',
            'validationPct': None,
            'reps': None,
            'cvHoldoutLevel': None,
            'holdoutLevel': None,
            'userPartitionCol': None,
            'validationType': 'TVH',
            'trainingLevel': None,
            'partitionKeyCols': None,
            'holdoutPct': None,
            'validationLevel': None
        },
        'recommender': {
            'recommenderItemId': None,
            'isRecommender': None,
            'recommenderUserId': None
        },
        'advancedOptions': {
            'responseCap': False,
            'downsampledMinorityRows': None,
            'downsampledMajorityRows': None,
            'blueprintThreshold': 3,
            'seed': None,
            'weights': None,
            'smartDownsampled': False,
            'majorityDownsamplingRate': None
        },
        'positiveClass': 1,
        'maxTrainPct': 78.125,
        'holdoutUnlocked': False,
        'targetType': 'Binary'
    }


@pytest.fixture
def datetime_project(datetime_project_server_data):
    return Project.from_server_data(datetime_project_server_data)


@pytest.fixture
def datetime_model_server_data(project_id):
    return {
        'featurelistId': '586ef743ccf94e7d7310c288',
        'processes': [
            'Ordinal encoding of categorical variables',
            'Missing Values Imputed',
            'Gradient Boosted Trees Classifier'
        ],
        'featurelistName': 'Informative Features',
        'backtests': [
            {
                'index': 0,
                'score': 0.7,
                'status': 'COMPLETED',
                'training_start_date': '2015-10-26T19:00:00.000000Z',
                'training_duration': 'P0Y1M0D',
                'training_row_count': 880,
                'training_end_date': '2015-11-26T19:00:00.000000Z'
            },
            {
                'index': 1,
                'score': 0.4,
                'status': 'COMPLETED',
                'training_start_date': '2015-10-26T19:00:00.000000Z',
                'training_duration': 'P0Y1M0D',
                'training_row_count': 880,
                'training_end_date': '2015-11-26T19:00:00.000000Z'
            },
            {
                'index': 1,
                'score': None,
                'status': 'BOUNDARIES_EXCEEDED',
                'training_start_date': None,
                'training_duration': None,
                'training_row_count': None,
                'training_end_date': None
            }
        ],
        'modelType': 'Gradient Boosted Trees Classifier',
        'modelCategory': 'model',
        'projectId': project_id,
        'dataSelectionMethod': 'rowCount',
        'samplePct': None,
        'holdoutStatus': 'COMPLETED',
        'trainingStartDate': None,
        'metrics': {
            'AUC': {
                'backtesting': None,
                'holdout': None,
                'backtestingScores': [0.3, 0.23, None],
                'crossValidation': None,
                'validation': 0.75862
            },
            'Rate@Top5%': {
                'backtesting': None,
                'holdout': None,
                'backtestingScores': [1.0, 2.5, None],
                'crossValidation': None,
                'validation': 0.75
            },
            'Rate@TopTenth%': {
                'backtesting': None,
                'holdout': None,
                'backtestingScores': [1.223, 1.23, None],
                'crossValidation': None,
                'validation': 1
            },
            'RMSE': {
                'backtesting': None,
                'holdout': None,
                'backtestingScores': [1.5, 0.2, None],
                'crossValidation': None,
                'validation': 0.3721
            },
            'LogLoss': {
                'backtesting': None,
                'holdout': None,
                'backtestingScores': [0.7, 0.4, None],
                'crossValidation': None,
                'validation': 0.46308
            },
            'FVE Binomial': {
                'backtesting': None,
                'holdout': None,
                'backtestingScores': [0.9, 0.8, None],
                'crossValidation': None,
                'validation': 0.1381
            },
            'Gini Norm': {
                'backtesting': None,
                'holdout': None,
                'backtestingScores': [0.4, 0.3, None],
                'crossValidation': None,
                'validation': 0.51724
            },
            'Rate@Top10%': {
                'backtesting': None,
                'holdout': None,
                'backtestingScores': [0.5, 0.4, None],
                'crossValidation': None,
                'validation': 0.84615
            }
        },
        'trainingDuration': None,
        'trainingRowCount': 880,
        'holdoutScore': None,
        'trainingInfo': {
            'predictionTrainingDuration': 'P0Y1M0D',
            'holdoutTrainingStartDate': '2015-10-26T19:00:00.000000Z',
            'predictionTrainingStartDate': '2015-10-26T19:00:00.000000Z',
            'holdoutTrainingDuration': 'P0Y1M0D',
            'predictionTrainingRowCount': 880,
            'holdoutTrainingEndDate': '2015-12-10T19:00:00.000000Z',
            'predictionTrainingEndDate': '2015-12-10T19:00:00.000000Z',
            'holdoutTrainingRowCount': 880
        },
        'isFrozen': False,
        'blueprintId': '588d02115164b77809d1223820c8933f',
        'timeWindowSamplePct': None,
        'trainingEndDate': None,
        'id': '586ef75cccf94e7da010c294'
    }


@pytest.fixture
def datetime_start_end_model_server_data(datetime_model_server_data):
    final = dict(datetime_model_server_data)
    final['dataSelectionMethod'] = 'selectedDateRange'
    final['trainingRowCount'] = None
    final['trainingStartDate'] = '2015-10-26T19:00:00.000000Z'
    final['trainingEndDate'] = '2015-12-10T19:00:00.000000Z'
    final['timeWindowSamplePct'] = 50
    return final


@pytest.fixture
def datetime_model(datetime_model_server_data):
    return DatetimeModel.from_server_data(datetime_model_server_data)


@pytest.fixture
def datetime_model_job_server_data(project_id):
    body = {
        'status': 'inprogress',
        'processes': [
            'One-Hot Encoding',
            'Bernoulli Naive Bayes classifier (scikit-learn)',
            'Missing Values Imputed',
            'Gaussian Naive Bayes classifier (scikit-learn)',
            'Naive Bayes combiner classifier',
            'Calibrate predictions'
        ],
        'projectId': project_id,
        'samplePct': None,
        'modelType': 'Gradient Boosted Trees Classifier',
        'featurelistId': '586ef743ccf94e7d7310c288',
        'modelCategory': 'model',
        'blueprintId': '588d02115164b77809d1223820c8933f',
        'id': '1'
    }
    return body
