import json
import re

with open("mkvdb.json", "r") as f:
    words = json.load(f)

new = {}

for key, val in words.items():
    rstring = r'\b(whores?|cunts?|tits?|boobs?|ass(holes?)?|milfs?|dick(s|heads?)?|cocks?|anals?|homos?' \
              r'|w?tf*|gays?|vaginas?|puss(y|ies))\b|\b((skull)?f(u)?(c+)?k|bitch|sex|cum|fuc+)'
    if not re.search(
            rstring,
            key.lower()) or not key.isascii():
        new[key] = val
    # for v in val:
    #     if not new.get(key):
    #         new[key] = []
    #     if not re.search(
    #             rstring,
    #             v.lower()) or not v.isascii():
    #         new[key].append(v)

with open("mkvdb.json", "w") as f:
    json.dump(new, f, indent=3)