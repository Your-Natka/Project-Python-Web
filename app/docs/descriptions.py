# Загальні описи для Swagger документації

auth_description = {
    "login": {
        "summary": "User login",
        "description": "Authenticate user and return JWT access and refresh tokens."
    },
    "register": {
        "summary": "User registration",
        "description": "Register a new user with email and password. First registered user becomes an admin."
    },
    "refresh": {
        "summary": "Refresh access token",
        "description": "Generate a new access token using a valid refresh token."
    },
    "logout": {
        "summary": "Logout user",
        "description": (
            "Logs out the currently authenticated user by adding their JWT token to the Redis blacklist. "
            "After logout, the token becomes invalid for any future requests."
        )
    }
}

users_description = {
    "signup": {
        "summary": "User registration",
        "description": (
            "Creates a new user account. "
            "The email must be unique. Password will be securely hashed. "
            "After successful registration, a verification email is sent."
        )
    },
    "login": {
        "summary": "User login",
        "description": (
            "Authenticates a user and returns an access and refresh token. "
            "Use these tokens to access protected routes."
        )
    },
    "refresh_token": {
        "summary": "Refresh JWT tokens",
        "description": (
            "Refreshes an expired access token using a valid refresh token."
        )
    },
    "request_mail": {
        "summary": "Request email verification",
        "description": (
            "Sends a verification email to the provided address. "
            "Used during account creation or email change."
        )
    },
    "confirm_mail": {
        "summary": "Confirm email verification",
        "description": (
            "Verifies user email via the token sent to their inbox."
        )
    },
    "admin": {
        "summary": "Admin access route",
        "description": "Restricted endpoint for users with role `admin` only."
    },
    "moderator": {
        "summary": "Moderator access route",
        "description": "Restricted endpoint for users with role `moderator` only."
    },
    "logout": {
        "summary": "Logout user",
        "description": (
            "Logs out the user by invalidating their JWT (adds it to the Redis blacklist)."
        )
    }
}

photos_description = {
    "upload": {
        "summary": "Upload a new photo",
        "description": (
            "Allows authenticated users to upload a new photo to Cloudinary. "
            "You can also add a description and up to 5 tags. "
            "Requires a valid access token."
        )
    },
    "get_by_id": {
        "summary": "Get photo by ID",
        "description": "Retrieve detailed information about a specific photo by its ID."
    },
    "update": {
        "summary": "Update photo details",
        "description": (
            "Allows the photo owner to update description and tags. "
            "Authentication is required. Other users cannot modify this photo."
        )
    },
    "delete": {
        "summary": "Delete photo",
        "description": (
            "Deletes the user's own photo from Cloudinary and the database. "
            "Only the photo owner can perform this action."
        )
    },
    "transform": {
        "summary": "Transform photo",
        "description": (
            "Performs a transformation (resize, crop, etc.) using Cloudinary "
            "and generates a QR code for the transformed image."
        )
    },
    "search": {
        "summary": "Search photos",
        "description": (
            "Search for photos by keyword in description or by tag. "
            "You can use query parameters `keyword` and `tag`."
        )
    }
}

comments_description = {
    "create_comment": {
        "summary": "Add a comment to a photo",
        "description": (
            "Creates a new comment for the specified photo. "
            "Only authenticated users can leave comments. "
            "The `photo_id` in the URL identifies the photo being commented on."
        )
    },
    "update_comment": {
        "summary": "Update a comment",
        "description": (
            "Allows the author of a comment to update its content. "
            "Returns 404 if the comment does not exist or the user does not have permission."
        )
    },
    "delete_comment": {
        "summary": "Delete a comment",
        "description": (
            "Deletes a comment by ID. "
            "Only the comment's author or an admin can delete it. "
            "Returns 404 if the comment is not found or access is denied."
        )
    },
    "get_comments": {
        "summary": "List comments for a photo",
        "description": (
            "Retrieves all comments associated with the specified photo. "
            "Available for all users, including unauthenticated visitors."
        )
    }
}

ratings_description = {
    "create_rating": {
        "summary": "Add a rating to a photo",
        "description": (
            "Allows an authenticated user to rate a specific photo. "
            "Each user can rate a photo only once. "
            "Returns the created rating object if successful."
        )
    },
    "get_ratings": {
        "summary": "Get all ratings for a photo",
        "description": (
            "Retrieves all ratings given to a specific photo by all users. "
            "This endpoint is public and does not require authentication."
        )
    },
    "delete_rating": {
        "summary": "Delete a rating",
        "description": (
            "Deletes a rating by its ID. "
            "Only the rating's author or an admin can remove it. "
            "Returns 404 if the rating is not found."
        )
    }
}

tags_description = {
    "get_tags": {
        "summary": "Get all tags",
        "description": (
            "Retrieves a list of all tags available in the system. "
            "Useful for displaying available categories or filters for photos. "
            "Does not require authentication."
        )
    }
}

search_description = {
    "search": {
        "summary": "Пошук фотографій за тегом, описом або рейтингом",
        "description": (
            "Цей ендпоінт дозволяє здійснювати пошук фотографій за ключовими словами "
            "в описі, тегом, а також сортувати результати за рейтингом або датою. "
            "Підтримується пагінація через параметри `limit` і `offset`."
        )
    }
}
