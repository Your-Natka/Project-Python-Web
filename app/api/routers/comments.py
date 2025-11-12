# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
# from app.crud import comment as crud_comment
# from app.deps import get_current_user
# from app.db.session import get_db
# from app.docs.descriptions import comments_description  # ✅ імпортуємо описи

# router = APIRouter(prefix="/api/comments", tags=["Comments"])

# @router.post(
#     "/photos/{photo_id}/comments/",
#     response_model=CommentResponse,
#     status_code=status.HTTP_201_CREATED,
#     summary=comments_description["create_comment"]["summary"],
#     description=comments_description["create_comment"]["description"]
# )
# async def create_comment(
#     photo_id: int,
#     comment_in: CommentCreate,
#     db: Session = Depends(get_db),
#     current_user=Depends(get_current_user)
# ):
#     comment_in.photo_id = photo_id
#     comment = await crud_comment.create_comment(db, comment_in, user_id=current_user.user_id)
#     if not comment:
#         raise HTTPException(status_code=400, detail="Unable to create comment")
#     return comment


# @router.put(
#     "/comments/{comment_id}/",
#     response_model=CommentResponse,
#     summary=comments_description["update_comment"]["summary"],
#     description=comments_description["update_comment"]["description"]
# )
# async def update_comment(
#     comment_id: int,
#     comment_in: CommentUpdate,
#     db: Session = Depends(get_db),
#     current_user=Depends(get_current_user)
# ):
#     comment = await crud_comment.update_comment(db, comment_id, comment_in, current_user.user_id)
#     if not comment:
#         raise HTTPException(status_code=404, detail="Comment not found or no permission")
#     return comment


# @router.delete(
#     "/comments/{comment_id}/",
#     status_code=status.HTTP_204_NO_CONTENT,
#     summary=comments_description["delete_comment"]["summary"],
#     description=comments_description["delete_comment"]["description"]
# )
# async def delete_comment(
#     comment_id: int,
#     db: Session = Depends(get_db),
#     current_user=Depends(get_current_user)
# ):
#     success = await crud_comment.delete_comment(db, comment_id, current_user.user_id)
#     if not success:
#         raise HTTPException(status_code=404, detail="Comment not found or no permission")
#     return {"detail": "Comment deleted"}


# @router.get(
#     "/photos/{photo_id}/comments/",
#     response_model=list[CommentResponse],
#     summary=comments_description["get_comments"]["summary"],
#     description=comments_description["get_comments"]["description"]
# )
# async def get_comments(photo_id: int, db: Session = Depends(get_db)):
#     return await crud_comment.get_comments_by_photo(db, photo_id)

from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.orm import Session

from fastapi_limiter.depends import RateLimiter

from src.database.db import get_db
from src.database.models import User, Role
from src.services.auth import auth_service
from src.schemas import CommentBase, CommentResponse
from src.repository import comments as repository_comments
from src.conf import messages
from src.services.roles import RoleAccess


router = APIRouter(prefix="/comments/{image_id}", tags=["Comments by picture"])


allowed_operation_get = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_post = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_patch = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_delete = RoleAccess([Role.admin, Role.moderator])


