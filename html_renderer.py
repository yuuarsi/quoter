from src.discord_markdown.discord_markdown import convert_to_html
from html2image import Html2Image
from PIL import Image
from pathlib import Path
from uuid import uuid4
from urllib.parse import quote_plus
from emoji import unicode_codes
from config import CONFIGS as cfg
import tempfile, io, re, os

with open('body.html') as b:
    HTML_BODY = b.read()

with open('style.css') as s:
    CSS = s.read()
    CSS = CSS.format(dFont=(Path.cwd() / f"./fonts/{cfg['DefaultFont']['Name']}").as_uri(), dFontFormat=cfg['DefaultFont']['Format'],
                     fbFont=(Path.cwd() / f"./fonts/{cfg['FallbackFont']['Name']}").as_uri(), fbFontFormat=cfg['FallbackFont']['Format'])

BASE_GD_PATH = (Path.cwd() / './images/base-gd.png').as_uri()
HTML_IMG_TEMPLATE = '<img class="emoji" src="{}">'
BASE_EMOJI_CDN_URL = 'https://emojicdn.elk.sh/'

language_pack = unicode_codes.get_emoji_unicode_dict('en')
_UNICODE_EMOJI_REGEX = '|'.join(map(re.escape, sorted(language_pack.values(), key=len, reverse=True)))
EMOJI_REGEX = re.compile(f'({_UNICODE_EMOJI_REGEX})')

try:
    CHROME_PATH = cfg['ChromePath']
except:
    CHROME_PATH = None

hti = Html2Image(browser_executable=CHROME_PATH,
                 output_path=tempfile.gettempdir(),
                 custom_flags=['--no-sandbox', '--disable-gpu', "--log-level=3", "--hide-scrollbars"],
                 size=(800, 200),)

if cfg['RandomReply']['Enable']:
    QUOTE_SAVE_PATH = Path('saved_quotes')
    QUOTE_SAVE_PATH.mkdir(exist_ok=True)

def get_url(emoji):
    return BASE_EMOJI_CDN_URL + quote_plus(emoji) + '?style=' + quote_plus('twitter')
        
def parse_emoji(content: str):
    result = content
    for emoji in EMOJI_REGEX.findall(content):
        result = result.replace(emoji, HTML_IMG_TEMPLATE.format(get_url(emoji)))
    return result

def render(name, nickname, content, icon):
    name = f'@{name}'
    nickname = f'- {nickname}'
    para = convert_to_html(content)   
    para = parse_emoji(para) 

    body = HTML_BODY.format(name=name, nickname=nickname, para=para, icon=icon, base_gd=BASE_GD_PATH)
    
    # with open('result.html', 'w', encoding='utf-8') as h:
    #     h.write(body)
    # with open('result.css', 'w', encoding='utf-8') as h:
    #     h.write(CSS)
    temp_dir = os.environ['TMP'] if os.name == 'nt' else '/tmp'
    Path.mkdir(Path(temp_dir, 'html2image'), exist_ok=True)

    file_name = str(uuid4())
    tp = hti.screenshot(html_str=body, css_str=CSS, save_as=file_name + '.png')
    img = Image.open(tp[0])
    img = img.crop((0, 0, 800, 200))
    file = io.BytesIO()
    img.save(file, format="PNG")
    if cfg['RandomReply']['Enable']:
        img.save(QUOTE_SAVE_PATH / (file_name + '.png'), format="PNG")
    file.seek(0)
    return file, file_name
