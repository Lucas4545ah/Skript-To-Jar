import os
import sys
import urllib.request
import zipfile
import shutil
import time
import PySimpleGUI as sg

def convertScripttoJar(skriptJarPath, scriptName):
    if not os.path.exists("WORK"): #Remove and reset work folder
        os.mkdir("WORK") #Make work directory
    else:
        shutil.rmtree("WORK")
        os.mkdir("WORK")

    print("[Builder] Downloading Skript.jar")
    skriptDownloadURL = "https://github.com/SkriptLang/Skript/releases/download/2.5-alpha5/Skript.jar" #Set DownloadURL
    urllib.request.urlretrieve(skriptDownloadURL, "skript.jar") #Download the file

    print("[Builder] Extracting Jar files")
    try:
        with zipfile.ZipFile("skript.jar", 'r') as zip_ref:
            zip_ref.extractall("WORK") #Extract the jar contents into WORK folder
    except Exception as error:
        print("[Builder] ERROR on task ExtractJar: " + str(error))
        return "ERROR on task ExtractJar: " + str(error)

    print("[Builder] Copying your script")
    try:
        shutil.rmtree("WORK/scripts") #Remove Built in Scripts
        os.mkdir("WORK/scripts") #Create folder again
        shutil.copyfile(skriptJarPath, "WORK/scripts/-" + scriptName + ".sk") #Copy the file to the new directory
    except Exception as error:
        print("[Builder] ERROR on task CopySkript: " + str(error))
        return "ERROR on task CopySkript: " + str(error)

    print("[Builder] Rebuilding plugin information...")
    try:
        with open("WORK/plugin.yml") as f:
            fileRead = f.read().splitlines()
        fileRead[21] = "name: " + scriptName
        os.remove("WORK/plugin.yml")
        with open("WORK/plugin.yml", "a") as f:
            for line in fileRead:
                f.write(line + "\n")
    except Exception as error:
        print("[Builder] ERROR on task ReBuiltPluginInformation: " + str(error))
        return "ERROR on task ReBuiltPluginInformation: " + str(error)

    print("[Builder] Rebuilding jar")
    try:
        shutil.make_archive("BuiltSkriptJar", 'zip', "WORK") #Zip The Work Directory
        os.rename("BuiltSkriptJar.zip", scriptName + ".jar") #Rename file
    except Exception as error:
        print("[Builder] ERROR on task BuildJar: " + str(error))
        return "ERROR on task BuildJar: " + str(error)

    try:
        print("[Builder] Cleaning Up")
        shutil.rmtree("WORK") # Remove the work directory
        os.remove("skript.jar") #Remove the file
    except Exception as error:
        print("[Builder] ERROR on task CleanUp: " + str(error))
        return "ERROR on task CleanUp: " + str(error)

    print("[Builder] Build complete! Saved: " + scriptName + ".jar")

    return "BuildSuccessfull"

versionNum = "2.0"

sg.theme("DarkBlue")
layout = [
    [sg.Text(f"Skript to Jar | v{versionNum}", font=("Arial", 20), size=(22, 2))],
    [sg.Text("Select a .SK file")],
    [sg.FileBrowse(size=(7, 1)), sg.InputText(size=(45, 1), key="skriptPath")],
    [sg.Text("Create a new name")],
    [sg.InputText(size=(55, 1), key="name")],
    [sg.Button("Build Jar", size=(48, 1))],
    [sg.Text("IWick Development 2020", size=(42, 1)), sg.Button("Close")],
]
window = sg.Window(f"Skript to Jar | v{versionNum}", layout=layout)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == "Close":
        break

    if event == "Build Jar":
        if values["name"] == "":
            sg.popup_error("You must specify a name for your built Skript")
        elif len(values["name"]) < 4:
            sg.popup_error("The skripts name must be larger than 4 characters")
        elif not os.path.exists(values["skriptPath"]):
            sg.popup_error("Could not locate the skript file, was it moved?")
        elif not values["skriptPath"].lower().endswith(".sk"):
            sg.popup_error("The file you selected is not a Skript file")
        else:
            outputBuild = convertScripttoJar(values["skriptPath"], values["name"])
            if outputBuild == "BuildSuccessfull":
                sg.popup("Build successfull, check current directory for your built jar.")
            else:
                sg.popup_error("Build failed send this error message to the developer:\n" + outputBuild)
