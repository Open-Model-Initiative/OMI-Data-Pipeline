================
Database Schemas
================

This section provides detailed documentation for each schema component in the Open Data Repository database.

.. toctree::
   :maxdepth: 2
   :caption: Schema Components:

   authentication
   content
   annotations
   embeddings
   teams

Schema Overview
===============

The database schema is organized into several logical components:

Authentication Schema
---------------------
Handles user accounts, sessions, and authentication providers. See :doc:`authentication` for details.

Content Schema
--------------
Manages digital assets and their metadata. See :doc:`content` for details.

Annotation Schema
-----------------
Controls content annotations and their metadata. See :doc:`annotations` for details.

Embedding Schema
----------------
Manages vector embeddings for search and similarity. See :doc:`embeddings` for details.

Team Schema
-----------
Handles team organization and membership. See :doc:`teams` for details.

Relationships
=============

The schemas are interconnected through foreign key relationships:

- Users can belong to multiple teams through ``userTeams``
- Content can be owned by users and teams
- Annotations can reference content and have associated embeddings
- Content can be organized into sets and collections

For detailed information about specific schemas, click the relevant links above.
