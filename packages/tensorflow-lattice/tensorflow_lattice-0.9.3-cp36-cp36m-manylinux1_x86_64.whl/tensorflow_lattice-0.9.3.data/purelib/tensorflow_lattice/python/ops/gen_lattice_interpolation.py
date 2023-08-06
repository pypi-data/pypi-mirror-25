"""Python wrappers around TensorFlow ops.

This file is MACHINE GENERATED! Do not edit.
"""

import collections as _collections

from tensorflow.core.framework import op_def_pb2 as _op_def_pb2

# Needed to trigger the call to _set_call_cpp_shape_fn.
from tensorflow.python.framework import common_shapes as _common_shapes

from tensorflow.python.framework import op_def_registry as _op_def_registry
from tensorflow.python.framework import ops as _ops
from tensorflow.python.framework import op_def_library as _op_def_library

def hypercube_gradient(input, weight, grad_wrt_weight, lattice_sizes=None,
                       name=None):
  r"""Computes gradients of HypercubeInterpolation. Returns a dense gradient.

  Inputs
    input: input tensor, `[?, d]`.
    grad_wrt_weight: Gradient with respect to the outputs of this operator,
    `[?, m_0 x m_1 x .. x m_{d - 1}]`

  Outputs
    grad_wrt_input: A gradient tensor, `[?, d]`, with respect to input.

  Args:
    input: A `Tensor`. Must be one of the following types: `float32`, `float64`.
    weight: A `Tensor`. Must have the same type as `input`.
    grad_wrt_weight: A `Tensor`. Must have the same type as `input`.
    lattice_sizes: An optional list of `ints`. Defaults to `[]`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor`. Has the same type as `input`.
  """
  result = _op_def_lib.apply_op("HypercubeGradient", input=input,
                                weight=weight,
                                grad_wrt_weight=grad_wrt_weight,
                                lattice_sizes=lattice_sizes, name=name)
  return result



def hypercube_interpolation(input, lattice_sizes=None, name=None):
  r"""Returns a tensor representing interpolation weights in a hypercube lattice

  interpolation.

  Inputs
    input: 2D tensor, `[?, d]`

  Params
    lattice_sizes: 1D int tensor that contains a lattice size per each dimension,
    [m_0, ..., m_{d - 1}].

  Outputs
    weights: 2D tensor that contains interpolation weights.
    [?, m_0 x m_1 ... x m_{d - 1}].

  Args:
    input: A `Tensor`. Must be one of the following types: `float32`, `float64`.
    lattice_sizes: An optional list of `ints`. Defaults to `[]`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor`. Has the same type as `input`.
  """
  result = _op_def_lib.apply_op("HypercubeInterpolation", input=input,
                                lattice_sizes=lattice_sizes, name=name)
  return result



def simplex_gradient(input, weight, grad_wrt_weight, lattice_sizes=None,
                     name=None):
  r"""Computes gradients of SimplexInterpolation. Returns a dense gradient.

  Inputs
    input: input tensor, `[?, d]`.
    grad_wrt_weight: Gradient with respect to the outputs of this operator,
    `[?, m_0 x m_1 x .. x m_{d - 1}]`

  Outputs
    grad_wrt_input: A gradient tensor, `[?, d]`, with respect to input.

  Args:
    input: A `Tensor`. Must be one of the following types: `float32`, `float64`.
    weight: A `Tensor`. Must have the same type as `input`.
    grad_wrt_weight: A `Tensor`. Must have the same type as `input`.
    lattice_sizes: An optional list of `ints`. Defaults to `[]`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor`. Has the same type as `input`.
  """
  result = _op_def_lib.apply_op("SimplexGradient", input=input, weight=weight,
                                grad_wrt_weight=grad_wrt_weight,
                                lattice_sizes=lattice_sizes, name=name)
  return result



def simplex_interpolation(input, lattice_sizes=None, name=None):
  r"""Returns a tensor representing interpolation weights in a simplex lattice

  interpolation.

  Inputs
    input: 2D tensor, `[?, d]`

  Params
    lattice_sizes: 1D int tensor that contains a lattice size per each dimension,
    [m_0, ..., m_{d - 1}].

  Outputs
    weights: 2D tensor that contains interpolation weights.
    [?, m_0 x m_1 ... x m_{d - 1}].

  Args:
    input: A `Tensor`. Must be one of the following types: `float32`, `float64`.
    lattice_sizes: An optional list of `ints`. Defaults to `[]`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor`. Has the same type as `input`.
  """
  result = _op_def_lib.apply_op("SimplexInterpolation", input=input,
                                lattice_sizes=lattice_sizes, name=name)
  return result


