# Quoter
Make it a quote bot for discord.  
![image](https://user-images.githubusercontent.com/48019531/228881427-6887d1ac-4b16-4ecf-8342-f43c81506673.png)  

# Feature
- Emoji rendering
- Discord custom emoji support
- Random reply

# Installation
## 1. Install Requirements
- Any chromium browser
- python >= 3.8

```python
pip install -r requirements.txt
```



## 2. Download Fonts
The default font is [source-han-sans](https://github.com/adobe-fonts/source-han-sans), download and rename to `default.otf`, place under `/fonts`.  
Or replace with the font you like.

## 3. Configs
Make sure to change the `configs.json` file.

### Basic: 
`Token` :  Your discord token here.  
`ChromePath` : If bot can not found chrome on your machine you can manually set here.  
`PostChannel` : Discord channel ID. Bot will record all quotes to this channel.

### Font settings:
Specify file name and its format. Place your font under `/fonts` folder.

`DefaultFont` : Default font use to render the image,   
`FallbackFont`: If there is any character default font can not display, fallback font specify here will try.  

### Random Reply:
Bot will save quotes, and randomly reply to message using them.

`Enable` :  Enable this function.  
`StoreChannel` : Discord channel ID. Bot will save all quote's information here, delete message will exclude corresponding quote from random reply.  
`ReplyChannel` : Discord channel ID. Which channel should bot reply to.  
`ReplyTrigger` : Reply every X ~ X+50 messages.


# Usage
```
python client.py
```
Reply to a message then mentioning this bot.
# Credits

- [discord-markdown](https://github.com/bitjockey42/discord-markdown)  
Modified to support custom emoji parsing.

- [pilmoji](https://github.com/jay3332/pilmoji)
