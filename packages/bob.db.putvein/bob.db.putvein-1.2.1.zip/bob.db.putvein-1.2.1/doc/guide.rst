
*************
 User's Guide
*************

Data
####

This package is part of the signal-processing and machine learning toolbox
Bob_. It contains an interface for the `PUT Vein Dataset`_. This package does
not contain the original data files, which need to be obtained through the link
above.

The vein pattern recognition is one of the most promising and intensively
developing field of studies in biometrics research. One of main obstacles in
creating new methods of segmentation and classification of vein patterns was a
lack of benchmarking dataset that would allow to obtain comparable results. Put
Vein Database was created to overcame this problem and crate common platform
for algorithms comparison.

PUT Vein pattern database is free available for research purposes can be
applied as common platform for evaluation and comparison of new segmentation
and classification algorithms. Enabling comparison of algorithms without
different hardware systems used by researchers will help to chose the best
algorithm, thus helping in biometrics systems design.

PUT Vein pattern database consists of 2400 images presenting human vein
patterns. Half of images contains a palmar vein pattern (1200 images) and
another half contains a wrist vein pattern (another 1200 images). Data was
acquired from both hands of 50 students, with means it has a 100 different
patterns for palm and wrist region. Pictures ware taken in 3 series, 4 pictures
each, with at least one week interval between each series. In case of palm
region volunteers ware asked to put his/her hand on the device to cover
acquisition window, in way that line below their fingers coincident with its
edge. No additional positioning systems ware used. In case of wrist region only
construction allowing to place palm and wrist in comfortable way was used to
help position a hand.


In this implementation we use both - original 50 client x 2 hand data - in the 
database clients with IDs between ``1`` and ``50`` -  and also -- mirrored file 
representations (left hand / palm data mirrored to look like right hand data and
vice versa) - clients with IDs between ``51`` and ``100``.


Protocols
#########

Each protocol of the PUTVEIN database consists of the following ``groups`` and
purposes:

+-------------+-----------+-----------------------+------------------------+
| **groups**  | ``world`` |         ``dev``       |         ``eval``       |
+-------------+-----------+-----------------------+------------------------+
|**purposes** | ``train`` |``enroll`` / ``probe`` | ``enroll`` / ``probe`` |
+-------------+-----------+-----------------------+------------------------+

Currently (as on 08.02.2017) there are 10 protocols:

    - ``L_4``,
    - ``R_4``,
    - ``LR_4``,
    - ``RL_4``,
    - ``R_BEAT_4``,
    - ``L_1``,
    - ``R_1``,
    - ``LR_1``
    - ``RL_1``,
    - ``R_BEAT_1``.
    
Protocols (except the ``BEAT`` protocols) still contains the original protocol 
('L', 'R', 'LR', 'RL') data, the difference is, whether each enroll model is 
constructed  using all 4 hand's images (protocol name ends with ``4``), or each
enroll image is used as a model (corresponding protocol names ends with ``1``).

The original protocols consists of following data, ``world`` purpose dataset 
consists of the **same** data, as ``dev`` purpose dataset, so won't be 
separately described:

+-------------+-----------------------------------------+-------------------------------------------+
|**protocol** |                  ``dev``                |                  ``eval``                 |
+-------------+-----------------------------------------+-------------------------------------------+
|     L       | IDs 1-25, un-mirrored left hand images  |  IDs 26-50, un-mirrored left hand images  |
+-------------+-----------------------------------------+-------------------------------------------+
|     R       | IDs 1-25, un-mirrored right hand images |  IDs 26-50, un-mirrored right hand images |
+-------------+-----------------------------------------+-------------------------------------------+
|             | IDs 1-50, un-mirrored right hand images |  IDs 51-100, mirrored left hand images    |
|     RL      |                                         |                                           |
|             |                                         |         (to represent right hand)         |
+-------------+-----------------------------------------+-------------------------------------------+
|             | IDs 1-50, un-mirrored left hand images  |  IDs 51-100, mirrored right hand images   |
|     LR      |                                         |                                           |
|             |                                         |         (to represent left hand)          |
+-------------+-----------------------------------------+-------------------------------------------+


The new test protocols ``R_BEAT_1`` and ``R_BEAT_4` are intended for use with 
``bob.bio.vein`` and ``BEAT`` platform for quick tests, if necessary. Both 
protocols consist of such data:

+-------------+-------------------------------------------------+----------------------------------------------------+
|**protocol** |                  ``dev``                        |                       ``eval``                     |
+-------------+-------------------------------------------------+----------------------------------------------------+
|   R_BEAT    | IDs ``1``, ``2``, un-mirrored right hand images |  IDs ``26``, ``27``, un-mirrored right hand images |
+-------------+-------------------------------------------------+----------------------------------------------------+

**Please find additional information about protocols there**:

1) :py:meth:`bob.db.putvein.Database.objects()`


.. Place your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _put vein dataset: http://biometrics.put.poznan.pl/vein-dataset/
