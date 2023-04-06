import json

CONFIGS = {
    'Token': None,
    'ChromePath': None,
    'DefaultFont': {
        'Name': 'default.otf',
        'Format': 'opentype',    
    },
    'FallbackFont': {
        'Name': 'fallback.ttf',
        'Format': 'truetype',    
    },
    'PostChannel': None,
    'RandomReply': {
        'Enable': False,
        'StoreChannel': None,
        'ReplyChannel': None,
        'ReplyTrigger': 100,
    },
}
try:
    with open('configs.json', 'r') as f:
        cf = json.load(f)
        CONFIGS.update(cf)
except:
    pass

with open('configs.json', 'w') as f:
    json.dump(CONFIGS, f, indent=4)
