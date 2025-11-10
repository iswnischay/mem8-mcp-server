#!/usr/bin/env python3
"""
Simple mem8 Secrets Manager MCP Server - Secure secrets management through AI
"""
import os
import sys
import logging
import json
from datetime import datetime, timezone
from pathlib import Path
import httpx
from mcp.server.fastmcp import FastMCP

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("mem8-server")

# Initialize MCP server
mcp = FastMCP("mem8")

# Configuration
FIREBASE_API_KEY = os.environ.get("VITE_FIREBASE_API_KEY", "")
FIREBASE_AUTH_DOMAIN = os.environ.get("VITE_FIREBASE_AUTH_DOMAIN", "")
FIREBASE_PROJECT_ID = os.environ.get("VITE_FIREBASE_PROJECT_ID", "")
FIREBASE_REST_API = f"https://identitytoolkit.googleapis.com/v1/accounts"

# Session file path (persistent across calls)
SESSION_FILE = Path("/tmp/mem8_session.json")

# === SESSION MANAGEMENT ===

def load_session():
    """Load session from file."""
    try:
        if SESSION_FILE.exists():
            with open(SESSION_FILE, 'r') as f:
                session = json.load(f)
                logger.info(f"Loaded session for user: {session.get('uid', 'unknown')[:8]}...")
                return session
    except Exception as e:
        logger.error(f"Error loading session: {e}")
    return {"uid": "", "token": ""}

def save_session(uid, token):
    """Save session to file."""
    try:
        session = {"uid": uid, "token": token}
        SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(SESSION_FILE, 'w') as f:
            json.dump(session, f)
        logger.info(f"Session saved for user: {uid[:8]}...")
    except Exception as e:
        logger.error(f"Error saving session: {e}")

def clear_session():
    """Clear session file."""
    try:
        if SESSION_FILE.exists():
            SESSION_FILE.unlink()
        logger.info("Session cleared")
    except Exception as e:
        logger.error(f"Error clearing session: {e}")

# === UTILITY FUNCTIONS ===

def format_secret_list(secrets):
    """Format secrets list for display."""
    if not secrets:
        return "📭 No secrets found"
    
    output = "🔒 Secrets List:\n\n"
    for secret in secrets:
        output += f"• {secret.get('key', 'Unknown')}\n"
    return output

def format_secret_detail(key, value):
    """Format secret detail for display."""
    return f"""🔐 Secret Retrieved:

Key: {key}
Value: {value}

⚠️ Handle this information securely!"""

# === MCP TOOLS ===

