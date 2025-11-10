# mem8 MCP Server - Complete Installation Guide

## Prerequisites Check

Before starting, ensure you have:

- [ ] Docker Desktop installed and running
- [ ] Docker MCP Toolkit enabled in Docker Desktop settings
- [ ] `docker mcp` command available (test with `docker mcp --version`)
- [ ] Firebase credentials from the mem8 project
- [ ] A valid mem8 user account (created via the web app)

---

## Step 1: Save the Files

All files should already be in the `mem8-mcp-server` directory:

- Dockerfile
- requirements.txt
- mem8_server.py
- readme.txt
- CLAUDE.md

Verify with:

```powershell
cd E:\mem8\mem8-mcp-server
dir
```

---

## Step 2: Build Docker Image

```powershell
cd E:\mem8\mem8-mcp-server
docker build -t mem8-mcp-server .
```

**Expected output**: Should see "Successfully built" and "Successfully tagged mem8-mcp-server:latest"

Verify the image:

```powershell
docker images | findstr mem8
```

---

## Step 3: Set Up Your Firebase Project

### Option A: Create Your Own Firebase Project (Recommended)

1. **Go to Firebase Console**: https://console.firebase.google.com/
2. **Create New Project**:

   - Click "Add project"
   - Enter project name (e.g., "my-secrets-manager")
   - Disable Google Analytics (optional)
   - Click "Create project"

3. **Enable Authentication**:

   - Go to "Authentication" → "Get started"
   - Click "Email/Password" → Enable → Save
   - Go to "Users" tab → "Add user"
   - Create your account with email/password

4. **Enable Firestore Database**:

   - Go to "Firestore Database" → "Create database"
   - Choose "Start in production mode"
   - Select a location (closest to you)
   - Click "Enable"

5. **Set Security Rules**:

   - In Firestore, go to "Rules" tab
   - Replace with this:

   ```javascript
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       match /secrets/{userId}/items/{secretId} {
         allow read, write: if request.auth != null && request.auth.uid == userId;
       }
     }
   }
   ```

   - Click "Publish"

6. **Get Your Credentials**:
   - Go to "Project Settings" (gear icon) → "General"
   - Scroll to "Your apps" → Click web icon (</>)
   - Register app (name: "mem8-mcp")
   - Copy these values from "Firebase SDK snippet":
     - `apiKey` → Your VITE_FIREBASE_API_KEY
     - `authDomain` → Your VITE_FIREBASE_AUTH_DOMAIN
     - `projectId` → Your VITE_FIREBASE_PROJECT_ID

### Option B: Use Shared Firebase Project

If someone shared their Firebase project with you, they'll provide:

- Firebase API Key
- Auth Domain
- Project ID
- Your email/password for authentication

---

## Step 4: Set Up Firebase Secrets in Docker

Replace the placeholder values with your actual Firebase credentials:

```powershell
# Set Firebase API Key (replace with YOUR values)
docker mcp secret set VITE_FIREBASE_API_KEY=your_api_key_here

# Set Firebase Auth Domain (replace with YOUR values)
docker mcp secret set VITE_FIREBASE_AUTH_DOMAIN=your-project-id.firebaseapp.com

# Set Firebase Project ID (replace with YOUR values)
docker mcp secret set VITE_FIREBASE_PROJECT_ID=your-project-id
```

**Note**: Use `KEY=VALUE` format (no quotes, no spaces around `=`)

Verify secrets were created:

```powershell
docker mcp secret ls
```

You should see three secrets listed:

- VITE_FIREBASE_API_KEY
- VITE_FIREBASE_AUTH_DOMAIN
- VITE_FIREBASE_PROJECT_ID

---

## Step 5: Automated Setup (Recommended)

Copy and paste this entire PowerShell script to set up everything automatically:

```powershell
# Pull the latest Docker image
Write-Host "`n=== Pulling Docker Image ===" -ForegroundColor Cyan
docker pull iswnischay/mem8-mcp-server:latest

# Create catalogs directory
Write-Host "`n=== Creating Directories ===" -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.docker\mcp\catalogs" | Out-Null
Write-Host "✓ Created catalogs directory" -ForegroundColor Green

