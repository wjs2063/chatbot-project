import requests
import os



def post_db_name():
    movies = os.listdir()
    movies = [movie for movie in movies if not movie.startswith('.')]
    movies = [movie for movie in movies if not movie.endswith(".sh") and not movie.endswith(".py") ]
    url = 'http://localhost:50000/api/v1/db_test/create_db_detail'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    for movie in movies:
        try :
            response = requests.post(url, headers=headers, json={"name":movie})
            print(f"Status Code: {response.status_code}")
            print("Response Content:")
            print(response.json())
        except:
            print("DB 중복값")


if __name__ == "__main__":
    post_db_name()