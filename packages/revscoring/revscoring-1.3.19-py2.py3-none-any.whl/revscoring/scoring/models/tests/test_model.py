from nose.tools import eq_

from ....features import Feature
from ..model import Classifier, Learned, Model


def test_model():
    m = Model([Feature("foo")], version="0.0.1")

    eq_(m.info.lookup('version'), "0.0.1")


def test_from_config():
    config = {
        'scorer_models': {
            'test': {
                'module': "nose.tools.eq_"
            }
        }
    }
    model = Model.from_config(config, 'test')
    eq_(model, eq_)


def test_learned_model():
    model = Learned([Feature("foo")])
    eq_(model.trained, None)


def test_classifier():
    model = Classifier([Feature("foo")], [True, False])
    assert 'statustics' not in model.info
