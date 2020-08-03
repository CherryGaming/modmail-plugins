import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel

class NitroHub(commands.Cog):
    """Provides commands for Nitro Hub staff"""
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)

    @commands.group(invoke_without_command=True)
    async def partner_role(self, ctx):
        """Checks the partner role"""
        try:
            roles = ((await self.db.find_one({'_id': 'config'})) or {})['nitrohub']
            await ctx.send(embed=discord.Embed(description="The partner role is <@&"+roles['partner']+">", color=0x9b59b6))
        except KeyError:
            await ctx.send(embed=discord.Embed(description="There isn't a partner role set\nAdmins can set it with `partnerrole set [role]`", color=0x9b59b6))

    @partner_role.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def partner_role_set(self, ctx, *, role: discord.Role):
        """Sets the partner role"""
        await self.db.find_one_and_update(
            {'_id': 'config'},
            {'$set': {'nitrohub': {'partner': str(role.id)}}},
            upsert=True
        )
        await ctx.send(embed=discord.Embed(description="The partner role is now "+role, color=0x9b59b6))
    
    @commands.command(aliases=["apartner", "addpartner"])
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @checks.thread_only()
    async def add_partner(self, ctx):
        """Adds the partner role to the thread recipient"""
        try:
            roles = ((await self.db.find_one({'_id': 'config'})) or {})['nitrohub']
            async with ctx.typing():
                try:
                    await ctx.thread.recipient.add_roles(roles['partner'], reason="Role added by "+ctx.author.display_name+" ("+ctx.author.username+"#"+ctx.author.discriminator+") ["+ctx.author.id+"]") 
                    await ctx.send(embed=discord.Embed(description="Added <@&"+roles['partner']+"> to "+ctx.thread.recipient, color=0x9b59b6))
                except:
                    await ctx.send(embed=discord.Embed(description="Failed to add <@&"+roles['partner']+"> to "+ctx.thread.recipient, color=0xff0000))
        except KeyError:
            await ctx.send(embed=discord.Embed(description="Partner role not found", color=0xff0000))
    
    @commands.command(aliases=["rpartner", "removepartner"])
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @checks.thread_only()
    async def remove_partner(self, ctx):
        """Removes the partner role from the thread recipient"""
        try:
            roles = ((await self.db.find_one({'_id': 'config'})) or {})['nitrohub']
            async with ctx.typing():
                try:
                    await ctx.thread.recipient.add_roles(roles['partner'], reason="Role removed by "+ctx.author.display_name+" ("+ctx.author.username+"#"+ctx.author.discriminator+") ["+ctx.author.id+"]") 
                    await ctx.send(embed=discord.Embed(description="Removed <@&"+roles['partner']+"> from "+ctx.thread.recipient, color=0x9b59b6))
                except:
                    await ctx.send(embed=discord.Embed(description="Failed to remove <@&"+roles['partner']+"> from "+ctx.thread.recipient, color=0xff0000))
        except KeyError:
            await ctx.send(embed=discord.Embed(description="Partner role not found", color=0xff0000))

def setup(bot):
    bot.add_cog(NitroHub(bot))
