# import aiohttp
# import asyncio
# from bs4 import BeautifulSoup
#
#
# async def test():
#     async with aiohttp.ClientSession() as hg:
#         async with hg.get("https://hangouts.google.com/?authuser=1") as req:
#             return BeautifulSoup(await req.text(), 'lxml')
#
#
# soup: BeautifulSoup = asyncio.get_event_loop().run_until_complete(test())
#
# result = soup.prettify()
#
# print(result)
# from PyDictionary import PyDictionary
# import asyncio
#
#
#
# async def func():
#     dcnry = PyDictionary()
#     word = input("Word: ")
#     print(f"{await dcnry.meaning(word)}\n{await dcnry.antonym(word)}\n{await dcnry.synonym(word)}")
#
# asyncio.get_event_loop().run_until_complete(func())
import json

with open("C:/Users/Shlok/J.A.R.V.I.SV2021/text_files/birthdays.txt", "r") as f:
    lines = f.readlines()

new_dict = {}

for line in lines:
    new_dict[line.split(': ')[0]] = line.split(' - ')[1][:-1]

with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/birthdays.json", "w") as f:
    json.dump(new_dict, f, indent=3)
