# from fastapi import APIRouter, Depends, Header
# from sqlalchemy.orm import Session
# from app.docs.descriptions import users_description
# from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
# from app.deps import require_role, get_current_user, oauth2_scheme
# from app.db.session import get_db
# from app.services.auth_service import AuthService 
# from app.models.user import User
# from fastapi.security import OAuth2PasswordRequestForm


# auth_service = AuthService()

# router = APIRouter(prefix="/api/users", tags=["Users"])


# @router.get("/me", response_model=UserResponse)
# async def get_me(current_user: User = Depends(get_current_user)):
#     return UserResponse.from_orm(current_user)


# @router.post(
#     "/signup",
#     response_model=UserResponse,
#     summary=users_description["signup"]["summary"],
#     description=users_description["signup"]["description"]
# )
# async def signup(user_in: UserCreate, db: Session = Depends(get_db)):
#     """Реєстрація нового користувача"""
#     return await auth_service.register_user(db=db, user_in=user_in)


# @router.post(
#     "/login",
#     summary=users_description["login"]["summary"],
#     description=users_description["login"]["description"]
# )
# async def login(user_in: UserLogin, db: Session = Depends(get_db)):
#     """Авторизація користувача"""
#     return await auth_service.login_user(db=db, user_in=user_in)


# @router.post("/token", response_model=Token)
# async def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     """
#     Swagger UI робить POST сюди через form-data (email + password)
#     Тепер response_model=Token
#     """
#     user_in = UserLogin(email=form_data.username, password=form_data.password)
#     return await auth_service.login_user(db=db, user_in=user_in)


# @router.post(
#     "/refresh_token",
#     summary=users_description["refresh_token"]["summary"],
#     description=users_description["refresh_token"]["description"]
# )
# # async def refresh(token: str):
# #     """Оновлення access токена"""
# #     return await auth_service.refresh_token(token)
# async def refresh(authorization: str = Header(..., description="Bearer token")):
#     token = authorization.split(" ")[1]
#     return await auth_service.refresh_token(token)

# @router.post(
#     "/request_mail",
#     summary=users_description["request_mail"]["summary"],
#     description=users_description["request_mail"]["description"]
# )
# async def send_mail_request(email: str):
#     """Надіслати лист для верифікації"""
#     return await auth_service.request_mail(email)


# @router.get(
#     "/request_mail/{token}",
#     summary=users_description["confirm_mail"]["summary"],
#     description=users_description["confirm_mail"]["description"]
# )
# # async def confirm_mail(token: str):
# #     """Підтвердити email через токен"""
# #     return await auth_service.verify_mail(db, token)
# async def confirm_mail(token: str, db: Session = Depends(get_db)):
#     return await auth_service.verify_mail(db, token)



# @router.get(
#     "/admin",
#     dependencies=[Depends(require_role("admin"))],
#     summary=users_description["admin"]["summary"],
#     description=users_description["admin"]["description"]
# )
# # async def get_admins():
# #     """Доступ лише для адміністраторів"""
# #     return {"message": "Admin access granted"}
# async def get_admins(current_user: User = Depends(get_current_user)):  # додаємо Depends
#     """Доступ лише для адміністраторів"""
#     return {"message": f"Admin access granted for {current_user.email}"}

# @router.get(
#     "/moderator",
#     dependencies=[Depends(require_role("moderator"))],
#     summary=users_description["moderator"]["summary"],
#     description=users_description["moderator"]["description"]
# )
# # async def get_moderators():
# #     """Доступ лише для модераторів"""
# #     return {"message": "Moderator access granted"}
# async def get_moderators(current_user: User = Depends(get_current_user)):  # додаємо Depends
#     """Доступ лише для модераторів"""
#     return {"message": f"Moderator access granted for {current_user.email}"}


# @router.post(
#     "/logout",
#     summary=users_description["logout"]["summary"],
#     description=users_description["logout"]["description"]
# )
# # async def logout(authorization: str = Header(...)):
# #     """Вихід користувача (деактивація токена)"""
# #     token = authorization.split(" ")[1]  # Bearer <token>
# #     return await auth_service.logout_user(token)
# async def logout(authorization: str = Header(..., description="Bearer token")):
#     """Вихід користувача (деактивація токена)"""
#     token = authorization.split(" ")[1]  # Bearer <token>
#     return await auth_service.logout_user(token)


from fastapi import APIRouter, Depends, File, Form, HTTPException, Path, UploadFile, status
from sqlalchemy.orm import Session

from src.conf import messages
from src.database.db import get_db
from src.database.models import User, Role
from src.repository import users as repository_users
from src.repository import profile as repository_profile
from src.services.auth import auth_service
from src.schemas import UpdateFullProfile, UpdateProfile, UserDb
from src.services.roles import RoleAccess
from src.services import cloudinary_avatar


router = APIRouter(prefix="/users", tags=["Users"])

