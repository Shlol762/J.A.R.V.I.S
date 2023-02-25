import random
import json
import asyncio
from discord.ext.commands import Context

code_own: dict[str: str] = {
    'a': '1', 'b': '`', 'c': '~', 'd': "'", 'e': ']', 'f': '/',
    'g': '[', 'h': 'A', 'i': '$', 'j': '&', 'k': '-', 'l': '_',
    'm': '9', 'n': '(', 'o': '=', 'p': '6', 'q': '.', 'r': ';',
    's': "\\", 't': ')', 'u': '#', 'v': '!', 'w': ',', 'x': '>',
    'y': '?', 'z': '<', " ": " ",
    # Special characters:
    '!': 'a', '@': 'c', '#': 'r', '$': 'g', '%': 'd', '^': 'j',
    '*': 'l', '(': 'q', '/': 'b', '`': 'i', '~': 'z', ')': 'f',
    '-': 'u', '_': 'e', '+': 'k', '=': '3', '[': '4', ']': '7',
    '&': '5', '\\': '2', ';': 'y', '.': 'z', '<': 'c', '>': '|',
    '?': '{', ':': '^', '"': '}', '{': '8', '}': '0', '|': '"',
    ',': '%',
    # Numbers
    '1': 't', '2': 'w', '3': 'h', '4': 'o', '5': 's', '6': 'v',
    '7': 'n', '8': 'm', '9': 'p', '0': 'x'
}

morse_code: dict[str: str] = {
    # Alphabets
    'a': '•–', 'b': '–•••', 'c': '-•-•', 'd': '-••', 'e': '•',
    'f': '••-•', 'g': '--•', 'h': '••••', 'i': '••', 'j': '•---',
    'k': '-•-', 'l': '•-••', 'm': '--', 'n': '-•', 'o': '---',
    'p': '•--•', 'q': '--•-', 'r': '•-•', 's': '•••', 't': '-',
    'u': '••-', 'v': '•••-', 'w': '•--', 'x': '-••-', 'y': '-•--',
    'z': '--••', " ": " / ",
    # Numbers
    "1": "•----", '2': '••---', '3': '•••--', '4': '••••-',
    '5': '•••••', '6': '-••••', '7': '--•••', '8': '---••',
    '9': '----•', '0': '-----',
    # Symbols
    '.': '•-•-•-', ',': '--••--', ';': '-•-•-•', ':': '---•••',
    '?': '••--••', '!': '-•-•--', "+": "•-•-•", "-": "-••••-",
    "=": "-•••-"
}


async def encrypt(code: str = None, text: str = None) -> str:
    if code:
        if text:
            codec_out: str = ''
            if code.lower() == 'code':
                for char in text.lower():
                    for key, val in code_own.items():
                        if char == key:
                            codec_out += val
            elif code.lower() == 'morse':
                text = text.replace(".", "•")
                morse_char: str = ''
                for char in text.lower():
                    for key, val in morse_code.items():
                        if char == key:
                            morse_char += val + " "
                codec_out = morse_char
            elif code.lower() == 'rcipher':

                blank = '`-1~;;'
                iter = 0
                text_length = len(text)

                encryption_lvl = random.randint(2, 2000)

                key = ''
                while iter < encryption_lvl:
                    rail_count = random.randint(2, int((text_length / 4) ** 1.45))

                    rails = [[blank for _ in range(text_length)] for _ in range(rail_count)]

                    index = 0
                    rail_idx = 0
                    reverse = False
                    for char in text:
                        if rail_idx == rail_count - 1:
                            reverse = True
                        elif rail_idx == 0:
                            reverse = False

                        rails[rail_idx][index] = char
                        if reverse:
                            rail_idx -= 1
                        else:
                            rail_idx += 1

                        index += 1

                    cipher = ''
                    for rail in rails:
                        for char in rail:
                            cipher += char if char != blank else ''

                    # print('],\n'.join(str(rails).split('],')))
                    # print(iter, cipher, str(hex(rail_count)).replace('0x', ''), rail_count)
                    text = cipher
                    key += str(hex(rail_count)).replace('0x', '') + ';'
                    iter += 1

                keys_path = 'C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/encryption-keys.json'

                with open(keys_path) as _f:
                    keys: dict = json.load(_f)

                serial = str(hex((int(list(keys.keys())[-1], base = 16) if len(keys) >= 1 else 0) + 1))
                keys[serial] = key

                with open(keys_path, 'w') as f_:
                    json.dump(keys, f_, indent = 3)

                cipher = list(cipher)

                if text_length % 2 == 0:
                    injection_idx = int(text_length / 2) - 1
                else:
                    injection_idx = int(text_length / 2)

                serial_len = len(serial)
                cipher.insert(injection_idx, serial)

                cipher = f"{str(hex(injection_idx + serial_len)).replace('0', '')}.{''.join(cipher)}.{str(hex(injection_idx)).replace('0', '')}"[
                         ::-1]

                codec_out = cipher
    return codec_out


