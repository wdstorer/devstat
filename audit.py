import yaml

stream = open("config.yml", "r")
docs = yaml.load_all(stream)
for doc in docs:
    for k,v in doc.items():
        print k, "->", v
    print "\n",
