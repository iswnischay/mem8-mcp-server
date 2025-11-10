# mem8 Discord Bot Setup Guide

Complete guide to set up a Discord bot that lets you manage mem8 secrets via Discord chat.

---

## 🎯 **What You'll Get**

A Discord bot that responds to commands like:

- `!mem8 auth email@example.com password` - Login to mem8
- `!mem8 list` - List all your secrets
- `!mem8 get API_KEY` - Get a specific secret
- `!mem8 add DB_PASSWORD secret123` - Add a new secret
- `!mem8 delete OLD_KEY` - Delete a secret
- `!mem8 logout` - Logout

---

## 📋 **Prerequisites**

- ✅ mem8 MCP server already set up (you have this!)
- ✅ Docker Desktop running
- ✅ Node.js installed (v16 or higher)
- ✅ Discord account

---

## 🚀 **Quick Setup (5 minutes)**

### **Step 1: Create Discord Bot**

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"**
3. Name it: "mem8 Bot"
4. Go to **"Bot"** tab
5. Click **"Add Bot"** → Confirm
6. Click **"Reset Token"** → Copy the token (save it!)
7. Enable these **Privileged Gateway Intents**:

   - ✅ Message Content Intent
   - ✅ Server Members Intent (optional)
   - ✅ Presence Intent (optional)

8. Go to **"OAuth2"** → **"URL Generator"**
   - Scopes: ✅ `bot`
   - Bot Permissions:
     - ✅ Send Messages
     - ✅ Read Messages/View Channels
     - ✅ Read Message History
9. Copy the generated URL
10. Paste in browser and invite bot to your Discord server

---

### **Step 2: Install Dependencies**

```powershell
cd E:\mem8\mem8-mcp-server\discord-bot
npm install
```

---

### **Step 3: Configure Environment**

Create `.env` file:

```powershell
Copy-Item .env.example .env
notepad .env
```

Update with your Discord bot token:

```env
DISCORD_BOT_TOKEN=YOUR_DISCORD_BOT_TOKEN_HERE

VITE_FIREBASE_API_KEY=AIzaSyC5ieG4PgXYXTn0BvUFVK_NixcCXElnXjE
VITE_FIREBASE_AUTH_DOMAIN=mem-08.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=mem-08
```

---

### **Step 4: Run the Bot**

```powershell
cd E:\mem8\mem8-mcp-server\discord-bot
npm start
```

You should see:

```
✅ mem8 Discord Bot is online as mem8 Bot#1234
📋 Use !mem8 <command> to interact
```

---

## 💬 **Using the Bot in Discord**

### **Commands**

| Command                         | Description          | Example                               |
| ------------------------------- | -------------------- | ------------------------------------- |
| `!mem8 auth <email> <password>` | Login to mem8        | `!mem8 auth user@example.com pass123` |
| `!mem8 list`                    | List all secret keys | `!mem8 list`                          |
| `!mem8 get <key>`               | Get secret value     | `!mem8 get API_KEY`                   |
| `!mem8 add <key> <value>`       | Add/update secret    | `!mem8 add DB_URL postgres://...`     |
| `!mem8 delete <key>`            | Delete secret        | `!mem8 delete OLD_TOKEN`              |
| `!mem8 logout`                  | Logout               | `!mem8 logout`                        |
| `!mem8 help`                    | Show help            | `!mem8 help`                          |

### **Example Conversation**

```
You: !mem8 auth iswnischay@gmail.com 123456789
Bot: ✅ Successfully authenticated as iswnischay@gmail.com

You: !mem8 list
Bot: 🔒 Secrets List:
     • API_KEY
     • DATABASE_URL
     • AWS_SECRET

You: !mem8 get API_KEY
Bot: 🔐 Secret Retrieved:
     Key: API_KEY
     Value: sk_abc123xyz...
     ⚠️ Handle this information securely!

You: !mem8 add GITHUB_TOKEN ghp_newtoken123
Bot: ✅ Secret 'GITHUB_TOKEN' added successfully

You: !mem8 logout
Bot: ✅ Successfully logged out
```

