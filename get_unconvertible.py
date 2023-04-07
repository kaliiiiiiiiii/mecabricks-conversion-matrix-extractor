import json

not_convertibles = []
with_skins = {}

with open("export_ldraw.json", "r") as file:
    data = json.load(file)

alphabet = "abcdefghijklmnopqrstuvwxyz"

for key, val in data.items():
    if not val["c"]:
        not_convertibles.append(key)
    for char in alphabet:
        if char in key:
            with_skins.update({key: True})
with_skins = list(with_skins.keys())

print("")
