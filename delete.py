import requests

def delete_user(username):
    url = "http://127.0.0.1:5000/delete_user"  
    data = {
        "username": username
    }
    try:
        response = requests.delete(url, data=data)
        if response.status_code == 200:
            print(f"User '{username}' deleted successfully!")
        else:
            print(f"Failed to delete user: {response.json().get('error')}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    username = input("Enter the username to delete: ")
    delete_user(username)

