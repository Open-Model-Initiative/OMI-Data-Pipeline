.. SPDX-License-Identifier: Apache-2.0

OMI Data Pipeline CDK Infrastructure
==================================

This project contains the AWS CDK infrastructure code for the OMI Data Pipeline. It defines a complete AWS infrastructure setup using Infrastructure as Code (IaC) principles with AWS CDK in Python.

Infrastructure Components
-----------------------

The infrastructure is composed of several stacks that work together:

* ``VpcStack`` - Creates the Virtual Private Cloud (VPC) network infrastructure
* ``DatabaseStack`` - Sets up the database infrastructure (depends on VPC)
* ``EcrStack`` - Creates Elastic Container Registry (ECR) repositories for Docker images
* ``S3Stack`` - Configures S3 buckets for data storage
* ``EcsStack`` - Deploys ECS services and tasks (depends on VPC, ECR, S3, and Database)
* ``WafStack`` - Implements AWS WAF web application firewall (depends on ECS)

Prerequisites
------------

Before you begin, ensure you have:

* Python 3.x installed
* AWS CLI configured with appropriate credentials
* Node.js and npm (required by CDK)
* Docker (for building and pushing container images)

Setup
-----

1. Create a Python virtual environment:

   .. code-block:: bash

       $ python -m venv .venv

2. Activate the virtual environment:

   For Linux/MacOS:

   .. code-block:: bash

       $ source .venv/bin/activate

   For Windows:

   .. code-block:: bash

       % .venv\Scripts\activate.bat

3. Install dependencies:

   .. code-block:: bash

       $ pip install -r requirements.txt
       $ pip install -r requirements-dev.txt  # for development dependencies

Deployment
---------

The stacks are designed to be deployed in a specific order due to their dependencies. To deploy:

1. Bootstrap your AWS environment (if not already done):

   .. code-block:: bash

       $ cdk bootstrap

2. Review the changes:

   .. code-block:: bash

       $ cdk diff

3. Deploy all stacks:

   .. code-block:: bash

       $ cdk deploy --all

   Or deploy individual stacks (respecting dependencies):

   .. code-block:: bash

       $ cdk deploy VpcStack
       $ cdk deploy DatabaseStack
       $ cdk deploy EcrStack
       $ cdk deploy S3Stack
       $ cdk deploy EcsStack
       $ cdk deploy WafStack

Useful Commands
--------------

* ``cdk ls``          List all stacks in the application
* ``cdk diff``        Compare deployed stack with current state
* ``cdk synth``       Emit synthesized CloudFormation template
* ``cdk deploy``      Deploy this stack to your default AWS account/region
* ``cdk destroy``     Destroy the deployed stack(s)
* ``cdk docs``        Open CDK documentation

Configuration
------------

The infrastructure is configured to deploy in the ``us-east-1`` region by default. Environment-specific configurations can be modified in ``app.py``.

Security
--------

This project follows AWS security best practices including:

* VPC isolation for network security
* WAF protection for web applications
* Proper IAM roles and permissions
* Encrypted data storage

For security issues, please report them following the project's security policy.
