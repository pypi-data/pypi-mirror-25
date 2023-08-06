import os

import pytest

import aospy


def test_tutorial_notebook():
    pytest.importorskip('IPython')
    pytest.importorskip('matplotlib')
    pytest.importorskip('runipy')

    from IPython.nbformat.current import read
    from runipy.notebook_runner import NotebookRunner

    rootdir = os.path.join(aospy.__path__[0], 'examples')
    with open(os.path.join(rootdir, 'tutorial.ipynb')) as nb:
        notebook = read(nb, 'json')
    r = NotebookRunner(notebook)
    r.run_notebook()
    r.shutdown_kernel()
