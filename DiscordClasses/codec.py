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
    'u': '••--', 'v': '•••-', 'w': '•--', 'x': '-••-', 'y': '-•--',
    'z': '--••', " ": "•------",
    # Numbers
    "1": "•----", '2': '••---', '3': '•••--', '4': '••••-',
    '5': '•••••', '6': '-••••', '7': '--•••', '8': '---••',
    '9': '----•', '0': '-----',
    # Symbols
    '.': '••••••', ',': '•-•-•-', ';': '-•-•-•', ':': '---•••',
    '?': '••--••', '!': '--••--'
}


def encrypt(code: str = None, text: str = None):
    if code:
        if text:
            codec_out: str = ''
            if code.lower() == 'code':
                for char in text.lower():
                    for key, val in code_own.items():
                        if char == key:
                            codec_out += val
            elif code.lower() == 'morse':
                morse_char: str = ''
                for char in text.lower():
                    for key, val in morse_code.items():
                        if char == key:
                            morse_char += val + " "
                codec_out = morse_char
    return codec_out


def decrypt(code: str = None, text: str = None):
    codec_out: str = ''
    if code.lower() == "code":
        for char in text:
            for key, val in code_own.items():
                if char == val:
                    codec_out += key
        codec_out = codec_out[:1].upper() + codec_out[1:]
    elif code.lower() == "morse":
        letters: list = text.split()
        for letter in letters:
            for key, val in morse_code.items():
                if letter == val:
                    codec_out += key
        codec_out = codec_out[:1].upper() + codec_out[1:]
    return codec_out
