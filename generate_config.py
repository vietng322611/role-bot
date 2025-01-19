import os

def gen():
    if (os.path.exists("./config.json")): return
    
    with open('./config.json', "w") as f:
        f.write('{\n'
                    '\t"creator_id": 0,\n'
                    '\t"log_path": "./logs/",\n'
                    '\t"prefix": "!!",\n'
                    '\t"client_id": 0,\n'
                    '\t"client_secret": "",\n'
                    '\t"redirect_uri": ""\n'
                '}')