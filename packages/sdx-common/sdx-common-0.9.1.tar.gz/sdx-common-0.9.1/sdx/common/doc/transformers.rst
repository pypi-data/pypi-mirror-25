..  Titling
    ##++::==~~--''``

.. _transformers:

Transformers
::::::::::::

Every different survey type which passes through SDX may require:

    * validation of data fields
    * application of business logic
    * conversion to downstream formats

We give each survey type its own transformer class. The class implements
the custom behaviour required.

In order to minimise duplication of code, each new transformer class should inherit
from a base class which already provides that functionality: Transformer_.

Two legacy classes exist for the generation of page images. Transformer classes
delegate to them for image generation:

    * ImageTransformer_
    * PDFTransformer_
 
Transformer
===========

.. automodule:: sdx.common.transformer

.. autoclass:: sdx.common.transformer.Transformer
   :members:
   :member-order: bysource

ImageTransformer
================

.. automodule:: sdx.common.transforms.ImageTransformer

.. autoclass:: sdx.common.transforms.ImageTransformer.ImageTransformer
   :members:
   :member-order: bysource

PDFTransformer
==============

.. automodule:: sdx.common.transforms.PDFTransformer

.. autoclass:: sdx.common.transforms.PDFTransformer.PDFTransformer
   :members:
