import requests

def register_user(username, password):
    url = "http://127.0.0.1:5000/register"
    data = {
        "username": username,
        "password": password
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code == 201:
            print(f"User '{username}' registered successfully!")
        else:
            print(f"Failed to register user: {response.json().get('error')}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    username = input("Enter a username to register: ")
    password = input("Enter a password: ")
    register_user(username, password)

