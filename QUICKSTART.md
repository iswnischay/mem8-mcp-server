# mem8 MCP Server - Quick Start

## ⚡ One-Command Setup (Easiest!)

Copy and paste this entire script into PowerShell:

```powershell
# One-command automated setup
Write-Host "`n=== mem8 MCP Server Setup ===" -ForegroundColor Cyan

# Pull Docker image
Write-Host "`nPulling Docker image..." -ForegroundColor Yellow
docker pull iswnischay/mem8-mcp-server:latest

# Create directories
Write-Host "Creating directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.docker\mcp\catalogs" | Out-Null
New-Item -ItemType Directory -Force -Path "$env:APPDATA\Claude" | Out-Null

# Create catalog
Write-Host "Creating catalog..." -ForegroundColor Yellow
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

# Create registry
Write-Host "Creating registry..." -ForegroundColor Yellow
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

# Create Claude config
Write-Host "Creating Claude Desktop config..." -ForegroundColor Yellow
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

Write-Host "`n✓ Setup complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Set Firebase secrets (see below)" -ForegroundColor White
Write-Host "2. Restart Claude Desktop completely" -ForegroundColor White
Write-Host "3. Ask Claude: 'What MCP tools do you have available?'" -ForegroundColor White
```

---

## 🔑 Set Firebase Secrets

**IMPORTANT**: Replace with YOUR Firebase credentials from [console.firebase.google.com](https://console.firebase.google.com)

```powershell
# Use KEY=VALUE format (no quotes, no spaces around =)
docker mcp secret set VITE_FIREBASE_API_KEY=your_api_key_here
docker mcp secret set VITE_FIREBASE_AUTH_DOMAIN=your-project-id.firebaseapp.com
docker mcp secret set VITE_FIREBASE_PROJECT_ID=your-project-id
```

Verify:

```powershell
docker mcp secret ls
```

**Don't have Firebase?** See [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) Step 3 to create a FREE Firebase project.

---

## � Manual Commands (Alternative)

If you prefer step-by-step:

```powershell
# 1. Pull image
docker pull iswnischay/mem8-mcp-server:latest

# 2. Create catalog directory
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.docker\mcp\catalogs"

# 3. Create catalog file
notepad "$env:USERPROFILE\.docker\mcp\catalogs\custom.yaml"
# Copy content from INSTALLATION_GUIDE.md Step 6

# 4. Create registry file
notepad "$env:USERPROFILE\.docker\mcp\registry.yaml"
# Copy content from INSTALLATION_GUIDE.md Step 6

# 5. Create Claude config
notepad "$env:APPDATA\Claude\claude_desktop_config.json"
# Copy content from INSTALLATION_GUIDE.md Step 6
```

---

## 🔧 Files Information

1. **mem8_server.py** - Main MCP server code (6 tools)
2. **Dockerfile** - Container configuration
3. **requirements.txt** - Python dependencies
4. **INSTALLATION_GUIDE.md** - Complete step-by-step setup
5. **README.md** - Overview and usage guide
6. **CLAUDE.md** - Technical implementation details
7. **N8N_GUIDE.md** - n8n integration guide

---

## 🎯 Available Tools

| Tool                 | Purpose                   |
| -------------------- | ------------------------- |
| `mem8_authenticate`  | Login with email/password |
| `mem8_list_secrets`  | List all secret keys      |
| `mem8_get_secret`    | Get specific secret value |
| `mem8_add_secret`    | Add/update a secret       |
| `mem8_delete_secret` | Delete a secret           |
| `mem8_logout`        | Clear credentials         |

---

## 📋 Installation Checklist

- [ ] Run the one-command setup script above
- [ ] Set 3 Firebase secrets with YOUR credentials
- [ ] Verify secrets: `docker mcp secret ls`
- [ ] Restart Claude Desktop completely
- [ ] Test: Ask Claude "What MCP tools do you have available?"
- [ ] You should see 6 mem8 tools listed

---

## 🚀 Usage in Claude

Try these prompts:

```
Authenticate to mem8 with email user@example.com and password mypass123
```

```
List all my secrets in mem8
```

```
Get the API_KEY secret from mem8
```

```
Add a secret called DB_PASSWORD with value secretpass456
```

```
Delete the OLD_TOKEN secret
```

```
Logout from mem8
```

---

## ⚠️ Important Notes

1. **Always authenticate first** - Other tools won't work without auth
2. **Secrets are session-based** - Cleared on logout or server restart
3. **Use real Firebase credentials** - From your mem8 project
4. **Claude config is JSON** - No comments allowed in the file
5. **YAML is indentation-sensitive** - Use spaces, not tabs

---

## 🐛 Quick Troubleshooting

**Tools not showing up?**
→ Restart Claude Desktop completely

**Authentication fails?**
→ Check Firebase secrets: `docker mcp secret list`

**Can't build image?**
→ Make sure Docker Desktop is running

**Registry errors?**
→ Check YAML indentation in custom.yaml

---

## 📚 Full Documentation

- **INSTALLATION_GUIDE.md** - Complete setup instructions
- **readme.txt** - Full feature documentation
- **CLAUDE.md** - Technical implementation details

---

## 🎉 You're Ready!

1. Follow INSTALLATION_GUIDE.md step-by-step
2. Test each tool in Claude Desktop
3. Start managing your secrets with AI!

**The mem8 MCP Server brings secure secret management to your AI assistant!** 🔐
