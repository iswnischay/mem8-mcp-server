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

```powershell
# Set Firebase API Key (replace with YOUR values)
docker mcp secret set VITE_FIREBASE_API_KEY="your_api_key_here"

# Set Firebase Auth Domain (replace with YOUR values)
docker mcp secret set VITE_FIREBASE_AUTH_DOMAIN="your-project-id.firebaseapp.com"

# Set Firebase Project ID (replace with YOUR values)
docker mcp secret set VITE_FIREBASE_PROJECT_ID="your-project-id"
```

Verify secrets were created:

```powershell
docker mcp secret list
```

You should see:

- VITE_FIREBASE_API_KEY
- VITE_FIREBASE_AUTH_DOMAIN
- VITE_FIREBASE_PROJECT_ID

---

## Step 5: Create Custom Catalog

Create the catalogs directory if it doesn't exist:

```powershell
# For Windows
mkdir $env:USERPROFILE\.docker\mcp\catalogs -Force
```

Create or edit the custom catalog file:

```powershell
notepad $env:USERPROFILE\.docker\mcp\catalogs\custom.yaml
```

Add this content (replace existing if file exists):

```yaml
version: 2
name: custom
displayName: Custom MCP Servers
registry:
  mem8:
    description: "Secure secrets management through the mem8 application"
    title: "mem8 Secrets Manager"
    type: server
    dateAdded: "2025-11-10T00:00:00Z"
    image: mem8-mcp-server:latest
    ref: ""
    readme: ""
    toolsUrl: ""
    source: ""
    upstream: ""
    icon: ""
    tools:
      - name: mem8_authenticate
      - name: mem8_list_secrets
      - name: mem8_get_secret
      - name: mem8_add_secret
      - name: mem8_delete_secret
      - name: mem8_logout
    secrets:
      - name: VITE_FIREBASE_API_KEY
        env: VITE_FIREBASE_API_KEY
        example: AIzaSyC...
      - name: VITE_FIREBASE_AUTH_DOMAIN
        env: VITE_FIREBASE_AUTH_DOMAIN
        example: your-project.firebaseapp.com
      - name: VITE_FIREBASE_PROJECT_ID
        env: VITE_FIREBASE_PROJECT_ID
        example: your-project-id
    metadata:
      category: productivity
      tags:
        - secrets
        - security
        - firebase
        - password-manager
      license: MIT
      owner: local
```

Save and close the file.

---

## Step 5: Update Registry

Edit the registry file:

```powershell
notepad $env:USERPROFILE\.docker\mcp\registry.yaml
```

Add this entry under the existing `registry:` key (NOT at the root):

```yaml
registry:
  # ... existing servers ...
  mem8:
    ref: ""
```

**IMPORTANT**: Make sure it's indented under `registry:`, not at the root level.

Save and close.

---

## Step 6: Configure Claude Desktop

Find your Claude Desktop config file:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Open it:

```powershell
notepad $env:APPDATA\Claude\claude_desktop_config.json
```

Update the configuration to include the custom catalog. Your config should look like this:

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
        "C:\\Users\\YOUR_USERNAME\\.docker\\mcp:/mcp",
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

**CRITICAL**:

1. Replace `YOUR_USERNAME` with your actual Windows username
2. Use double backslashes (`\\`) in Windows paths
3. Ensure the `--catalog=/mcp/catalogs/custom.yaml` line is present
4. JSON does not support comments - remove any if you added them

Save and close.

---

## Step 7: Restart Claude Desktop

1. **Completely quit** Claude Desktop (right-click system tray icon → Quit)
2. **Wait 5 seconds**
3. **Start Claude Desktop** again

---

## Step 8: Verify Installation

### Check if server is listed:

```powershell
docker mcp server list
```

You should see `mem8` in the list.

### Test in Claude Desktop:

Try asking Claude:

```
Can you list the available mem8 tools?
```

Or:

```
Authenticate to mem8 with email test@example.com and password testpass123
```

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
