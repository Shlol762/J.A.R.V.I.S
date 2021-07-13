import json
from discord import Embed, Colour, TextChannel
from discord.ext.commands import command, Bot, Cog, Context
from MyCogs import command_log_and_err, set_timestamp


class School(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.name = "School"
        self.description = "Commands based on school stuff."

    @command(name="Textbook", aliases=['text', 'tb'],
             help="Gets an NCERT chapter or subject for the 9th grade",
             usage="textbook|text|tb (subject) (chapter)", brief="📋sc1")
    async def _textbook(self, ctx: Context, subject: str = None, *, chapter: str = None):
        def drivify_link(tag: str):
            return f"https://drive.google.com/drive/folders/{tag}?usp=sharing"

        with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/drive_links.json", "r") as f:
            subjects: dict[str: dict[str:str]] = json.load(f)
        await command_log_and_err(ctx, self.bot, status="Success")
        if subject:
            chapters: dict = subjects.get(subject.lower())
            if chapters:
                embed = await set_timestamp(Embed(title=f"`{subject.title()}`", description="",
                                                  colour=Colour.random(), url=drivify_link(chapters.get("link"))))
                try: chapter_link: str = drivify_link(chapters.get(chapter.lower()))
                except AttributeError: chapter_link = None
                if chapter_link:
                    embed.title, embed.url = None, None
                    embed.description = f"[**`{chapter.title()}`**]({chapter_link})"
                    return await ctx.reply(embed=embed)
                for chapter, link in chapters.items():
                    if chapter.lower() != 'link':
                        embed.description += f"**{f'• [`{chapter.title()}`]({drivify_link(link)})'}**\n"
                if len(embed.description) >= 2048:
                    lines = embed.description.split("\n")
                    emb, embed.timestamp, embed._footer = Embed(description="\n".join(lines[15:]),
                                timestamp=embed.timestamp, colour=embed.colour).set_footer(text=
                        embed._footer['text']
                    )\
                        , Embed.Empty, None
                    embed.description = "\n".join(lines[:15])
                    await ctx.reply(embed=embed)
                    await ctx.reply(embed=emb)
                    return
                else: return await ctx.reply(embed=embed)
        else:
            embed = Embed(title="NCERT Textbooks", description="", colour=Colour.random())
            for subject, chapters in subjects.items():
                embed.description += f"""**{f'• [`{subject.title()}`]({drivify_link(chapters["link"])})'}**\n"""
            return await ctx.reply(embed=embed)


    @command(name='Homework', aliases=['hw'], brief = '📋sc2',
             help="Set's homework with a default deadline as 2 days.",
             usage="$define|de <channel> <word> as <definition>")
    async def homework_(self, ctx: Context, channel: TextChannel = None, *, text: str = None):
        status = None
        err_code = None
        msg = None
        if channel:
            if text:
                components = text.split(" as ")
                word = components[0]
                definition = components[1].split('. - ')[0]
                time = components[1].split('. - ')[1]
                await channel.send(f"**{word}** - ***`{definition}`***\n**Time** - `{time}`")
                status: str = 'Successful'
            else: err_code, msg = '31348', 'Uh what do you want to define.'
        else: err_code, msg = '31348', 'Which channel do you wanna define in??'
        await command_log_and_err(ctx, status=status, err_code=err_code, text=msg)


def setup(bot: Bot):
    bot.add_cog(School(bot))