allowed_operations_modify = RoleAccess([Role.admin])
allowed_operations_bans = RoleAccess([Role.admin])
allowed_operations_delete = RoleAccess([Role.admin])
allowed_operations_admin = RoleAccess([Role.admin])


@router.get("/me/", response_model=UserDb)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    Gets a current user.

    :param current_user: The current user.
    :type current_user: User
    :return: The current user.
    :rtype: UserDb
    """
    return current_user


# @router.get(
#     "/ban/{user_id}",
#     dependencies=[Depends(allowed_operations_bans)],
#     status_code=status.HTTP_200_OK,
#     response_description=messages.USER_ACCEPTED,
#     name="Ban user",
# )
# async def ban_user(
#     user_id: int,
#     owner: User = Depends(auth_service.get_current_user),
#     db: Session = Depends(get_db),
# ):
#     """Ban user by their ID, does not allow users to log in.  Allowed for roles: admin.

#     :param user_id: id of user
#     :type user_id: int
#     :param owner: _description_, defaults to Depends(auth_service.get_current_user)
#     :type owner: User, optional
#     :param db: _description_, defaults to Depends(get_db)
#     :type db: Session, optional
#     """

#     # if str(owner.role) != "Role.admin":
#     #     print(f"{str(owner.role)=}")
#     #     raise HTTPException(
#     #         status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.USER_INVALID_ROLE
#     #     )
#     if owner.id == user_id:  # type: ignore
#         raise HTTPException(
#             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             detail=messages.USER_CANT_OPERATE_HIMSELF,
#         )
#     user = await repository_users.update_active(user_id, active=False, db=db)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail=messages.USER_NOT_FOUND
#         )
#     return {"detail": messages.USER_ACCEPTED}


# @router.get(
#     "/unban/{user_id}",
#     dependencies=[Depends(allowed_operations_bans)],
#     status_code=status.HTTP_200_OK,
#     response_description=messages.USER_ACCEPTED,
#     name="UnBan user",
# )
# async def unban_user(
#     user_id: int,
#     owner: User = Depends(auth_service.get_current_user),
#     db: Session = Depends(get_db),
# ):
#     """Unban user by their ID, allow users to log in.  Allowed for roles: admin.

#     :param user_id: id of user
#     :type user_id: int
#     :param owner: _description_, defaults to Depends(auth_service.get_current_user)
#     :type owner: User, optional
#     :param db: _description_, defaults to Depends(get_db)
#     :type db: Session, optional
#     """
#     # if str(owner.role) != "Role.admin":
#     #     raise HTTPException(
#     #         status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.USER_INVALID_ROLE
#     #     )
#     if owner.id == user_id:  # type: ignore
#         raise HTTPException(
#             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             detail=messages.USER_CANT_OPERATE_HIMSELF,
#         )
#     user = await repository_users.update_active(user_id, active=True, db=db)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail=messages.USER_NOT_FOUND
#         )
#     return {"detail": messages.USER_ACCEPTED}


# @router.patch(
#     "/role/{user_id}",
#     dependencies=[Depends(allowed_operations_modify)],
#     status_code=status.HTTP_200_OK,
#     response_description=messages.USER_ACCEPTED,
#     name="Change role of user",
# )
# async def update_role_user(
#     user_id: int,
#     user_role: UserRole,
#     owner: User = Depends(auth_service.get_current_user),
#     db: Session = Depends(get_db),
# ):
#     """Unban user by their ID, allow users to log in..

#     :param user_id: id of user
#     :type user_id: int
#     :param owner: _description_, defaults to Depends(auth_service.get_current_user)
#     :type owner: User, optional
#     :param db: _description_, defaults to Depends(get_db)
#     :type db: Session, optional
#     """
#     # if str(owner.role) != "Role.admin":
#     #     raise HTTPException(
#     #         status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.USER_INVALID_ROLE
#     #     )
#     if owner.id == user_id:  # type: ignore
#         raise HTTPException(
#             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             detail=messages.USER_CANT_OPERATE_HIMSELF,
#         )
#     user = await repository_users.update_role_user(user_id, role=user_role.role, db=db)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail=messages.USER_NOT_FOUND
#         )
#     return {"detail": messages.USER_ACCEPTED}


@router.patch(
    "/{user_id}",
    dependencies=[Depends(allowed_operations_modify)],
    status_code=status.HTTP_200_OK,
    response_description=messages.USER_ACCEPTED,
    name="Change user's data",
)
async def update_user(
    data: UpdateFullProfile,
    user_id: int = Path(gt=0),
    owner: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """Update user data by their ID, Allowed only for Admin.

    :param user_id: id of user
    :type user_id: int
    :param owner: _description_, defaults to Depends(auth_service.get_current_user)
    :type owner: User, optional
    :param db: _description_, defaults to Depends(get_db)
    :type db: Session, optional
    """
    # if str(owner.role) != "Role.admin":
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.USER_INVALID_ROLE
    #     )
    if owner.id == user_id:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=messages.USER_CANT_OPERATE_HIMSELF,
        )
    data_dict = data.model_dump()
    if repository_users.dict_not_empty(data_dict):
        user = await repository_users.update_user(user_id, data=data_dict, db=db)
        if user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=messages.USER_NOT_FOUND
            )
        return {"detail": messages.USER_ACCEPTED}
    raise HTTPException(
        status_code=status.HTTP_304_NOT_MODIFIED, detail=messages.USER_NOT_CHANGED
    )


