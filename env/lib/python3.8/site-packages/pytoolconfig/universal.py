from pathlib import Path

from .pytoolconfig import PyToolConfig, UniversalConfig

universal = PyToolConfig(
    "pytoolconfig", Path("."), UniversalConfig
)  # Documentation purposes
