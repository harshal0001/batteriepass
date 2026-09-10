"""Catena-X battery passport assembly, Annex XIII conformance and SoH estimation.

Nothing under this package may import ``torch``. Training lives in ``training/``
and the only artefact that crosses the boundary is an ONNX file. See
``scripts/no_torch_in_src.py``, which fails CI if that rule is broken.
"""

__version__ = "0.1.0"
