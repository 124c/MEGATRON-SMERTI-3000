import pandas as pd
import numpy as np


def slippage_and_comission(data, com=0.003):
    """
    Adds Slippage to the dataset while final execution
    """
    mu = data.mean()
    sigma = data.std()
    slip = np.random.normal(mu, sigma, len(data))
    comission = data*com
    return slip+comission
