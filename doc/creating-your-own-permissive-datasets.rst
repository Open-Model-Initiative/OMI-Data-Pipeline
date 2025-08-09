Creating Your Own Permissive Datasets
======================================

Overview
--------

This is a guide to help you create your own permissive datasets on Hugging Face.

Contribution Requirements
-------------------------

For any images you upload, you must:

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

By uploading datasets on Hugging Face, you are agreeing to follow all aspects of the Hugging Face Content Policy.

Suggested Contribution Guidelines
---------------------------------

For photography, please see our separate Photography Dataset Guidelines for guidance on creating valuable photography datasets. Similarly, for synthetic/generated images, please see our Synthetic Images Guidelines. (TBD by Temporarium)

How to Contribute
-----------------

Step 1: Set Up Your Account
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Create a Hugging Face account: https://huggingface.co/join
2. Familiarize yourself with the platform if needed

Step 2: Create your Hugging Face Dataset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Follow the steps on https://huggingface.co/docs/datasets/en/upload_dataset#upload-with-the-hub-ui to create your hugging face dataset. Ensure you set the dataset to public so others can see and use it.
2. Edit the dataset card by clicking the 'Edit dataset card' button, and set the license to 'Community Data License Agreement – Permissive, Version 2.0'. Ensure you read and understand https://cdla.dev/permissive-2-0/ before contributing. Note, OMI cannot provide legal guidance on licensing matters.
3. If your dataset will have any adult content, ensure you add the tag 'not-for-all-audiences'.

Step 3: Prepare Your Images
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Ensure your images all comply with the Hugging Face Content Policy
2. Ensure you own the copyright to all images and that they do not contain anyone else's copyrights
3. **Important** Ensure your images do not contain any sensitive metadata such as your location if not intended. Please see our separate guide on viewing and cleaning out image metadata as necessary.

Step 4: Upload Your Images
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Follow the instructions on https://huggingface.co/docs/datasets/en/upload_dataset#upload-dataset to upload your images, however
2. **Important** Add the following to the 'Add an extended description...' section of the pull request to ensure OMI and others are able to use your dataset:

   I agree to the following:

   - [x] I have read, understood, and agree to comply with the Hugging Face Content Policy: https://huggingface.co/content-policy
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

3. Click "Commit Changes"

What Next?
----------

Thank you for helping build open, community-driven AI datasets!

Please feel free to reach out to us in the Open Model Initiative Discord in the #data-working-public to help us find your dataset!