---

## 🔐 **Security Best Practices**

### **1. Private Channels Only**

Set up a private Discord channel for secrets:

1. Create a new channel (e.g., `#mem8-secrets`)
2. Make it private (only you can see it)
3. Use the bot only in this channel

### **2. Delete Sensitive Messages**

After viewing a secret, delete the Discord message:

- Right-click message → Delete

### **3. Bot Permissions**

Keep bot permissions minimal:

- Only give access to specific channels
- Don't make it admin

### **4. Environment Variables**

Never commit `.env` file to git!

---

## 🐳 **Alternative: Run Bot in Docker**

Create `Dockerfile` in `discord-bot/` folder:

```dockerfile
FROM node:18-slim

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY mem8-bot.js ./

CMD ["node", "mem8-bot.js"]
```

Build and run:

```powershell
cd E:\mem8\mem8-mcp-server\discord-bot
docker build -t mem8-discord-bot .

docker run -d --name mem8-bot `
  -v mem8-session-data:/tmp `
  -v /var/run/docker.sock:/var/run/docker.sock `
  -e DISCORD_BOT_TOKEN="your_token" `
  -e VITE_FIREBASE_API_KEY="AIzaSyC5ieG4PgXYXTn0BvUFVK_NixcCXElnXjE" `
  -e VITE_FIREBASE_AUTH_DOMAIN="mem-08.firebaseapp.com" `
  -e VITE_FIREBASE_PROJECT_ID="mem-08" `
  mem8-discord-bot
```

---

## 🛠️ **n8n Integration (Advanced)**

If you want to use n8n instead:

### **1. Start n8n**

```powershell
docker run -d --name n8n `
  -p 5678:5678 `
  -v n8n_data:/home/node/.n8n `
  -v mem8-session-data:/tmp `
  -v /var/run/docker.sock:/var/run/docker.sock `
  n8nio/n8n
```

### **2. Import Workflow**

1. Open n8n at `http://localhost:5678`
2. Click **"+ Add workflow"**
3. Click **"⋮"** → **"Import from File"**
4. Select `n8n-discord-workflow.json`

### **3. Configure Discord Webhook**

1. In Discord server settings → Integrations → Webhooks
2. Create new webhook
3. Copy webhook URL
4. In n8n, paste URL in Discord nodes

### **4. Set Environment Variables**

In n8n settings, add:

- `VITE_FIREBASE_API_KEY`
- `VITE_FIREBASE_AUTH_DOMAIN`
- `VITE_FIREBASE_PROJECT_ID`

---

## 🐛 **Troubleshooting**

### **Bot doesn't respond**

- Check bot has permissions in the channel
- Verify "Message Content Intent" is enabled
- Check bot is online (green dot)

### **Authentication fails**

- Verify Firebase credentials in `.env`
- Check Docker volume exists: `docker volume ls | findstr mem8`
- Ensure mem8 MCP server image is built

### **"Permission denied" errors**

- Give bot "Send Messages" permission
- Check channel-specific permissions

---

## 📱 **Mobile Access**

With the Discord bot:

- ✅ Manage secrets from Discord mobile app
- ✅ Access from anywhere
- ✅ Quick secret retrieval on-the-go

---

## 🎉 **You're Done!**

You now have a Discord bot that can:

- ✅ Manage secrets via chat commands
- ✅ Work with your existing mem8 infrastructure
- ✅ Access from desktop or mobile
- ✅ Secure session management

**Start the bot and try it out!**

```powershell
cd E:\mem8\mem8-mcp-server\discord-bot
npm start
```

Then in Discord:

```
!mem8 help
```

---

## 🚀 **Next Steps**

- [ ] Set up private Discord channel for secrets
- [ ] Add more team members with controlled access
- [ ] Set up automated secret rotation
- [ ] Create custom commands for your workflow
- [ ] Integrate with CI/CD pipelines

Enjoy your Discord-powered secrets manager! 🔐🤖
