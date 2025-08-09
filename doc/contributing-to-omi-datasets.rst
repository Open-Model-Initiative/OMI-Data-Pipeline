Contributing to OMI Datasets
=============================

Overview
--------

Thank you for your interest in helping out with the Open Model Initiative!

The OMI machine learning working group is looking to get as much properly licensed, community-driven content as possible to help support the OMI ML team's progress. We're asking our community to share images that we can collect and organize into datasets on Hugging Face.

In addition to training our own models, one of the goals of the OMI is to freely share tools and datasets with the wider community and enable other AI projects. As such, our datasets will use the 'Community Data License Agreement – Permissive, Version 2.0' license. Ensure you read and understand https://cdla.dev/permissive-2-0/ before contributing. Note, OMI cannot provide legal guidance on licensing matters.

What We Need
------------

We're looking for images! Depending on the number of images we receive, we're loosely planning to organize them into 4 datasets:

1. **Photography** - Standard photographs of real-world subjects
2. **Digital art** - Created artwork and illustrations
3. **HDR/RAW photography or HDR digital art** - High dynamic range or raw format images
4. **Synthetic or generated art** - AI-generated images

For photography, please see our separate Photography Dataset Guidelines for guidance on creating valuable photography datasets. Similarly, for synthetic/generated images, please see our Synthetic Images Guidelines. (TBD by Temporarium)

If you have more than one type of data, please separate your data into these 4 categories.

**Important:** Please review all guidelines below before taking or submitting any images, especially the `Content Policy Requirements`_.

Contribution Requirements
-------------------------

For any images you contribute, you must:

- Have taken or created the image yourself
- Own the copyright
- Have permission to license the work under the specified terms and license
- Read, understand and follow the Hugging Face Content Policy: https://huggingface.co/content-policy

Content Policy Requirements
---------------------------

All contributions must comply with the Hugging Face Content Policy (https://huggingface.co/content-policy). This policy covers:

- Prohibited content types and restrictions
- Requirements for consent and privacy
- Legal compliance standards
- Community guidelines and standards

By contributing to our datasets, you are agreeing to follow all aspects of the Hugging Face Content Policy.

Additional Ethical Guidelines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

While the Hugging Face Content Policy covers most requirements, please also consider:

Legal Compliance
^^^^^^^^^^^^^^^^

- All photographs must be taken legally
- Do not trespass to take pictures
- You are responsible for complying with local laws

Location Considerations
^^^^^^^^^^^^^^^^^^^^^^^

- Do not photograph private areas without permission
- Avoid photos of single residences (including your own, for safety)
- Photos of larger buildings (apartments, street scenes) are acceptable

Information Security
^^^^^^^^^^^^^^^^^^^^

- Do not include personally identifying information (personal emails, addresses, phone numbers)
- Business signs intended for public viewing are acceptable
- Incidental house numbers and license plates in backgrounds are okay

How to Contribute
-----------------

Step 1: Set Up Your Account
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Create a Hugging Face account: https://huggingface.co/join
2. Familiarize yourself with the platform if needed

Step 2: Prepare Your Images
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Sort images into the appropriate categories (Photography, Digital Art, HDR/RAW, Synthetic)
2. Ensure your images all comply with the Hugging Face Content Policy
3. Ensure you own the copyright to all images and that they do not contain anyone else's copyrights
4. **Important** Ensure your images do not contain any sensitive metadata such as your location if not intended. Please see our separate guide on viewing and cleaning out image metadata as necessary.

Step 3: Find the appropriate OMI dataset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For each category of images, find the appropriate dataset and navigate to the Files and Versions tab:

- For Photography: https://huggingface.co/datasets/openmodelinitiative/photography/tree/main
- For Digital art: https://huggingface.co/datasets/openmodelinitiative/digital-art/tree/main
- For HDR or RAW images: https://huggingface.co/datasets/openmodelinitiative/hdr-or-raw/tree/main
- For synthetic or generated images: https://huggingface.co/datasets/openmodelinitiative/synthetic-images/tree/main

Step 4: Submit your pull request
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. In the top right of the page, click the '+ Contribute' button.
2. Select "Upload files"
3. Use the file selector to select your images for this dataset.
4. **Important** Add the following to the 'Add an extended description...' section of the pull request or we will not be able to accept your pull request:

   I agree to the following:

   - [x] I have read, understood, and agree to comply with the Hugging Face Content Policy: https://huggingface.co/content-policy
   - [x] I have done my best to follow the quality guidelines provided by the OMI team.
   - [x] I attest that I own the copyright to all images I am submitting
   - [x] I have read, understood, and agree to the terms of the following Developer Certificate of Origin:

   .. code-block:: text

      Developer Certificate of Origin Version 1.1

      Copyright (C) 2004, 2006 The Linux Foundation and its contributors. 1 Letterman Drive Suite D4700 San Francisco, CA, 94129

      Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed.

      Developer's Certificate of Origin 1.1

      By making a contribution to this project, I certify that:

      (a) The contribution was created in whole or in part by me and I have the right to submit it under the open source license indicated in the file; or

      (b) The contribution is based upon previous work that, to the best of my knowledge, is covered under an appropriate open source license and I have the right under that license to submit that work with modifications, whether created in whole or in part by me, under the same open source license (unless I am permitted to submit under a different license), as indicated in the file; or

      (c) The contribution was provided directly to me by some other person who certified (a), (b) or (c) and I have not modified it.

      (d) I understand and agree that this project and the contribution are public and that a record of the contribution (including all personal information I submit with it, including my sign-off) is maintained indefinitely and may be redistributed consistent with this project or the open source license(s) involved.

5. Click "Open a Pull Request"

Step 5: Wait for your pull request to be reviewed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Members of OMI should be automatically notified of a new PR being made in our datasets, but please feel free to reach out in our Discord in the #data-working-public channel if you don't hear anything or see any progress on the PR after a couple days!

FAQ
---

What happened to the OMI Data Pipeline application?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We want the community to start providing data to the Machine Learning working group without waiting for completion of the OMI Data Pipeline application.

We're still seeking committed developers with experience in Sveltekit, AWS, Docker, etc. to help with that initiative. However, we don't want to delay the machine learning team due to limited members currently on the data working group or their availability.

Can images be removed after submission?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can remove images from active datasets by removing the file. However, images may still appear in the Hugging Face commit history, and the permissive licensing means copies may have already been made. We will make best efforts to honor removal requests while working within the constraints of the platform and licensing structure.

Questions?
----------

If you have questions about these guidelines or the contribution process, please reach out in the #data-working-public channel.

Thank you for helping build open, community-driven AI datasets!
