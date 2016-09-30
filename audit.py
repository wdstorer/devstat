import yaml
import os
import json
from fnmatch import fnmatch
from pprint import pprint

def loadConfig(configFile):
    stream = open("config.yml", "r")
    docs = yaml.load(stream)
    #print docs
    return docs

def getDevEnvs(rootPath):
    root = rootPath
    envs = os.walk(root).next()[1]
    return envs

def getJSONFiles(rootPath):
    root = rootPath
    pattern = "*.json"
    apps = []

    for path, subdirs, files in os.walk(root):
        for name in files:
          if fnmatch(name, pattern):
            apps.append(os.path.join(path, name))
    return apps

def getContainerImages(envApps, envName):
    ctImages = []
    for app in envApps:
        with open(app) as data_file:    
            #print app
            ctImages.append([[envName],[app],(json.load(data_file)["container"]["docker"]["image"].rsplit(':',1))])
    return ctImages

loadedConfig = loadConfig("config.yml")
templateApps = getJSONFiles(loadedConfig['MARATHON_APPS'] + 'dev.TEMPLATE')
templateContainerImages = getContainerImages(templateApps, 'dev.TEMPLATE')

#pprint(data)
#print templateContainerImages

print "v2 Dev Environment baseline configuration:"
for ct in templateContainerImages:
    print '{0: <40}'.format(ct[1][0].replace("resources/dev-env/com.birchbox/","")) +  '{0: <40}'.format(ct[2][0]) + ct[2][1]

# Check tag versions 
devEnvironments = getDevEnvs(loadedConfig['MARATHON_APPS'])

for env in devEnvironments:
    devEnvironmentApps = getJSONFiles(loadedConfig['MARATHON_APPS'] + env)
    devEnvironmentContainerImages = getContainerImages(devEnvironmentApps, env)
    #print devEnvironmentContainerImages
    print "validating " + env
    for templateCt in templateContainerImages:
        # check to see if this container exists and is the same version
        appMatch=0
        versionMatch=0
        for devCt in devEnvironmentContainerImages:
            if templateCt[1][0].replace("resources/dev-env/com.birchbox/dev.TEMPLATE","") == devCt[1][0].replace("resources/dev-env/com.birchbox/" + env,""):
                #print '\t' + devCt[1][0] + " match!"
                appMatch=1
        
        if appMatch == 0:
            print "\tno match was found for " + templateCt[1][0]


        

            #else:
                #print templateCt[1][0].replace("resources/dev-env/com.birchbox/dev.TEMPLATE","") + "\t\t" + devCt[1][0].replace("resources/dev-env/com.birchbox/" + env,"")

    #for ct in devEnvironmentContainerImages:
        #print '{0: <65}'.format(ct[1][0].replace("resources/dev-env/com.birchbox/","")) +  '{0: <40}'.format(ct[2][0]) + ct[2][1]
    
