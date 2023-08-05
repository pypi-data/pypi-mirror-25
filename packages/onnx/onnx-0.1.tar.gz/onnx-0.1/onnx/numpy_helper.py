import sys

import numpy as np
from onnx.onnx_pb2 import TensorProto


if sys.byteorder != 'little':
    raise RuntimeError(
        'Numpy helper for tensor/ndarray is not available on big endian '
        'systems yet.')


def to_array(tensor):
    """Converts a tensor def object to a numpy array.

    Inputs:
        tensor: a TensorProto object.
    Returns:
        arr: the converted array.
    """
    if tensor.HasField("segment"):
        raise ValueError(
            "Currently not supporting loading segments.")
    if tensor.data_type == TensorProto.UNDEFINED:
        raise ValueError("The data type is not defined.")
    data_type = tensor.data_type
    dims = tensor.dims
    if tensor.HasField("raw_data"):
        # Raw_bytes support: using frombuffer.
        dtype_map = {
            TensorProto.FLOAT: np.float32,
            TensorProto.UINT8: np.uint8,
            TensorProto.INT8: np.int8,
            TensorProto.UINT16: np.uint16,
            TensorProto.INT16: np.int16,
            TensorProto.INT32: np.int32,
            TensorProto.INT64: np.int64,
            TensorProto.BOOL: np.bool,
            TensorProto.FLOAT16: np.float16,
        }
        if data_type == TensorProto.STRING:
            raise RuntimeError("You cannot use raw bytes for string type.")
        try:
            dtype = dtype_map[tensor.data_type]
        except KeyError:
            # TODO: complete the data type.
            raise RuntimeError(
                "Tensor data type not understood yet: {}".format(str(data_type)))
        return np.frombuffer(
            tensor.raw_data,
            dtype=dtype).reshape(dims)
    else:
        # Conventional fields not using raw bytes.
        if data_type == TensorProto.FLOAT:
            return np.asarray(
                tensor.float_data, dtype=np.float32).reshape(dims)
        elif data_type == TensorProto.UINT8:
            return np.asarray(
                tensor.int32_data, dtype=np.int32).reshape(dims).astype(np.uint8)
        elif data_type == TensorProto.INT8:
            return np.asarray(
                tensor.int32_data, dtype=np.int32).reshape(dims).astype(np.int8)
        elif data_type == TensorProto.UINT16:
            return np.asarray(
                tensor.int32_data, dtype=np.int32).reshape(dims).astype(np.uint16)
        elif data_type == TensorProto.INT16:
            return np.asarray(
                tensor.int32_data, dtype=np.int32).reshape(dims).astype(np.int16)
        elif data_type == TensorProto.INT32:
            return np.asarray(
                tensor.int32_data, dtype=np.int32).reshape(dims)
        elif data_type == TensorProto.INT64:
            return np.asarray(
                tensor.int64_data, dtype=np.int64).reshape(dims)
        elif data_type == TensorProto.STRING:
            raise NotImplementedError("Not implemented.")
        elif data_type == TensorProto.BOOL:
            return np.asarray(
                tensor.int32_data, dtype=np.int32).reshape(dims).astype(np.bool)
        elif data_type == TensorProto.FLOAT16:
            return np.asarray(
                tensor.int32_data, dtype=np.uint16).reshape(dims).view(np.float16)
        else:
            # TODO: complete the data type.
            raise RuntimeError(
                "Tensor data type not understood yet: {}".format(str(data_type)))


def from_array(arr, name=None):
    """Converts a numpy array to a tensor def.

    Inputs:
        arr: a numpy array.
        name: (optional) the name of the tensor.
    Returns:
        tensor_def: the converted tensor def.
    """
    tensor = TensorProto()
    tensor.dims.extend(arr.shape)
    if name:
        tensor.name = name

    dtype_map = {
        np.dtype("float32"): TensorProto.FLOAT,
        np.dtype("uint8"): TensorProto.UINT8,
        np.dtype("int8"): TensorProto.INT8,
        np.dtype("uint16"): TensorProto.UINT16,
        np.dtype("int16"): TensorProto.INT16,
        np.dtype("int32"): TensorProto.INT32,
        np.dtype("int64"): TensorProto.INT64,
        np.dtype("bool"): TensorProto.BOOL,
        np.dtype("float16"): TensorProto.FLOAT16,
    }

    if arr.dtype == np.object:
        # Special care for strings.
        raise NotImplementedError("Need to properly implement string.")
    # For numerical types, directly use numpy raw bytes.
    try:
        dtype = dtype_map[arr.dtype]
    except KeyError:
        raise RuntimeError(
            "Numpy data type not understood yet: {}".format(str(arr.dtype)))
    tensor.data_type = dtype
    tensor.raw_data = arr.tobytes()  # note: tobytes() is only after 1.9.
    
    return tensor
