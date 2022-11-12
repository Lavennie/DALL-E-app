# DALL-E-app
## Prepare for use
First download a release from: https://github.com/Lavennie/DALL-E-app/releases and unpack it (files are directly in archive not inside a folder).
Then replace the *sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX* inside *config.txt* with your openai API key.

## Getting the openai API key
- Go to https://beta.openai.com/overview.
- Log in or sign up for an account.
- Click your profile icon.
- Select *View API keys*.
- Click create new secret key and copy to the clipboard
- Paste it into *config.txt* file.

## Config file options
Options are defined in lines. Each line is of format "keyword:value".
Valid keywords and their values are: 
- key: the openai API key of form *sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX*,
- color-theme: values can be *light* or *dark*,
- size: *1024x1024*, *512x512* or *256x256*.

## Input image limitations
Source image for variations and source image and mask for image edit have to be *.png* and smaller than *4MB*.
