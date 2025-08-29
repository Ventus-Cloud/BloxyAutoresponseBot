# Discord Auto-Response Bot

## Overview

This is a Discord bot designed to automatically respond to trigger words and phrases in chat messages. The bot monitors messages in Discord servers and responds with predefined messages when specific trigger words are detected. It features a configurable JSON-based trigger system with multiple response options, different matching types, and basic bot management commands for monitoring status and performance.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Bot Framework
- **Discord.py Library**: Uses the discord.py library with the commands extension for Discord API integration
- **Command System**: Implements a prefix-based command system using '!' as the command prefix
- **Intents Configuration**: Configured with message_content, guilds, and default intents to access necessary Discord features

### Response System
- **Trigger-Based Responses**: Core functionality built around detecting trigger words/phrases in messages
- **Configuration-Driven**: All triggers, responses, and matching rules stored in a JSON configuration file
- **Multiple Response Options**: Each trigger can have multiple possible responses, randomly selected
- **Flexible Matching**: Supports different match types (currently "contains" matching implemented)
- **Enable/Disable Controls**: Individual triggers can be enabled or disabled without removing them

### Configuration Management
- **JSON-Based Config**: Uses config.json for storing all trigger configurations
- **Hot Reloading**: Config can be reloaded without restarting the bot
- **Default Fallback**: Automatically creates default configuration if file is missing or corrupted
- **Error Handling**: Robust error handling for malformed JSON or missing files

### Bot Management
- **Status Monitoring**: Commands to check bot latency, guild count, user count, and trigger count
- **Health Checks**: Ping command for basic connectivity testing
- **Logging System**: Comprehensive logging to both file and console with different log levels

### Event Handling
- **Message Processing**: Monitors all messages for trigger detection
- **Ready Event**: Handles bot initialization and status setting
- **Activity Status**: Sets bot presence to indicate its purpose

## External Dependencies

### Core Dependencies
- **discord.py**: Primary library for Discord bot functionality and API communication
- **python-dotenv**: Environment variable management for secure token storage

### Python Standard Library
- **asyncio**: Asynchronous programming support for Discord's async nature
- **logging**: Comprehensive logging system for monitoring and debugging
- **json**: Configuration file parsing and management
- **re**: Regular expression support for advanced message matching
- **random**: Random response selection from multiple options
- **typing**: Type hints for better code documentation and IDE support
- **os**: Operating system interface for environment variables

### External Services
- **Discord API**: Primary external service for bot functionality
- **Environment Variables**: Secure storage of Discord bot token and other sensitive configuration