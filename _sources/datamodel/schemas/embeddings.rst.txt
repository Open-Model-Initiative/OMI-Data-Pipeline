================
Embedding Schema
================

The embedding schema manages vector embeddings for content and annotations.

Embedding Engines
-----------------

.. code-block:: typescript

   embeddingEngines {
     id: serial PRIMARY KEY
     name: varchar UNIQUE
     description: varchar
     version: varchar
     createdAt: timestamp
     updatedAt: timestamp NOT NULL
     type: embeddingenginetype ENUM
     supported: boolean
   }

Content Embeddings
------------------

.. code-block:: typescript

   contentEmbeddings {
     id: serial PRIMARY KEY
     contentId: integer
     embeddingEngineId: integer
     fromUserId: integer
     fromTeamId: integer
     createdAt: timestamp
     embedding: vector(512)
   }

The embedding system provides vector representations for search and similarity matching.
