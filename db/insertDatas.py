from testDb import TsViodes
from connectDb import session
import datetime
import os

root_path = '/'

for dirpath, dirnames, filenames in os.walk(root_path):
    for file in filenames:
        if file.endswith('.mp3'):
            file_path = os.path.join(dirpath, file)
            file_size = os.path.getsize(file_path)
            new_data = TsViodes(message_id="001", 
                                send_user_id="001", 
                                send_user_name="tester", 
                                created_date = datetime.datetime.now(),
                                message_data = file_path)
session.add(new_data)
session.commit()