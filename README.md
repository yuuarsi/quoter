# Quoter
Make it a quote bot for discord.  
![image](https://user-images.githubusercontent.com/48019531/228881427-6887d1ac-4b16-4ecf-8342-f43c81506673.png)  

# Feature
- Emoji rendering
- Discord custom emoji support
- Random reply

# Installation
### 1. Install Requirements
- Any chromium browser
- python >= 3.8

```python
pip install -r requirements.txt
```



### 2. Download Fonts

Get fonts from [source-han-sans](https://github.com/adobe-fonts/source-han-sans) and rename it to `SourceHanSansTC-Medium.otf`, place under `/fonts`.  
Or replace it with the one you like.

### 3. Config  
  

`Token` : Your discord token here.  
`ChromePath` : Manually set here if bot can't found it.  
`RandomReply` : Bot will randomly reply using saved quotes.  
`StoreChannel` : Discord channel ID, bot will save all quote's information here, delete message will exclude corresponding quote from random reply.  
`ReplyChannel` : Discord channel ID, which channel should bot reply to.  
`ReplyTrigger` : Reply every X ~ X+50 messages.

  

# Credits

- [discord-markdown](https://github.com/bitjockey42/discord-markdown)  
Modified to support custom emoji parsing.

- [pilmoji](https://github.com/jay3332/pilmoji)
