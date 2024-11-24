import dotenv
import os
dotenv.load_dotenv()
def test_py():
    api_key = os.getenv('DATABASE_URL')
    print(api_key)

test_py()