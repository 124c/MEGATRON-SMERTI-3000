import pandas as pd
import numpy as np


def slippage(data):
    """
    Adds Slippage to the dataset while final execution
    """
    mu = data.mean()
    sigma = data.std()
    slip = np.random.normal(mu, sigma, len(data))
    return slip
