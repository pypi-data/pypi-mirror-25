ZAP (the Zurich Atmosphere Purge)
---------------------------------

Tired of sky subtraction residuals? ZAP them!

ZAP is a high precision sky subtraction tool which can be used as complete sky
subtraction solution, or as an enhancement to previously sky-subtracted MUSE
data.  The method uses PCA to isolate the residual sky subtraction features and
remove them from the observed datacube. Future developments will include
modification for use on a variety of instruments.

The last stable release of ZAP can be installed simply with pip::

    pip install zap

Or into the user path with::

    pip install --user zap

Links
~~~~~

- `documentation <http://zap.readthedocs.io/en/latest/>`_

- `git repository <https://github.com/musevlt/zap>`_

- `changelog <https://github.com/musevlt/zap/blob/master/CHANGELOG>`_

Citation
~~~~~~~~

The paper describing the original method can be found here:
http://adsabs.harvard.edu/abs/2016MNRAS.458.3210S

Please cite ZAP as::

\bibitem[Soto et al.(2016)]{2016MNRAS.458.3210S} Soto, K.~T., Lilly, S.~J., Bacon, R., Richard, J., \& Conseil, S.\ 2016, \mnras, 458, 3210
