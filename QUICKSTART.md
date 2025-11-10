# mem8 MCP Server - Quick Start

## ⚡ Quick Commands Reference

### Build the Server

```powershell
cd E:\mem8\mem8-mcp-server
docker build -t mem8-mcp-server .
```

### Set Firebase Secrets (Use YOUR credentials!)

```powershell
# Replace these with YOUR Firebase project credentials
docker mcp secret set VITE_FIREBASE_API_KEY="your_api_key_here"
docker mcp secret set VITE_FIREBASE_AUTH_DOMAIN="your-project.firebaseapp.com"
docker mcp secret set VITE_FIREBASE_PROJECT_ID="your-project-id"
```

**Don't have Firebase?** See [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) Step 3 to create your own Firebase project (free!).

### Verify Installation

```powershell
docker mcp server list
docker mcp secret list
```

---

## 🔧 Files Created

1. **Dockerfile** - Container configuration
2. **requirements.txt** - Python dependencies
3. **mem8_server.py** - Main MCP server code (6 tools)
4. **readme.txt** - Full documentation
5. **CLAUDE.md** - Implementation details
6. **INSTALLATION_GUIDE.md** - Step-by-step setup (READ THIS FIRST!)

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

- [ ] Docker Desktop running
- [ ] Build image: `docker build -t mem8-mcp-server .`
- [ ] Set 3 Firebase secrets (see above)
- [ ] Create `custom.yaml` in `~/.docker/mcp/catalogs/`
- [ ] Update `registry.yaml` with mem8 entry
- [ ] Add custom.yaml to Claude config
- [ ] Restart Claude Desktop
- [ ] Test authentication

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
