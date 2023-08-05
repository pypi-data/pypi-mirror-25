"""
JAABA
=====

Tools to work with the classification output from JAABA.
"""

import os

import pandas as pd
from scipy.io import loadmat


def read_behavior_predictions(output_folder, target, behavior):
    """Read JAABA behavior predictions of a movie processed using
    FlyTracker.

    output_folder: path to FlyTracker output folder of a video
    target:        number of the fly as JAABA labeled it (0,...,N)
    behavior:      behavior name of the jab file

    Returns a boolean pandas.Series whose indexes are the frames and the
    truthfulness indicating the behavior prediction.
    """
    foldername = os.path.split(output_folder)[-1]
    scores_filepath = os.path.join(
        output_folder, foldername + '_JAABA', 'scores_' + behavior + '.mat')
    return read_scores(scores_filepath, target)


def read_scores(filename, target):
    """
    Read JAABA behavior predictions into a `pandas.Series`.

    filename: a scores_*.mat file
    target:   number of the fly as JAABA labeled it (0,...,N)

    Returns a boolean pandas.Series whose indexes are the frames and the
    truthfulness indicating the behavior prediction.
    """
    mat = loadmat(filename)
    mdata = mat['allScores']
    scores = {n: mdata[n][0, 0] for n in mdata.dtype.names}
    return pd.Series(scores['postprocessed'][0, target][0], dtype=bool)
