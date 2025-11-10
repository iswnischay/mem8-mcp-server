# ✅ TESTED SETUP - Copy & Paste Ready

This file contains the **TESTED and WORKING** automated setup commands. All commands have been verified on Windows PowerShell.

---

## 🚀 Complete Automated Setup (Copy This!)

**Simply copy and paste this entire block into PowerShell:**

```powershell
# ===================================================================
# mem8 MCP Server - Automated Setup Script
# Tested on: Windows 11, PowerShell 5.1, Docker Desktop 4.x
# ===================================================================

Write-Host "`n=== mem8 MCP Server Setup ===" -ForegroundColor Cyan

# Pull Docker image from Docker Hub
Write-Host "`n[1/4] Pulling Docker image..." -ForegroundColor Yellow
docker pull iswnischay/mem8-mcp-server:latest

# Create necessary directories
Write-Host "`n[2/4] Creating directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.docker\mcp\catalogs" | Out-Null
New-Item -ItemType Directory -Force -Path "$env:APPDATA\Claude" | Out-Null
Write-Host "  ✓ Directories created" -ForegroundColor Green

# Create custom catalog file
Write-Host "`n[3/4] Creating catalog..." -ForegroundColor Yellow
@"
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
"@ | Out-File -FilePath "$env:USERPROFILE\.docker\mcp\catalogs\custom.yaml" -Encoding UTF8 -Force
Write-Host "  ✓ Catalog created: $env:USERPROFILE\.docker\mcp\catalogs\custom.yaml" -ForegroundColor Green

# Create registry file
@"
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
"@ | Out-File -FilePath "$env:USERPROFILE\.docker\mcp\registry.yaml" -Encoding UTF8 -Force
Write-Host "  ✓ Registry created: $env:USERPROFILE\.docker\mcp\registry.yaml" -ForegroundColor Green

# Create Claude Desktop config
Write-Host "`n[4/4] Creating Claude Desktop config..." -ForegroundColor Yellow
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
Write-Host "  ✓ Claude config created: $env:APPDATA\Claude\claude_desktop_config.json" -ForegroundColor Green

# Verify everything
Write-Host "`n=== Verification ===" -ForegroundColor Cyan
Write-Host "Checking files..." -ForegroundColor Yellow
if (Test-Path "$env:USERPROFILE\.docker\mcp\catalogs\custom.yaml") {
    Write-Host "  ✓ custom.yaml exists" -ForegroundColor Green
} else {
    Write-Host "  ✗ custom.yaml missing!" -ForegroundColor Red
}
if (Test-Path "$env:USERPROFILE\.docker\mcp\registry.yaml") {
    Write-Host "  ✓ registry.yaml exists" -ForegroundColor Green
} else {
    Write-Host "  ✗ registry.yaml missing!" -ForegroundColor Red
}
if (Test-Path "$env:APPDATA\Claude\claude_desktop_config.json") {
    Write-Host "  ✓ claude_desktop_config.json exists" -ForegroundColor Green
} else {
    Write-Host "  ✗ claude_desktop_config.json missing!" -ForegroundColor Red
}

Write-Host "`nChecking secrets..." -ForegroundColor Yellow
docker mcp secret ls

