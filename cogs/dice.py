import discord
from discord.ext import commands, tasks
import random
import re

channellist = [508905628652142592, 339235017760833536, 508225092530995220, 339155308767215618]
rolllist = []


class diceCog(commands.Cog, name="dice"):
    def __init__(self, bot):
        self.bot = bot
        self.clear.start()
        self.dieRegex = re.compile(r"^(?P<numDie>\d)\s?d(?P<numSides>\d)$")

    def dice(self, sides):
        roll = random.randint(1,sides)
        return str(roll)



# the idea is you can choose the number of dice and what dice to roll
    @commands.command()
    async def roll(self, ctx, *arg):

        global rolllist
        print(rolllist)
        if ctx.author.id in rolllist:
            await ctx.message.add_reaction(emoji=':worst:579662420537114626')
            return

        else:
            if ctx.channel.id in channellist: 
                r = 0
                resultnum = 0
                output = []
                author = ctx.author.name
                titlestring = author + " just rolled the dice 🎲 \n"
                embed = discord.Embed(color=0x9062d3)
                embed.set_author(name="ullec bot")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                try:
                    if len(arg) <= 2:
                        result = self.dieRegex.search(" ".join(arg))
                        numDie = result.get("numDie")
                        numFaces = result.get("numFaces")
                        if numDie and numFaces:
                            if numFaces > 100:
                                raise Exception
                            if numDie > 14:
                                raise Exception

                            # normal way of doing it
                            # for x in range(numDie):
                            #    result = self.dice(x)

                            # map way of doing it
                            for result in map(self.dice, range(numDie)):
                                resultnum += int(result)
                                output.append("You rolled " + result + "/" + str(numFaces))

                    foutput = '\n'.join(output)
                    embed.insert_field_at(index=1, name=titlestring, value=foutput)
                    # print(str(resultnum) + " " + str(numDie) + " " + str(b))
                    totalstr = "Total: " + str(resultnum) + " Average: " + str(round(int(resultnum)/int(numDie),2)) + " Percentile: " + str(int(int(resultnum) * 100 / (int(rolls) * int(b))))
                    embed.insert_field_at(index=5, name=totalstr, value="\u200b", inline=False)
                    await ctx.send(embed=embed)
                    rolllist.append(ctx.author.id)
                    
                except Exception as e:
                    print('Exception: ' + str(e)) 
                    await ctx.message.add_reaction(emoji=':worst:579662420537114626')

    @tasks.loop(minutes=2)
    async def clear(self):
        global rolllist
        rolllist=[]
        print("cleared rollist")

def setup(bot):
    bot.add_cog(diceCog(bot))
    print('dice cog loaded')
