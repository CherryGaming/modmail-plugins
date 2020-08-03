import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel

class FumplePartnershipRole(commands.Cog):
    """Provides commands for giving/taking away a partner role in a thread"""
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)

    @commands.group(aliases=["partnerrole"], invoke_without_command=True)
    async def partner_role(self, ctx):
        """Checks the partner role"""
        try:
            roles = ((await self.db.find_one({'_id': 'config'})) or {})['fumpleroles']
            await ctx.send(embed=discord.Embed(description="The partner role is <@&"+roles['partner']+">", color=0x9b59b6))
        except KeyError:
            await ctx.send(embed=discord.Embed(description="There isn't a partner role set\nAdmins can set it with `partner_role set [role]`", color=0x9b59b6))

    @partner_role.command(name="set")
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def partner_role_set(self, ctx, *, role: discord.Role):
        """Sets the partner role"""
        await self.db.find_one_and_update(
            {'_id': 'config'},
            {'$set': {'fumpleroles': {'partner': str(role.id)}}},
            upsert=True
        )
        await ctx.send(embed=discord.Embed(description="The partner role is now "+role.mention, color=0x9b59b6))
    
    @commands.command(aliases=["apartner", "addpartner"])
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @checks.thread_only()
    async def add_partner(self, ctx):
        """Adds the partner role to the thread recipient"""
        try:
            roles = ((await self.db.find_one({'_id': 'config'})) or {})['fumpleroles']
            try:
                await ctx.guild.get_member(ctx.thread.recipient.id).add_roles(ctx.guild.get_role(int(roles['partner'])), reason="Role added by "+ctx.author.display_name+" ("+ctx.author.name+"#"+ctx.author.discriminator+") ["+str(ctx.author.id)+"]")
                await ctx.send(embed=discord.Embed(description="Added <@&"+roles['partner']+"> to "+ctx.thread.recipient.mention, color=0x9b59b6))
            except discord.Forbidden:
                await ctx.send(embed=discord.Embed(description="Failed to add <@&"+roles['partner']+"> to "+ctx.thread.recipient.mention, color=0xff0000))
        except KeyError:
            await ctx.send(embed=discord.Embed(description="Partner role not found", color=0xff0000))
    
    @commands.command(aliases=["rpartner", "removepartner"])
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @checks.thread_only()
    async def remove_partner(self, ctx):
        """Removes the partner role from the thread recipient"""
        try:
            roles = ((await self.db.find_one({'_id': 'config'})) or {})['fumpleroles']
            try:
                await ctx.guild.get_member(ctx.thread.recipient.id).remove_roles(ctx.guild.get_role(int(roles['partner'])), reason="Role removed by "+ctx.author.display_name+" ("+ctx.author.name+"#"+ctx.author.discriminator+") ["+str(ctx.author.id)+"]") 
                await ctx.send(embed=discord.Embed(description="Removed <@&"+roles['partner']+"> from "+ctx.thread.recipient.mention, color=0x9b59b6))
            except discord.Forbidden:
                await ctx.send(embed=discord.Embed(description="Failed to remove <@&"+roles['partner']+"> from "+ctx.thread.recipient.mention, color=0xff0000))
        except KeyError:
            await ctx.send(embed=discord.Embed(description="Partner role not found", color=0xff0000))

def setup(bot):
    bot.add_cog(FumplePartnershipRole(bot))