@router.patch(
    "/me/",
    status_code=status.HTTP_200_OK,
    response_description=messages.USER_ACCEPTED,
    name="Change user's data",
)
async def update_user_me(
    data: UpdateProfile,
    owner: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """Update current user data .

    :param user_id: id of user
    :type user_id: int
    :param owner: _description_, defaults to Depends(auth_service.get_current_user)
    :type owner: User, optional
    :param db: _description_, defaults to Depends(get_db)
    :type db: Session, optional
    """
    data_dict = data.model_dump()
    if repository_users.dict_not_empty(data_dict):
        data_dict["role"] = None
        data_dict["is_active"] = None
        user = await repository_users.update_user(owner.id, data=data_dict, db=db) # type: ignore
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=messages.USER_NOT_FOUND
            )
        return {"detail": messages.USER_ACCEPTED}
    raise HTTPException(
        status_code=status.HTTP_304_NOT_MODIFIED, detail=messages.USER_NOT_CHANGED
    )


@router.delete(
    "/{user_id}",
    dependencies=[Depends(allowed_operations_delete)],
    status_code=status.HTTP_200_OK,
    response_description=messages.USER_ACCEPTED,
    name="Delete user",
)
async def delete_user(
    user_id: int = Path(gt=0),
    owner: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """Delete user by their ID, with not active state.  Allowed for roles: admin.

    :param user_id: id of user
    :type user_id: int
    :param owner: _description_, defaults to Depends(auth_service.get_current_user)
    :type owner: User, optional
    :param db: _description_, defaults to Depends(get_db)
    :type db: Session, optional
    """
    if owner.id == user_id:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=messages.USER_CANT_OPERATE_HIMSELF,
        )
    user = await repository_users.delete_user(user_id, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.USER_NOT_FOUND
        )
    return {"detail": messages.USER_ACCEPTED}


@router.patch(
    "/{user_id}/avatar/",
    response_model=UserDb,
    dependencies=[Depends(allowed_operations_modify)],
)
async def update_avatar(
    user_id: int = Path(gt=0),
    file: UploadFile = File(description="Upload image file for user's avatar"),
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Updates user's avatar by their id. Allowed only for Admin.

    :param file: The image file of the avatar.
    :type file: UploadFile
    :param current_user: The current user.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: The User with a new avatar.
    :rtype: UserDb
    """
    target_user = await repository_users.get_user_by_id(id=user_id, db=db, active=None)
    if target_user:
        src_url = cloudinary_avatar.build_avatar_cloudinary_url(
            file, str(target_user.email)
        )
        user = await repository_users.update_avatar(target_user.email, src_url, db)  # type: ignore
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=messages.USER_NOT_FOUND
    )


@router.patch("/avatar/", response_model=UserDb)
async def update_avatar_me(
    file: UploadFile = File(description="Upload image file for your avatar"),
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Updates user's avatar.

    :param file: The image file of the avatar.
    :type file: UploadFile
    :param current_user: The current user.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: The User with a new avatar.
    :rtype: UserDb
    """
    src_url = cloudinary_avatar.build_avatar_cloudinary_url(
        file, str(current_user.email)
    )
    user = await repository_users.update_avatar(current_user.email, src_url, db)  # type: ignore
    return user


@router.get("/profile/", status_code=status.HTTP_200_OK)
async def read_profile(
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get profile of current user

    :param current_user: The current user.
    :type current_user: User
    :return: The current user.
    :rtype: dict
    """
    result = await repository_profile.read_profile(current_user, db)
    return result


@router.patch("/profile/", status_code=status.HTTP_200_OK)
async def update_profile(
    data: UpdateProfile,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get profile of current user

    :param current_user: The current user.
    :type current_user: User
    :return: The current user.
    :rtype: dict
    """
    updated = await repository_profile.update_profile(data, current_user, db)
    if updated:
        result = await repository_profile.read_profile(current_user, db)
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=messages.USER_NOT_FOUND
    )



@router.get("/{username}/profile/", status_code=status.HTTP_200_OK)
async def read_profile_user(
    username: str = Path(min_length=5, max_length=16),
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get profile of selected user by their username

    :param username: username of user.
    :type current_user: str
    :return: The current user.
    :rtype: dict
    """
    user = await repository_users.get_user_by_username(username, db)
    if user:
        result = await repository_profile.read_profile(user, db)
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=messages.USER_NOT_FOUND
    )

