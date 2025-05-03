===============
Data Migrations
===============

The Open Data Repository uses Drizzle ORM for database management and migrations. This document outlines our migration system and database schema management approach.

Migration System Overview
=========================

We use Drizzle Kit for handling database migrations, which provides a type-safe and declarative way to manage database schemas in TypeScript.

Key Components
--------------

- **Schema Definition**: Located in ``src/db/schemas/``
- **Migration Files**: Generated in ``drizzle/`` directory
- **Configuration**: Managed via ``drizzle.config.ts``

Available Commands
------------------

.. code-block:: bash

   # Pull current database schema
   pnpm run db:pull

   # Push schema changes to database
   pnpm run db:push

   # Generate new migration
   pnpm run db:generate

   # Apply pending migrations
   pnpm run db:migrate

   # Launch Drizzle Studio UI
   pnpm run db:studio

Schema Structure
================


Best Practices
==============

1. **Schema Changes**

   - Always generate migrations for schema changes
   - Review migration files before applying
   - Test migrations in development environment first

2. **Naming Conventions**

   - Use snake_case for database objects
   - Prefix related tables appropriately
   - Use descriptive but concise names

3. **Version Control**

   - Commit migration files to version control
   - Include both up and down migrations
   - Document breaking changes

Migration Workflow
==================

1. **Development Phase**

   .. code-block:: bash

      # Make schema changes in TypeScript files
      # Generate new migration
      pnpm run db:generate
      # Review generated migration
      # Apply migration
      pnpm run db:migrate

2. **Testing Phase**

   - Test migrations in development environment
   - Verify data integrity
   - Check for breaking changes

3. **Deployment Phase**

   - Back up production database
   - Apply migrations during maintenance window
   - Verify application functionality

Troubleshooting
===============

Common Issues
-------------

1. **Migration Conflicts**

   - Reset development database
   - Regenerate migrations
   - Ensure consistent migration history

2. **Schema Sync Issues**

   - Use ``db:pull`` to verify current state
   - Compare with version control
   - Manually resolve conflicts

3. **Performance Concerns**

   - Review index usage
   - Check migration impact
   - Consider batching large changes

Getting Help
============

For issues with migrations:

1. Check the `Drizzle documentation <https://orm.drizzle.team/docs/migrations>`_
2. Review our issue tracker
3. Contact the development team
4. Ask for help in our Discord community `here <https://discord.gg/vANKjzDDkQ>`_
