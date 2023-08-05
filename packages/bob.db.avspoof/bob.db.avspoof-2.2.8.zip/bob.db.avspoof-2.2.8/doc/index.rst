.. vim: set fileencoding=utf-8 :
.. @author: Pavel Korshunov <Pavel.Korshunov@idiap.ch>
.. @date:   Wed Nov 11 15:06:22 CEST 2015

.. _bob.db.avspoof:

==========================================
 AVspoof Database Verification Protocols
==========================================

For verification experiments, protocols `licit` (only genuine speech samples are used in train, dev, and eval sets)
and `spoof` (train and dev sets contain only genuine data, while eval contains only attacks) are supported by this package.

==========================================
 AVspoof Database Anti-spoofing Protocols
==========================================

For anti-spoofing experiments, several protocols are supported which for each train, dev, or eval sets return two types of data
genuine (real) and spoofed (attacks). The anti-spoofing protocols are `grandtest` (all data), `smalletest` (small subset with
two clients per train, dev, and eval, sets - useful for debugging), `physical_access` (only spoofed data that was obtained by replaying
the audio into physical microphone), and `logical_access` (only the generated voice conversion and speech synthesis spoofed data
excluding samples that were played back to the microphone).


=======================================================
 Speaker recognition protocol on the AVspoof Database
=======================================================

AVspoof_ is intended to provide stable, non-biased spoofing attacks in order for researchers to test both their ASV systems and anti-spoofing algorithms. The attacks are created based on newly acquired audio recordings. The data acquisition process lasted approximately two months with 44 persons, each participating in several sessions configured in different environmental conditions and setups. After the collection of the data, the attacks, more precisely, replay, voice conversion and speech synthesis attacks were generated. 


If you use this package and/or its results, please cite the following publication:

1. The original paper is presented at the IEEE BTAS 2015:

   .. code-block:: latex

    @inproceedings{avspoof,
      author = {Serife Kucur Erg\"unay and Elie Khoury and Alexandros Lazaridis and S\'ebastien Marcel },
      title = {On the Vulnerability of Speaker Verification to Realistic Voice Spoofing},
      booktitle = {IEEE Intl. Conf. on Biometrics: Theory, Applications and Systems (BTAS)},
      year = {2015},
      url = {https://publidiap.idiap.ch/downloads//papers/2015/KucurErgunay_IEEEBTAS_2015.pdf},
    }

Getting the data
--------------------------

The original data can be downloaded directly from AVspoof_, which is free of charge but requires to sign the EULA. 


Documentation
------------------------

.. toctree::
   :maxdepth: 2

   guide
   py_api

Indices and tables
-------------------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _bob: https://www.idiap.ch/software/bob
.. _AVspoof: https://www.idiap.ch/dataset/avspoof
.. _nist sre 2012 evaluation: http://www.nist.gov/itl/iad/mig/sre12.cfm
.. _idiap: http://www.idiap.ch


