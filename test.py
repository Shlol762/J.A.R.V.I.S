import json

new_dict = {}

with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/drive_links.json", "r") as f:
    subjects: dict = json.load(f)

subjects: dict = {key.lower(): {chp.lower(): link for chp, link in val.items()} for key, val in subjects.items()}

with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/drive_links.json", "w") as f:
    json.dump(subjects, f, indent=3)