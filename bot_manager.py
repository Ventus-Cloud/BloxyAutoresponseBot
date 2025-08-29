import discord
from discord.ext import commands
import logging
import json
from typing import List

logger = logging.getLogger(__name__)

class BotManager:
    def __init__(self, bot):
        self.bot = bot
        self.setup_commands()
        
    def setup_commands(self):
        """Set up bot management commands"""
        
        @self.bot.command(name='ping')
        async def ping_command(ctx):
            """Check if bot is responsive"""
            latency = round(self.bot.latency * 1000)
            await ctx.send(f'Pong! Latency: {latency}ms')
            
        @self.bot.command(name='status')
        async def status_command(ctx):
            """Get bot status information"""
            embed = discord.Embed(
                title="Bot Status",
                color=discord.Color.green()
            )
            embed.add_field(
                name="Guilds",
                value=len(self.bot.guilds),
                inline=True
            )
            embed.add_field(
                name="Users",
                value=len(self.bot.users),
                inline=True
            )
            embed.add_field(
                name="Triggers",
                value=len(self.bot.response_handler.triggers),
                inline=True
            )
            embed.add_field(
                name="Latency",
                value=f"{round(self.bot.latency * 1000)}ms",
                inline=True
            )
            
            await ctx.send(embed=embed)
            
        @self.bot.command(name='triggers')
        async def list_triggers(ctx):
            """List all configured triggers"""
            triggers = self.bot.response_handler.triggers
            if not triggers:
                await ctx.send("No triggers configured.")
                return
                
            embed = discord.Embed(
                title="Configured Triggers",
                color=discord.Color.blue()
            )
            
            for trigger, config in list(triggers.items())[:10]:  # Limit to 10 for display
                status = "✅" if config.get('enabled', True) else "❌"
                match_type = config.get('match_type', 'contains')
                response_count = len(config.get('responses', []))
                
                embed.add_field(
                    name=f"{status} {trigger}",
                    value=f"Type: {match_type}\nResponses: {response_count}",
                    inline=True
                )
                
            if len(triggers) > 10:
                embed.set_footer(text=f"Showing 10 of {len(triggers)} triggers")
                
            await ctx.send(embed=embed)
            
        @self.bot.command(name='addtrigger')
        @commands.has_permissions(manage_messages=True)
        async def add_trigger(ctx, trigger: str, *, responses: str):
            """Add a new trigger (requires manage messages permission)"""
            try:
                # Parse responses (split by | for multiple responses)
                response_list = [r.strip() for r in responses.split('|') if r.strip()]
                
                if not response_list:
                    await ctx.send("❌ No valid responses provided.")
                    return
                    
                success = self.bot.response_handler.add_trigger(
                    trigger.lower(),
                    response_list
                )
                
                if success:
                    await ctx.send(f"✅ Added trigger: `{trigger}` with {len(response_list)} response(s)")
                else:
                    await ctx.send("❌ Failed to add trigger.")
                    
            except Exception as e:
                logger.error(f"Error adding trigger: {e}")
                await ctx.send("❌ Error adding trigger.")
                
        @self.bot.command(name='removetrigger')
        @commands.has_permissions(manage_messages=True)
        async def remove_trigger(ctx, trigger: str):
            """Remove a trigger (requires manage messages permission)"""
            try:
                success = self.bot.response_handler.remove_trigger(trigger.lower())
                
                if success:
                    await ctx.send(f"✅ Removed trigger: `{trigger}`")
                else:
                    await ctx.send(f"❌ Trigger `{trigger}` not found.")
                    
            except Exception as e:
                logger.error(f"Error removing trigger: {e}")
                await ctx.send("❌ Error removing trigger.")
                
        @self.bot.command(name='reload')
        @commands.has_permissions(administrator=True)
        async def reload_config(ctx):
            """Reload configuration from file (requires administrator permission)"""
            try:
                self.bot.response_handler.reload_config()
                trigger_count = len(self.bot.response_handler.triggers)
                await ctx.send(f"✅ Configuration reloaded. {trigger_count} triggers loaded.")
                
            except Exception as e:
                logger.error(f"Error reloading config: {e}")
                await ctx.send("❌ Error reloading configuration.")
                
        @self.bot.command(name='help')
        async def help_command(ctx):
            """Show bot help information"""
            embed = discord.Embed(
                title="Auto Response Bot Help",
                description="I automatically respond to trigger words and phrases!",
                color=discord.Color.purple()
            )
            
            embed.add_field(
                name="Basic Commands",
                value="`!ping` - Check bot responsiveness\n"
                      "`!status` - Show bot status\n"
                      "`!triggers` - List configured triggers\n"
                      "`!help` - Show this help message",
                inline=False
            )
            
            embed.add_field(
                name="Admin Commands",
                value="`!addtrigger <word> <response1|response2>` - Add trigger\n"
                      "`!removetrigger <word>` - Remove trigger\n"
                      "`!reload` - Reload configuration",
                inline=False
            )
            
            embed.add_field(
                name="How it works",
                value="I monitor all messages for trigger words and automatically respond with random messages from my configuration.",
                inline=False
            )
            
            embed.set_footer(text="Use | to separate multiple responses when adding triggers")
            
            await ctx.send(embed=embed)
            
        # Error handlers
        @add_trigger.error
        @remove_trigger.error
        @reload_config.error
        async def command_error(ctx, error):
            if isinstance(error, commands.MissingPermissions):
                await ctx.send("❌ You don't have permission to use this command.")
            else:
                logger.error(f"Command error: {error}")
                await ctx.send("❌ An error occurred while executing the command.")
