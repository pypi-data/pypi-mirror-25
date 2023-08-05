.. vim: set fileencoding=utf-8 :
.. Andre Anjos <andre.dos.anjos@gmail.com>
.. Sat 16 Nov 20:52:58 2013

.. testsetup::

   def get_file(f):
     from os.path import join
     from pkg_resources import resource_filename
     return resource_filename('bob.ip.flandmark', join('data', f))

==============================================
 Face Landmark Detection Using Python and Bob
==============================================

:py:class:`bob.ip.flandmark` detects 8 coordinates of important keypoints in **frontal** human faces.
To properly work, the keypoint localizer requires the input of an image (of type ``uint8``, gray-scaled) and of a bounding box describing a rectangle where the face is supposed to be located in the image (see :py:meth:`bob.ip.flandmark.Flandmark.locate`).

The keypoints returned are, in this order:

[0]
  Face center

[1]
  Canthus-rl (inner corner of the right eye).

  .. note::

     The "right eye" means the right eye at the face w.r.t. the person on the
     image. That is the left eye in the image, from the viewer's perspective.

[2]
  Canthus-lr (inner corner of the left eye)

[3]
  Mouth-corner-r (right corner of the mouth)

[4]
  Mouth-corner-l (left corner of the mouth)

[5]
  Canthus-rr (outer corner of the right eye)

[6]
  Canthus-ll (outer corner of the left eye)

[7]
  Nose

Each point is returned as tuple defining the pixel positions in the form ``(y, x)``.

The input bounding box describes the rectangle coordinates using 4 values: ``(y, x, height, width)``.
Square bounding boxes, i.e. when ``height == width``, will give best results.

If you don't know the bounding box coordinates of faces on the provided image, you will need to either manually annotate them or use an automatic face detector.
:ref:`bob.ip.facedetect` provides an easy to use frontal face detector.
The code below shall detect most frontal faces in a provided image:

.. doctest::
   :options: +NORMALIZE_WHITESPACE, +ELLIPSIS

   >>> import bob.io.base
   >>> import bob.io.image
   >>> import bob.ip.facedetect
   >>> lena = bob.io.base.load(get_file('lena.jpg'))
   >>> bounding_box, quality = bob.ip.facedetect.detect_single_face(lena)
   >>> # scale the bounding box to cover more of the face
   >>> bounding_box = bounding_box.scale(1.2, True)
   >>> y, x = bounding_box.topleft
   >>> height, width = bounding_box.size
   >>> width = height  # make it square
   >>> print((y, x, height, width))
   (...)

.. note::
   To enable the :py:func:`bob.io.base.load` function to load images, :ref:`bob.io.image <bob.io.image>` must be imported, see :ref:`bob.io.image`.

Once in possession of bounding boxes for the provided (gray-scaled) image, you can find the keypoints in the following way:

.. doctest::
   :options: +NORMALIZE_WHITESPACE, +ELLIPSIS

   >>> import bob.ip.color
   >>> from bob.ip.flandmark import Flandmark
   >>> localizer = Flandmark()
   >>> lena_gray = bob.ip.color.rgb_to_gray(lena)
   >>> keypoints = localizer.locate(lena_gray, y, x, height, width)
   >>> keypoints
   array([[...]])

You can use the package :ref:`bob.ip.draw <bob.ip.draw>` to draw the rectangles and key-points on the target image.
A complete script would be something like:

.. plot:: plot/show_lena.py
   :include-source: True

.. include:: links.rst
