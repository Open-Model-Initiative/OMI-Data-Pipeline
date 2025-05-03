===========
Team Schema
===========

The team schema manages team organization and membership.

Teams
-----

.. code-block:: typescript

   teams {
     id: serial PRIMARY KEY
     name: varchar UNIQUE
     createdAt: timestamp DEFAULT now()
     updatedAt: timestamp DEFAULT now()
   }

Team Membership
---------------

.. code-block:: typescript

   userTeams {
     userId: integer NOT NULL
     teamId: integer NOT NULL
     role: varchar
     createdAt: timestamp DEFAULT now()
     updatedAt: timestamp DEFAULT now()
     PRIMARY KEY (userId, teamId)
   }

The team system enables collaborative work and access control across the platform.
