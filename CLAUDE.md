# mem8 MCP Server - Claude Desktop Integration Guide

## Overview

This MCP server allows Claude Desktop to securely interact with the mem8 secrets management application. It provides tools for managing secrets stored in Firebase Firestore.

## Implementation Details

### Architecture

The server uses Firebase REST APIs to interact with:

- Firebase Authentication (for user login)
- Cloud Firestore (for secrets storage)

### Authentication Flow

1. User authenticates via `mem8_authenticate` with email/password
2. Firebase returns an ID token and user ID
3. Token is stored in server memory for subsequent requests
4. Token is used for all Firestore operations
5. User can logout to clear credentials

### Data Storage

Secrets are stored in Firestore at:

```
/users/{userId}/secrets/{secretKey}
  - value: string
```

### Security Features

- Credentials never hardcoded
- Firebase credentials stored as Docker secrets
- User tokens are session-based
- All operations require authentication
- Non-root Docker user
- All secrets transmitted over HTTPS

## Tool Descriptions

### mem8_authenticate

- **Purpose**: Login to mem8 account
- **Parameters**: email, password
- **Returns**: Success/failure message
- **Note**: Must be called before any other operations

### mem8_list_secrets

- **Purpose**: Get all secret keys for authenticated user
- **Parameters**: None
- **Returns**: Formatted list of secret keys
- **Note**: Only shows keys, not values

### mem8_get_secret

- **Purpose**: Retrieve specific secret value
- **Parameters**: key (secret name)
- **Returns**: Secret key and value
- **Security**: Value is displayed - handle carefully

### mem8_add_secret

- **Purpose**: Create or update a secret
- **Parameters**: key (secret name), value (secret content)
- **Returns**: Success/failure message
- **Note**: Overwrites existing secrets with same key

### mem8_delete_secret

- **Purpose**: Remove a secret permanently
- **Parameters**: key (secret name)
- **Returns**: Success/failure message
- **Note**: Cannot be undone

### mem8_logout

- **Purpose**: Clear authentication credentials
- **Parameters**: None
- **Returns**: Logout confirmation
- **Note**: Requires re-authentication for future operations

## Configuration Requirements

The following environment variables must be set as Docker secrets:

- `VITE_FIREBASE_API_KEY` - Firebase Web API key
- `VITE_FIREBASE_PROJECT_ID` - Firebase project identifier
- `VITE_FIREBASE_AUTH_DOMAIN` - Firebase auth domain

These match the mem8 web application configuration for consistency.

## Error Handling

All tools return user-friendly error messages:

- ❌ for errors
- ✅ for success
- ⚠️ for warnings
- 🔒 for secrets-related operations
- 📭 for empty results

## Usage Guidelines

1. Always authenticate first
2. List secrets to see what's available
3. Get specific secrets only when needed
4. Add secrets with descriptive keys
5. Delete secrets when no longer needed
6. Logout when done to clear credentials

## Development Notes

- Uses Firebase REST API instead of Admin SDK for simplicity
- Session state stored in memory (not persistent)
- All operations are async using httpx
- Comprehensive logging to stderr for debugging
- Follows MCP best practices (single-line docstrings, string returns)

## Future Enhancements

Potential additions:

- Secret expiration/rotation
- Secret sharing between users
- Audit logging
- Secret categories/tags
- Bulk operations
- Secret search functionality
