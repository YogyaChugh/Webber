from platformdirs import user_data_dir
import os

app_name = "Webber"
author = "main"

data_dir = user_data_dir(app_name, author)
print(data_dir)
os.makedirs(data_dir, exist_ok=True)
 
config_file = os.path.join(data_dir, "config.json")  
with open(config_file, 'w') as f:
    f.write('{"setting": "darkmode"}')