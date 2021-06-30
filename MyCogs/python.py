import discord
from MyCogs import command, Cog, Bot, datetime,\
    Colour, Embed, find_nth_occurrence, send_to_paste_service,\
    command_log_and_err, cooldown, Context
from discord.utils import escape_markdown
import datetime, re, itertools, aiohttp
from typing import Tuple, Any, Optional
from io import StringIO
import inspect, contextlib, textwrap, traceback, random


URL = "https://pypi.org/pypi/{package}/json"
PYPI_ICON = "https://cdn.discordapp.com/emojis/766274397257334814.png"

PYPI_COLOURS = itertools.cycle((0xffd241, 0x3775a8, 0xfffffe))

ILLEGAL_CHARACTERS = re.compile(r"[^-_.a-zA-Z0-9]+")
NEGATIVE_REPLIES = [
    "Noooooo!!",
    "Nope.",
    "I'm sorry Dave, I'm afraid I can't do that.",
    "I don't think so.",
    "Not gonna happen.",
    "Out of the question.",
    "Huh? No.",
    "Nah.",
    "Naw.",
    "Not likely.",
    "No way, José.",
    "Not in a million years.",
    "Fat chance.",
    "Certainly not.",
    "NEGATORY.",
    "Nuh-uh.",
    "Not in my house!",
]


