# mem8 MCP Server

Docker-based MCP server for secrets management, compatible with Claude Desktop and n8n.

---

## 🚀 Quick Start

### For Claude Desktop Users

1. **Pull Docker image:**

   ```bash
   docker pull iswnischay/mem8-mcp-server:latest
   ```

2. **Set up Docker secrets:**

   ```bash
   docker mcp secret set mem8 VITE_FIREBASE_API_KEY your_api_key
   docker mcp secret set mem8 VITE_FIREBASE_AUTH_DOMAIN your_domain
   docker mcp secret set mem8 VITE_FIREBASE_PROJECT_ID your_project_id
   ```

3. **Configure Claude Desktop** - See [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)

4. **Done!** Use mem8 tools in Claude Desktop 🎉

---

### For n8n Users

1. **Pull Docker image:**

   ```bash
   docker pull iswnischay/mem8-mcp-server:latest
   ```

2. **Import workflow:**

   - Import `n8n-simple-workflow.json` in n8n
   - Configure Firebase credentials
   - Start automating!

3. **Full guide:** See [N8N_GUIDE.md](N8N_GUIDE.md)

---

## � Firebase Setup

### Don't have Firebase credentials?

Create your own Firebase project (free!) in 5 minutes:

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create new project → Enable Authentication (Email/Password) → Enable Firestore
3. Get credentials from Project Settings
4. Full guide: [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) - Step 3

**Your Firebase API keys are safe to share!** Security comes from authentication and Firestore rules, not credential secrecy.

---

## �📁 What's Included

### Core Files

- **`mem8_server.py`** - MCP server implementation
- **`requirements.txt`** - Python dependencies
- **`Dockerfile`** - Container configuration

### Documentation

- **`INSTALLATION_GUIDE.md`** - Complete setup for Claude Desktop
- **`QUICKSTART.md`** - Quick reference guide
- **`CLAUDE.md`** - Technical details and protocol
- **`N8N_GUIDE.md`** - n8n integration guide

### Testing & Examples

- **`test-mcp.sh`** - Test script for validation
- **`n8n-simple-workflow.json`** - Example n8n workflow

---

## 🔐 Available Tools

1. **mem8_authenticate** - Login with email/password
2. **mem8_list_secrets** - List all your secrets
3. **mem8_get_secret** - Get a specific secret
4. **mem8_add_secret** - Add or update a secret
5. **mem8_delete_secret** - Delete a secret
6. **mem8_logout** - Logout and clear session

---

## 🧪 Testing

```bash
# Set environment variables
export VITE_FIREBASE_API_KEY="your_api_key"
export VITE_FIREBASE_AUTH_DOMAIN="your_domain"
export VITE_FIREBASE_PROJECT_ID="your_project_id"

# Run test script
./test-mcp.sh
```

---

## 📚 Documentation

- **[INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)** - Full setup guide for Claude Desktop
- **[QUICKSTART.md](QUICKSTART.md)** - Quick reference
- **[CLAUDE.md](CLAUDE.md)** - Technical details
- **[N8N_GUIDE.md](N8N_GUIDE.md)** - n8n integration

---

## 🐳 Building from Source

```bash
# Clone repository
git clone https://github.com/iswnischay/mem8-mcp-server.git
cd mem8-mcp-server

# Build Docker image
docker build -t mem8-mcp-server .

# Test it
./test-mcp.sh
```

---

## 🔒 Security

- Firebase credentials are stored securely via Docker secrets or environment variables
- Session data persists in Docker volume (encrypted on disk)
- Each user has isolated secrets (protected by Firebase Auth + Firestore rules)
- API keys are public by design (security via authentication)

---

## 🆘 Support

- **Issues:** https://github.com/iswnischay/mem8-mcp-server/issues
- **Main Project:** https://github.com/iswnischay/mem08

---

## 📝 License

MIT License - see main project for details

---

**✨ Ready to manage your secrets with AI!**
