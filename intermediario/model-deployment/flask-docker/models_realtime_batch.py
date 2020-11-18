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

from datetime import datetime
import pickle
from typing import Any, Dict, List

from flask import Flask, request
from gevent.pywsgi import WSGIServer
from pandas import DataFrame, read_csv


app = Flask(__name__)


@app.route('/')
def hello() -> str:
    return 'Welcome to my model!'


@app.route('/api/version')
def show_version() -> str:
    return '3.2.1'


# =============================================================================
# REALTIME MODEL
# =============================================================================

def load_realtime_model(model_name: str = 'model.pkl'):
    with open(model_name,'rb') as model:
        return pickle.load(model)


def predict_proba_pickle(model, features: Dict[str, float]) -> List[float]:
    features_to_model: List[List] = [list(features.values())]
    return model.predict_proba(features_to_model)[0].tolist()


def predict_proba_implemented(features: Dict[str, float]) -> List[float]:
    # Alternative for not loading the model pickle: implement
    # the model inside the code. Not always possible.
    #
    # Returns: [prob. class 1, prob. class 2, prob. class 3]
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
    return {
      'feat3': 3.3,
      'feat4': 4.4,
    }


print('Loading realtime model...')
model_clf = load_realtime_model()
print('Done!')


@app.route('/api/predict')
def predict() -> Dict[str, Any]:
    some_id = request.args.get('some_id', default='', type=str)

    feat1 = request.args.get('feat1', default=0, type=float)
    feat2 = request.args.get('feat2', default=0, type=float)
    features_from_endpoint = {'feat1': feat1, 'feat2': feat2}

    features_external = fetch_features_and_perform_feature_engineering(some_id)

    features = {**features_from_endpoint, **features_external}

    return {
      'id': some_id,
      'prediction_probability1': predict_proba_implemented(features),
      'prediction_probability2': predict_proba_pickle(model_clf, features),
      'features': features,
      'run_at': datetime.now().isoformat(),
    }


# =============================================================================
# BATCH MODEL
# =============================================================================

def read_batch_predictions() -> DataFrame:
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
    return {
      'id': some_id,
      'prediction_probability': probs,
      'run_at': datetime.now().isoformat(),
    }


# =============================================================================
# START APP
# =============================================================================

if __name__ == '__main__':
    # app.run(debug=True) # Flask + Werkzeug WSGI (not for production)
    print('Serving model on port 5000...')
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
