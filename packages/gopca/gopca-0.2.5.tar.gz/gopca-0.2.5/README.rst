..
    Copyright (c) 2015, 2016 Florian Wagner
    
    This file is part of GO-PCA.
    
    GO-PCA is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License, Version 3,
    as published by the Free Software Foundation.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.

GO-PCA
======

| |pypi| |versions| |license|

===========  =================================================
**latest**   |travis-latest| |codecov-latest| |docs-latest|
**develop**  |travis-develop| |codecov-develop| |docs-develop|
===========  =================================================

GO-PCA (`Wagner, 2015`__) is an unsupervised method to **explore gene
expression data using prior knowledge**. This is a free and open-source
implementation of GO-PCA in Python.

__ go_pca_paper_

Briefly, GO-PCA combines `principal component analysis (PCA)`__  with
`nonparametric GO enrichment analysis`__ in order to generate **signatures**,
i.e., small sets of genes that are both strongly correlated and closely
functionally related. It then visualizes the expression profiles of all
signatures in a **signature matrix**, designed to serve as a systematic and
easily interpretable representation of biologically relevant expression
patterns.

__ pca_
__ go_enrich_

.. _go_pca_paper: https://dx.doi.org/10.1371/journal.pone.0143196
.. _pca: https://en.wikipedia.org/wiki/Principal_component_analysis
.. _go_enrich: https://dx.doi.org/10.1186/1471-2105-10-48

Links
-----

- `Demos <https://github.com/flo-compbio/gopca-demos>`_
- `Documentation <https://gopca.readthedocs.org/en/latest>`_
- `Download of GO-derived gene sets <https://www.dropbox.com/sh/m0r7uqnfdr5x0xu/AADqqJ-8VzPchBRhDm50QxWaa?dl=0>`_
- `PLoS One paper <https://dx.doi.org/10.1371/journal.pone.0143196>`_

Support and Development
-----------------------

- For feature requests and bug reports, please create an `issue`__ on GitHub.
- For technical questions, please feel free to `email`__.
- If you want to contribute code to GO-PCA, please `email`__ and/or create a
  pull request on GitHub.
- For a list of the latest changes, please see the
  `Changelog <CHANGELOG.rst>`_.

__ github_issue_
__ email_
__ email_

.. _github_issue: https://github.com/flo-compbio/gopca/issues
.. _email: mailto:florian.wagner@duke.edu

How to Cite GO-PCA
------------------

If you use GO-PCA in your research, please cite `Wagner (PLoS One, 2015)`__

__ wagner_pone_

.. _wagner_pone: https://dx.doi.org/10.1371/journal.pone.0143196

Copyright and License
---------------------

Copyright (c) 2015, 2016 Florian Wagner

::

  GO-PCA is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License, Version 3,
  as published by the Free Software Foundation.
  
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
  
  You should have received a copy of the GNU General Public License
  along with this program. If not, see <http://www.gnu.org/licenses/>.

.. |pypi| image:: https://img.shields.io/pypi/v/gopca.svg
    :target: https://pypi.python.org/pypi/gopca
    :alt: PyPI version

.. |versions| image:: https://img.shields.io/pypi/pyversions/gopca.svg
    :target: https://pypi.python.org/pypi/gopca
    :alt: Python versions supported

.. |license| image:: https://img.shields.io/pypi/l/gopca.svg
    :target: https://pypi.python.org/pypi/gopca
    :alt: License

.. |travis-latest| image:: https://travis-ci.org/flo-compbio/gopca.svg?branch=master
    :alt: Build Status (master branch)
    :scale: 100%
    :target: https://travis-ci.org/flo-compbio/gopca

.. |travis-develop| image:: https://travis-ci.org/flo-compbio/gopca.svg?branch=develop
    :alt: Build Status (develop branch)
    :scale: 100%
    :target: https://travis-ci.org/flo-compbio/gopca

.. |codecov-latest| image:: https://codecov.io/github/flo-compbio/gopca/coverage.svg?branch=master
    :alt: Coverage (master branch)
    :target: https://codecov.io/github/flo-compbio/gopca?branch=master

.. |codecov-develop| image:: https://codecov.io/github/flo-compbio/gopca/coverage.svg?branch=develop
    :alt: Coverage (develop branch)
    :target: https://codecov.io/github/flo-compbio/gopca?branch=develop

.. |docs-latest| image:: https://readthedocs.org/projects/gopca/badge/?version=latest
    :alt: Documentation Status (master branch)
    :scale: 100%
    :target: https://gopca.readthedocs.org/en/latest

.. |docs-develop| image:: https://readthedocs.org/projects/gopca/badge/?version=develop
    :alt: Documentation Status (develop branch)
    :scale: 100%
    :target: https://gopca.readthedocs.org/en/develop

