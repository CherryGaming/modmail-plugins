import discord
from discord.ext import commands


class NitroHub(commands.Cog):
    """Provides commands for Nitro Hub staff"""
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)

    @commands.group(invoke_without_command=True)
    async def partnerrole(self, ctx, *):
        """Checks the partner role"""
        role = (await self.db.find_one({'_id': 'config'}))['nitrohub']['partner']
        if role:
            await ctx.send(embed=discord.Embed(description="The partner role is <@&"+role+">", color=0x9b59b6))
        else:
            await ctx.send(embed=discord.Embed(description="There isn't a partner role set\nAdmins can set it with `partnerrole set [role]`", color=0x9b59b6))

    @partnerrole.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def partnerrole_set(self, ctx, role: discord.Role, *, message):
        """Sets the partner role"""
        await self.db.find_one_and_update(
            {'_id': 'config'},
            {'$set': {'nitrohub': {'partner': str(role.id)}}},
            upsert=True
        )
        await ctx.send(embed=discord.Embed(description="Added <@&"+self.partner_role+"> to "+ctx.thread.recipient, color=0x9b59b6))
    
    @commands.command()
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @checks.thread_only()
    async def addpartner(self, ctx, *):
        """Adds the partner role to the thread recipient"""
        role = (await self.db.find_one({'_id': 'config'}))['nitrohub']['partner']
        if role:
            async with ctx.typing():
                try:
                    await ctx.thread.recipient.add_roles("681051722692427816", reason="Role added by "+ctx.author.display_name+" ("+ctx.author.username+"#"+ctx.author.discriminator+") ["+ctx.author.id+"]") 
                    await ctx.send(embed=discord.Embed(description="Added <@&"+self.partner_role+"> to "+ctx.thread.recipient, color=0x9b59b6))
                except:
                    await ctx.send(embed=discord.Embed(description="Failed to add <@&"+self.partner_role+"> to "+ctx.thread.recipient, color=0xff0000))
        else:
            await ctx.send(embed=discord.Embed(description="Partner role not found", color=0xff0000))
    
    @commands.command()
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @checks.thread_only()
    async def removepartner(self, ctx, *):
        """Removes the partner role from the thread recipient"""
        role = (await self.db.find_one({'_id': 'config'}))['nitrohub']['partner']
        if role:
            async with ctx.typing():
                try:
                    await ctx.thread.recipient.add_roles("681051722692427816", reason="Role removed by "+ctx.author.display_name+" ("+ctx.author.username+"#"+ctx.author.discriminator+") ["+ctx.author.id+"]") 
                    await ctx.send(embed=discord.Embed(description="Removed <@&"+self.partner_role+"> from "+ctx.thread.recipient, color=0x9b59b6))
                except:
                    await ctx.send(embed=discord.Embed(description="Failed to remove <@&"+self.partner_role+"> from "+ctx.thread.recipient, color=0xff0000))
        else:
            await ctx.send(embed=discord.Embed(description="Partner role not found", color=0xff0000))

def setup(bot):
    bot.add_cog(NitroHub(bot))
