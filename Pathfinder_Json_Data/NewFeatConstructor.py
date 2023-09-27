import os, json, re



while True:
    feat_name = input("Enter the feat name.")
    file = feat_name.lower().replace(" ", "_")
    feats = open(f'PSRD-Data\spheres_of_might\\feat\{file}', "w")
    sections = []
    
    prereqs = []
    source = "Spheres of Might"
    benefit = input("Enter the feat's benefits.")
    sections.append({
            "body": benefit,
            "source": source,
            "type": "section",
            "name": "Benefits"

        })
    prereqs = input("Enter the prerequisites")
    if prereqs!= "":
        sections.append({"source": "source", 
            "type": "section", 
            "name": "Prerequisites", 
            "description": prereqs})

    
    description = input("Enter the feat's description.")
    while True:
        more_sections = input("Enter additional sections? Enter Y/N to continue")
        if more_sections.lower() == "y":
            section_name = input("Name of section?")
            section_body = input("Body of section")
            sections.append({"body": section_body,
                             "name": section_name.title(),
                             "source": source,
                             "type": "section"})
        else:
            break;
    cont = input("Add another feat? Enter Y to continue.")
    new_feat= {
        "name": feat_name,
        "sections": sections,
        "source": source,
        "feat_types": {
            "feat_type": "Combat"
        },
        "type": "feat",
        "description": description
    }
   
    feats.write(json.dumps(new_feat, indent=4))
    if cont.lower()!= "y":
        break;
