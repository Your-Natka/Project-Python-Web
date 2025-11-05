# Project-Python-Web

📁 Структура проєкту PhotoShare
app/
├── main.py
├── core/
│   ├── config.py
│   └── security.py
├── crud/
│   ├── user.py
├── db/
│   ├── base.py
│   └── session.py
├── models/
│   ├── user.py
│   ├── photo.py
│   ├── tag.py
│   ├── comment.py
│   ├── rating.py
│   └── transformed_link.py
├── api/
│   ├── auth.py
│   ├── users.py
│   ├── photos.py
│   ├── comments.py
│   ├── ratings.py
│   └── tags.py
├── services/
│   ├── cloudinary_service.py
│   ├── qr_service.py
│   ├── rating_service.py
│   └── user_service.py
├── deps/
│   └── auth_deps.py
├── schemas/
│   ├── user.py
│   ├── photo.py
│   ├── tag.py
│   ├── comment.py
│   └── rating.py
├── tests/
│   ├── test_auth.py
│   ├── test_users.py
│   ├── test_photos.py
│   ├── test_comments.py
│   └── test_ratings.py
└── utils/
    └── slugify.py

🔹 Файли по модулях
app/main.py

Головна точка входу застосунку FastAPI.

Імпортує FastAPI

Створює app = FastAPI()

Підключає маршрути (include_router із api/)

Підключає базу даних (middleware)

Конфігурація CORS

Створює /health endpoint

Swagger доступний за /docs

app/core/config.py

Конфігурація застосунку.

Читає змінні середовища (os.getenv, pydantic.BaseSettings)

Містить:

DATABASE_URL

REDIS_URL

CLOUDINARY_URL

SECRET_KEY

ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES

Створює клас Settings (через pydantic.BaseSettings)

Експортує об’єкт settings

app/core/security.py

Безпека: JWT, хешування паролів, blacklist токенів.

Хешування пароля через passlib.context.CryptContext

Генерація JWT (python-jose)

Перевірка/декодування токена

Функції:

create_access_token(data, expires_delta)

verify_password(plain, hashed)

get_password_hash(password)

is_token_blacklisted(jti) — перевірка через Redis

app/db/session.py

Ініціалізація бази даних.

Async engine SQLAlchemy (create_async_engine)

AsyncSession (sessionmaker)

Функція get_db() для залежностей FastAPI

app/db/base.py

Імпортує всі моделі для Alembic.

from app.models.user import User

from app.models.photo import Photo

...

Base = declarative_base()

🧱 Моделі SQLAlchemy (ORM)
app/models/user.py

Модель користувача.

Таблиця users

Поля:

id, username, email, full_name

password_hash, role, is_active

created_at

Ролі (Enum): user, moderator, admin

Відношення:

photos, comments, ratings

app/models/photo.py

Модель світлини.

Таблиця photos

Поля:

id, owner_id, cloudinary_public_id, original_url

description, unique_slug, created_at, updated_at

Відношення:

owner → User

tags → many-to-many

comments, ratings, transformed_links

app/models/tag.py

Модель тегів.

Таблиця tags

Поля: id, name (унікальний)

Відношення many-to-many до photos через photo_tags

app/models/comment.py

Коментарі під світлинами.

Поля:

id, photo_id, author_id, text

created_at, updated_at

Відношення: photo, author

app/models/rating.py

Рейтинг світлин.

Поля:

id, photo_id, user_id, score, created_at

Обмеження: UniqueConstraint(photo_id, user_id)

app/models/transformed_link.py

Посилання на трансформовані зображення + QR.

Поля:

id, photo_id, transformation_params, url, qr_code_url

created_by, created_at

🧩 Схеми Pydantic
app/schemas/user.py

DTO: UserCreate, UserLogin, UserOut, UserUpdate

Валідація пароля, email

app/schemas/photo.py

DTO: PhotoCreate, PhotoOut, PhotoUpdate

Валідація тегів (max 5)

Поля з Cloudinary URL, description, slug

