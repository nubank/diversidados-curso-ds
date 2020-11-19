# Versao simples de processamento batch:
# EDITOR=VIM crontab -e
#
# * * * * 1-5 /path/to/python3 /path/to/model-scores.py
#
# crontab -l  # list
# crontab -r  # remove

import logging
import os
from pathlib import Path
import pickle
from string import ascii_lowercase

import pandas as pd
from sklearn.datasets import load_iris

CUR_DIR = os.path.dirname(__file__)
LOG_FILE = os.path.join(CUR_DIR, 'model-scores.log')
logging.basicConfig(filename=LOG_FILE,
                    level=logging.DEBUG,
                    format='%(asctime)s [%(name)s:%(levelname)s] %(message)s',
                    # default: logging.BASIC_FORMAT ('%(levelname)s:%(name)s:%(message)s')
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)

PATH = Path(CUR_DIR)  # Path.cwd()
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
