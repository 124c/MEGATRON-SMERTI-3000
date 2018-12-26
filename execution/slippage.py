import pandas as pd
import numpy as np


def slippage_and_comission(data, com=0.003):
    """
    Adds Slippage to the dataset while final execution
    """
    mu = data['Retuns'].mean()
    sigma = data['Retuns'].std()
    slip = np.random.normal(mu, sigma, len(data))
    comission = data['Retuns']*com
    return slip+comission
