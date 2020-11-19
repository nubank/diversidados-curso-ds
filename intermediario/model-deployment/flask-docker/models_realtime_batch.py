# Instrucoes:
# 
# 1. Configurar aplicacao Flask:
#    export FLASK_APP=models_realtime_batch.py
#    export FLASK_ENV=development
# 
# 2. Mostrar rotas do app:
#    python -m flask routes
# 
# 3. Rodar app Flask:
#    python -m flask run
#    # default host=localhost=127.0.0.1; port=5000
#    # ou escolhe outros valores, p.ex.: --host=0.0.0.0 --port=8080
#
#    Ou mais geral: python models_realtime_batch.py
# 
# 4. Abrir enderecos no browser
#    (ou rodar no terminal: 'curl ...'; lembrar de usar aspas ou fazer & --> \&)
#    - http://localhost:5000
#    - http://localhost:5000/api/version
#    - http://localhost:5000/api/predict?some_id=my-id&feat1=2&feat2=1
#    - http://localhost:5000/api/predict-batch?some_id=b
#      (IDs de "a" a "z")
#
# 5. Fazendo requisicao POST:
# curl \
#   -X POST \
#   --data '{"feat1": 2, "feat2": 1}' \
#   -H "Content-Type: application/json" \
#   "http://localhost:5000/api/predict-post"
#
# 6. Fazendo rollout:
# curl "http://localhost:5000/api/predict/rollout?some_id=a&feat1=2&feat2=1"
# curl "http://localhost:5000/api/predict/rollout?some_id=d&feat1=2&feat2=1"


from datetime import datetime
import logging
import os
import pickle
import random
from typing import Any, Dict, List

from flask import Flask, request
from gevent.pywsgi import WSGIServer
from pandas import DataFrame, read_csv


# CUR_DIR = os.path.dirname(__file__)
# LOG_FILE = os.path.join(CUR_DIR, 'logs', 'model-app.log')
# logging.basicConfig(filename=LOG_FILE,
#                     level=logging.DEBUG)

logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/')
def hello() -> str:
    return 'Welcome to my model!'


@app.route('/api/version')
def show_version() -> str:
    app.logger.info(request.path)
    return '3.2.1'


# =============================================================================
# REALTIME MODEL
# =============================================================================

def load_realtime_model(model_name: str = 'model.pkl'):
    app.logger.info('Loading model...')
    with open(model_name,'rb') as model:
        return pickle.load(model)


def predict_proba_pickle(model, features: Dict[str, float]) -> List[float]:
    app.logger.info('Getting prediction from model...')
    features_to_model: List[List] = [list(features.values())]
    return model.predict_proba(features_to_model)[0].tolist()


def predict_proba_implemented(features: Dict[str, float]) -> List[float]:
    # Alternative for not loading the model pickle: implement
    # the model inside the code. Not always possible.
    #
    # This is just a dummy code.
    #
    # Returns: [prob. class 1, prob. class 2, prob. class 3]
    app.logger.info('Getting prediction from implemented model in code...')
    predict_proba = [0.0, 0.0, 0.0]
    predict_proba[round(sum(features.values())) % 3] = 1.0
    return predict_proba


def fetch_features_and_perform_feature_engineering(some_id: str) -> Dict[str, float]:
    # This function may take some time to finish.
    #
    # 1. Fetch data from other services/databases
    # ...
    # 2. Perform feature engineering
    # ...
    app.logger.info('Fetching features...')
    return {
      'feat3': 3.3,
      'feat4': 4.4,
    }


model_clf = load_realtime_model()


@app.route('/api/predict')
def predict() -> Dict[str, Any]:

    # Read input
    some_id = request.args.get('some_id', default='', type=str)
    feat1 = request.args.get('feat1', default=0, type=float)
    feat2 = request.args.get('feat2', default=0, type=float)
    features_from_request = {'feat1': feat1, 'feat2': feat2}

    # Get features
    features_external = fetch_features_and_perform_feature_engineering(some_id)

    # Join all features
    features = {**features_from_request, **features_external}

    output = {
      'id': some_id,
      'prediction_probability1': predict_proba_implemented(features),
      'prediction_probability2': predict_proba_pickle(model_clf, features),
      'features': features,
      'run_at': datetime.now().isoformat(),
    }

    app.logger.info({
        'output': output,
        'request.path': request.path,
    })

    return output


@app.route('/api/predict-post', methods=['POST'])
def predict_post() -> Dict[str, Any]:

    # Read input
    params: dict = request.json
    some_id: str = params.get('some_id', '')
    feat1: float = params.get('feat1', 0)
    feat2: float = params.get('feat2', 0)
    features_from_request = {'feat1': feat1, 'feat2': feat2}

    # Get features
    features_external = fetch_features_and_perform_feature_engineering(some_id)

    # Join all features
    features = {**features_from_request, **features_external}

    output = {
      'id': some_id,
      'prediction_probability1': predict_proba_implemented(features),
      'prediction_probability2': predict_proba_pickle(model_clf, features),
      'features': features,
      'run_at': datetime.now().isoformat(),
    }

    app.logger.info({
        'output': output,
        'request.path': request.path,
    })

    return output


# =============================================================================
# BATCH MODEL
# =============================================================================

def read_batch_predictions() -> DataFrame:
    app.logger.info('Reading batch predictions...')
    return read_csv('scores.csv', index_col=0)


batch_predictions = read_batch_predictions()


@app.route('/api/predict-batch')
def predict_batch() -> Dict[str, Any]:
    some_id = request.args.get('some_id', default='', type=str)

    try:
        probs_Series = batch_predictions.loc[some_id, :]
        probs = [probs_Series['prob1'], probs_Series['prob2'], probs_Series['prob3']]
    except KeyError:
        probs = None

    output = {
      'id': some_id,
      'prediction_probability': probs,
      'run_at': datetime.now().isoformat(),
    }

    app.logger.info({
        'output': output,
        'request.path': request.path,
    })

    return output


# =============================================================================
# ROLL OUT MODEL
# =============================================================================

@app.route('/api/predict/rollout')
def predict_rollout() -> dict:

    # Read input
    some_id = request.args.get('some_id', default='', type=str)
    feat1 = request.args.get('feat1', default=0, type=float)
    feat2 = request.args.get('feat2', default=0, type=float)
    features_from_request = {'feat1': feat1, 'feat2': feat2}

    # Get features
    features_external = fetch_features_and_perform_feature_engineering(some_id)

    # Join all features
    features = {**features_from_request, **features_external}

    # Random number based on the ID
    random.seed(hash(some_id))
    random_0_1: float = random.random()

    if random_0_1 < 0.5:
        version = 'v1'
        prediction = predict_proba_implemented(features)
    else:
        version = 'v2'
        prediction = predict_proba_pickle(model_clf, features),

    output = {
      'id': some_id,
      'version': version,
      'prediction': prediction,
      'features': features,
      'run_at': datetime.now().isoformat(),
    }

    app.logger.info({
        'output': output,
        'request.path': request.path,
    })

    return output


# =============================================================================
# START APP
# =============================================================================

if __name__ == '__main__':
    # app.run(debug=True) # Flask + Werkzeug WSGI (not for production)
    app.logger.info('Serving model on port 5000...')
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
