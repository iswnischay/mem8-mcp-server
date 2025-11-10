# mem8 MCP Server - n8n Integration Guide

How to use the mem8 MCP server in n8n workflows.

---

## 🚀 Quick Setup

### Prerequisites

- n8n installed (cloud or self-hosted)
- Docker installed on the n8n server
- mem8 Docker image pulled: `docker pull iswnischay/mem8-mcp-server:latest`

---

## 📦 Method 1: Execute Command Node (Simplest)

### Step 1: Create Workflow

1. Add **Execute Command** node
2. Set command to call Docker with MCP server

### Step 2: Configure Command

**For authentication:**

```bash
echo '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"n8n","version":"1.0"}},"id":1}
{"jsonrpc":"2.0","method":"tools/call","params":{"name":"mem8_authenticate","arguments":{"email":"user@example.com","password":"password123"}},"id":2}' | docker run -i --rm -v mem8-session-data:/tmp -e VITE_FIREBASE_API_KEY=AIzaSyC5ieG4PgXYXTn0BvUFVK_NixcCXElnXjE -e VITE_FIREBASE_AUTH_DOMAIN=mem-08.firebaseapp.com -e VITE_FIREBASE_PROJECT_ID=mem-08 iswnischay/mem8-mcp-server:latest
```

**For listing secrets:**

```bash
echo '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"n8n","version":"1.0"}},"id":1}
{"jsonrpc":"2.0","method":"tools/call","params":{"name":"mem8_list_secrets","arguments":{}},"id":2}' | docker run -i --rm -v mem8-session-data:/tmp -e VITE_FIREBASE_API_KEY=AIzaSyC5ieG4PgXYXTn0BvUFVK_NixcCXElnXjE -e VITE_FIREBASE_AUTH_DOMAIN=mem-08.firebaseapp.com -e VITE_FIREBASE_PROJECT_ID=mem-08 iswnischay/mem8-mcp-server:latest
```

**For getting a secret:**

```bash
echo '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"n8n","version":"1.0"}},"id":1}
{"jsonrpc":"2.0","method":"tools/call","params":{"name":"mem8_get_secret","arguments":{"key":"MY_KEY"}},"id":2}' | docker run -i --rm -v mem8-session-data:/tmp -e VITE_FIREBASE_API_KEY=AIzaSyC5ieG4PgXYXTn0BvUFVK_NixcCXElnXjE -e VITE_FIREBASE_AUTH_DOMAIN=mem-08.firebaseapp.com -e VITE_FIREBASE_PROJECT_ID=mem-08 iswnischay/mem8-mcp-server:latest
```

### Step 3: Parse Output

Add **Code** node to parse JSON:

```javascript
// Parse the last line of output (contains the result)
const lines = $input.item.json.stdout.trim().split("\n");
for (let i = lines.length - 1; i >= 0; i--) {
  try {
    const result = JSON.parse(lines[i]);
    if (result.id === 2) {
      // Tool call response
      return { json: result };
    }
  } catch (e) {
    continue;
  }
}
return { json: { error: "No valid response" } };
```

---

## 🔐 Method 2: Using n8n Credentials (Recommended)

### Step 1: Create Credential

1. **Settings → Credentials → New Credential**
2. **Type:** Generic Credential (or HTTP Header Auth)
3. **Add these fields:**
   - `firebase_api_key`
   - `firebase_auth_domain`
   - `firebase_project_id`
   - `user_email` (optional - for auto-login)
   - `user_password` (optional - for auto-login)

### Step 2: Use in Execute Command

```bash
echo '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"n8n","version":"1.0"}},"id":1}
{"jsonrpc":"2.0","method":"tools/call","params":{"name":"mem8_list_secrets","arguments":{}},"id":2}' | docker run -i --rm -v mem8-session-data:/tmp -e VITE_FIREBASE_API_KEY={{$credentials.mem8.firebase_api_key}} -e VITE_FIREBASE_AUTH_DOMAIN={{$credentials.mem8.firebase_auth_domain}} -e VITE_FIREBASE_PROJECT_ID={{$credentials.mem8.firebase_project_id}} iswnischay/mem8-mcp-server:latest
```

---

## 🤖 Example Workflows

### Workflow 1: Discord Bot → Check Secrets

