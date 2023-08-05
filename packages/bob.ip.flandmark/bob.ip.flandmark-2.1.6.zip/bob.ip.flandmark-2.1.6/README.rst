.. vim: set fileencoding=utf-8 :
.. Mon 15 Aug 2016 18:52:57 CEST

.. image:: http://img.shields.io/badge/docs-stable-yellow.svg
   :target: https://www.idiap.ch/software/bob/docs/bob/bob.ip.flandmark/stable/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.svg
   :target: https://www.idiap.ch/software/bob/docs/bob/bob.ip.flandmark/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.ip.flandmark/badges/v2.1.6/build.svg
   :target: https://gitlab.idiap.ch/bob/bob.ip.flandmark/commits/v2.1.6
.. image:: https://gitlab.idiap.ch/bob/bob.ip.flandmark/badges/v2.1.6/coverage.svg
   :target: https://gitlab.idiap.ch/bob/bob.ip.flandmark/commits/v2.1.6
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.ip.flandmark
.. image:: http://img.shields.io/pypi/v/bob.ip.flandmark.svg
   :target: https://pypi.python.org/pypi/bob.ip.flandmark


=========================================
 Flandmark keypoint localization library
=========================================

This package is part of the signal-processing and machine learning toolbox
Bob_. It contains a simple Python wrapper to the (rather quick) open-source
facial landmark detector Flandmark_, **version 1.0.7** (or the github state as
of 10/february/2013). If you use this package, the author asks you to cite the
following paper::

  @inproceedings{Uricar-Franc-Hlavac-VISAPP-2012,
    author =      {U\v{r}i\v{c}\'a\v{r}, Michal and Franc, Vojt\v{e}ch and Hlav\'a\v{c}, V\'{a}clav},
    title =       {Detector of Facial Landmarks Learned by the Structured Output {SVM}},
    year =        {2012},
    pages =       {547-556},
    booktitle =   {VISAPP '12: Proceedings of the 7th International Conference on Computer Vision Theory and Applications},
    editor =      {Csurka, Gabriela and Braz, Jos{\'{e}}},
    publisher =   {SciTePress --- Science and Technology Publications},
    address =     {Portugal},
    volume =      {1},
    isbn =        {978-989-8565-03-7},
    book_pages =  {747},
    month =       {February},
    day =         {24-26},
    venue =       {Rome, Italy},
    keywords =    {Facial Landmark Detection, Structured Output Classification, Support Vector Machines, Deformable Part Models},
    prestige =    {important},
    authorship =  {50-40-10},
    status =      {published},
    project =     {FP7-ICT-247525 HUMAVIPS, PERG04-GA-2008-239455 SEMISOL, Czech Ministry of Education project 1M0567},
    www = {http://www.visapp.visigrapp.org},
  }


Installation
------------

Complete Bob's `installation`_ instructions. Then, to install this package,
run::

  $ conda install bob.ip.flandmark


Contact
-------

For questions or reporting issues to this software package, contact our
development `mailing list`_.


.. Place your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _installation: https://www.idiap.ch/software/bob/install
.. _mailing list: https://www.idiap.ch/software/bob/discuss
.. _flandmark: http://cmp.felk.cvut.cz/~uricamic/flandmark/index.php
