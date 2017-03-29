===============================
D3R Grand Challenge Evaluator
===============================

.. image:: https://pyup.io/repos/github/drugdata/d3r_gcevaluator/shield.svg
     :target: https://pyup.io/repos/github/drugdata/d3r_gcevaluator/
     :alt: Updates


Python based scripts for D3R grand challenge

For more information please visit:

https://drugdesigndata.org/

1, pose prediction:
    The script D3R_GC2_rmsd_calculation.py under folder pose_prediction_rmsd_calculation calculate the RMSDs between submitted ligand and answsers.
    Please check out the front of the script for usage and examples.

2, scoring and free energy predictions:
    The script D3R_GC2_ranking_calculation.py under folder ranking_calculations calculate the ranking related statistics: Kendall's Tau, Spearman's rho for both scoring and free energy submissions, and Pearson's R, RMSE for free energy submissions only. 
    Please check out the front of the script for usage and examples.

Dependencies
------------

* `argparse <https://pypi.python.org/pypi/argparse>`_

Installation
------------

pip install coming soon, but for now

.. code:: bash

   # download or clone repo 
   cd D3R_grandchallenge_evaluator
   make dist
   pip install dist/*.whl

Usage
-----

.. code:: bash

   # Add instructions


License
-------

See LICENSE_

Bugs
-----

Please report them `here <https://github.com/drugdata/D3R_grandchallenge_evaluator/issues>`_


Acknowledgements
----------------

* This work is funded in part by NIH grant 1U01GM111528 from the National Institute of General Medical Sciences

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _LICENSE: https://github.com/drugdata/D3R_grandchallenge_evaluator/blob/master/LICENSE
