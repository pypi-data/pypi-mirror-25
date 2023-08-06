..  Titling
    ##++::==~~--''``

.. _survey:

Survey accessors
::::::::::::::::

Surveys come to SDX as JSON messages. They are then loaded via Python's ``json`` module,
which returns a nested dictionary.


.. automodule:: sdx.common.survey

.. autoclass:: sdx.common.survey.Survey
   :members: load_survey, bind_logger, identifiers, parse_timestamp
   :member-order: bysource

.. autoattribute:: sdx.common.survey.Survey.Identifiers
   :annotation: (batch_nr, seq_nr, ts, tx_id, survey_id, inst_id, user_ts, user_id, ru_ref, ru_check, period)
