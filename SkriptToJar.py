import os
import sys
import urllib.request
import zipfile
import shutil
import time

def helpPage(error):
    print("\n")
    print("ERROR: " + str(error))
    print("Usage:  SkriptToJar.py 'SkriptName' 'C:\\Path\\To\\Skript\\File\\YourCoolSkript.sk' (Opt)-customSkript 'C:\\Path\\To\\Skript\\Jar\\Skript.jar'")
    print("Arguments:                   1                              2                                3                              4                 ")
    print("\n")

if len(sys.argv) == 1: #Check to make sure that the argument exists
    helpPage("Argument 1 did not exist")
    sys.exit()
else:
    skriptNewName = sys.argv[1] #Getnew skript name

if len(sys.argv) == 2:
    helpPage("Argument 2 did not exist")
    sys.exit()

if not os.path.exists(sys.argv[2]): #Make sure that the Skript file exists
    helpPage("Skript path did not exist")
    sys.exit()

skriptJarPath = None
if len(sys.argv) > 3:
    if not sys.argv[3] == "-customSkript":
        helpPage("Invalid Argument 2")
        sys.exit()
    else:
        if os.path.exists(sys.argv[4]):
            skriptJarPath = sys.argv[4]
        else:
            helpPage("Custom skript jar could not be found : Argument 4")
            sys.exit()

if skriptJarPath:
    print("WARNING: Custom Skript jars do NOT come with support")
    time.sleep(5)

if not os.path.exists("WORK"): #Remove and reset work folder
    os.mkdir("WORK") #Make work directory
else:
    shutil.rmtree("WORK")
    os.mkdir("WORK")

print("[Builder] Downloading Skript.jar")
if not skriptJarPath:
    skriptDownloadURL = "https://github.com/SkriptLang/Skript/releases/download/2.5-alpha3/Skript.jar" #Set DownloadURL
    urllib.request.urlretrieve(skriptDownloadURL, "skript.jar") #Download the file
else:
    print("[Builder] Custom jar detected, setting up custom jar...")
    try:
        shutil.copyfile(skriptJarPath, "skript.jar")
    except:
        pass

print("[Builder] Extracting Jar files")
try:
    with zipfile.ZipFile("skript.jar", 'r') as zip_ref:
        zip_ref.extractall("WORK") #Extract the jar contents into WORK folder
except Exception as error:
    print("[Builder] ERROR on task ExtractJar: " + str(error))
    sys.exit()

print("[Builder] Copying your script")
try:
    shutil.rmtree("WORK/scripts") #Remove Built in Scripts
    os.mkdir("WORK/scripts") #Create folder again
    shutil.copyfile(sys.argv[2], "WORK/scripts/-" + sys.argv[1] + ".sk") #Copy the file to the new directory
except Exception as error:
    print("[Builder] ERROR on task CopySkript: " + str(error))
    sys.exit()

print("[Builder] Rebuilding plugin information...")
try:
    with open("WORK/plugin.yml") as f:
        fileRead = f.read().splitlines()
    fileRead[21] = "name: " + skriptNewName
    os.remove("WORK/plugin.yml")
    with open("WORK/plugin.yml", "a") as f:
        for line in fileRead:
            f.write(line + "\n")
except Exception as error:
    print("[Builder] ERROR on task ReBuiltPluginInformation: " + str(error))
    sys.exit()

print("[Builder] Rebuilding jar")
try:
    shutil.make_archive("BuiltSkriptJar", 'zip', "WORK") #Zip The Work Directory
    os.rename("BuiltSkriptJar.zip", sys.argv[1] + ".jar") #Rename file
except Exception as error:
    print("[Builder] ERROR on task BuildJar: " + str(error))
    sys.exit()

try:
    print("[Builder] Cleaning Up")
    shutil.rmtree("WORK") # Remove the work directory
    os.remove("skript.jar") #Remove the file
except Exception as error:
    print("[Builder] ERROR on task CleanUp: " + str(error))
    sys.exit()

print("[Builder] Build complete! Saved: " + sys.argv[1] + ".jar")