import asyncio
from typing import Optional
import discord
from MyCogs import encrypt, decrypt, command_log_and_err,\
    commands, Cog, command, cooldown, BucketType, Context,\
    Member, guild_only, Client, Embed, Colour, Message,\
    choice, randint, Bot, comm_log_local
import json
#

class Games(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.description = 'Have fun while you at it.'
        self.name: str = 'Games(gs)'

    # 401
    @command(aliases=['rd', 'rolldice'], name='Roll Dice',
                      help='Rolls an imaginary dice.',
                      usage='rolldice|rd', extras={'emoji': '🎲', 'number': '401'})
    @cooldown(1, 0.5, BucketType.member)
    @comm_log_local
    async def rolldice(self, ctx: Context):
        author: Member = ctx.message.author
        dice_num: int = randint(1, 6)
        await command_log_and_err(ctx=ctx, status="Success")
        await ctx.reply(f'You rolled {dice_num}, {author.mention}')

    # 402
    @command(aliases=['8b', 'eightball', 'oracle'], name='8ball', extras={'emoji': '🎱', 'number': '402'},
                      help='Answers questions with 8ball ish results.',
                      usage='8ball|8b|eightball|oracle <question>')
    @cooldown(1, 1.5, BucketType.member)
    @comm_log_local
    async def eightball(self, ctx: Context, *, question: str = None):
        if question:
            eight_ball_response: str = choice(['As I see it, yes.', 'Ask again later',
                                                 'Better not tell you now', 'Cannot predict now',
                                                 'Concentrate and ask again.', "Don't count on it.",
                                                 'It is certain.', 'It is decidedly so.',
                                                 'Most likely.', 'My reply is no.',
                                                 'My sources say no.', 'Outlook not so good.',
                                                 'Outlook good.', 'Reply hazy, try again.',
                                                 'Signs point to yes.', 'Very doubtful',
                                                 'Without a doubt.', 'Yes',
                                                 'Yes - definitely.', 'You may rely on it.'])
            await command_log_and_err(ctx=ctx, status="Success")
            await ctx.reply(embed=Embed(title="8ball",
                                               description=f"`Seeker`: {ctx.author.mention}\n\n `Question`: {question}\n\n `Reply`: {eight_ball_response}",
                                               colour=Colour.random()))
        else:
            await command_log_and_err(ctx=ctx, err_code='Err_40248',
                                      text='Ask a question maybe??')

    # 403
    @command(aliases=['ynm'], name='YesNoMaybe',
                      help='Answers questions with Yes, No and Maybe.',
                      usage='yesnomaybe|ynm <question>', extras={'emoji': '🎱', 'number': '403'})
    @cooldown(1, 1.5, BucketType.member)
    @comm_log_local
    async def yesnomaybe(self, ctx: Context, *, question: str = None):
        if question:
            await ctx.reply(embed=Embed(title="YesNoMaybe",
                                               description=f"`Seeker`: {ctx.author.mention}\n\n `Question`: {question}\n\n `Reply`: {choice(['Yes', 'No', 'Maybe']) if ctx.author.id != 822302911114903584 else 'No'}",
                                               colour=Colour.random()))
            await command_log_and_err(ctx=ctx, status="Success")
        else:
            await command_log_and_err(ctx=ctx, err_code='Err_40348',
                                      text='Ask me a question dummy!')

    # 404
    @command(aliases=['hk'], name='Hack', extras={'emoji': '💻', 'number': '404'},
                      help='Hacks into a members account and steals all their information.(Not really)',
                      usage='hack|hk <member>')
    @cooldown(1, 1.5, BucketType.member)
    @guild_only()
    @comm_log_local
    async def hack(self, ctx: Context, member: Member = None):
        author: Member = ctx.message.author
        if member:
            await command_log_and_err(ctx=ctx, status="Success", used_on=member)
            if member == author:
                await ctx.reply("Ya can't hack yourself dummy!")
                await ctx.message.add_reaction('⁉')
            elif member == ctx.bot.user:
                await ctx.message.add_reaction('⁉')
                await ctx.reply("You would ask me to infect myself with a virus?")
            else:
                disc: str = f'`{member.discriminator}`'
                hack_msg: Message = await ctx.reply(f"Hacking {member.name}...")
                email_tag: str = choice(['gmail.com', 'yahoo.com', 'outlook.com', 'discord.gg', 'insta.com', 'xbox.com',
                             'apple.com'])
                hack_pass: str = choice(['discord.pass23', 'fghdAHj4952lldO', 'Pass108asimDisc', '12euRiuSH96', 'weirdo245dep',
                               'trumsuxYaBoi1984', 'daylight643nyc'])
                ip_hack: str = choice(['199.234.347.845', '193.001.832', '93.40.720', '442.658.920', '022.435.671',
                           '5103.3840.8832.9045', '692.730.4400'])
                await hack_msg.add_reaction('🇭')
                await hack_msg.edit(content="`[▘]` finding login...(2f authentication bypassed)")
                await hack_msg.add_reaction('🇦')
                await hack_msg.edit(content=
                                    f'''
`[▝]` Found `E-credentials`:
```
Email - {member.name}@{email_tag}
Password: {hack_pass}
```''')
                await hack_msg.add_reaction('🇨')
                await hack_msg.edit(content=f'`[▗]` Injecting `Trojan virus` into discriminator {disc}...')
                await hack_msg.add_reaction('🇰')
                await hack_msg.edit(content=
                                    f'''
`[▖]` Virus Injected into discriminator {disc}:
`‖████                   ‖`
            ''')
                await hack_msg.add_reaction('🇮')
                await hack_msg.edit(content=
                                    f'''
`[▖]` Virus Injected into discriminator {disc}:
`‖█████████              ‖`
''')
                await hack_msg.add_reaction('🇳')
                await hack_msg.edit(content=
                                    f'''
`[▖]` Virus Injected into discriminator {disc}:
`‖████████████████████   ‖`
''')
                await hack_msg.add_reaction('🇬')
                await hack_msg.edit(content=
                        f'''
`[▖]` Virus Injected into discriminator {disc}:
`‖███                    ‖`
''')
                await hack_msg.clear_reactions()
                await hack_msg.edit(content=
                        f'''
`[▖]` Virus Injected into discriminator {disc}:
`‖███████████████████████‖`
''')
                await hack_msg.add_reaction('🇭')
                await hack_msg.edit(content=
                        f'''
`[▖]` Virus Injected into discriminator {disc}:
`‖█                      ‖`
''')
                await hack_msg.add_reaction('🇦')
                await hack_msg.edit(content=
                                    f'''
`[▖]` Virus Injected into discriminator {disc}:
`‖███████████████████████‖`
''')
                await hack_msg.add_reaction('🇨')
                await hack_msg.edit(content=f"`[▘]` Getting `{member.name}`'s `IP address`...")
                await hack_msg.add_reaction('🇰')
                await hack_msg.edit(content=f"`[▝]` **IP ADDRESS**: `{ip_hack}`")
                await hack_msg.add_reaction('🇪')
                await hack_msg.add_reaction('🇩')
                await hack_msg.edit(content=f'Finished hacking `{member.name}`')
                await ctx.reply('*Totally* hacked that person...')
                await asyncio.sleep(2)
                await hack_msg.clear_reactions()
        else:
            await command_log_and_err(ctx=ctx, err_code='Err_40448',
                                      text='Hack who??')

    # 405
    @command(aliases=['fc'], name='Flipcoin',
                      help='Using this command you can either flip a coin by yourself or, challenge another player to flip a coin with you.',
                      usage='flipcoin|fc (member)', extras={'emoji': '💰', 'number': '405'})
    @cooldown(1, 1, BucketType.member)
    @comm_log_local
    async def flipcoin(self, ctx: Context, member: Optional[Member] = None):
        author: Member = ctx.message.author
        bot: Bot = ctx.bot
        h_t_r: str = choice(['heads', 'tails'])
        if member:
            if member != author:
                if member.id == bot.user.id:
                    await ctx.reply("Oooh you wish to challenge me eh? It's on like donkey kong! What do you choose?")
                    try:
                        msg: Message = await bot.wait_for(event="message", timeout=7, check=lambda
                            message: message.author == author and message.channel == ctx.message.channel)
                        if msg.content.lower() == 'heads':
                            await ctx.reply("I get tails then...")
                            if h_t_r == 'heads':
                                await command_log_and_err(ctx=ctx, status=f"I won ",
                                                          used_on=member if member else None)
                                await ctx.reply(
                                    f"Dang it! Fine. The coin flipped heads... You win this round {author.mention}...")
                            elif h_t_r == 'tails':
                                await command_log_and_err(ctx=ctx, status=f"I won ",
                                                          used_on=member if member else None)
                                await ctx.reply("Told ya I'd win ;), the coin flipped tails!")
                        elif msg.content.lower() == 'tails':
                            await ctx.reply("I get heads then...")
                            if h_t_r == 'tails':
                                await command_log_and_err(ctx=ctx,
                                                          status=f"I lost",
                                                          used_on=member if member else None)
                                await ctx.reply(
                                    f"Dang it! Fine. The coin flipped tails... You win this round {author.mention}...")
                            elif h_t_r == 'heads':
                                await command_log_and_err(ctx=ctx, status=f"I won ",
                                                          used_on=member if member else None)
                                await ctx.reply("Told ya I'd win ;), the coin flipped heads!")
                    except TimeoutError:
                        await command_log_and_err(ctx=ctx,
                                                  status=f"{author.mention} is a big sissy",
                                                  used_on=member if member else None)
                        await ctx.reply("WUSS! Come back and finish the game ya bum!")
                else:
                    await ctx.reply(
                        f"Alright {author.mention} and {member.mention} playing the flippin game. {author.mention} heads or tails?")
                    try:
                        msg: Message = await bot.wait_for(event='message', timeout=7, check=lambda
                            message: message.author == author and message.channel == ctx.message.channel)
                        if msg.content.lower() == 'heads':
                            await ctx.reply(
                                f"So you choose heads, that makes {member.mention}'s choice tails....")
                            if msg.content.lower() == h_t_r:
                                await command_log_and_err(ctx=ctx,
                                                          status=f"Idk who played against {author.mention} but Success",
                                                          used_on=member if member else None)
                                await ctx.reply(
                                    f"{author.mention} your luck seems to better... You win! Congrats! Tough break {member.mention}... better luck next time")
                            else:
                                await command_log_and_err(ctx=ctx,
                                                          status=f"Idk who played against {author.mention} but Success",
                                                          used_on=member if member else None)
                                await ctx.reply(
                                    f"{member.mention} your luck seems to better... You win! Congrats! Tough break {author.mention}... better luck next time")
                        elif msg.content.lower() == 'tails':
                            await ctx.reply(
                                f"So you choose tails, that makes {member.mention}'s choice heads....")
                            if msg.content.lower() == h_t_r:
                                await command_log_and_err(ctx=ctx,
                                                          status=f"Idk who played against {author.mention} but Success",
                                                          used_on=member if member else None)
                                await ctx.reply(
                                    f"{author.mention} your luck seems to better... You win! Congrats! Tough break {member.mention}... better luck next time")
                            else:
                                await command_log_and_err(ctx=ctx,
                                                          status=f"Idk who played against {author.mention} but Success",
                                                          used_on=member if member else None)
                                await ctx.reply(
                                    f"{member.mention} your luck seems to better... You win! Congrats! Tough break {author.mention}... better luck next time")
                        else:
                            await command_log_and_err(ctx=ctx,
                                                      status=f"Wrong argument",
                                                      used_on=member if member else None)
                            await ctx.reply("Heads or tails only dum dum...")
                    except TimeoutError:
                        await ctx.reply("Wuss, why'd you give up?")
            else:
                await command_log_and_err(ctx=ctx,
                                          status=f"Success",
                                          used_on=member if member else None)
                await ctx.reply(f"{author.mention} you got {h_t_r}")
        else:
            await command_log_and_err(ctx=ctx,
                                      status=f"Success",
                                      used_on=member if member else None)
            await ctx.reply(f"{author.mention} you got {h_t_r}")

    # 406
    @command(aliases=['ncrpt'], name='Encrypt', extras={'emoji': '💬', 'number': '406'},
                      help='This command currently uses two types of encoding languages to encrypt a sample of text',
                      usage='encrypt|ncrpt <code/morse> <text>')
    @cooldown(1, 1.5, BucketType.member)
    @comm_log_local
    async def encrypt(self, ctx: Context, code: str = None, *, text: str = None):
        if code:
            if text:
                await command_log_and_err(ctx=ctx, status="Success")
                await ctx.author.send(embed=Embed(title="Encrypting Text...",
                                                          description=f"`Encoding type`: {code}\n `Encryption requested by`: {ctx.author.mention}",
                                                          colour=Colour.random()).add_field(name="Encrypted:",
                                                                                                    value=f"`{encrypt(code, text)}`"))
            else:
                await command_log_and_err(ctx=ctx, err_code="Err_40648",
                                          text="Specify the text you want to encrypt")
        else:
            await command_log_and_err(ctx=ctx, err_code="Err_40648",
                                      text="Specify the code you want to encrypt your text in")

    # 407
    @command(aliases=['dcrpt'], name='Decrypt', extras={'emoji': '🗨', 'number': '407'},
                      help='This command decrypts messages in code and morse.',
                      usage='decrypt|dcrypt <code/morse> <encrypt text>')
    @cooldown(1, 1.5, BucketType.member)
    @comm_log_local
    async def decrypt(self, ctx: Context, code: str = None, *, text: str = None):
        if code:
            if text:
                await command_log_and_err(ctx=ctx, status="Success")
                await ctx.author.send(embed=Embed(title="Decrypting Code...",
                                                          description=f"`Encoding type`: {code}\n `Decryption requested by`: {ctx.author.mention}",
                                                          colour=Colour.random()).add_field(name="Decrypted:",
                                                                                                    value=f"`{decrypt(code, text)}`"))
            else:
                await command_log_and_err(ctx=ctx, err_code="Err_40748",
                                          text="Specify the code you want to decrypt")
        else:
            await command_log_and_err(ctx=ctx, err_code="Err_40748",
                                      text="Specify the coding type you want to decrypt your code in")

    #408
    @command(aliases=['imp'], name="Impersonate", extras={'emoji': '🎭', 'number': '408'},
             help="Of course it impersonates people.",
             usage="impersonate|imp (member) (text)")
    @cooldown(1, 10, BucketType.channel)
    @comm_log_local
    async def _impersonate(self, ctx: Context, member: Member = None, *, text: str = None):
        member: Member = member or ctx.author
        await command_log_and_err(ctx, "Success", used_on=member)
        if member.id == ctx.bot.user.id:
            await ctx.reply("Go away don't twist my opinions you idiot.")
        else:
            await ctx.message.delete()
            if ctx.bot.user not in [webhook.user for webhook in await ctx.channel.webhooks()]:
                webhook: discord.Webhook = await ctx.channel.create_webhook(name=ctx.bot.user.name, avatar=None)
                await webhook.send(text or f"I have no idea who to impersonate so I'll just impersonate you.",
                                   username=member.display_name,
                                   avatar_url=member.avatar.url)
                with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/webhooks.json", "r") as f:
                    webhooks: dict = json.load(f)
                    webhooks[str(ctx.channel.id)] = str(webhook.id)
                with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/webhooks.json", "w") as f:
                    json.dump(webhooks, f, indent=3)
            else:
                with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/webhooks.json", "r") as f:
                    webhooks: dict = json.load(f)
                webhook: discord.Webhook = await ctx.bot.fetch_webhook(int(webhooks.get(str(ctx.channel.id))))
                await webhook.send(text or f"I have no idea who to impersonate so I'll just impersonate you.",
                                   username=member.display_name,
                                   avatar_url=member.avatar.url)


def setup(bot: Bot):
    bot.add_cog(Games(bot))
