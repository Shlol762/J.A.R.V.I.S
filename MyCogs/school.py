import json
from discord import Embed, Colour
from discord.ext.commands import command, Bot, Cog, Context
from MyCogs import command_log_and_err, set_timestamp


class School(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.name = "School"
        self.description = "Commands based on school stuff."

    @command(name="Textbook", aliases=['text', 'tb'],
             help="Gets an NCERT chapter or subject for the 9th grade",
             usage="textbook|text|tb (subject) (chapter)", brief="sc3")
    async def _textbook(self, ctx: Context, subject: str = None, chapter: str = None):
        def drivify_link(tag: str):
            return f"https://drive.google.com/drive/folders/{tag}?usp=sharing"

        with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/drive_links.json", "r") as f:
            subjects: dict[str: dict[str:str]] = json.load(f)
        if subject:
            chapters: dict = subjects.get(subject.title())
            if chapters:
                embed = await set_timestamp(Embed(title=f"`{subject.title()}`", description="",
                                                  colour=Colour.random(), url=drivify_link(chapters.get("link"))))
                try: chapter_link: str = drivify_link(chapters.get(chapter.title()))
                except AttributeError: chapter_link = None
                if chapter_link:
                    embed.title, embed.url = None, None
                    embed.description = f"[**`{chapter.title()}`**]({chapter_link})"
                    return await ctx.send(embed=embed)
                for chapter, link in chapters.items():
                    if chapter.lower() != 'link':
                        embed.description += f"**{f'• [`{chapter.title()}`]({drivify_link(link)})'}**\n"
                print(len(embed.description))
                if len(embed.description) >= 2048:
                    lines = embed.description.split("\n")
                    emb, embed.timestamp, embed._footer = Embed(description="\n".join(lines[15:]),
                                timestamp=embed.timestamp, colour=embed.colour).set_footer(text=
                        embed._footer['text']
                    )\
                        , Embed.Empty, None
                    embed.description = "\n".join(lines[:15])
                    await ctx.send(embed=embed)
                    await ctx.send(embed=emb)
                    return
                else: return await ctx.send(embed=embed)
        else:
            embed = Embed(title="NCERT Textbooks", description="", colour=Colour.random())
            for subject, chapters in subjects.items():
                embed.description += f"""**{f'• [`{subject.title()}`]({drivify_link(chapters["link"])})'}**\n"""
            return await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(School(bot))
