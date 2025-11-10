#!/bin/bash
# Test script for mem8 MCP server

# Check environment variables
if [ -z "$VITE_FIREBASE_API_KEY" ]; then
    echo "Error: VITE_FIREBASE_API_KEY not set"
    exit 1
fi

echo "=== Testing mem8 MCP Server ==="
echo ""

# Test 1: Initialize
echo "1. Initialize connection..."
echo '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test-client","version":"1.0.0"}},"id":1}' | \
docker run -i --rm \
  -v mem8-session-data:/tmp \
  -e VITE_FIREBASE_API_KEY="${VITE_FIREBASE_API_KEY}" \
  -e VITE_FIREBASE_AUTH_DOMAIN="${VITE_FIREBASE_AUTH_DOMAIN}" \
  -e VITE_FIREBASE_PROJECT_ID="${VITE_FIREBASE_PROJECT_ID}" \
  mem8-mcp-server:latest

echo ""
echo "2. List available tools..."
echo '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test-client","version":"1.0.0"}},"id":1}
{"jsonrpc":"2.0","method":"tools/list","id":2}' | \
docker run -i --rm \
  -v mem8-session-data:/tmp \
  -e VITE_FIREBASE_API_KEY="${VITE_FIREBASE_API_KEY}" \
  -e VITE_FIREBASE_AUTH_DOMAIN="${VITE_FIREBASE_AUTH_DOMAIN}" \
  -e VITE_FIREBASE_PROJECT_ID="${VITE_FIREBASE_PROJECT_ID}" \
  mem8-mcp-server:latest

echo ""
echo "=== Test complete! ==="
