import discord
from discord.ext import commands
import asyncio
import logging
import os
from dotenv import load_dotenv
from response_handler import ResponseHandler
from bot_manager import BotManager

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
        # Ignore messages from the bot itself
        if message.author == self.user:
            return
            
        # Log the message (without content for privacy)
        logger.info(f'Message from {message.author} in {message.guild}/{message.channel}')
        
        try:
            # Check for trigger words and respond
            response = await self.response_handler.check_triggers(message.content.lower())
            if response:
                await message.channel.send(response)
                logger.info(f'Sent auto-response to trigger in {message.guild}/{message.channel}')
                
        except discord.HTTPException as e:
            logger.error(f'Failed to send message: {e}')
        except Exception as e:
            logger.error(f'Error processing message: {e}')
            
        # Process commands
        await self.process_commands(message)
        
    async def on_guild_join(self, guild):
        """Called when bot joins a guild"""
        logger.info(f'Joined guild: {guild.name} (ID: {guild.id})')
        
    async def on_guild_remove(self, guild):
        """Called when bot leaves a guild"""
        logger.info(f'Left guild: {guild.name} (ID: {guild.id})')
        
    async def on_error(self, event, *args, **kwargs):
        """Handle errors"""
        logger.error(f'Error in event {event}', exc_info=True)

async def main():
    """Main function to run the bot"""
    # Get Discord token from environment
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        logger.error('DISCORD_TOKEN not found in environment variables!')
        return
        
    # Create and run bot
    bot = AutoResponseBot()
    
    try:
        await bot.start(token)
    except discord.LoginFailure:
        logger.error('Invalid Discord token provided!')
    except discord.HTTPException as e:
        logger.error(f'HTTP error occurred: {e}')
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