def _InitOpDefLibrary(op_list_proto_bytes):
  op_list = _op_def_pb2.OpList()
  op_list.ParseFromString(op_list_proto_bytes)
  _op_def_registry.register_op_list(op_list)
  op_def_lib = _op_def_library.OpDefLibrary()
  op_def_lib.add_op_list(op_list)
  return op_def_lib


# op {
#   name: "HypercubeGradient"
#   input_arg {
#     name: "input"
#     type_attr: "Dtype"
#   }
#   input_arg {
#     name: "weight"
#     type_attr: "Dtype"
#   }
#   input_arg {
#     name: "grad_wrt_weight"
#     type_attr: "Dtype"
#   }
#   output_arg {
#     name: "grad_wrt_input"
#     type_attr: "Dtype"
#   }
#   attr {
#     name: "Dtype"
#     type: "type"
#     default_value {
#       type: DT_FLOAT
#     }
#     allowed_values {
#       list {
#         type: DT_FLOAT
#         type: DT_DOUBLE
#       }
#     }
#   }
#   attr {
#     name: "lattice_sizes"
#     type: "list(int)"
#     default_value {
#       list {
#       }
#     }
#   }
# }
# op {
#   name: "HypercubeInterpolation"
#   input_arg {
#     name: "input"
#     type_attr: "Dtype"
#   }
#   output_arg {
#     name: "weights"
#     type_attr: "Dtype"
#   }
#   attr {
#     name: "Dtype"
#     type: "type"
#     default_value {
#       type: DT_FLOAT
#     }
#     allowed_values {
#       list {
#         type: DT_FLOAT
#         type: DT_DOUBLE
#       }
#     }
#   }
#   attr {
#     name: "lattice_sizes"
#     type: "list(int)"
#     default_value {
#       list {
#       }
#     }
#   }
# }
# op {
#   name: "SimplexGradient"
#   input_arg {
#     name: "input"
#     type_attr: "Dtype"
#   }
#   input_arg {
#     name: "weight"
#     type_attr: "Dtype"
#   }
#   input_arg {
#     name: "grad_wrt_weight"
#     type_attr: "Dtype"
#   }
#   output_arg {
#     name: "grad_wrt_input"
#     type_attr: "Dtype"
#   }
#   attr {
#     name: "Dtype"
#     type: "type"
#     default_value {
#       type: DT_FLOAT
#     }
#     allowed_values {
#       list {
#         type: DT_FLOAT
#         type: DT_DOUBLE
#       }
#     }
#   }
#   attr {
#     name: "lattice_sizes"
#     type: "list(int)"
#     default_value {
#       list {
#       }
#     }
#   }
# }
# op {
#   name: "SimplexInterpolation"
#   input_arg {
#     name: "input"
#     type_attr: "Dtype"
#   }
#   output_arg {
#     name: "weights"
#     type_attr: "Dtype"
#   }
#   attr {
#     name: "Dtype"
#     type: "type"
#     default_value {
#       type: DT_FLOAT
#     }
#     allowed_values {
#       list {
#         type: DT_FLOAT
#         type: DT_DOUBLE
#       }
#     }
#   }
#   attr {
#     name: "lattice_sizes"
#     type: "list(int)"
#     default_value {
#       list {
#       }
#     }
#   }
# }
_op_def_lib = _InitOpDefLibrary(b"\n\242\001\n\021HypercubeGradient\022\016\n\005input\"\005Dtype\022\017\n\006weight\"\005Dtype\022\030\n\017grad_wrt_weight\"\005Dtype\032\027\n\016grad_wrt_input\"\005Dtype\"\031\n\005Dtype\022\004type\032\0020\001:\006\n\0042\002\001\002\"\036\n\rlattice_sizes\022\tlist(int)\032\002\n\000\nu\n\026HypercubeInterpolation\022\016\n\005input\"\005Dtype\032\020\n\007weights\"\005Dtype\"\031\n\005Dtype\022\004type\032\0020\001:\006\n\0042\002\001\002\"\036\n\rlattice_sizes\022\tlist(int)\032\002\n\000\n\240\001\n\017SimplexGradient\022\016\n\005input\"\005Dtype\022\017\n\006weight\"\005Dtype\022\030\n\017grad_wrt_weight\"\005Dtype\032\027\n\016grad_wrt_input\"\005Dtype\"\031\n\005Dtype\022\004type\032\0020\001:\006\n\0042\002\001\002\"\036\n\rlattice_sizes\022\tlist(int)\032\002\n\000\ns\n\024SimplexInterpolation\022\016\n\005input\"\005Dtype\032\020\n\007weights\"\005Dtype\"\031\n\005Dtype\022\004type\032\0020\001:\006\n\0042\002\001\002\"\036\n\rlattice_sizes\022\tlist(int)\032\002\n\000")
