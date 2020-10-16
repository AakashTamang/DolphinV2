.. Dolphwin documentation master file, created by
   sphinx-quickstart on Fri Oct 16 14:09:09 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Dolphwin's documentation!
====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   README

Datareader
=====================
.. automodule:: datareader
   :members:

Data Preprocessing
==========================
.. autoclass:: data_preprocessing.PreprocessData
   :members:

   .. automethod:: __init__

Word2Vec
==============
.. autoclass:: word2vec.Word2VecScorer
   :members:

   .. automethod:: __init__

Document_categorization
===================================
.. autoclass:: cvparser.document_categorization.doc_classifier_test.DocClassifier
   :members:

   .. automethod:: __init__

Resume_segmentation
===================================
.. autoclass:: cvparser.segmentation.segmentresume.ResumeSegmentCreator
   :members:

   .. automethod:: __init__

Named_entity_recognition
===================================
.. autoclass:: cvparser.stanfordNER.namedentityrecognition.StanfordNER
   :members:

   .. automethod:: __init__

.. automodule:: cvparser.stanfordNER.formatdata
	:members:

.. automodule:: cvparser.stanfordNER.standarizedata
	:members:

spaCy pipeline
=======================
.. autoclass:: cvparser.pipeline.NlpPipeline
   :members:

   .. automethod:: __init__

Parsing a Document
=======================
.. autoclass:: cvparser.newParse.Parser
   :members:

   .. automethod:: __init__

Job Parsing
============================
.. autoclass:: job_parsing.jd_parsing.SpacyNer
   :members:

   .. automethod:: __init__

.. autoclass:: job_parsing.stanford_ner.Stanford_NER
   :members:

   .. automethod:: __init__

.. automodule:: job_parsing.createngrams
   :members:
   
.. automodule:: job_parsing.skill_parser
   :members:

Matcher Component
=========================
.. autoclass:: matcher.match.matcher
   :members:

   .. automethod:: __init__

Scoring Component
======================
.. autoclass:: scorer.helper.PreprocessData
   :members:

   .. automethod:: __init__

.. automodule:: scorer.resume_scorer
   :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
