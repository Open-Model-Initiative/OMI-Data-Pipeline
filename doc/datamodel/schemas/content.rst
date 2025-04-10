==============
Content Schema
==============

The content schema manages digital assets and their metadata.

Core Content
------------

.. code-block:: typescript

   contents {
     id: serial PRIMARY KEY
     name: varchar
     type: contenttype ENUM
     hash: varchar
     phash: varchar
     width: integer
     height: integer
     format: varchar
     size: integer
     status: contentstatus ENUM
     license: varchar
     licenseUrl: varchar
     flags: integer
     meta: json
     fromUserId: integer
     fromTeamId: integer
     createdAt: timestamp
     updatedAt: timestamp
     url: varchar
   }

Content Metadata
----------------

.. code-block:: typescript

   contentAuthors {
     id: serial PRIMARY KEY
     name: varchar
     url: varchar
     contentId: integer
     createdAt: timestamp
     updatedAt: timestamp
   }

   contentSources {
     id: serial PRIMARY KEY
     contentId: integer
     type: contentsourcetype ENUM
     value: varchar UNIQUE
     sourceMetadata: varchar
     createdAt: timestamp
     updatedAt: timestamp
   }

Content Organization
--------------------

.. code-block:: typescript

   contentSets {
     id: serial PRIMARY KEY
     name: varchar NOT NULL
     description: varchar
     createdById: integer NOT NULL
     createdAt: timestamp
     updatedAt: timestamp
   }

   contentSetItems {
     contentSetId: integer NOT NULL
     contentId: integer NOT NULL
     addedAt: timestamp
     PRIMARY KEY (contentSetId, contentId)
   }

Content Status Tracking
-----------------------

.. code-block:: typescript

   contentEvents {
     id: serial PRIMARY KEY
     contentId: integer NOT NULL
     status: contentstatus NOT NULL
     setBy: integer NOT NULL
     note: varchar
     createdAt: timestamp
     updatedAt: timestamp
   }

   contentReports {
     id: serial PRIMARY KEY
     contentId: integer NOT NULL
     reporterId: integer NOT NULL
     reason: varchar NOT NULL
     description: varchar
     status: reportstatus
     createdAt: timestamp
     updatedAt: timestamp
   }