async def decrypt(code: str = None, text: str = None, ctx: Context = None) -> str:
    codec_out: str = ''
    if code.lower() == "code":
        for char in text:
            for key, val in code_own.items():
                if char == val:
                    codec_out += key
        codec_out = codec_out[:1].upper() + codec_out[1:]
    elif code.lower() == "morse":
        text = text.replace(".", "•")
        letters: list = text.split()
        for letter in letters:
            for key, val in morse_code.items():
                if letter == val:
                    codec_out += key
        codec_out = codec_out[:1].upper() + codec_out[1:]
    elif code.lower() == 'rcipher':
        cipher = text
        og_cipher = cipher = cipher[::-1]

        message = await ctx.send(f'`Decryption complete`\n'
                                 f'***```fix\n{og_cipher}\n```***')

        bounds = (cipher[::-1].split('.', 1)[0][::-1], cipher.split('.', 1)[0])
        cipher = cipher.replace('.' + bounds[0], '').replace(bounds[1] + '.', '')
        secondary_key = cipher[int('0' + bounds[0], base = 16):int('0' + bounds[1], base = 16)]
        cipher = cipher.replace(secondary_key, '')

        keys_path = 'C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/encryption-keys.json'
        with open(keys_path) as _f:
            keys: dict = json.load(_f)

        primary_key: str = keys[secondary_key]

        encryption_level = primary_key.count(';')
        key = [int(f'0x{rail_count}', base = 16) for rail_count in primary_key[:-1].split(';')][::-1]

        blank = '`-1~;;'
        iter = 0
        cipher_length = len(cipher)
        text = og_cipher

        while iter < encryption_level:

            rail_count = key[iter]

            rails = [[blank for _ in range(cipher_length)] for _ in range(rail_count)]

            for i in range(rail_count):
                nth_odd = lambda n: 1 + (n - 1) * 2 if n >= 1 else 0
                first_space = nth_odd(rail_count - i - 1)
                second_space = nth_odd(i)
                spacing = (first_space + (1 if first_space else 0), second_space + (1 if second_space else 0))
                exception = False
                start = True
                prev_idx = 0

                while not exception:
                    try:
                        prev_idx = idx = i if start else (spacing[0] + prev_idx)
                        if spacing[0] != 0 or start:
                            rails[i][idx] = cipher[0]
                            cipher = cipher[1:]
                        spacing = (spacing[1], spacing[0]) if not start else spacing
                    except IndexError:
                        exception = True
                    start = False
                rails[i] = [char.replace(blank, '') for char in rails[i]]

            index = 0
            rail_idx = 0
            reverse = False
            for i in range(cipher_length):
                if rail_idx == rail_count - 1:
                    reverse = True
                elif rail_idx == 0:
                    reverse = False

                cipher += rails[rail_idx][index]
                if reverse:
                    rail_idx -= 1
                else:
                    rail_idx += 1

                index += 1

            text = cipher
            iter += 1

        keys.pop(secondary_key)

        with open(keys_path, 'w') as f_:
            json.dump(keys, f_, indent = 3)

        if len(og_cipher) <= 40:
            og_cipher = list(og_cipher)
            for i, char in enumerate(cipher):
                await asyncio.sleep(0.25)
                og_cipher[i] = char
                message = await message.edit(content = f"`Decrypting{'.' * ((i % 3) + 1): <3}`\n"
                                                       f"***```fix\n{''.join(og_cipher)}\n```***")

        else:
            og_cipher = og_cipher.split()
            for i, char in enumerate(cipher.split()):
                try:
                    await asyncio.sleep(0.25)
                    og_cipher[i] = char
                except IndexError:
                    og_cipher.append(char)
                message = await message.edit(content = f"`Decrypting{'.' * ((i % 3) + 1): <3}`\n"
                                                       f"***```fix\n{' '.join(og_cipher)}\n```***")

        message = await message.edit(content = f'`Decryption complete`\n'
                                               f'***```fix\n{cipher}\n```***')
        codec_out = cipher
    return codec_out
