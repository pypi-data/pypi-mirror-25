import logging

from sklearn.base import BaseEstimator
import holtwinters
from lore.util import timed


class HoltWinters(BaseEstimator):

  def __init__(self, periodicity, forecasts, **kwargs):
    super(HoltWinters, self).__init__()
    self.periodicity = periodicity
    self.forecasts = forecasts
    self.kwargs = kwargs

  @timed(logging.INFO)
  def predict(self, X):
    return holtwinters.additive(X, self.periodicity, self.forecasts, **self.kwargs)
    