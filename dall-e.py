# documentation: https://beta.openai.com/docs/guides/images/
import openai
import webbrowser
import os

# at start so that colors work for error messages (light)
os.system('color F0')

FG_COLOR = "\033[30m" # black
PROMPT_COLOR = "\033[34m" # blue
RED_FG = "\033[31m"
BLUE_FG = "\033[34m"
GREEN_FG = "\033[32m"
YELLOW_FG = "\033[93m"

def printError(msg):
    print(RED_FG + str(msg) + "\n")
def imageGenerateCountPrompt():
    return min(max(int(input(FG_COLOR + "Enter image count between 1-10" +
        "(inputs will be limited to this range)\n" + PROMPT_COLOR)), 1), 10)
    

# read user settings
configFilePath = "config.txt"
colorTheme = "light"
imageSize = "1024x1024"

if (os.path.exists(configFilePath)):
    for line in open(configFilePath):
        stripped = line.strip()
        # color theme
        if (stripped.startswith("color-theme:")):
            readTheme = (line.strip()[12:]).strip()
            if(readTheme == "dark"):
                colorTheme = "dark"
        # generated image size
        elif (stripped.startswith("size:")):
            readSize = (line.strip()[5:]).strip()
            if(readTheme in ["256x256", "512x512", "1024x1024"]):
                imageSize = readSize
        # key from openai account
        elif (stripped.startswith("key:")):
            readKey = (line.strip()[4:]).strip()
            if(readKey.startswith("sk-") and len(readKey) == 51):
                openai.api_key = readKey
            else:
                printError("Please add a \'key: [sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX]\' " +
                           "line to \'config.txt\' file where \'sk-...\' represents a " +
                           "key generated in your openai account")
                input()
                exit()
                
else:
    printError("Please create a \'" + configFilePath + "\' file in same folder as this script.\n" +
               "Avalible options inside config file:\n" +
               "- key: [sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX]\n" +
               "- color-theme: [light/dark]\n" +
               "- size: [1024x1024/512x512/256x256]")
    input()
    exit()

# dark color theme background
if (colorTheme == "dark"):
    os.system('color 07')
    FG_COLOR = "\033[37m" # white
    PROMPT_COLOR = "\033[36m" # yellow
    
inputText = ""
generateCount = 0;
mode = 0;

while (inputText != "q"):
    nextStepPrompt = ""
    if (mode == 0):
        nextStepPrompt = "Describe what you wish to generate"
    elif (mode == 1):
        nextStepPrompt = "Enter path to source image for image edit (absolute or relative to script folder)"
    elif (mode == 2):
        nextStepPrompt = "Enter path to source image for variations (absolute or relative to script folder)"
        
    inputText = input(FG_COLOR + nextStepPrompt + " or enter:\n- \'q\' to exit\n" +
        "- \'c\' to generate image (default)\n- \'e\' to edit existing image\n- \'v\' to generate variations\n" + PROMPT_COLOR)

    if(inputText == "q"):
        break;
    elif(inputText == "c"):
        mode = 0
        print(FG_COLOR + "Mode swapped to" + GREEN_FG + "\'Generate Image\'\n")
    elif(inputText == "e"):
        mode = 1
        print(FG_COLOR + "Mode swapped to" + GREEN_FG + "\'Edit Image\'\n")
    elif(inputText == "v"):
        mode = 2
        print(FG_COLOR + "Mode swapped to" + GREEN_FG + "\'Generate Image Variations\'\n")
    else:
        try:
            if (mode == 0):
                generateCount = imageGenerateCountPrompt();
                response = openai.Image.create(
                  prompt = inputText,
                  n = generateCount,
                  size = imageSize
                )
                
                for image_url in response['data']:
                    webbrowser.open(image_url['url'], new=2)
                print()
            elif (mode == 1):
                if (os.path.exists(inputText)):
                    maskPath = input(FG_COLOR + "Enter path to mask image for image edit (absolute or relative to script folder)\n" + PROMPT_COLOR)
                    if (os.path.exists(maskPath)):
                        readPrompt = input(FG_COLOR + "Describe what you wish to generate\n" + PROMPT_COLOR)
                        generateCount = imageGenerateCountPrompt();
                        response = openai.Image.create_edit(
                            image = open(inputText, "rb"),
                            mask = open(maskPath, "rb"),
                            prompt = readPrompt,
                            n = generateCount,
                            size = imageSize
                        )
                    
                        for image_url in response['data']:
                            webbrowser.open(image_url['url'], new=2)
                        print()
                    else:
                        printError("Given path to mask image does not exist")
                else:
                    printError("Hiven path to source image does not exist")       
            elif (mode == 2):
                if (os.path.exists(inputText)):
                    generateCount = imageGenerateCountPrompt();
                    response = openai.Image.create_variation(
                        image = open(inputText, "rb"),
                        n = generateCount,
                        size = imageSize
                    )
                    
                    for image_url in response['data']:
                        webbrowser.open(image_url['url'], new=2)
                    print()
                else:
                    printError("Given path to source image does not exist")
            else:
                printError("This mode is not yet imaplemented, please swap to another mode")
        except Exception as e:
            printError("Failed request. Possible reasons:\n" +
                       "- Key in \'config.txt\' is invalid\n" +
                       "- Limit of 10 images per minute or 25 images per 5 minutes has been reached, in this case please wait a bit")
            printError(e)
            input()
            break
