import re


class Version:
    __slots__ = ['q1', 'q2', 'q3']
    __doc__ = "A class created for keeping track of the bot's VERSION."

    def __init__(self, vers):
        self.q1: int = int(vers[:1])
        self.q2: int = int(vers[2:4])
        self.q3: int = int(vers[5])

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
        return other.version == self.versions

    def increment(self):
        if 0 <= self.q3 < 9:
            self.q3 += 1
        else:
            self.q3 = 10 - (self.q3 + 1)
            if 0 <= self.q2 < 99:
                self.q2 += 1
            else:
                self.q2 = 100 - (self.q2 + 1)
                self.q1 += 1
        return self

    @property
    def version(self):
        return f'{self.q1}.{self.q2:0>2}.{self.q3}'


with open("C:/Users/Shlok/bot_stuff/version.txt", 'r') as f:
    ver = Version(f.read())

VERSION = ver.increment().version

with open("C:/Users/Shlok/bot_stuff/version.txt", 'w') as f:
    f.write(VERSION)
