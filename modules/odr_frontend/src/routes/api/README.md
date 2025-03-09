# API Layer for Data Access

This directory contains the API layer for data access in the Svelte backend, built using Drizzle ORM. It provides a clean interface for accessing the database from the application code.

## API Endpoints

### Users

- `GET /api/users` - Get all users with optional filtering
  - Query parameters: `limit`, `offset`, `email`

- `GET /api/users/:id` - Get a single user by ID

- `POST /api/users` - Create a new user
  - Required fields: `email`
  - Optional fields: `name`, `isActive`, `isSuperuser`, `dcoAccepted`

- `PUT /api/users/:id` - Update a user
  - Optional fields: `email`, `name`, `isActive`, `isSuperuser`, `dcoAccepted`

- `DELETE /api/users/:id` - Delete a user

### Teams

- `GET /api/teams` - Get all teams with optional filtering
  - Query parameters: `limit`, `offset`, `name`

- `GET /api/teams/:id` - Get a single team by ID

- `GET /api/teams/:id/members` - Get all members of a team

- `POST /api/teams` - Create a new team
  - Required fields: `name`

- `PUT /api/teams/:id` - Update a team
  - Optional fields: `name`

- `DELETE /api/teams/:id` - Delete a team

### User-Team Relationships

- `GET /api/user-teams` - Get all user-team associations with optional filtering
  - Query parameters: `userId`, `teamId`, `limit`, `offset`

- `POST /api/user-teams` - Add a user to a team
  - Required fields: `userId`, `teamId`
  - Optional fields: `role`

- `DELETE /api/user-teams` - Remove a user from a team
  - Query parameters: `userId`, `teamId`

### Contents

- `GET /api/contents` - Get all content items with optional filtering
  - Query parameters: `limit`, `offset`, `name`, `type`, `status`

- `GET /api/contents/:id` - Get a single content item by ID

- `POST /api/contents` - Create a new content item
  - Required fields: `name`, `type`
  - Optional fields: `hash`, `phash`, `width`, `height`, `format`, `size`, `status`, `license`, `licenseUrl`, `flags`, `meta`, `fromUserId`, `fromTeamId`, `url`

- `PUT /api/contents/:id` - Update a content item
  - Optional fields: `name`, `type`, `hash`, `phash`, `width`, `height`, `format`, `size`, `status`, `license`, `licenseUrl`, `flags`, `meta`, `url`

- `DELETE /api/contents/:id` - Delete a content item

### Annotations

- `GET /api/annotations` - Get all annotations with optional filtering
  - Query parameters: `limit`, `offset`, `contentId`, `fromUserId`, `fromTeamId`

- `GET /api/annotations/:id` - Get a single annotation by ID

- `POST /api/annotations` - Create a new annotation
  - Required fields: `contentId`
  - Optional fields: `annotation`, `manuallyAdjusted`, `overallRating`, `fromUserId`, `fromTeamId`

- `PUT /api/annotations/:id` - Update an annotation
  - Optional fields: `annotation`, `manuallyAdjusted`, `overallRating`, `fromUserId`, `fromTeamId`

- `DELETE /api/annotations/:id` - Delete an annotation

### Annotation Sources

- `GET /api/annotation-sources` - Get all annotation sources with optional filtering
  - Query parameters: `limit`, `offset`, `name`, `ecosystem`, `type`

- `POST /api/annotation-sources` - Create a new annotation source
  - Required fields: `name`
  - Optional fields: `ecosystem`, `type`, `annotationSchema`, `license`, `licenseUrl`, `addedById`

### Embeddings

- `GET /api/embeddings/engines` - Get all embedding engines with optional filtering
  - Query parameters: `limit`, `offset`, `type`, `supported`

- `GET /api/embeddings` - Get all content embeddings with optional filtering
  - Query parameters: `limit`, `offset`, `contentId`, `embeddingEngineId`

- `POST /api/embeddings/engines` - Create a new embedding engine
  - Required fields: `name`, `type`
  - Optional fields: `description`, `version`, `supported`

- `POST /api/embeddings` - Create a new content embedding
  - Required fields: `contentId`, `embeddingEngineId`, `embedding`
  - Optional fields: `fromUserId`, `fromTeamId`

### Feature Toggles

- `GET /api/feature-toggles` - Get all feature toggles with optional filtering
  - Query parameters: `limit`, `offset`, `featureName`, `isEnabled`

- `POST /api/feature-toggles` - Create a new feature toggle
  - Required fields: `featureName`
  - Optional fields: `isEnabled`, `defaultState`

- `PUT /api/feature-toggles/:name` - Update a feature toggle
  - Optional fields: `isEnabled`, `defaultState`

## Usage Example

```typescript
// Get all users with pagination
const response = await fetch('/api/users?limit=10&offset=0');
const { data, count } = await response.json();

// Create a new user
const newUser = await fetch('/api/users', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'user@example.com', name: 'John Doe' })
});

// Add a user to a team
const addUserToTeam = await fetch('/api/user-teams', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ userId: 1, teamId: 2, role: 'admin' })
});

// Get annotations for a specific content
const annotations = await fetch('/api/annotations?contentId=123');
const { data: annotationData } = await annotations.json();

// Create a new content item
const newContent = await fetch('/api/contents', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'Example Image',
    type: 'IMAGE',
    format: 'jpeg',
    status: 'PENDING'
  })
});

// Create a new embedding engine
const newEngine = await fetch('/api/embeddings/engines', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'CLIP-ViT-B-32',
    type: 'IMAGE',
    description: 'OpenAI CLIP vision model',
    version: '1.0.0'
  })
});

// Toggle a feature flag
const updateToggle = await fetch('/api/feature-toggles/new-ui', {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ isEnabled: true })
});
```
