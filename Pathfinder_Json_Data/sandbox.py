import  re


reqs = "caster level 3rd"
class_req = re.search("([a-z]+)\s?(?:level|lvl)\s?([0-9]+)", reqs)
print(class_req.groups())