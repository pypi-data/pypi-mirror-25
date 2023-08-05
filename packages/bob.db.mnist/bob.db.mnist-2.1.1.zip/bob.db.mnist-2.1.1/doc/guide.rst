.. vim: set fileencoding=utf-8 :

==============
 User's Guide
==============

After launching the python interpreter (assuming that the environment is
properly set up), you can access samples from this database like the following:


.. code-block:: py

  >>> import bob.db.mnist
  >>> db = bob.db.mnist.Database()
  >>> images, labels = db.data(groups='train', labels=[0,1,2,3,4,5,6,7,8,9])


In this case, this should return two :py:class:`numpy.ndarray`\s:

1. `images` contain the raw data (60,000 samples of dimension 784 [28x28 pixels
   images])
2. `labels` are the corresponding classes (digits 0 to 9) for each of the
   60,000 samples


.. todo::
   Improve users guide.
