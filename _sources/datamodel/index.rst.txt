==========
Data Model
==========

This section documents the database schema and data migration system used in the Open Data Repository.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   migrations
   schemas/index

Overview
========

The Open Data Repository uses a PostgreSQL database with the following key features:

- Drizzle ORM for type-safe database operations
- Vector support for embeddings and similarity search
- Role-based access control
- Team-based content organization
- Comprehensive content and annotation tracking

Key Components
--------------

1. **Authentication System**
   - User management
   - OAuth provider integration
   - Session handling

2. **Content Management**
   - Digital asset storage
   - Metadata tracking
   - Content sets and collections

3. **Annotation System**
   - Multi-source annotations
   - Quality ratings
   - Embedding support

4. **Team Organization**
   - Team management
   - Role-based permissions
   - Collaborative workflows

For detailed information about specific components, please refer to the relevant sections in the documentation.
