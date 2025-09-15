import discord
from discord.ext import commands
import asyncio
import logging
import os
from dotenv import load_dotenv
from response_handler import ResponseHandler
from bot_manager import BotManager
from keep_alive import keep_alive   # 👈 añadido para mantener el bot activo

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AutoResponseBot(commands.Bot):
    def __init__(self):
        # Set up bot intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True

        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )

        # Initialize response handler
        self.response_handler = ResponseHandler()
        self.bot_manager = BotManager(self)

    async def on_ready(self):
        """Called when the bot is ready"""
        logger.info(f'{self.user} has connected to Discord!')
        logger.info(f'Bot is in {len(self.guilds)} guilds')

        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="for trigger messages"
            )
        )

    async def on_message(self, message):
        """Handle incoming messages"""
        if message.author == self.user:
            return

        logger.info(f'Message from {message.author} in {message.guild}/{message.channel}')

        try:
            content = message.content.lower()

            # === CONFIGURA TUS CANALES AQUÍ ===
            GENERAL_CHANNELS = [1378441550111182999, 1378454645046775938, 1378454971812413520]
            BLOX_GENERAL = 1378462317888667820
            RAIDS_CHANNEL = 1378461461222785215
            TRADE_CHANNEL = 1378461201343971328
            SEA_EVENTS_CHANNEL = 1378461952434503790

            # Pedimos respuesta al handler
            response = await self.response_handler.check_triggers(content)

            # Caso 1: en los canales generales normales
            if message.channel.id in GENERAL_CHANNELS:
                if "crosstrade" in content or "brainrot" in content:
                    await message.channel.send("🚫 No está permitido el crosstrade <@&1375924625975939163>.")
                elif "fruta" in content or "bloxfruits" in content or "pvp" in content:
                    await message.channel.send(f"👋 Ese tema va en el canal: <#{BLOX_GENERAL}>")
                elif "raid" in content or "trial" in content or "v4" in content:
                    await message.channel.send(f"⚔️ Para organizar raids o trials usa <#{RAIDS_CHANNEL}>.")
                elif "trade" in content or "que me das" in content or "que das" in content:
                    await message.channel.send(f"💱 Para intercambios usa <#{TRADE_CHANNEL}>.")
                elif "marino" in content or "barco" in content or "levi" in content or "sb" in content or "bestias marinas" in content or "terror" in content or "terrorshark" in content or "sea beast" in content or "bestia marina" in content or "prehistorica" in content or "mirage" in content or "isla espejo" in content or "isla kit" in content or "kit island" in content or "kitsune island" in content or "kitsune shrine" in content or "kit shrine" in content or "prehistórica" in content:
                    await message.channel.send(f"🌊 Para eventos marinos usa <#{SEA_EVENTS_CHANNEL}>.")

            # Caso 2: canal general de blox
            elif message.channel.id == BLOX_GENERAL:
                if "cuentas" in content or "crosstrade" in content or "cuenta" in content:
                    await message.channel.send("🚫 No está permitido el intercambio o venta de cuentas <@&1411163528890679358>.")
                elif "raid" in content or "trial" in content or "v4" in content:
                    await message.channel.send(f"⚔️ Para organizar raids o trials usa <#{RAIDS_CHANNEL}>.")
                elif "trade" in content or "que me das" in content or "que das" in content:
                    await message.channel.send(f"💱 Para intercambios de objetos usa <#{TRADE_CHANNEL}>.")
                elif "marino" in content or "barco" in content or "levi" in content or "sb" in content or "bestias marinas" in content or "terror" in content or "terrorshark" in content or "sea beast" in content or "bestia marina" in content or "prehistorica" in content or "mirage" in content or "isla espejo" in content or "isla kit" in content or "kit island" in content or "kitsune island" in content or "kitsune shrine" in content or "kit shrine" in content or "prehistórica" in content:
                    await message.channel.send(f"🌊 Para eventos marinos usa <#{SEA_EVENTS_CHANNEL}>.")

            # Caso 3: en los canales específicos de blox
            elif message.channel.id == TRADE_CHANNEL:
                if "cuentas" in content or "crosstrade" in content or "cuenta" in content:
                    await message.channel.send("🚫 No está permitido el intercambio o venta de cuentas <@&1411163528890679358>.")
                elif "raid" in content or "trial" in content or "v4" in content:
                    await message.channel.send(f"⚔️ Para organizar raids o trials usa <#{RAIDS_CHANNEL}>.")
                elif "marino" in content:
                    await message.channel.send(f"🌊 Para eventos marinos usa <#{SEA_EVENTS_CHANNEL}>.")
             
            elif message.channel.id == RAIDS_CHANNEL:
                if "cuentas" in content or "crosstrade" in content or "cuenta" in content:
                    await message.channel.send("🚫 No está permitido el intercambio o venta de cuentas <@&1411163528890679358>.")
                elif "trade" in content:
                    await message.channel.send(f"💱 Para intercambios de objetos usa <#{TRADE_CHANNEL}>.")
                elif "marino" in content:
                    await message.channel.send(f"🌊 Para eventos marinos usa <#{SEA_EVENTS_CHANNEL}>.")

            elif message.channel.id == SEA_EVENTS_CHANNEL:
                if "cuentas" in content or "crosstrade" in content or "cuenta" in content:
                    await message.channel.send("🚫 No está permitido el intercambio o venta de cuentas <@&1411163528890679358>.")
                elif "trade" in content:
                    await message.channel.send(f"💱 Para intercambios de objetos usa <#{TRADE_CHANNEL}>.")
                elif "raid" in content:
                    await message.channel.send(f"⚔️ Para organizar raids o trials usa <#{RAIDS_CHANNEL}>.")

            if response:
                await message.channel.send(response)

        except discord.HTTPException as e:
            logger.error(f'Failed to send message: {e}')
        except Exception as e:
            logger.error(f'Error processing message: {e}')

        await self.process_commands(message)

    async def on_guild_join(self, guild):
        logger.info(f'Joined guild: {guild.name} (ID: {guild.id})')

    async def on_guild_remove(self, guild):
        logger.info(f'Left guild: {guild.name} (ID: {guild.id})')

    async def on_error(self, event, *args, **kwargs):
        logger.error(f'Error in event {event}', exc_info=True)

async def main():
    """Main function to run the bot"""
    keep_alive()   # 👈 inicia el servidor Flask para que Replit no apague el bot

    token = os.getenv('DISCORD_TOKEN')
    if not token:
        logger.error('DISCORD_TOKEN not found in environment variables!')
        return

    bot = AutoResponseBot()

    try:
        await bot.start(token)
    except discord.LoginFailure:
        logger.error('Invalid Discord token provided!')
    except Exception as e:
        logger.error(f'Unexpected error: {e}')
    finally:
        if not bot.is_closed():
            await bot.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Bot shutdown requested by user')
    except Exception as e:
        logger.error(f'Failed to start bot: {e}')