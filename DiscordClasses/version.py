import re


class Version:
    __slots__ = ['major', 'minor', 'micro']
    __doc__ = "A class created for keeping track of the bot's VERSION."

    def __init__(self, vers):
        self.major: int = int(vers[:1])
        self.minor: int = int(vers[2:4])
        self.micro: int = int(vers[5])

    def __str__(self):
        return self.version

    def __repr__(self):
        return f"<Version Obj:{self.version}>"

    def __eq__(self, other):
        if not isinstance(other, Version) and not isinstance(other, str):
            raise TypeError(f'{other} of type {type(other)} cannot be compared to {repr(self)}')
        if isinstance(other, str):
            if re.search(r'[0-9]\.[0-9]{2}\.[0-9]', other):
                return other == self.version
            raise ValueError(f'Value of {other} cannot be compared to {repr(self)}')
        return other.version == self.version

    def increment(self):
        if 0 <= self.micro < 9:
            self.micro += 1
        else:
            self.micro = 10 - (self.micro + 1)
            if 0 <= self.minor < 99:
                self.minor += 1
            else:
                self.minor = 100 - (self.minor + 1)
                self.major += 1
        return self

    @property
    def version(self):
        return f'{self.major}.{self.minor:0>2}.{self.micro}'


with open("C:/Users/Shlok/bot_stuff/version.txt", 'r') as f:
    ver = Version(f.read())

VERSION = ver.increment().version if not re.search("(no?(ah)?|deny)", input("Version increment? ")) else ver.version

with open("C:/Users/Shlok/bot_stuff/version.txt", 'w') as f:
    f.write(VERSION)
