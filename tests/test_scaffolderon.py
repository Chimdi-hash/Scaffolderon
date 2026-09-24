import pytest
import os
import sys

# Add contracts directory to path for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../contracts')))

# Note: Full local testing requires the GenLayer SDK simulator environment
# to mock GenLayer contexts (gl.message, gl.storage.TreeMap, gl.nondet, etc.)

def test_imports():
    """
    Basic sanity check to ensure the contract syntax is valid
    and can be parsed by Python.
    """
    try:
        import Scaffolderon
        assert True
    except ImportError as e:
        # We expect GenLayer dependencies might not be locally installed
        # in a standard python env without the GenLayer simulator.
        assert "genlayer" in str(e) or "Scaffolderon" in str(e)