# Create custom.yaml catalog
Write-Host "`n=== Creating Catalog File ===" -ForegroundColor Cyan
$catalogContent = @"
version: 2
name: custom
displayName: Custom MCP Servers
catalogs:
  - name: mem8
    image: iswnischay/mem8-mcp-server:latest
    secrets:
      - VITE_FIREBASE_API_KEY
      - VITE_FIREBASE_AUTH_DOMAIN
      - VITE_FIREBASE_PROJECT_ID
    volumes:
      - mem8-session-data:/tmp
"@
$catalogContent | Out-File -FilePath "$env:USERPROFILE\.docker\mcp\catalogs\custom.yaml" -Encoding UTF8 -Force
Write-Host "✓ Created custom.yaml" -ForegroundColor Green

# Create registry.yaml
Write-Host "`n=== Creating Registry File ===" -ForegroundColor Cyan
$registryContent = @"
version: 2
mcpServers:
  mem8:
    command: docker
    args:
      - run
      - -i
      - --rm
      - -v
      - mem8-session-data:/tmp
      - iswnischay/mem8-mcp-server:latest
"@
$registryContent | Out-File -FilePath "$env:USERPROFILE\.docker\mcp\registry.yaml" -Encoding UTF8 -Force
Write-Host "✓ Created registry.yaml" -ForegroundColor Green

# Create Claude Desktop config
Write-Host "`n=== Creating Claude Desktop Config ===" -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path "$env:APPDATA\Claude" | Out-Null
$json = @"
{
  "mcpServers": {
    "mcp-toolkit-gateway": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-v",
        "/var/run/docker.sock:/var/run/docker.sock",
        "-v",
        "C:\\Users\\$env:USERNAME\\.docker\\mcp:/mcp",
        "docker/mcp-gateway",
        "--catalog=/mcp/catalogs/docker-mcp.yaml",
        "--catalog=/mcp/catalogs/custom.yaml",
        "--config=/mcp/config.yaml",
        "--registry=/mcp/registry.yaml",
        "--tools-config=/mcp/tools.yaml",
        "--transport=stdio"
      ]
    }
  }
}
"@
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText("$env:APPDATA\Claude\claude_desktop_config.json", $json, $utf8NoBom)
Write-Host "✓ Created claude_desktop_config.json" -ForegroundColor Green

# Verify files
Write-Host "`n=== Verification ===" -ForegroundColor Cyan
Write-Host "Catalog file:" -ForegroundColor Yellow
Get-Content "$env:USERPROFILE\.docker\mcp\catalogs\custom.yaml"
Write-Host "`nRegistry file:" -ForegroundColor Yellow
Get-Content "$env:USERPROFILE\.docker\mcp\registry.yaml"
Write-Host "`nClaude config:" -ForegroundColor Yellow
Get-Content "$env:APPDATA\Claude\claude_desktop_config.json"

Write-Host "`n=== Setup Complete! ===" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Restart Claude Desktop completely" -ForegroundColor White
Write-Host "2. Ask Claude: 'What MCP tools do you have available?'" -ForegroundColor White
Write-Host "3. You should see 6 mem8 tools listed" -ForegroundColor White
```

**This script will**:

- Pull the Docker image from Docker Hub
- Create all necessary directories
- Generate custom.yaml with correct configuration
- Generate registry.yaml with correct configuration
- Generate claude_desktop_config.json with correct configuration
- Show you all the files for verification

---

## Step 6: Manual Setup (Alternative)

If you prefer to create files manually, use these commands:

### Create Catalog File

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.docker\mcp\catalogs"
notepad "$env:USERPROFILE\.docker\mcp\catalogs\custom.yaml"
```

Paste this content:

```yaml
version: 2
name: custom
displayName: Custom MCP Servers
catalogs:
  - name: mem8
    image: iswnischay/mem8-mcp-server:latest
    secrets:
      - VITE_FIREBASE_API_KEY
      - VITE_FIREBASE_AUTH_DOMAIN
      - VITE_FIREBASE_PROJECT_ID
    volumes:
      - mem8-session-data:/tmp
```

