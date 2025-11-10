const { Client, GatewayIntentBits } = require('discord.js');
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

// Discord bot configuration
const DISCORD_TOKEN = process.env.DISCORD_BOT_TOKEN;
const COMMAND_PREFIX = '!mem8';

// Firebase credentials from environment
const FIREBASE_API_KEY = process.env.VITE_FIREBASE_API_KEY;
const FIREBASE_AUTH_DOMAIN = process.env.VITE_FIREBASE_AUTH_DOMAIN;
const FIREBASE_PROJECT_ID = process.env.VITE_FIREBASE_PROJECT_ID;

// Create Discord client
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
  ],
});

// Helper function to run mem8 commands via Docker
async function runMem8Command(command, args = []) {
  const baseCmd = `docker run --rm -v mem8-session-data:/tmp ` +
    `-e VITE_FIREBASE_API_KEY="${FIREBASE_API_KEY}" ` +
    `-e VITE_FIREBASE_AUTH_DOMAIN="${FIREBASE_AUTH_DOMAIN}" ` +
    `-e VITE_FIREBASE_PROJECT_ID="${FIREBASE_PROJECT_ID}" ` +
    `mem8-mcp-server:latest python -c `;

  let pythonCode;
  
  switch (command) {
    case 'auth':
      const [email, password] = args;
      pythonCode = `"import asyncio; import sys; sys.path.insert(0, '/app'); from mem8_server import mem8_authenticate; result = asyncio.run(mem8_authenticate(email='${email}', password='${password}')); print(result)"`;
      break;
    
    case 'list':
      pythonCode = `"import asyncio; import sys; sys.path.insert(0, '/app'); from mem8_server import mem8_list_secrets; result = asyncio.run(mem8_list_secrets()); print(result)"`;
      break;
    
    case 'get':
      const [key] = args;
      pythonCode = `"import asyncio; import sys; sys.path.insert(0, '/app'); from mem8_server import mem8_get_secret; result = asyncio.run(mem8_get_secret(key='${key}')); print(result)"`;
      break;
    
    case 'add':
      const [addKey, value] = args;
      pythonCode = `"import asyncio; import sys; sys.path.insert(0, '/app'); from mem8_server import mem8_add_secret; result = asyncio.run(mem8_add_secret(key='${addKey}', value='${value}')); print(result)"`;
      break;
    
    case 'delete':
      const [delKey] = args;
      pythonCode = `"import asyncio; import sys; sys.path.insert(0, '/app'); from mem8_server import mem8_delete_secret; result = asyncio.run(mem8_delete_secret(key='${delKey}')); print(result)"`;
      break;
    
    case 'logout':
      pythonCode = `"import asyncio; import sys; sys.path.insert(0, '/app'); from mem8_server import mem8_logout; result = asyncio.run(mem8_logout()); print(result)"`;
      break;
    
    default:
      return '❌ Unknown command';
  }

  try {
    const { stdout, stderr } = await execPromise(baseCmd + pythonCode);
    return stdout.trim() || stderr.trim();
  } catch (error) {
    console.error('Error executing command:', error);
    return `❌ Error: ${error.message}`;
  }
}

// Bot ready event
client.once('ready', () => {
  console.log(`✅ mem8 Discord Bot is online as ${client.user.tag}`);
  console.log(`📋 Use ${COMMAND_PREFIX} <command> to interact`);
});

// Message handler
client.on('messageCreate', async (message) => {
  // Ignore bot messages
  if (message.author.bot) return;

  // Check if message starts with command prefix
  if (!message.content.startsWith(COMMAND_PREFIX)) return;

  // Parse command
  const args = message.content.slice(COMMAND_PREFIX.length).trim().split(/\s+/);
  const command = args.shift().toLowerCase();

  // Send typing indicator
  await message.channel.sendTyping();

  try {
    let response;

    switch (command) {
      case 'auth':
      case 'login':
        if (args.length < 2) {
          response = '❌ Usage: !mem8 auth <email> <password>';
        } else {
          response = await runMem8Command('auth', args);
        }
        break;

      case 'list':
      case 'ls':
        response = await runMem8Command('list');
        break;

      case 'get':
        if (args.length < 1) {
          response = '❌ Usage: !mem8 get <secret-key>';
        } else {
          response = await runMem8Command('get', args);
        }
        break;

      case 'add':
      case 'set':
        if (args.length < 2) {
          response = '❌ Usage: !mem8 add <key> <value>';
        } else {
          const key = args[0];
          const value = args.slice(1).join(' ');
          response = await runMem8Command('add', [key, value]);
        }
        break;

      case 'delete':
      case 'del':
      case 'rm':
        if (args.length < 1) {
          response = '❌ Usage: !mem8 delete <secret-key>';
        } else {
          response = await runMem8Command('delete', args);
        }
        break;

      case 'logout':
        response = await runMem8Command('logout');
        break;

      case 'help':
        response = `
🔐 **mem8 Discord Bot Commands**

\`${COMMAND_PREFIX} auth <email> <password>\` - Authenticate with mem8
\`${COMMAND_PREFIX} list\` - List all secret keys
\`${COMMAND_PREFIX} get <key>\` - Get a specific secret value
\`${COMMAND_PREFIX} add <key> <value>\` - Add or update a secret
\`${COMMAND_PREFIX} delete <key>\` - Delete a secret
\`${COMMAND_PREFIX} logout\` - Logout from mem8
\`${COMMAND_PREFIX} help\` - Show this help message

**Example:**
\`${COMMAND_PREFIX} auth user@example.com mypassword\`
\`${COMMAND_PREFIX} list\`
\`${COMMAND_PREFIX} get API_KEY\`
        `.trim();
        break;

      default:
        response = `❌ Unknown command: ${command}\nUse \`${COMMAND_PREFIX} help\` for available commands`;
    }

    // Send response
    await message.reply(response);

  } catch (error) {
    console.error('Error handling command:', error);
    await message.reply(`❌ An error occurred: ${error.message}`);
  }
});

// Error handling
client.on('error', (error) => {
  console.error('Discord client error:', error);
});

process.on('unhandledRejection', (error) => {
  console.error('Unhandled promise rejection:', error);
});

// Login to Discord
if (!DISCORD_TOKEN) {
  console.error('❌ DISCORD_BOT_TOKEN environment variable is required!');
  process.exit(1);
}

client.login(DISCORD_TOKEN).catch((error) => {
  console.error('❌ Failed to login to Discord:', error);
  process.exit(1);
});