@mcp.tool()
async def mem8_authenticate(email: str = "", password: str = "") -> str:
    """Authenticate with mem8 using email and password to access secrets."""
    logger.info(f"Authenticating user: {email}")
    
    if not email.strip() or not password.strip():
        return "❌ Error: Email and password are required"
    
    if not FIREBASE_API_KEY:
        return "❌ Error: Firebase API key not configured"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{FIREBASE_REST_API}:signInWithPassword?key={FIREBASE_API_KEY}",
                json={
                    "email": email,
                    "password": password,
                    "returnSecureToken": True
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                uid = data.get("localId", "")
                token = data.get("idToken", "")
                
                # Save session to persistent storage
                save_session(uid, token)
                
                logger.info(f"Authentication successful for {email}")
                return f"✅ Successfully authenticated as {email}"
            else:
                error_data = response.json()
                error_msg = error_data.get("error", {}).get("message", "Unknown error")
                return f"❌ Authentication failed: {error_msg}"
                
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e}")
        return f"❌ Authentication error: {e.response.status_code}"
    except Exception as e:
        logger.error(f"Error: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def mem8_list_secrets() -> str:
    """List all secret keys stored in mem8 for the authenticated user."""
    logger.info("Listing secrets")
    
    # Load session from persistent storage
    session = load_session()
    
    if not session.get("uid") or not session.get("token"):
        return "❌ Error: Not authenticated. Please use mem8_authenticate first"
    
    if not FIREBASE_PROJECT_ID:
        return "❌ Error: Firebase project ID not configured"
    
    try:
        async with httpx.AsyncClient() as client:
            url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents/users/{session['uid']}/secrets"
            
            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {session['token']}"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                documents = data.get("documents", [])
                
                secrets = []
                for doc in documents:
                    doc_name = doc.get("name", "")
                    key = doc_name.split("/")[-1] if doc_name else "Unknown"
                    secrets.append({"key": key})
                
                return format_secret_list(secrets)
            elif response.status_code == 404:
                return "📭 No secrets found"
            else:
                return f"❌ Error: Failed to list secrets (Status: {response.status_code})"
                
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e}")
        return f"❌ API Error: {e.response.status_code}"
    except Exception as e:
        logger.error(f"Error: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def mem8_get_secret(key: str = "") -> str:
    """Retrieve a specific secret value by its key from mem8."""
    logger.info(f"Getting secret: {key}")
    
    if not key.strip():
        return "❌ Error: Secret key is required"
    
    # Load session from persistent storage
    session = load_session()
    
    if not session.get("uid") or not session.get("token"):
        return "❌ Error: Not authenticated. Please use mem8_authenticate first"
    
    if not FIREBASE_PROJECT_ID:
        return "❌ Error: Firebase project ID not configured"
    
    try:
        async with httpx.AsyncClient() as client:
            url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents/users/{session['uid']}/secrets/{key}"
            
            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {session['token']}"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                fields = data.get("fields", {})
                value = fields.get("value", {}).get("stringValue", "")
                return format_secret_detail(key, value)
            elif response.status_code == 404:
                return f"❌ Error: Secret '{key}' not found"
            else:
                return f"❌ Error: Failed to retrieve secret (Status: {response.status_code})"
                
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e}")
        return f"❌ API Error: {e.response.status_code}"
    except Exception as e:
        logger.error(f"Error: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def mem8_add_secret(key: str = "", value: str = "") -> str:
    """Add or update a secret in mem8 with the specified key and value."""
    logger.info(f"Adding secret: {key}")
    
    if not key.strip():
        return "❌ Error: Secret key is required"
    
    # Load session from persistent storage
    session = load_session()
    
    if not session.get("uid") or not session.get("token"):
        return "❌ Error: Not authenticated. Please use mem8_authenticate first"
    
    if not FIREBASE_PROJECT_ID:
        return "❌ Error: Firebase project ID not configured"
    
    try:
        async with httpx.AsyncClient() as client:
            url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents/users/{session['uid']}/secrets/{key}"
            
            response = await client.patch(
                url,
                headers={
                    "Authorization": f"Bearer {session['token']}",
                    "Content-Type": "application/json"
                },
                json={
                    "fields": {
                        "value": {"stringValue": value}
                    }
                },
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                return f"✅ Secret '{key}' added successfully"
            else:
                return f"❌ Error: Failed to add secret (Status: {response.status_code})"
                
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e}")
        return f"❌ API Error: {e.response.status_code}"
    except Exception as e:
        logger.error(f"Error: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def mem8_delete_secret(key: str = "") -> str:
    """Delete a secret from mem8 by its key."""
    logger.info(f"Deleting secret: {key}")
    
    if not key.strip():
        return "❌ Error: Secret key is required"
    
    # Load session from persistent storage
    session = load_session()
    
    if not session.get("uid") or not session.get("token"):
        return "❌ Error: Not authenticated. Please use mem8_authenticate first"
    
    if not FIREBASE_PROJECT_ID:
        return "❌ Error: Firebase project ID not configured"
    
    try:
        async with httpx.AsyncClient() as client:
            url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents/users/{session['uid']}/secrets/{key}"
            
            response = await client.delete(
                url,
                headers={"Authorization": f"Bearer {session['token']}"},
                timeout=10
            )
            
            if response.status_code == 200:
                return f"✅ Secret '{key}' deleted successfully"
            elif response.status_code == 404:
                return f"❌ Error: Secret '{key}' not found"
            else:
                return f"❌ Error: Failed to delete secret (Status: {response.status_code})"
                
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e}")
        return f"❌ API Error: {e.response.status_code}"
    except Exception as e:
        logger.error(f"Error: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def mem8_logout() -> str:
    """Logout from mem8 and clear authentication credentials."""
    logger.info("Logging out")
    
    # Load session to check if authenticated
    session = load_session()
    
    if not session.get("uid"):
        return "ℹ️ Not currently authenticated"
    
    # Clear the session file
    clear_session()
    
    return "✅ Successfully logged out"

# === SERVER STARTUP ===
if __name__ == "__main__":
    logger.info("Starting mem8 Secrets Manager MCP server...")
    
    # Startup checks
    if not FIREBASE_API_KEY:
        logger.warning("VITE_FIREBASE_API_KEY not set")
    if not FIREBASE_PROJECT_ID:
        logger.warning("VITE_FIREBASE_PROJECT_ID not set")
    
    try:
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)
