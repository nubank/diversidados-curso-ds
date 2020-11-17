from functools import partial
import logging

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator, PythonVirtualenvOperator
from airflow.utils.dates import days_ago


logger = logging.getLogger("airflow.task")


def fetch_features(logger=logger):
    logger.info('Fetching features...')
    logger.info('(fetch features and save somewhere, e.g., S3)')
    logger.info('Done!')
    return


def feature_engineering(logger=logger):
    logger.info('Performing feature engineering...')
    logger.info('(read fetched features, perform feature engineering and save somewhere, e.g., S3)')
    logger.info('Done!')
    return


def batch_scoring(logger=logger):
    from pathlib import Path
    import pickle
    from string import ascii_lowercase
    
    import pandas as pd
    from sklearn.datasets import load_iris


    PATH = Path(Path.home(), 'Desktop/model-deployment/')
    MODEL_FNAME = PATH / 'model.pkl'
    OUTPUT_FNAME = PATH / 'scores.csv'

    # Load model pickle
    logger.info(f'Reading model from {MODEL_FNAME}...')
    with MODEL_FNAME.open(mode='rb') as model:
        clf = pickle.load(model)
    logger.info('Done!')
    
    # Get "random" features and IDs
    logger.info('Reading features...')
    X, y = load_iris(return_X_y=True)
    ids = list(ascii_lowercase)
    X = X[:len(ids), :]
    logger.info('Done!')
    
    # Get class probabilities
    logger.info('Calculating class probabilities...')
    probs = clf.predict_proba(X)
    logger.info('Done!')
    
    # Create DataFrame
    logger.info('Creating pandas.DataFrame...')
    df = pd.DataFrame(probs,
                      index=ids,
                      columns=['prob1', 'prob2', 'prob3'])
    logger.info('Done!')
    
    # Save scores
    logger.info(f'Saving scores in {OUTPUT_FNAME}...')
    with open(OUTPUT_FNAME, 'w') as scores:
        df.to_csv(scores)
    logger.info('Done!')

    return


dag = DAG('batch_model',
          description='Run batch model',
          schedule_interval='@daily',
          start_date=days_ago(1),
          )

begin_operator = DummyOperator(task_id='begin_execution', dag=dag)

random_operator = BashOperator(
    task_id='bash_op',
    bash_command='echo "Diretorio atual = $(pwd)"',
    dag=dag,
)

fetch_features_op = PythonOperator(
    task_id='fetch_features',
    python_callable=fetch_features,
    dag=dag,
)

feature_engineering_op = PythonOperator(
    task_id='feature_engineering',
    python_callable=feature_engineering,
    dag=dag,
)

# batch_model_op = PythonVirtualenvOperator(
#     task_id='score_ids',
#     python_callable=batch_scoring,
#     python_version='3.6',
#     requirements=['scikit-learn', 'pandas'],
#     dag=dag,
# )
# 
# Error: def batch_scoring(logger=logger):\nNameError: name \'logger\' is not defined

batch_model_op = PythonOperator(
    task_id='score_ids',
    python_callable=batch_scoring,
    dag=dag,
)

end_operator = DummyOperator(task_id='finish_execution', dag=dag)

(begin_operator
 >> fetch_features_op
 >> feature_engineering_op
 >> [random_operator, batch_model_op]
 >> end_operator)
