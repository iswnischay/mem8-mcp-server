# mem8 MCP Server on GitHub Codespaces

Complete guide to running the mem8 MCP server in GitHub Codespaces.

---

## 🚀 Quick Start

### Step 1: Create Codespace from MCP Server Directory

**Option A: From GitHub UI**

1. Go to https://github.com/iswnischay/mem08
2. Press `.` (period key) to open github.dev
3. Or create codespace and navigate to `mem8-mcp-server/` folder

**Option B: Direct Link**
Create a codespace that opens directly in the MCP server directory

### Step 2: Set Environment Variables

Create a `.env` file or set as Codespace secrets:

```bash
cat > .env << 'EOF'
VITE_FIREBASE_API_KEY=AIzaSyC5ieG4PgXYXTn0BvUFVK_NixcCXElnXjE
VITE_FIREBASE_AUTH_DOMAIN=mem-08.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=mem-08
EOF
```

Or export them:

```bash
export VITE_FIREBASE_API_KEY="AIzaSyC5ieG4PgXYXTn0BvUFVK_NixcCXElnXjE"
export VITE_FIREBASE_AUTH_DOMAIN="mem-08.firebaseapp.com"
export VITE_FIREBASE_PROJECT_ID="mem-08"
```

### Step 3: Build Docker Image

```bash
docker build -t mem8-mcp-server .
```

### Step 4: Run MCP Server

**Interactive mode (for testing):**

```bash
docker run -it --rm \
  -v mem8-session-data:/tmp \
  -e VITE_FIREBASE_API_KEY="${VITE_FIREBASE_API_KEY}" \
  -e VITE_FIREBASE_AUTH_DOMAIN="${VITE_FIREBASE_AUTH_DOMAIN}" \
  -e VITE_FIREBASE_PROJECT_ID="${VITE_FIREBASE_PROJECT_ID}" \
  mem8-mcp-server:latest
```

**Test with MCP protocol:**

```bash
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | \
docker run -i --rm \
  -v mem8-session-data:/tmp \
  -e VITE_FIREBASE_API_KEY="${VITE_FIREBASE_API_KEY}" \
  -e VITE_FIREBASE_AUTH_DOMAIN="${VITE_FIREBASE_AUTH_DOMAIN}" \
  -e VITE_FIREBASE_PROJECT_ID="${VITE_FIREBASE_PROJECT_ID}" \
  mem8-mcp-server:latest
```

---

## 🔧 Manual Setup (Without Docker)

If you want to run the MCP server directly in Python:

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Set Environment Variables

```bash
export VITE_FIREBASE_API_KEY="AIzaSyC5ieG4PgXYXTn0BvUFVK_NixcCXElnXjE"
export VITE_FIREBASE_AUTH_DOMAIN="mem-08.firebaseapp.com"
export VITE_FIREBASE_PROJECT_ID="mem-08"
```

### Step 3: Run Server

```bash
python mem8_server.py
```

---

## 🧪 Testing MCP Tools

Once the server is running, test each tool:

### Test Authentication

```bash
echo '{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "mem8_authenticate",
    "arguments": {
      "email": "your@email.com",
      "password": "yourpassword"
    }
  },
  "id": 1
}' | docker run -i --rm \
  -v mem8-session-data:/tmp \
  -e VITE_FIREBASE_API_KEY="${VITE_FIREBASE_API_KEY}" \
  -e VITE_FIREBASE_AUTH_DOMAIN="${VITE_FIREBASE_AUTH_DOMAIN}" \
  -e VITE_FIREBASE_PROJECT_ID="${VITE_FIREBASE_PROJECT_ID}" \
  mem8-mcp-server:latest
```

### Test List Secrets

```bash
echo '{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "mem8_list_secrets",
    "arguments": {}
  },
  "id": 2
}' | docker run -i --rm \
  -v mem8-session-data:/tmp \
  -e VITE_FIREBASE_API_KEY="${VITE_FIREBASE_API_KEY}" \
  -e VITE_FIREBASE_AUTH_DOMAIN="${VITE_FIREBASE_AUTH_DOMAIN}" \
  -e VITE_FIREBASE_PROJECT_ID="${VITE_FIREBASE_PROJECT_ID}" \
  mem8-mcp-server:latest
```

---

## 🌐 Exposing MCP Server as HTTP API

If you want to access the MCP server via HTTP (useful for testing in Codespaces):

### Create a Simple HTTP Wrapper

