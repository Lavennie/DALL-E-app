import openai
import webbrowser
import os

BLACK_FG = "\033[30m"
RED_FG = "\033[31m"
BLUE_FG = "\033[34m"
GREEN_FG = "\033[32m"
YELLOW_FG = "\033[93m"

os.system('color F0')
openai.api_key = ""

inputText = ""
generateCount = 0;
mode = 0;

while (inputText != "q"):
    inputText = input(BLACK_FG + "Describe what you wish to generate or enter:\n- \'q\' to exit\n" +
        "- \'c\' to generate image\n- \'e\' to edit existing image\n- \'v\' to generate variations\n" + BLUE_FG)
    if(inputText == "q"):
        break;
    elif(inputText == "c"):
        mode = 0;
        print(BLACK_FG + "Mode swapped to" + GREEN_FG + "\'Generate Image\'\n")
    elif(inputText == "e"):
        print(RED_FG + "Not yet implemented, please choose another option\n")
    elif(inputText == "v"):
        print(RED_FG + "Not yet implemented, please choose another option\n")
    else:
        generateCount = int(input(BLACK_FG + "Enter image count between 1-10 (inputs will be limited to this range)\n" + BLUE_FG))
        if (mode == 0):
            response = openai.Image.create(
              prompt=inputText,
              n=generateCount,
              size="1024x1024"
            )
            
            for image_url in response['data']:
                webbrowser.open(image_url['url'], new=2)
            print()
        else:
            print(RED_FG + "This mode is not yet imaplemented, please swap to another mode\n")
        
