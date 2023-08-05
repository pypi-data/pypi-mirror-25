from ._dataset import Dataset
from ._db import connect
from ._helpers import clear
from . import utils


def load(dataset_title):
    return Dataset(dataset_title)


__all__ = [load, connect, clear]
