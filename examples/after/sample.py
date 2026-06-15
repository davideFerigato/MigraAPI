# Example Python code with new API
from new_api import Client, fetch_user_by_id
import new_api as api

def main():
    client = Client(api_key="secret")
    
    # Direct call
    user = new_api.fetch_user_by_id(user_id=123)
    print(user)
    
    # Call via client instance
    posts = client.list_posts_by_user(user_id=123)
    
    # Function import call
    data = fetch_user_by_id(user_id=123)
    
    # Alias call
    result = api.fetch_user_by_id(user_id=456)
    
    return user, posts, data, result

if __name__ == "__main__":
    main()