```
[Discord Webhook]
      ↓
[Extract command] (!secrets list)
      ↓
[Execute Command] (call mem8_list_secrets)
      ↓
[Parse JSON]
      ↓
[Send Discord Reply]
```

### Workflow 2: Scheduled Secret Backup

```
[Schedule Trigger] (daily)
      ↓
[Execute Command] (mem8_list_secrets)
      ↓
[Parse JSON]
      ↓
[Save to Google Sheets]
```

### Workflow 3: API Endpoint to Get Secrets

```
[Webhook] (POST /get-secret)
      ↓
[Set Variables] (key from body)
      ↓
[Execute Command] (mem8_get_secret)
      ↓
[Parse JSON]
      ↓
[Return Response]
```

---

## 📝 All Available Tools

### 1. Authenticate

```bash
{"name":"mem8_authenticate","arguments":{"email":"user@example.com","password":"pass123"}}
```

### 2. List Secrets

```bash
{"name":"mem8_list_secrets","arguments":{}}
```

### 3. Get Secret

```bash
{"name":"mem8_get_secret","arguments":{"key":"MY_KEY"}}
```

### 4. Add Secret

```bash
{"name":"mem8_add_secret","arguments":{"key":"MY_KEY","value":"my_value"}}
```

### 5. Delete Secret

```bash
{"name":"mem8_delete_secret","arguments":{"key":"MY_KEY"}}
```

### 6. Logout

```bash
{"name":"mem8_logout","arguments":{}}
```

---

## 🎯 Complete n8n Workflow Template

Import `n8n-simple-workflow.json` for a ready-to-use example.

**To import:**

1. Copy the JSON from `n8n-simple-workflow.json`
2. In n8n: Workflows → Import from File/URL
3. Paste the JSON
4. Update credentials

---

## 🔒 Security in n8n

**Best practices:**

1. Store Firebase credentials in n8n Credentials (encrypted)
2. Use environment variables for sensitive data
3. Restrict webhook access with authentication
4. Enable n8n basic auth for production

**Set environment variables in n8n:**

```bash
# In n8n server
export VITE_FIREBASE_API_KEY="AIzaSyC5ieG4PgXYXTn0BvUFVK_NixcCXElnXjE"
export VITE_FIREBASE_AUTH_DOMAIN="mem-08.firebaseapp.com"
export VITE_FIREBASE_PROJECT_ID="mem-08"
```

Then in Execute Command:

```bash
docker run -i --rm -v mem8-session-data:/tmp -e VITE_FIREBASE_API_KEY=$VITE_FIREBASE_API_KEY -e VITE_FIREBASE_AUTH_DOMAIN=$VITE_FIREBASE_AUTH_DOMAIN -e VITE_FIREBASE_PROJECT_ID=$VITE_FIREBASE_PROJECT_ID iswnischay/mem8-mcp-server:latest
```

---

## 🧪 Testing

### Test 1: List Secrets

1. Add Execute Command node
2. Run the list_secrets command above
3. Check output - should see JSON response

### Test 2: Full Flow

```
[Manual Trigger]
      ↓
[Authenticate]
      ↓
[Add Secret]
      ↓
[List Secrets]
      ↓
[Get Secret]
      ↓
[Delete Secret]
```

---

## 🐛 Troubleshooting

### Issue: "Not authenticated"

**Solution:** Run `mem8_authenticate` first. Session persists via Docker volume.

### Issue: "Command not found: docker"

**Solution:** Install Docker on n8n server or use n8n with Docker enabled.

### Issue: Timeout errors

**Solution:** Increase command timeout in Execute Command node settings.

### Issue: JSON parsing fails

**Solution:** Check that you're parsing the LAST line with `id: 2` in the output.

---

## 💡 Pro Tips

1. **Session Persistence:** The Docker volume `mem8-session-data:/tmp` keeps you logged in between calls
2. **Parallel Execution:** You can run multiple MCP calls in parallel (each gets its own container)
3. **Error Handling:** Always add error handling nodes to catch failed Docker commands
4. **Logging:** Enable Execute Command logging to debug issues

---

## 📚 Related Docs

- **Discord Bot Integration:** [discord-bot/README.md](discord-bot/README.md)
- **Claude Desktop Setup:** [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
- **MCP Protocol:** [CLAUDE.md](CLAUDE.md)

---

**Ready to integrate? Import the example workflow and start building!** 🚀
