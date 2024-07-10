

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