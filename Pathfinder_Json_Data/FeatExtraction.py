#This program is made to read through the database, and convert it into a format that's more useful for my purposes. 

#It accepts json files, and specifically was made to help me compile the multiple files into a single database, that could be more clearly used for my purposes. Notes on the structure of the JSONS: Every feat is of this structure: 

#{
#     "name": string
#      "url": string
#       "sections": {"source":string, , "type": string, "name": string, "body"|"description": string}
#       "source":   string
#       "feat_types": string
#       "type": string
#       "description"|"body": string
#}

#Categories of prerequisites need to be defined. 
race = "(elf|half-elf|orc|human|ratfolk|tiefling|dwarf|halfling|goblin|nagaji|fetchling|tengu|vanara|catfolk|kobold|ifrit|merfolk|gnome)"
#categories of stats: 

numbercheck= "[0-9]+"

#Setting the initial directory, for opening up the file
import os, re, json  
directory = 'C:\\Users\\benbd\\PersonalCodingProjects\\MartialFlexTracker\\Pathfinder_Json_Data\\PSRD-Data'
feats = open("FeatList.json", "w")
#This is where we are storing the data, before writing to the json.
all_feats= {}
prereq_set = {"dwarf"}

feat_name_set = set({})
temp_feat_holder =  {}
#The files are stored within 'feat' folders within the subdirectories of the encompassing folder. 
for filename in os.scandir(directory):
    feat_list = f'{filename.path}\\feat'
    feat_dict = {}
    #Checking to see if there is a 'feats' folder, inside the domain.
    if os.path.exists(feat_list):
        #For each json inside, we add the data to a single dictionary, to ease the process of cleaning up the work, and diminish nesting where possible. 
        for json_file in os.scandir(feat_list):
              
            if re.search("json$", json_file.path):
                feat_json = open(json_file.path)

                feat_data = json.load(feat_json)
                feat_json.close()
                feat_for_set = re.sub("[\.-]", " ", feat_data["name"]).lower().strip()
                feat_name_set.add(feat_for_set)
                if feat_data.get("feat_types").get("feat_type")== "Combat":
                    feat_dict.update({feat_data["name"]: feat_data})
                    

    temp_feat_holder.update({filename.name: feat_dict})
misc_set = set({})
#Now that we have the data, we can begin processing it into a more usable form. 
for sources in temp_feat_holder.keys():
    source = temp_feat_holder[sources]
    all_feats.update({sources: {}})
    for a_feat in source.keys():
        feat = source[a_feat]
        new_feat = {"name": feat["name"]}
        #This is for extraction of the prerequisites of feats. 
        for sections in feat["sections"]: 
            if sections["name"]=="Prerequisites" or sections["name"] == "Prerequisite":
                if "description" in sections.keys():
                    prerequisites = sections["description"].split(",")
                else:
                    prerequisites = sections["body"].split(",")
                new_feat.update({"Prerequisites":{}})
                new_feat["Prerequisites"].update({"Feats": []})
                for reqs in prerequisites: 
                    reqs = re.sub("[\.-]", " ", reqs).lower().strip().strip().lower()
                    html_remove = re.search("(<.+>)?([^<>]+)(</.+>)?", reqs)
                    if html_remove:
                        reqs = html_remove.groups()[1]
                  
                    prereq_set.add(reqs)
                    race_req= re.search(race, reqs)
                    stat_req= re.search("(str|dex|con|int|wis|cha) ([0-9]+)", reqs)

                    class_level_format = True
                    class_req = re.search("([a-z]+)\s?(?:level|lvl)\s?([0-9]+)", reqs)
                    if not class_req:
                        class_req = re.search("([0-9]*)(?:th)?(?:\s)?(?:level|lvl)\s?([a-z]+)", reqs)
                        class_level_format = False;
                    bab_req = re.search("(base attack bonus|bab) (\+[0-9]+)", reqs)
                    feat_req = re.search("(([^\.]+))", reqs)
                    race_trait_req = re.search("(.+) racial trait", reqs)
                    sneak_req = re.search("sneak attack (.+)", reqs)
                    size_req = re.search("(.+) size (or .+)", reqs)
                    skill_req = re.search("(.+) ([0-9]*) ?ranks?\s?([0-9]*)", reqs)
                    feature_req = re.search("(.*)(?:class feature)(.*)", reqs)
                    prof_req = re.search("(.*)\s?(?:proficient|proficiency)(?:\swith)?\s?(.*)", reqs)
                    if race_req:
                       new_feat["Prerequisites"].update({"Race": race_req.groups()[0].title()})
                    elif stat_req:
                        new_feat["Prerequisites"].update({"Stats": {stat_req[1] : stat_req[2].title()}})
                    elif feat_req.groups()[0] in feat_name_set:
                        new_feat["Prerequisites"]["Feats"].append(reqs.title())
                    elif class_req:
                        if class_level_format:
                            new_feat["Prerequisites"].update({"Class": {class_req.groups()[0]: class_req.groups()[1],}})
                        else:
                            new_feat["Prerequisites"].update({"Class": {class_req.groups()[1]: class_req.groups()[0],}})

                    elif bab_req:
                        new_feat["Prerequisites"].update({"BAB": bab_req.groups()[1]})
                    elif race_trait_req:
                        new_feat["Prerequisites"].update({"Racial Trait":reqs})
                    elif size_req:
                        new_feat["Prerequisites"].update({"Size":reqs})
                    elif skill_req:
                        new_feat["Prerequisites"].update({skill_req.groups()[0].title(): skill_req.groups()[1]})
                    elif sneak_req:
                        new_feat["Prerequisites"].update({"Sneak Attack": sneak_req.groups()[0]})
                    elif feature_req:
                        new_feat["Prerequisites"].update({"Class Features": feature_req.groups()[0]+feature_req.groups()[1]})
                    elif prof_req:
                        new_feat["Prerequisites"].update({"Proficiency": prof_req.groups()[0]+prof_req.groups()[1]})
                    else:
                        new_feat["Prerequisites"].update({"Misc": reqs})
                        misc_set.add(reqs)
        all_feats[sources].update({new_feat["name"]: new_feat})


feats.write(json.dumps(all_feats, indent=4))
print(misc_set)

