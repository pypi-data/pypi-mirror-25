from typing import Iterable, Dict
from collections import namedtuple
import json

import numpy as np

FileFormat = namedtuple('FileFormat', ['ext', 'is_', 'save', 'load'])

np_array_ext = '.npy'
np_array = FileFormat(np_array_ext,
                      lambda x: isinstance(x, np.ndarray),
                      lambda name, value: np.save(name + np_array_ext, value),
                      lambda name: np.load(name + np_array_ext))

np_arrays_ext = '.npz'


def np_arrays_save(name: str, value_dict: Dict[str, Iterable]) -> None:
    np.savez_compressed(name + np_arrays_ext, **value_dict)


np_arrays = FileFormat(np_arrays_ext,
                       lambda x: isinstance(x, dict) and all([isinstance(value, Iterable) for value in x.values()]),
                       np_arrays_save,
                       lambda name: np.load(name + np_arrays_ext))

csv_ext = '.csv'
csv_file = FileFormat(csv_ext,
                      lambda x: False,  # never save as such
                      None,
                      lambda name: np.loadtxt(name + csv_ext))

log_ext = '.log'
log_file = FileFormat(log_ext,
                      lambda x: False,
                      None,
                      lambda name: json.load(open(name + log_ext, 'r')))

try:
    import pandas as pd

    pd_ext = '.msg'
    pd_data = FileFormat(pd_ext,
                         lambda x: isinstance(x, pd.DataFrame),
                         lambda name, value: pd.to_msgpack(name + pd_ext, value),
                         lambda name: pd.read_msgpack(name + pd_ext))
except ImportError:
    pd = None
    pd_data = None

formats = {cls.ext: cls for cls in [np_array, np_arrays, pd_data, log_file] if cls is not None}
