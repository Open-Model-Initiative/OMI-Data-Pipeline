CDK Stack Documentation
=======================

Overview
--------
This document provides an introduction to our AWS Cloud Development Kit (CDK) stack.
It explains the various elements that make up our cloud infrastructure, the GitHub Actions workflow
used to deploy it, and the key AWS services that are configured.

GitHub Actions Workflow
-----------------------
The repository includes a GitHub Actions workflow defined in ``.github/workflows/build-and-deploy-aws.yml``.
This workflow automates the following tasks:

- **Build and Push Docker Images:**
  - Checks out the repository.
  - Configures AWS credentials by assuming a dedicated IAM role.
  - Builds Docker images for both the frontend and backend using their respective Dockerfiles.
  - Pushes these images to Amazon ECR (Elastic Container Registry).

- **Deployment:**
  - The workflow is triggered manually via ``workflow_dispatch``.
  - It accepts an input parameter ``deployment_type`` with three options:

    - ``all``: Deploy all AWS stacks.
    - ``app-only``: Deploy only the ECS (Elastic Container Service) stack.
    - ``none``: Only build and push the Docker images.

  - Depending on the selected option, the workflow sets up Node.js, installs AWS CDK dependencies, and executes the appropriate CDK deployment commands.

AWS CDK Project Structure
-------------------------
Our CDK project, located under the ``cdk/`` directory, uses Python to define our cloud infrastructure. Key files include:

- **README.rst:**
  Provides instructions on how to set up the virtual environment, install dependencies, and use the CDK CLI.

- **cdk.json:**
  Instructs the CDK Toolkit on how to execute the application (e.g., by running ``python app.py``).

- **app.py:**
  The main entry point for the CDK application. It instantiates several stacks (see below) that represent different parts of our infrastructure.

- **requirements.txt / requirements-dev.txt:**
  These files list the Python dependencies necessary for the CDK project.

- **.gitignore:**
  Specifies files and directories to be excluded from version control (e.g. virtual environments, temporary files).

CDK Stacks
----------
Our infrastructure is divided into multiple modular stacks. Each stack is responsible for provisioning a set of related AWS resources.

VpcStack
~~~~~~~~
- **Purpose:**
  Creates a Virtual Private Cloud (VPC), which is an isolated network environment in AWS.
- **Key Elements:**
  - Custom IP address range.
  - Creation of public, private, and isolated subnets.
  - An interface endpoint for AWS Secrets Manager to securely access secrets without leaving the VPC.

DatabaseStack
~~~~~~~~~~~~~
- **Purpose:**
  Provisions a managed PostgreSQL database using Amazon RDS.
- **Key Elements:**
  - Creates an RDS instance with PostgreSQL.
  - Configures a security group to control access to the database.
  - Sets up an AWS Secrets Manager secret to securely store database credentials.
  - Defines policies (e.g., backup retention and removal policy) suitable for testing environments.

EcrStack
~~~~~~~~
- **Purpose:**
  Establishes container registries using Amazon ECR.
- **Key Elements:**
  - Creates separate repositories for the frontend and backend Docker images.
  - Configures lifecycle rules to automatically remove old images (keeping only the latest 10).
  - Enables image scanning to help identify vulnerabilities.

EcsStack
~~~~~~~~
- **Purpose:**
  Deploys the application containers using Amazon ECS with Fargate.
- **Key Elements:**
  - Creates an ECS cluster within the VPC.
  - Defines Fargate task definitions for both backend and frontend services.
  - Configures Application Load Balancers to distribute incoming traffic.
  - Sets up security groups and assigns IAM policies so that the containers can access necessary AWS resources (such as S3 and Secrets Manager).
  - Injects environment variables and secrets into the container tasks.

S3Stack
~~~~~~~
- **Purpose:**
  Creates an S3 bucket for object storage.
- **Key Elements:**
  - Configures versioning and encryption.
  - Applies lifecycle rules to transition older objects to a cost-effective storage class.
  - Blocks public access by default.

WafStack
~~~~~~~~
- **Purpose:**
  Implements a Web Application Firewall (WAF) to protect the application.
- **Key Elements:**
  - Creates a WAF WebACL (Access Control List) with rules for rate limiting, SQL injection protection, and mitigating common vulnerabilities.
  - Associates the WAF with the frontend Application Load Balancer to monitor and filter incoming traffic.

Dockerfiles
-----------
Dockerfiles define the process of building Docker images for our application components:

- **Frontend Dockerfile (``modules/odr_frontend/docker/Dockerfile.frontend.dev``):**
  Specifies the instructions to build the frontend application image.
- **Backend Dockerfile (``modules/odr_api/docker/Dockerfile.api``):**
  Specifies the instructions to build the backend API image.

These Docker images are built in the GitHub Actions workflow and pushed to the ECR repositories, from where they are deployed by the ECS stack.

Overall Workflow
----------------
1. **Development:**
   Code changes are made locally and pushed to the repository.

2. **CI/CD Pipeline:**
   The GitHub Actions workflow automatically:
   - Builds the Docker images.
   - Pushes the images to AWS ECR.
   - Deploys or updates the cloud infrastructure via AWS CDK (based on the selected deployment mode).

3. **Production Deployment:**
   The application runs on AWS using a combination of managed services (ECS for containers,
   RDS for databases, S3 for storage, etc.), with the infrastructure defined and maintained
   through code.
