.. vim: set fileencoding=utf-8 :
.. Mon 13 Aug 2012 12:36:40 CEST

==============
 User's Guide
==============

Data for the 3DFV database was collected through various campaings in
Switzerland, at different locations. Each of the campaigns and outcomes are
summarized next:

* Foire du Valais (FDV): 89 subjects provided data from both index fingers in a
  single data-acquisition session with a single attempt. For each subject
  finger, 5 snapshots were taken. The unique subject identifiers vary between 1
  and 94, but numeration is not contiguous.
* Idiap (IDI): 50 subjects provided data from both left and right index, middle
  and ring fingers in 3 data acquisition sessions, each with 2 attempts. Two
  more subjects provided data for the same fingers, but for only 1 acquisition
  session (subjects 131 and 147). The unique subject identifiers range from 101
  to 153. Numeration is contiguous.


Filename Structure
------------------

Filenames inside the 3D Fingervein are structured like this:

.. code-block:: text

   <database-root>/<client:%03d>/<session:%d>/<attempt:%d>/<client:%03d>-<age:%02d>-<gender:%s><skin:%s><occ:%s><side:%s><finger:%s><session:%d><attempt:%d><snap:%d><cam:%d>.png

Each field can have these values:

    * client: integer > 0
    * age = integer > 0
    * gender = str, 'm' or 'f'
    * skin (color) = str, '1'..'6' or 'x'
    * occ(upation) = str, '0'..'9' or 'x'
    * side = str, 'l' or 'r'
    * finger = str, 't', 'i', 'm', 'r', 'l'
    * session = int > 0
    * attempt = int > 0
    * snap = int > 0
    * cam = int, one of 1, 2, 3 or S (1 is left, 2 is central, 3 is right and S means the "stitched" image using the three cameras)



Protocols
---------


Central
=======

The ``central`` protocol only makes use of images from the central camera of
the prototype (camera 2). Each finger is supposed to be considered a
*different* individual. Existing samples are divided like this:

* **Training set**: All subjects with only one session from FDV and Idiap
* **Development set**: Snapshots (2 per finger) and 2 attempts using the system
  from all subjects with 3 sessions from Idiap. Modelling uses snapshots from
  session 1, probing uses snapshots from sessions 2 and 3. While probing, one
  should match every file listed as probe against all models in the set. In
  this protocol, 1 snapshot image generates one model for the subject.


Stitched
========

The ``stitched`` protocol is the same as ``central``, but uses the stitched
images for training and development.


.. Place your references here
.. _bob: http://www.idiap.ch/software/bob
.. _3d fingervein database: https://www.idiap.ch/dataset/3d-fingervein
