#!/bin/bash
# Simple interactive test for mem8 MCP server

echo "=== mem8 MCP Server - Interactive Test ==="
echo ""
echo "Starting MCP server in interactive mode..."
echo "You can now test the server with MCP protocol messages."
echo ""
echo "The server will:"
echo "1. Wait for 'initialize' request first"
echo "2. Then accept tool calls like 'tools/list', 'tools/call', etc."
echo ""
echo "Press Ctrl+C to exit"
echo ""
echo "---"

docker run -i --rm \
  -v mem8-session-data:/tmp \
  -e VITE_FIREBASE_API_KEY="${VITE_FIREBASE_API_KEY}" \
  -e VITE_FIREBASE_AUTH_DOMAIN="${VITE_FIREBASE_AUTH_DOMAIN}" \
  -e VITE_FIREBASE_PROJECT_ID="${VITE_FIREBASE_PROJECT_ID}" \
  mem8-mcp-server:latest
