# mem8 Secrets Manager MCP Server

A Model Context Protocol (MCP) server that provides secure access to the mem8 secrets management application through AI assistants.

## Purpose

This MCP server provides a secure interface for AI assistants to interact with mem8, allowing them to:
- Authenticate users
- List stored secrets
- Retrieve secret values
- Add or update secrets
- Delete secrets
- Manage authentication sessions

## Features

### Current Implementation

- **`mem8_authenticate`** - Authenticate with email and password to access secrets
- **`mem8_list_secrets`** - List all secret keys for the authenticated user
- **`mem8_get_secret`** - Retrieve a specific secret value by key
- **`mem8_add_secret`** - Add or update a secret with key and value
- **`mem8_delete_secret`** - Delete a secret by key
- **`mem8_logout`** - Clear authentication credentials

## Prerequisites

- Docker Desktop with MCP Toolkit enabled
- Docker MCP CLI plugin (`docker mcp` command)
- Firebase project configured (mem8 application)
- Valid mem8 user account

## Installation

Follow the step-by-step instructions in the Installation section below.

## Usage Examples

In Claude Desktop, you can ask:

- "Authenticate to mem8 with my email and password"
- "List all my secrets in mem8"
- "Get the value of the AWS_API_KEY secret from mem8"
- "Add a new secret called DATABASE_URL with value xyz123"
- "Delete the OLD_API_KEY secret from mem8"
- "Logout from mem8"

## Architecture

```
Claude Desktop → MCP Gateway → mem8 MCP Server → Firebase REST API
                                      ↓
                          Docker Desktop Secrets
                          (Firebase Credentials)
```

## Development

### Local Testing

```bash
# Set environment variables for testing
export VITE_FIREBASE_API_KEY="your-api-key"
export VITE_FIREBASE_PROJECT_ID="your-project-id"
export VITE_FIREBASE_AUTH_DOMAIN="your-auth-domain"

# Run directly
python mem8_server.py

# Test MCP protocol
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python mem8_server.py
```

### Adding New Tools

1. Add the function to `mem8_server.py`
2. Decorate with `@mcp.tool()`
3. Update the catalog entry with the new tool name
4. Rebuild the Docker image

## Troubleshooting

### Tools Not Appearing

- Verify Docker image built successfully: `docker images | grep mem8`
- Check catalog and registry files
- Ensure Claude Desktop config includes custom catalog
- Restart Claude Desktop completely

### Authentication Errors

- Verify secrets with `docker mcp secret list`
- Ensure secret names match: VITE_FIREBASE_API_KEY, VITE_FIREBASE_PROJECT_ID, VITE_FIREBASE_AUTH_DOMAIN
- Check that Firebase credentials are correct

### API Errors

- Verify Firebase project is active and accessible
- Check that Firestore database exists and has proper rules
- Ensure user account exists in Firebase Authentication

## Security Considerations

- All Firebase credentials stored in Docker Desktop secrets
- Never hardcode API keys or credentials
- Running as non-root user in Docker container
- Authentication tokens are session-based and cleared on logout
- Sensitive data never logged to stdout

## License

MIT License
