# Open Data Repository

This schema is the potential data model for a utility tool to support the training of vision and image models. It is focused on gathering annotations on images sourced from the community, and different caption sets of those images. It has a significant focus on moderation of the dataset to ensure that illegal content is not allowed, and certain subject can be filtered out easily from training of a model. 

It will be implemented with fastapi, postgres, and nextjs. We will likely want an orm like sqlalchemy with alembic to support data migrations. 

## Schema
```
user
  id
  type (user, bot)
  name
  email
  createdAt
  updateAt

team
  id
  permissions (can add embeddingEngines, can add annotation source)
  limits // rate limit to adding things
  name
  teamUsers*

teamUser
  team*
  user*
  permissions (can add, can remove, can post content, can post annotations)
  createdAt
  updatedAt

content
  id
  name?
  type (image, video, voice, music, text)
  hash
  phash
  url? []
  width
  height
  format (png, jpg, webp)
  size (bytes)
  status (pending, available, unavailable, delisted)
  license (cc0, copyrighted, CC BY-NC-SA...)
  licenseUrl?
  contentAuthor?[]*
  flags (bitwise flags: synthetic)
  meta (store data specific to the content, for example generation details for synthetic content)
  fromUser*
  fromTeam?*
  annotations*
  embeddings*
  createdAt
  updatedAt
  
contentAuthor
  id
  name
  url
  createdAt
  updateAt

contentEmbedding
  content*
  embedding
  embeddingEngine*
  fromUser*
  fromTeam?*
  createdAt
  updatedAt

embeddingEngine
  id
  name
  addedBy*
  createdAt
  updatedAt

contentEvents
  content*
  status
  setBy
  note?
  createdAt

contentReport
  contentId
  type (mislicensed, missing, illegal content)
  note?
  reportedBy*

contentSet
  id
  name
  description
  contents*
  fromUser*
  fromTeam?*
  createdAt
  updatedAt

annotation
  id
  content*
  annotation (json)
  annotationSource[]*
  manuallyAdjusted 
  embedding?
  fromUser*
  fromTeam?*
  createdAt
  updateAt
  overallRating
  
annotationEmbedding
  annotation*
  embedding
  embeddingEngine*
  fromUser*
  fromTeam?*
  createdAt
  updatedAt

annotationRating
  annotationId
  rating (0-10)
  reason? (mistake, incomplete, low quality)
  ratedBy*

annotationReport
  annotationId
  type (illegal content, malicious annotations)
  reportedBy*

annotationSource
  id
  name
  ecosystem? (a way to group different versions of the same annotator)
  type (content description, spatial analysis, tags)
  annotationSchema (used to validate the shape of the annotation submitted)
  license
  licenseUrl
  addedBy*
  createdAt
  updateAt
```

## Services
- Register a user
- Register a team
- Manage a team
- Add content to repo
- Report content
- Add annotations to content
- Report annotations
- Manage a content set
- Request an annotation dump

## Implementation Details
- Content would not be available until initial scans were done that assure:
  - The content is accessible
  - Basic annotations are ran:
    - does it contain a child?
    - does it contain sexual content?
    - does it contain violence?