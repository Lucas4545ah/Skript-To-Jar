import os
import sys
import urllib.request
import zipfile
import shutil

def helpPage(error):
    print("\n")
    print("ERROR: " + str(error))
    print("Usage:  SkriptToJar.py 'C:\\Path\\To\\Skript\\File\\YourCoolSkript.sk'")
    print("\n")

if len(sys.argv) == 1: #Check to make sure that the argument exists
    helpPage("Argument 1 did not exist")
    sys.exit(1)
if not os.path.exists(sys.argv[1]): #Make sure that the Skript file exists
    helpPage("Skript path did not exist")
    sys.exit()


if not os.path.exists("WORK"): #Remove and reset work folder
    os.mkdir("WORK") #Make work directory
else:
    shutil.rmtree("WORK")
    os.mkdir("WORK")

print("[Builder] Downloading Skript.jar")
skriptDownloadURL = "https://github.com/SkriptLang/Skript/releases/download/2.5-alpha3/Skript.jar" #Set DownloadURL
urllib.request.urlretrieve(skriptDownloadURL, "skript.jar") #Download the file

print("[Builder] Extracting Jar files")
with zipfile.ZipFile("skript.jar", 'r') as zip_ref:
    zip_ref.extractall("WORK") #Extract the jar contents into WORK folder

print("[Builder] Copying your script")
shutil.rmtree("WORK/scripts") #Remove Built in Scripts
os.mkdir("WORK/scripts") #Create folder again
shutil.copyfile(sys.argv[1], "WORK/scripts/-Main.sk") #Copy the file to the new directory

print("[Builder] Rebuilding jar")
shutil.make_archive("BuiltSkriptJar", 'zip', "WORK") #Zip The Work Directory
os.rename("BuiltSkriptJar.zip", "BuiltSkriptJar.jar") #Rename file

print("[Builder] Cleaning Up")
shutil.rmtree("WORK") # Remove the work directory
os.remove("skript.jar") #Remove the file

print("[Builder] Build complete! Saved: BuiltSkriptJar.jar")