### Create Registry File

```powershell
notepad "$env:USERPROFILE\.docker\mcp\registry.yaml"
```

Paste this content:

```yaml
version: 2
mcpServers:
  mem8:
    command: docker
    args:
      - run
      - -i
      - --rm
      - -v
      - mem8-session-data:/tmp
      - iswnischay/mem8-mcp-server:latest
```

### Create Claude Desktop Config

```powershell
New-Item -ItemType Directory -Force -Path "$env:APPDATA\Claude"
notepad "$env:APPDATA\Claude\claude_desktop_config.json"
```

Paste this content (replace `USERNAME` with your Windows username):

```json
{
  "mcpServers": {
    "mcp-toolkit-gateway": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-v",
        "/var/run/docker.sock:/var/run/docker.sock",
        "-v",
        "C:\\Users\\USERNAME\\.docker\\mcp:/mcp",
        "docker/mcp-gateway",
        "--catalog=/mcp/catalogs/docker-mcp.yaml",
        "--catalog=/mcp/catalogs/custom.yaml",
        "--config=/mcp/config.yaml",
        "--registry=/mcp/registry.yaml",
        "--tools-config=/mcp/tools.yaml",
        "--transport=stdio"
      ]
    }
  }
}
```

Save all files.

---

## Step 7: Restart Claude Desktop

1. **Completely quit** Claude Desktop:
   - Right-click system tray icon → Quit
   - Or close all Claude Desktop windows
2. **Wait 5 seconds**
3. **Start Claude Desktop** again

---

## Step 8: Verify Installation

In Claude Desktop, ask:

```
What MCP tools do you have available?
```

You should see 6 mem8 tools:

- `mem8_authenticate` - Login to mem8
- `mem8_list_secrets` - List all your secrets
- `mem8_get_secret` - Get a specific secret
- `mem8_add_secret` - Add a new secret
- `mem8_delete_secret` - Delete a secret
- `mem8_logout` - Logout from mem8

---

## Troubleshooting

### Issue: Tools not appearing in Claude

**Solution**:

1. Verify Docker image exists: `docker images | findstr mem8`
2. Check catalog file syntax (YAML is indentation-sensitive)
3. Ensure Claude config has custom.yaml in catalogs list
4. Completely restart Claude Desktop (don't just refresh)

### Issue: "Secret not found" errors

**Solution**:

1. List secrets: `docker mcp secret list`
2. Re-create missing secrets with the commands from Step 3
3. Verify secret names match exactly (case-sensitive)

### Issue: Authentication fails

**Solution**:

1. Verify Firebase credentials are correct
2. Test login via web app: https://iswnischay.github.io/mem08/
3. Check that user account exists in Firebase
4. Ensure Firestore database is set up with proper rules

### Issue: "Cannot connect to Firebase"

**Solution**:

1. Check internet connection
2. Verify Firebase project is active
3. Check Docker container logs: `docker ps` then `docker logs <container_id>`

---

## Testing Checklist

After installation, test these scenarios:

- [ ] List available tools
- [ ] Authenticate with valid credentials
- [ ] List secrets (should work after auth)
- [ ] Add a new secret
- [ ] Retrieve the secret you just added
- [ ] Delete the test secret
- [ ] Logout
- [ ] Try listing secrets again (should fail - not authenticated)

---

## Next Steps

Once installed and tested:

1. **Create secrets in mem8 web app** if you haven't already
2. **Use Claude to manage secrets** via natural language
3. **Explore integration possibilities** with other MCP servers
4. **Set up backup authentication** if needed

---

## Security Reminders

- ✅ Never share your Firebase credentials
- ✅ Always logout when done
- ✅ Don't expose secret values in logs or screenshots
- ✅ Use strong passwords for mem8 accounts
- ✅ Regularly review and rotate secrets

---

## Need Help?

Check the following files:

- `readme.txt` - General documentation
- `CLAUDE.md` - Implementation details
- Docker logs: `docker ps` then `docker logs <container_id>`
- Claude Desktop logs (in application settings)

---

**Installation complete!** 🎉

You can now use Claude Desktop to securely manage your secrets through the mem8 application.
