======================
Authentication Schema
======================

The authentication schema handles user accounts, sessions, and external provider authentication.

Users
-----

.. code-block:: typescript

   users {
     id: serial PRIMARY KEY
     email: varchar
     hashedPassword: varchar
     isActive: boolean DEFAULT true
     isSuperuser: boolean DEFAULT false
     createdAt: timestamp with timezone
     updatedAt: timestamp with timezone
     identityProvider: varchar
     dcoAccepted: boolean DEFAULT false
     name: varchar(255)
     emailVerified: timestamp with timezone
     image: varchar
   }

The users table is central to authentication and stores core user information.

Sessions & Accounts
------------------

.. code-block:: typescript

   sessions {
     userId: integer
     expires: timestamp with timezone
     sessionToken: varchar(255)
     id: serial
   }

   accounts {
     id: serial PRIMARY KEY
     userId: integer
     type: varchar(255)
     provider: varchar(255)
     providerAccountId: varchar(255)
     refreshToken: varchar
     accessToken: varchar
     expiresAt: bigint
     idToken: varchar
     scope: varchar
     sessionState: varchar
     tokenType: varchar
   }

These tables manage authentication state and external provider connections.

Verification
-----------

.. code-block:: typescript

   verificationToken {
     identifier: varchar
     token: varchar
     expires: timestamp with timezone
     PRIMARY KEY (identifier, token)
   }

Used for email verification and password reset functionality.
