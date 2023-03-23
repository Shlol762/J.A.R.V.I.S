import datetime
import tkinter
import tkinter.messagebox
import customtkinter as ctk
import asyncio
from typing import List
from discord import Message
from discord.ext.commands import Context


ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class Hotline(ctk.CTk):
    task_idk = 0
    prev_task: asyncio.Task = None

    def __init__(self, ctx: Context, messages: List[Message], loop: asyncio.ProactorEventLoop):
        super().__init__()

        self.ctx = ctx
        self.loop = loop

        print(type(self.loop), type(loop))

        # configure window
        self.title("J.A.R.V.I.S Hotline")
        self.geometry(f"{630}x{380}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        extra_bold_font = ctk.CTkFont(family="gg sans", size=16, weight="bold")
        light_bold_font = ctk.CTkFont(family="gg sans", size=16, weight="normal")

        # create main entry and button
        self.entry = ctk.CTkEntry(self, placeholder_text="Enter quick reply", font = light_bold_font)
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.entry.bind('<Return>', self.on_enter)

        username = ctx.author.name
        channelname = ctx.channel.name if ctx.guild else None

        self.label = ctk.CTkLabel(self, text = f"Origin:   #{channelname or 'DM'}   |   Caller:   @{username}",
                                  fg_color = "#3d4270", text_color = "#c9cdfb", font = extra_bold_font, corner_radius = 5,
                                  height = 10)
        self.label.grid(row = 0, column = 1, padx = (50, 50), pady = (20, 0), sticky = "nsew")


        # create textbox
        self.textbox = ctk.CTkTextbox(self, width=250, wrap = tkinter.WORD)
        self.textbox.grid(row=1, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.textbox.insert("0.0",
                            '\n'.join([message.content for message in messages]) + '\n')
        self.textbox.configure(state = 'disabled', font = light_bold_font)

        self.protocol('WM_DELETE_WINDOW', self.end_hotline)
        self.bind('<Visibility>', self.comm_established)

    def send(self, *args, **kwargs):
        self.prev_task = self.loop.create_task(self._send_(*args, **kwargs), name=f'hotline-task-{self.task_idk}')

        while not self.prev_task.done():
            ...
        self.task_idk += 1

    async def _send_(self, *args, **kwargs):
        async with self.ctx.typing():
            await self.ctx.send(*args, **kwargs)

    def comm_established(self, *args):
        self.send('```js\n>>> Connection Established\n```')
        self.unbind('<Visibility>')

    def on_enter(self, event):
        text = self.entry.get()
        self.entry.delete(0, tkinter.END)

        self.textbox.configure(state = 'normal')
        self.textbox.insert(tkinter.END, f'\n\nYou:\n{text}')
        self.textbox.configure(state = 'disabled')

        self.send("`Shlok's Desktop`: " + text)

    def end_hotline(self):
        self.send("```nim\n>>> Hotline Terminated: \"connection closed by reciever\"\n```")
        self.destroy()