```python
# http_wrapper.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FIREBASE_API_KEY = os.getenv("VITE_FIREBASE_API_KEY")
FIREBASE_AUTH_DOMAIN = os.getenv("VITE_FIREBASE_AUTH_DOMAIN")
FIREBASE_PROJECT_ID = os.getenv("VITE_FIREBASE_PROJECT_ID")

def run_mcp_tool(tool_name, arguments):
    """Run MCP tool via Docker"""
    mcp_request = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        },
        "id": 1
    }

    cmd = [
        "docker", "run", "-i", "--rm",
        "-v", "mem8-session-data:/tmp",
        "-e", f"VITE_FIREBASE_API_KEY={FIREBASE_API_KEY}",
        "-e", f"VITE_FIREBASE_AUTH_DOMAIN={FIREBASE_AUTH_DOMAIN}",
        "-e", f"VITE_FIREBASE_PROJECT_ID={FIREBASE_PROJECT_ID}",
        "mem8-mcp-server:latest"
    ]

    result = subprocess.run(
        cmd,
        input=json.dumps(mcp_request),
        capture_output=True,
        text=True
    )

    return json.loads(result.stdout)

@app.post("/authenticate")
async def authenticate(email: str, password: str):
    return run_mcp_tool("mem8_authenticate", {"email": email, "password": password})

@app.get("/secrets")
async def list_secrets():
    return run_mcp_tool("mem8_list_secrets", {})

@app.get("/secrets/{key}")
async def get_secret(key: str):
    return run_mcp_tool("mem8_get_secret", {"key": key})

@app.post("/secrets/{key}")
async def add_secret(key: str, value: str):
    return run_mcp_tool("mem8_add_secret", {"key": key, "value": value})

@app.delete("/secrets/{key}")
async def delete_secret(key: str):
    return run_mcp_tool("mem8_delete_secret", {"key": key})

@app.post("/logout")
async def logout():
    return run_mcp_tool("mem8_logout", {})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Install FastAPI

```bash
pip install fastapi uvicorn
```

### Run HTTP Wrapper

```bash
python http_wrapper.py
```

Access at: `http://localhost:8000/docs`

---

## 🔐 Setting Codespace Secrets

For secure credential management:

1. Go to https://github.com/settings/codespaces
2. Click **"New secret"**
3. Add these secrets:
   - `VITE_FIREBASE_API_KEY`
   - `VITE_FIREBASE_AUTH_DOMAIN`
   - `VITE_FIREBASE_PROJECT_ID`
4. Select `mem08` repository

These will automatically be available in your codespace!

---

## 📡 Using with Claude Desktop from Codespaces

**Note:** Claude Desktop cannot directly connect to a Codespaces MCP server since it requires local Docker access.

**Alternative approaches:**

### 1. Export MCP Server as REST API

- Use the HTTP wrapper above
- Expose via Codespaces port forwarding
- Create a client wrapper for Claude

### 2. Use Codespaces for Development Only

- Develop and test MCP server in Codespaces
- Deploy Docker image to Docker Hub
- Use from local Claude Desktop

### 3. Run MCP Server Locally

- Keep server running on your local machine
- Use Codespaces only for development/testing

---

## 🐛 Troubleshooting

### Devcontainer creation fails with Docker-in-Docker error

**Error:** `The 'moby' option is not supported on Debian 'trixie'`

**Solution:** Make sure you're using the latest version of the devcontainer configuration, which specifies `python:3.11-bookworm` instead of the default `python:3.11`. This fix is already in the repository.

If you still see this error:
1. Delete the codespace
2. Create a new one (it will use the updated config)

### Docker not working in Codespaces

If Docker commands fail:

```bash
# Check Docker is running
docker ps

# If not, restart Docker
sudo service docker start
```

### Session persistence issues

The volume mount may not work perfectly in Codespaces. For testing, you can:

```bash
# Use host filesystem instead
docker run -i --rm \
  -v $(pwd)/session:/tmp \
  -e VITE_FIREBASE_API_KEY="${VITE_FIREBASE_API_KEY}" \
  -e VITE_FIREBASE_AUTH_DOMAIN="${VITE_FIREBASE_AUTH_DOMAIN}" \
  -e VITE_FIREBASE_PROJECT_ID="${VITE_FIREBASE_PROJECT_ID}" \
  mem8-mcp-server:latest
```

### Port forwarding

Codespaces automatically forwards ports. If you're running HTTP wrapper:

- Port 8000 will be auto-forwarded
- Access via the Ports tab
- Click globe icon to open in browser

---

## 🎯 Best Use Cases for Codespaces

✅ **Development & Testing**

- Modify MCP server code
- Test new tools
- Debug issues

✅ **Building Docker Images**

- Build and test containers
- Push to Docker Hub
- CI/CD integration

✅ **HTTP API Development**

- Develop REST API wrapper
- Test with Postman/curl
- Share with team

❌ **Not Ideal For**

- Direct Claude Desktop integration (needs local Docker)
- Production deployment
- Long-running server (codespaces timeout)

---

## 📚 Additional Resources

- **INSTALLATION_GUIDE.md** - Full local setup
- **QUICKSTART.md** - Quick reference
- **CLAUDE.md** - Technical details
- **Main README** - Project overview

---

**For production use with Claude Desktop, deploy locally or to a Docker registry!**
