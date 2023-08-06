conx
====

Deep Learning for Simple Folk
-----------------------------

Built in Python 3 on Keras 2.

|CircleCI| |codecov| |Documentation Status| |PyPI version|

Read the documentation at
`conx.readthedocs.io <http://conx.readthedocs.io/>`__

Ask questions on the mailing list:
`conx-users <https://groups.google.com/forum/#!forum/conx-users>`__

Implements Deep Learning neural network algorithms using a simple
interface with easy visualizations and useful analytical. Built on top
of Keras, which can use either
`TensorFlow <https://www.tensorflow.org/>`__,
`Theano <http://www.deeplearning.net/software/theano/>`__, or
`CNTK <https://www.cntk.ai/pythondocs/>`__.

The network is specified to the constructor by providing sizes. For
example, Network("XOR", 2, 5, 1) specifies a network named "XOR" with a
2-node input layer, 5-unit hidden layer, and a 1-unit output layer.

Example
-------

Computing XOR via a target function:

.. code:: python

    from conx import Network, SGD

    dataset = [[[0, 0], [0]],
               [[0, 1], [1]],
               [[1, 0], [1]],
               [[1, 1], [0]]]

    net = Network("XOR", 2, 5, 1, activation="sigmoid")
    net.set_dataset(dataset)
    net.compile(error='mean_squared_error',
                optimizer=SGD(lr=0.3, momentum=0.9))
    net.train(2000, report_rate=10, accuracy=1)
    net.test()

Creates dynamic, rendered visualizations like this:

Install
-------

``conx`` requires Python3, and some other Python modules that are
installed automatically with pip.

**Note**: you may need to use pip3, or admin privileges (eg, sudo), or a
user environment.

.. code:: bash

    pip install conx -U

You will need to decide whether to use Theano, TensorFlow, or CNTK. Pick
one. See
`docs.microsoft.com <https://docs.microsoft.com/en-us/cognitive-toolkit/Setup-CNTK-on-your-machine>`__
for installing CNTK on Windows or Linux. All platforms can also install
either of the others using pip:

.. code:: bash

    pip install theano

or

.. code:: bash

    pip install tensorflow

On MacOS, you may also need to render the SVG visualizations:

.. code:: bash

    brew install cairo

Use with Jupyter Notebooks
~~~~~~~~~~~~~~~~~~~~~~~~~~

To use the Network.dashboard() and camera functions, you will need to
install and enable ``ipywidgets``:

With pip:

.. code:: bash

    pip install ipywidgets
    jupyter nbextension enable --py widgetsnbextension

With conda

.. code:: bash

    conda install -c conda-forge ipywidgets

Installing **ipywidgets** with conda will also enable the extension for
you.

Changing Keras Backends
~~~~~~~~~~~~~~~~~~~~~~~

To use a Keras backend other than TensorFlow, edit (or create)
``~/.keras/kerson.json``, like:

.. code:: json

    {
        "backend": "theano",
        "image_data_format": "channels_last",
        "epsilon": 1e-07,
        "floatx": "float32"
    }

Examples
--------

See the `notebooks
folder <https://github.com/Calysto/conx/tree/master/notebooks>`__ and
the `documentation <http://conx.readthedocs.io/en/latest/>`__ for
additional examples.

.. |CircleCI| image:: https://circleci.com/gh/Calysto/conx/tree/master.svg?style=svg
   :target: https://circleci.com/gh/Calysto/conx/tree/master
.. |codecov| image:: https://codecov.io/gh/Calysto/conx/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/Calysto/conx
.. |Documentation Status| image:: https://readthedocs.org/projects/conx/badge/?version=latest
   :target: http://conx.readthedocs.io/en/latest/?badge=latest
.. |PyPI version| image:: https://badge.fury.io/py/conx.svg
   :target: https://badge.fury.io/py/conx


