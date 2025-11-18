import { Client, GatewayIntentBits, EmbedBuilder, ActionRowBuilder, ButtonBuilder, ButtonStyle } from 'discord.js';
import { exec } from 'child_process';
import { promisify } from 'util';
import dotenv from 'dotenv';

dotenv.config();
const execAsync = promisify(exec);

const CRCON_PATH = process.env.CRCON_PATH?.trim() || '/root/hll_rcon_tool';
const CHANNEL_ID = process.env.DISCORD_CHANNEL_ID;
const TOKEN = process.env.DISCORD_TOKEN;

if (!TOKEN) {
  console.error('DISCORD_TOKEN is missing in .env');
  process.exit(1);
}

if (!CHANNEL_ID) {
  console.error('DISCORD_CHANNEL_ID is missing in .env');
  process.exit(1);
}

const client = new Client({
  intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages],
});

async function restartRcon() {
  let output = '';

  try {
    output += 'Stopping containers...\n';
    const down = await execAsync('docker compose down', { cwd: CRCON_PATH });
    output += down.stdout || '';
    if (down.stderr) output += down.stderr;

    output += '\nStarting containers...\n';
    const up = await execAsync('docker compose up -d --remove-orphans', { cwd: CRCON_PATH });
    output += up.stdout || '';
    if (up.stderr) output += up.stderr;
  } catch (err) {
    output += `\nFailed: ${err.message}\n`;
    if (err.stdout) output += err.stdout;
    if (err.stderr) output += err.stderr;
  }

  return output || 'No output captured.';
}

client.once('ready', async () => {
  console.log(`Bot online as ${client.user.tag}`);

  const channel = await client.channels.fetch(CHANNEL_ID).catch(() => null);
  if (!channel?.isTextBased()) {
    console.error(`Channel ${CHANNEL_ID} not found or not text-based`);
    return;
  }

  await channel.messages.fetch({ limit: 100 })
    .then(msgs => msgs.size > 0 && channel.bulkDelete(msgs, true))
    .catch(() => {});

  const embed = new EmbedBuilder()
    .setTitle('RCON Control')
    .setDescription('Restart the HLL RCON container')
    .setColor(0x00ff00);

  const row = new ActionRowBuilder().addComponents(
    new ButtonBuilder()
      .setCustomId('restart_rcon')
      .setLabel('Restart RCON')
      .setStyle(ButtonStyle.Primary)
  );

  await channel.send({ embeds: [embed], components: [row] });
  console.log('Control message posted');
});

client.on('interactionCreate', async (interaction) => {
  if (!interaction.isButton() || interaction.customId !== 'restart_rcon') return;

  if (interaction.replied || interaction.deferred) return;

  await interaction.deferReply({ ephemeral: true });

  const logs = await restartRcon();

  await interaction.editReply({
    content: 'RCON restart completed.\n```' + logs.slice(0, 1990) + '```',
  });
});

client.login(TOKEN).catch(err => {
  console.error('Login failed:', err.message);
  process.exit(1);
});
