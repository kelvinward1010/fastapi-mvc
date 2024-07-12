

def EntityUser(user) -> dict:
    return {
        "_id": str(user["_id"]),
        "name": str(user["name"]),
        "email": user["email"],
        "password": user["password"],
        "image": user["image"],
        "position": user["position"],
        "createdAt": user["createdAt"],
        "updatedAt": user["updatedAt"],
    }
    
def EntityPost(post) -> dict:
    return {
        "_id": str(post["_id"]),
        "topic": post["topic"],
        "title": post["title"],
        "authorID": post["authorID"],
        "content": post["content"],
        "description": post["description"],
        "image_thumbnail": post["image_thumbnail"],
        "createdAt": post["createdAt"],
        "updatedAt": post["updatedAt"],
    }