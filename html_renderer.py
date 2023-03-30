from src.discord_markdown.discord_markdown import convert_to_html
from html2image import Html2Image
from PIL import Image
from uuid import uuid4
import tempfile, io
from pathlib import Path
import re
from urllib.parse import quote_plus
from emoji import unicode_codes
from client import cfg

HTML_BODY = '''<body onload="resize_to_fit();">
  <div class="container">
    <img class="avatar" src="{icon}">
    <img class="base_gd" src="{base_gd}">
    <blockquote class="quote-card">{para}<cite>{nickname}</cite><aka>{name}</aka>
    </blockquote>
  </div>
</body>
<script>
  const output1 = document.querySelectorAll('p');
  const output2 = document.querySelector('cite');
  const output3 = document.querySelector('aka');
  const emoji = document.querySelectorAll('.emoji');
  const outputContainer = document.querySelector('.quote-card');

  function resize_to_fit(fontsize = 48) {{
    let fontSize = fontsize;
    let sum = 0;
    output1.forEach(function (x) {{
      sum += x.clientHeight;
    }})
    if (sum + output2.clientHeight + output3.clientHeight >= outputContainer.clientHeight) {{
      style = (parseFloat(fontSize) - 1) + 'px';
      output1.forEach(function (x) {{
        x.style.fontSize = style;
      }})   
      emoji.forEach(function (x) {{
        x.style.height = style;
      }})
      resize_to_fit(style);
    }}
    else {{
        emoji.forEach(function (x) {{
            x.style.paddingBottom = parseFloat(4 * Math.sqrt(fontSize / 48)) + 'px';
        }})
    }}
  }}
  </script>'''
CSS = f'''@font-face {{
    font-family: 'SourceHanSans';
    src: url('{(Path.cwd() / './fonts/SourceHanSansTC-Medium.otf').as_uri()}') format('opentype');
}}''' + \
f'''@font-face {{
    font-family: 'ArialUni';
    src: url('{(Path.cwd() / './fonts/ArialUnicodeMS.ttf').as_uri()}') format('truetype');
}}''' + \
'''body {
    font-family: SourceHanSans, ArialUni;
    height: 200px;
    width: 800px;
    margin: 0px;
}
.container {
    width: 800px;
    height: 200px;
}
.quote-card p {
    position: relative;
    color: white;
    font-size: 48px;
    margin: 0;
    width: 550px;
    line-height: 1.25;
}
.quote-card cite {
    position: relative;
    color: white;
    font-size: 20px;
    width: 550px;
    padding-top: 10px;
}
.quote-card aka {
    position: relative;
    color: white;
    font-size: 16px;
    width: 550px;
    opacity: 0.7;
}
blockquote.quote-card {
    padding-left: 0px;
    padding-right: 0px;
    margin: 10px;
    width: 580px;
    height: 180px;
    left: 200px;
    position: absolute;
    text-align: center;
    display: grid;
    align-content: center;
    z-index: 3;
    word-wrap: break-word;
}
.avatar {
    position: absolute;
    left: -10px;
    top: -25px;
    width: 250px;
    height: 250px;
    z-index: 0;
}
.base_gd {
    position: absolute;
    left: 0px;
    top: 0px;
    z-index: 1;
}
.emoji {
   display: inline-block;
   height: 48px;
   object-fit: contain;
   vertical-align: bottom;
}'''
HTML_IMG_TEMPLATE = '<img class="emoji" src="{}">'
BASE_EMOJI_CDN_URL = 'https://emojicdn.elk.sh/'

language_pack = unicode_codes.get_emoji_unicode_dict('en')
_UNICODE_EMOJI_REGEX = '|'.join(map(re.escape, sorted(language_pack.values(), key=len, reverse=True)))
EMOJI_REGEX = re.compile(f'({_UNICODE_EMOJI_REGEX})') #|{_DISCORD_EMOJI_REGEX})

try:
    CHROME_PATH = cfg['ChromePath']
except:
    CHROME_PATH = None

hti = Html2Image(browser_executable=CHROME_PATH,
                 output_path=tempfile.gettempdir(),
                 custom_flags=['--no-sandbox', '--disable-gpu', "--log-level=3"],
                 size=(800, 200),)

QUOTE_SAVE_PATH = Path('saved_quotes')
QUOTE_SAVE_PATH.mkdir(exist_ok=True)

def get_url(emoji):
    # if len(emoji) > 18:
    #     return BASE_DISCORD_EMOJI_URL + emoji.split(':')[-1][:] + '.png'
    # else:
    return BASE_EMOJI_CDN_URL + quote_plus(emoji) + '?style=' + quote_plus('twitter')
        
def parse_emoji(content: str):
    result = content
    for emoji in EMOJI_REGEX.findall(content):
        result = result.replace(emoji, HTML_IMG_TEMPLATE.format(get_url(emoji)))
    return result

def render(name, tag, nickname, content, icon):
    name = f'@{name}#{tag}'
    nickname = f'- {nickname}'
    para = convert_to_html(content)   
    para = parse_emoji(para) 

    body = HTML_BODY.format(name=name, nickname=nickname, para=para, icon=icon,
                            base_gd=(Path.cwd() / './images/base-gd.png').as_uri())
    
    # with open('result.html', 'w', encoding='utf-8') as h:
    #     h.write(body)

    file_name = str(uuid4())
    tp = hti.screenshot(html_str=body, css_str=CSS, save_as=file_name + '.png')
    img = Image.open(tp[0])
    img = img.crop((0, 0, 800, 200))
    file = io.BytesIO()
    img.save(file, format="PNG")
    img.save(QUOTE_SAVE_PATH / (file_name + '.png'), format="PNG")
    file.seek(0)
    return file, file_name
