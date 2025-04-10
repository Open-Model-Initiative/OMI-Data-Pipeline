=================
Annotation Schema
=================

The annotation schema manages content annotations and their embeddings.

Annotation Sources
------------------

.. code-block:: typescript

   annotationSources {
     id: serial PRIMARY KEY
     name: varchar
     ecosystem: varchar
     type: varchar
     annotationSchema: json
     license: varchar
     licenseUrl: varchar
     addedById: integer
     createdAt: timestamp NOT NULL
     updatedAt: timestamp NOT NULL
   }

Core Annotations
----------------

.. code-block:: typescript

   annotations {
     id: serial PRIMARY KEY
     contentId: integer NOT NULL
     annotation: json
     manuallyAdjusted: boolean
     overallRating: double precision
     fromUserId: integer
     fromTeamId: integer
     createdAt: timestamp
     updatedAt: timestamp
   }

Annotation Metadata
-------------------

.. code-block:: typescript

   annotationRatings {
     id: serial PRIMARY KEY
     annotationId: integer NOT NULL
     rating: integer NOT NULL
     reason: varchar
     ratedById: integer
     createdAt: timestamp NOT NULL
     updatedAt: timestamp NOT NULL
   }

   annotationReports {
     id: serial PRIMARY KEY
     annotationId: integer
     type: varchar NOT NULL
     reportedById: integer
     createdAt: timestamp NOT NULL
     updatedAt: timestamp NOT NULL
     description: varchar
   }

Annotation Embeddings
---------------------

.. code-block:: typescript

   annotationEmbeddings {
     id: serial PRIMARY KEY
     annotationId: integer
     embeddingEngineId: integer
     fromUserId: integer
     fromTeamId: integer
     createdAt: timestamp
     embedding: vector(384)
   }

Source Linking
--------------

.. code-block:: typescript

   annotationSourcesLink {
     annotationId: integer NOT NULL
     annotationSourceId: integer NOT NULL
     PRIMARY KEY (annotationId, annotationSourceId)
   }