Write-Host "`n=== ✅ Setup Complete! ===" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Set Firebase secrets (see below)" -ForegroundColor White
Write-Host "2. Restart Claude Desktop completely" -ForegroundColor White
Write-Host "3. Ask Claude: 'What MCP tools do you have available?'" -ForegroundColor White
Write-Host "4. You should see 6 mem8 tools listed!" -ForegroundColor White
```

---

## 🔑 Step 2: Set Your Firebase Secrets

**IMPORTANT**: Replace the placeholder values with YOUR actual Firebase credentials!

Get your Firebase credentials from: https://console.firebase.google.com/

```powershell
# Use KEY=VALUE format (no quotes needed, no spaces around =)
docker mcp secret set VITE_FIREBASE_API_KEY=your_actual_api_key_here
docker mcp secret set VITE_FIREBASE_AUTH_DOMAIN=your-project-id.firebaseapp.com
docker mcp secret set VITE_FIREBASE_PROJECT_ID=your-project-id
```

**Example** (with fake values):

```powershell
docker mcp secret set VITE_FIREBASE_API_KEY=AIzaSyC5ieG4PgXYXTn0BvUFVK_NixcCXElnXjE
docker mcp secret set VITE_FIREBASE_AUTH_DOMAIN=my-secrets-app.firebaseapp.com
docker mcp secret set VITE_FIREBASE_PROJECT_ID=my-secrets-app
```

Verify secrets were created:

```powershell
docker mcp secret ls
```

You should see 3 secrets listed:

- VITE_FIREBASE_API_KEY
- VITE_FIREBASE_AUTH_DOMAIN
- VITE_FIREBASE_PROJECT_ID

---

## 🆕 Don't Have Firebase Credentials?

See [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) **Step 3** for complete instructions on creating a FREE Firebase project.

**Quick summary**:

1. Go to https://console.firebase.google.com/
2. Create new project
3. Enable Email/Password authentication
4. Enable Firestore database
5. Copy your API key, auth domain, and project ID
6. Create a user account in Firebase Authentication

---

## 🔄 Step 3: Restart Claude Desktop

**Important**: Must restart Claude Desktop COMPLETELY for changes to take effect.

1. Close Claude Desktop (check system tray)
2. Wait 5 seconds
3. Open Claude Desktop again

---

## ✅ Step 4: Test the Installation

In Claude Desktop, type:

```
What MCP tools do you have available?
```

**Expected Result**: You should see 6 mem8 tools:

- `mem8_authenticate` - Login to mem8
- `mem8_list_secrets` - List all your secrets
- `mem8_get_secret` - Get a specific secret value
- `mem8_add_secret` - Add or update a secret
- `mem8_delete_secret` - Delete a secret
- `mem8_logout` - Clear authentication

---

## 🎯 Quick Test Flow

Once tools are available, test with these prompts:

1. **Authenticate**:

   ```
   Authenticate to mem8 with email YOUR_EMAIL and password YOUR_PASSWORD
   ```

2. **List secrets**:

   ```
   List all my secrets in mem8
   ```

3. **Add a test secret**:

   ```
   Add a secret to mem8 called TEST_KEY with value test123
   ```

4. **Get the secret**:

   ```
   Get the TEST_KEY secret from mem8
   ```

5. **Delete the secret**:

   ```
   Delete the TEST_KEY secret from mem8
   ```

6. **Logout**:
   ```
   Logout from mem8
   ```

---

## 🐛 Troubleshooting

### Tools not showing up in Claude?

1. **Verify Docker is running**:

   ```powershell
   docker ps
   ```

2. **Check secrets are set**:

   ```powershell
   docker mcp secret ls
   ```

3. **Verify files exist**:

   ```powershell
   Test-Path "$env:USERPROFILE\.docker\mcp\catalogs\custom.yaml"
   Test-Path "$env:USERPROFILE\.docker\mcp\registry.yaml"
   Test-Path "$env:APPDATA\Claude\claude_desktop_config.json"
   ```

4. **Check file contents**:

   ```powershell
   Get-Content "$env:USERPROFILE\.docker\mcp\catalogs\custom.yaml"
   Get-Content "$env:APPDATA\Claude\claude_desktop_config.json"
   ```

5. **Restart Claude Desktop** (completely close and reopen)

### Authentication fails?

1. Verify you created a user account in Firebase Authentication
2. Test login on the web app: https://iswnischay.github.io/mem08/
3. Check that Firebase secrets are set correctly
4. Ensure Firestore database is enabled in Firebase Console

### "Cannot find secret" errors?

The secrets might not be set correctly. Re-run:

```powershell
docker mcp secret set VITE_FIREBASE_API_KEY=your_key
docker mcp secret set VITE_FIREBASE_AUTH_DOMAIN=your_domain
docker mcp secret set VITE_FIREBASE_PROJECT_ID=your_project_id
```

---

## 📁 File Locations Reference

For your reference, these are the files created:

| File              | Path                                                                  |
| ----------------- | --------------------------------------------------------------------- |
| **Catalog**       | `C:\Users\USERNAME\.docker\mcp\catalogs\custom.yaml`                  |
| **Registry**      | `C:\Users\USERNAME\.docker\mcp\registry.yaml`                         |
| **Claude Config** | `C:\Users\USERNAME\AppData\Roaming\Claude\claude_desktop_config.json` |

Replace `USERNAME` with your Windows username (e.g., `Nischay`)

---

## 🎉 Success Checklist

- [x] Automated script ran without errors
- [x] All 3 files created successfully
- [x] Docker image pulled from Docker Hub
- [x] 3 Firebase secrets are set
- [ ] Claude Desktop restarted
- [ ] 6 mem8 tools visible in Claude Desktop
- [ ] Successfully authenticated to mem8
- [ ] Successfully tested listing/adding/getting/deleting secrets

---

## 📚 Additional Documentation

- **INSTALLATION_GUIDE.md** - Complete step-by-step guide with Firebase setup
- **QUICKSTART.md** - Quick reference commands
- **README.md** - Project overview and usage
- **N8N_GUIDE.md** - Integration with n8n automation
- **CLAUDE.md** - Technical implementation details

---

**All commands tested and verified working! 🚀**

Last tested: November 10, 2025
