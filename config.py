import json

CONFIGS = {
    'Token': None,
    'ChromePath': None,
    'RandomReply': {
        'Enable': False,
        'StoreChannel': None,
        'ReplyChannel': None,
        'ReplyTrigger': 100
    },    
}

# try:
with open('config.json', 'r') as f:
    cf = json.load(f)
    CONFIGS.update(cf)
# except:
#     CONFIGS = {
#     'Token': None,
#     'ChromePath': None,
#     'RandomReply': {
#         'Enable': False,
#         'StoreChannel': None,
#         'ReplyChannel': None,
#         'ReplyTrigger': 100
#     },    
# }

with open('config.json', 'w') as f:
    json.dump(CONFIGS, f)