class Python(Cog):
    def __init__(self, client: Bot):
        self.client = client
        self.name = 'Python'
        self.description = "Python related commands."
        self.env = {}
        self.ln = 0
        self.stdout = StringIO()

    def _format(self, inp: str, out: Any) -> Tuple[str, Optional[discord.Embed]]:
        """Format the eval output into a string & attempt to format it into an Embed."""
        self._ = out

        res = ""

        # Erase temp input we made
        if inp.startswith("_ = "):
            inp = inp[4:]

        # Get all non-empty lines
        lines = [line for line in inp.split("\n") if line.strip()]
        if len(lines) != 1:
            lines += [""]

        # Create the input dialog
        for i, line in enumerate(lines):
            if i == 0:
                # Start dialog
                start = f""

            else:
                # Indent the 3 dots correctly;
                # Normally, it's something like
                # In [X]:
                #    ...:
                #
                # But if it's
                # In [XX]:
                #    ...:
                #
                # You can see it doesn't look right.
                # This code simply indents the dots
                # far enough to align them.
                # we first `str()` the line number
                # then we get the length
                # and use `str.rjust()`
                # to indent it.
                start = ""

            if i == len(lines) - 2:
                if line.startswith("return"):
                    line = line[6:].strip()

            # Combine everything
            res += (start + line + "\n")

        self.stdout.seek(0)
        text = self.stdout.read()
        self.stdout.close()
        self.stdout = StringIO()

        if text:
            res += ("\n>>> " + text + "\n")

        if out is None:
            # No output, return the input statement
            return (res, None)


        if isinstance(out, discord.Embed):
            # We made an embed? Send that as embed
            res += "<Embed>"
            res = (res, out)

        else:
            if (isinstance(out, str) and out.startswith("Traceback (most recent call last):\n")):
                # Leave out the traceback message
                out = "\n" + "\n".join(out.split("\n")[:])

            if isinstance(out, str):
                pretty = out
            else:
                pretty = pprint.pformat(out, compact=True, width=60)

            if pretty != str(out):
                # We're using the pretty version, start on the next line
                res += "\n"

            if pretty.count("\n") > 20:
                # Text too long, shorten
                li = pretty.split("\n")

                pretty = ("\n".join(li[:3])  # First 3 lines
                          + "\n    \n"  # Ellipsis to indicate removed lines
                          + "\n".join(li[-3:]))  # last 3 lines

            # Add the output
            res += pretty
            res = (res, None)

        return res  # Return (text, embed)

    async def _eval(self, ctx: Context, code: str) -> Optional[discord.Message]:
        """Eval the input code string & send an embed to the invoking context."""
        self.ln += 1

        if code.startswith("exit"):
            self.ln = 0
            self.env = {}
            return await ctx.reply("```Reset history!```")

        env = {
            "message": ctx.message,
            "author": ctx.message.author,
            "channel": ctx.channel,
            "guild": ctx.guild,
            "ctx": ctx,
            "self": self,
            "bot": self.client,
            "inspect": inspect,
            "discord": discord,
            "contextlib": contextlib
        }

        self.env.update(env)

        # Ignore this code, it works
        code_ = """
async def func():  # (None,) -> Any
    try:
        with contextlib.redirect_stdout(self.stdout):
{0}
        if '_' in locals():
            if inspect.isawaitable(_):
                _ = await _
            return _
    finally:
        self.env.update(locals())
""".format(textwrap.indent(code, '            '))

        try:
            exec(code_, self.env)  # noqa: B102,S102
            func = self.env['func']
            res = await func()

        except Exception:
            res = traceback.format_exc()

        out, embed = self._format(code, res)
        out = out.rstrip("\n")  # Strip empty lines from output

        # Truncate output to max 15 lines or 1500 characters
        newline_truncate_index = find_nth_occurrence(out, "\n", 15)

        if newline_truncate_index is None or newline_truncate_index > 1500:
            truncate_index = 1500
        else:
            truncate_index = newline_truncate_index

        if len(out) > truncate_index:
            paste_link = await send_to_paste_service(out)
            if paste_link is not None:
                paste_text = f"full contents at {paste_link}"
            else:
                paste_text = "failed to upload contents to paste service."

            await ctx.reply(
                f"```py\n{out[:truncate_index]}\n```"
                f"... response truncated; {paste_text}",
                embed=embed
            )
            return

        await ctx.reply(embed=Embed(title="Python 3.9 Evaluation",
                                   description=f"```{'py' if 'Traceback' not in out else 'nim'}\n{out}```",
                                   colour=Colour.random() if 'Traceback' not in out else Colour.dark_red()))

    @command(name='Evaluate', aliases=['e', 'eval'],
                      brief='⌨P01', help='Runs python code',
                      usage='$evaluate|eval|e <code>')
    async def evaluate_(self, ctx: Context, *, code: str) -> None:
        """Run eval in a REPL-like format."""
        async with ctx.typing():
            caution_url = 'https://cdn.discordapp.com/emojis/849902617185484810.png?v=1'
            if 'C:/Users/Shlok' in code and ctx.author.id != 613044385910620190:
                await command_log_and_err(ctx, self.client, status="Security threat", send=False)
                await ctx.reply(embed=Embed(title="🛑 `SECURITY WARNING!` 🛑",
                description="Apologies for the warning signs, but you are not allowed to access files from"
                            " Shlok's computer.", colour=Colour.dark_red()).set_thumbnail(
                    url=caution_url).set_footer(text='SECRUITY HAZARD!',
                                                icon_url=caution_url))
            elif ('C:/Users/Shlok' in code and ctx.author.id == 613044385910620190) or 'C:/Users/Shlok' not in code:
                await command_log_and_err(ctx, self.client, status="Successfully Excecuted.")
                code = code.strip("`")
                if re.match('py(thon)?\n', code):
                    code = "\n".join(code.split("\n")[1:])

                if not re.search(  # Check if it's an expression
                        r"^(return|import|for|while|def|class|"
                        r"from|exit|[a-zA-Z0-9]+\s*=)", code, re.M) and len(
                    code.split("\n")) == 1:
                    code = "_ = " + code
                await self._eval(ctx, code)

    @command(name="PyPi", aliases=["package", "pack"],
             brief='P02')
    async def get_package_info(self, ctx: Context, package: str = None) -> None:
        """Provide information about a specific package from PyPI."""
        async with ctx.typing():
            if package:
                await command_log_and_err(ctx, self.client, status='Success')
                embed = Embed(title=random.choice(NEGATIVE_REPLIES), colour=0xcd6d6d)
                embed.set_thumbnail(url=PYPI_ICON)
                error = True
                if characters := re.search(ILLEGAL_CHARACTERS, package):
                    embed.description = f"Illegal character(s) passed into command: '{escape_markdown(characters.group(0))}'"
                else:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(URL.format(package=package)) as response:
                            if response.status == 404: embed.description = "Package could not be found."

                            elif response.status == 200 and response.content_type == "application/json":
                                response_json = await response.json()
                                info = response_json["info"]

                                embed.title = f"{info['name']} v{info['version']}"

                                embed.url = info["package_url"]
                                embed.colour = next(PYPI_COLOURS)

                                summary = escape_markdown(info["summary"])

                                # Summary could be completely empty, or just whitespace.
                                if summary and not summary.isspace(): embed.description = summary
                                else: embed.description = "No summary provided."

                                error = False

                            else: embed.description = "There was an error when fetching your PyPi package."
                        await session.close()

                if error: await ctx.reply(embed=embed)
                else: await ctx.reply(embed=embed)
            else: await command_log_and_err(ctx, self.client, err_code='P0248', text="You haven't given a package to search for...")


def setup(client: Bot):
    client.add_cog(Python(client))