app/schemas/comment.py

DTO: CommentCreate, CommentOut, CommentUpdate

app/schemas/rating.py

DTO: RatingCreate, RatingOut

app/schemas/tag.py

DTO: TagCreate, TagOut

🔐 Авторизація
app/deps/auth_deps.py

Функції залежностей FastAPI:

get_current_user(): декодує JWT

require_role("moderator"): обмеження доступу

Використовується у всіх @router ендпоінтах

🌐 API-модулі
app/api/auth.py

Реєстрація, логін, токени, logout.

POST /auth/register

POST /auth/token (отримати JWT)

POST /auth/logout (додати токен у blacklist)

Перший користувач → автоматично admin

app/api/users.py

Робота з профілем.

GET /users/me — дані поточного користувача

PUT /users/me — редагування себе

GET /users/{username} — публічний профіль

PATCH /users/{id}/deactivate — тільки admin

app/api/photos.py

CRUD для світлин.

POST /photos/ — завантажити світлину (Cloudinary)

GET /photos/{slug} — отримати світлину

PUT /photos/{id} — редагувати опис

DELETE /photos/{id} — видалити

POST /photos/{id}/transform — створити трансформовану версію + QR

GET /photos/search — пошук і фільтрація

app/api/comments.py

Коментарі.

POST /photos/{photo_id}/comments

PUT /comments/{id} — редагувати свій

DELETE /comments/{id} — видалити (admin/mod)

app/api/ratings.py

Рейтинги.

POST /photos/{photo_id}/rating

GET /photos/{photo_id}/rating

DELETE /ratings/{id} — admin/mod

app/api/tags.py

Перегляд усіх тегів, фільтрація.

GET /tags/

GET /tags/{name}/photos

⚙️ Services
app/services/cloudinary_service.py

Інтеграція з Cloudinary API.

upload_image(file) → URL + public_id

create_transformed_url(public_id, params)

delete_image(public_id)

app/services/qr_service.py

Генерація QR-кодів.

generate_qr_code(url) → повертає шлях до PNG або bytes

Зберігає QR у Cloudinary / локально

app/services/rating_service.py

Логіка підрахунку середнього рейтингу.

get_average_rating(photo_id)

user_already_rated(photo_id, user_id)

app/services/user_service.py

Адмін-функції для користувачів.

deactivate_user(user_id)

get_user_profile(username)

get_user_stats(user_id) (кількість фото, рейтинг тощо)

🧩 Утиліти
app/utils/slugify.py

Генерує унікальні URL-slugs для фото.

Наприклад: "My Cat Photo" → "my-cat-photo-uuid"

🧪 Тести
app/tests/test_auth.py

Тестує реєстрацію, логін, токени, logout.

app/tests/test_users.py

Тестує профіль користувача, оновлення, деактивацію.

app/tests/test_photos.py

Тестує завантаження, редагування, видалення, Cloudinary mock.

app/tests/test_comments.py

Тестує створення, редагування, видалення коментарів, права доступу.

app/tests/test_ratings.py

Тестує виставлення рейтингу, обмеження “1 раз на користувача”, середнє значення.

Як запустити додаток:
Створюємо віртуальне середовище.

python3 -m venv .venv source .venv/bin/activate # для Linux / Mac

або
.venv\Scripts\activate # для Windows PowerShell

Встановлюємо бібліотеки pip install -r requirements.txt

Запусти контейнер
docker-compose down --- для перезапуску видаляємо старі контейнера docker-compose up -d --build docker ps

docker-compose logs -f web

Коли попрацювали і зробили якісь зміни і нам треба зробити PR то ми виконуємо крок покрокові:

git add .
git commit -m '...(Тут буде назва вашого коментаря)'
git push
git push origin (назва вашої гілки)
Переходимо на гілку девелопер git checkout developer
git merge --no-ff (назва вашої гілки) -m '...(Короткий опис PR)'
git push origin developer
Виходимо віртуального середовища за допомогою команди: deactivate