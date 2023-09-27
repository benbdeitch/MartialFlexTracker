import os, json

char = { "stats" : {
            "Str": 10,
            "Dex": 10,
            "Con": 10,
            "Int": 10,
            "Wis": 10,
            "Cha": 10
    },
    "race": "dwarf",
    "bab": "3",
    "feats": [],
    "martialflex number": 1,
    "levels": {
        "fighter":2
    },
}
in_feats= set(char["feats"])
feats_file = open("FeatList.json")
feats_list = json.load(feats_file)
feats_file.close()
viable_set = set({})
for sources in feats_list.keys():
    for feats in feats_list[sources].keys():
        feats = feats_list[sources][feats]
        print(feats)

        if "Prerequisites" in feats and len(in_feats.difference(set(feats["Prerequisites"]["Feats"]))) < 2:
            viable_set.add(feats["name"])
        elif not "Prerequisites" in feats:
            viable_set.add(feats["name"])
print(in_feats)