@router.get(
    "/",
    response_model=List[CommentResponse],
    name="Show comments",
    description="No more than 10 requests per minute",
    dependencies=[Depends(allowed_operation_get), Depends(RateLimiter(times=10, seconds=60))],
)
async def get_comments(
    image_id: int = Path(ge=1),
    limit: int = Query(5, le=100),
    offset: int = 0,
    owner: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    The get_comments function returns a list of comments for the image with the given id.
    The limit and offset parameters are used to paginate through all comments.

    :param image_id: int: Get the image id from the url
    :param limit: int: Limit the number of comments that are returned
    :param offset: int: Get the next set of comments
    :param owner: User: Get the current user
    :param db: Session: Pass the database session to the repository_comments
    :return: A list of comments for a given image
    """
    image = await repository_comments.get_image_by_id(image_id, db)

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.IMAGE_NOT_FOUND)
    
    return await repository_comments.get_comments(image_id, limit, offset, db)


@router.get(
    "/{comment_id}",
    response_model=CommentResponse,
    name="Show comment by id",
    description="No more than 10 requests per minute",
    dependencies=[Depends(allowed_operation_get), Depends(RateLimiter(times=10, seconds=60))],
)
async def get_comment(
    image_id: int = Path(ge=1),
    comment_id: int = Path(ge=1),
    owner: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    The get_comment function returns a comment by its id.

    :param image_id: int: Get the image id from the url
    :param comment_id: int: Get the comment id from the url
    :param owner: User: Check if the user is logged in
    :param db: Session: Pass the database session to the repository layer
    :return: A comment object
    """
    image = await repository_comments.get_image_by_id(image_id, db)

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.IMAGE_NOT_FOUND)
    
    comment = await repository_comments.get_comment_by_id(image_id, comment_id, db)

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.COMMENT_NOT_FOUND
        )

    return comment


@router.post(
    "/",
    response_model=CommentResponse,
    # description="No more than 10 requests per minute",
    # dependencies=[Depends(RateLimiter(times=10, seconds=30))],
    name="Create comment",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(allowed_operation_post)],
)
async def create_comment(
    body: CommentBase,
    image_id: int = Path(ge=1),
    owner: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    The create_comment function creates a new comment in the database.
        The function takes an image_id and a body as input, and returns the created comment.


    :param body: CommentBase: Get the data from the request body
    :param image_id: int: Get the image id from the path
    :param owner: User: Get the current user
    :param db: Session: Pass the database session to the repository layer
    :return: A commentbase object
    """
    image = await repository_comments.get_image_by_id(image_id, db)

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.IMAGE_NOT_FOUND)
    
    comment = await repository_comments.create_comment(body, image_id, owner, db)
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.COMMENT_NOT_CREATED
        )
    return comment


@router.patch(
    "/{comment_id}",
    response_model=CommentResponse,
    # description="No more than 10 requests per minute",
    # dependencies=[Depends(RateLimiter(times=10, seconds=30))],
    name="Change comment",
    dependencies=[Depends(allowed_operation_patch)],
)
async def update_comment(
    body: CommentBase,
    image_id: int = Path(ge=1),
    comment_id: int = Path(ge=1),
    owner: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    The update_comment function updates a comment in the database.

    :param body: CommentBase: Pass the data of the comment that will be updated
    :param image_id: int: Get the image id from the url
    :param comment_id: int: Identify the comment that is to be updated
    :param owner: User: Get the current user
    :param db: Session: Get the database session
    :return: A comment
    """
    image = await repository_comments.get_image_by_id(image_id, db)

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.IMAGE_NOT_FOUND)
    
    comment = await repository_comments.update_comment(
        image_id, comment_id, body, owner, db
    )

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.COMMENT_NOT_FOUND
        )

    return comment


@router.delete(
    "/{comment_id}",
    response_model=CommentResponse,
    # description="No more than 10 requests per minute",
    # dependencies=[Depends(RateLimiter(times=10, seconds=30))],
    name="Remove comment",
    dependencies=[Depends(allowed_operation_delete)],
)
async def remove_comment(
    image_id: int = Path(ge=1),
    comment_id: int = Path(ge=1),
    owner: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    The remove_comment function removes a comment from an image.
        Allowed for roles: admin and moderator.

    :param image_id: int: Get the image id from the url
    :param comment_id: int: Identify which comment to remove
    :param owner: User: Get the current user and check if they are authorized to delete the comment
    :param db: Session: Pass the database session to the repository layer
    :return: A comment object
    """
    image = await repository_comments.get_image_by_id(image_id, db)

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.IMAGE_NOT_FOUND)
    
    comment = await repository_comments.remove_comment(image_id, comment_id, owner, db)

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.COMMENT_NOT_FOUND
        )

    return comment