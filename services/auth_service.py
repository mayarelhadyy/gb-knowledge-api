import jwt

from datetime import (
    datetime,
    timedelta,
    timezone
)

from pwdlib import PasswordHash

from services.database_service import get_connection


SECRET_KEY = "change-this-secret-key-later"
ALGORITHM = "HS256"

password_hash = PasswordHash.recommended()


def hash_password(password: str):
    return password_hash.hash(password)


def verify_password(
    password: str,
    hashed_password: str
):
    return password_hash.verify(
        password,
        hashed_password
    )


def create_user(
    email: str,
    password: str
):
    connection = get_connection()
    cursor = connection.cursor()

    hashed_password = hash_password(
        password
    )

    try:
        cursor.execute(
            """
            INSERT INTO users (
                email,
                hashed_password,
                role
            )
            VALUES (?, ?, ?)
            """,
            (
                email,
                hashed_password,
                "employee"
            )
        )

        connection.commit()

        user_id = cursor.lastrowid

    finally:
        connection.close()

    return user_id

def authenticate_user(
    email: str,
    password: str
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
    """
    SELECT id, email, hashed_password, role
    FROM users
    WHERE email = ?
    """,
    (email,)
)

    user = cursor.fetchone()

    connection.close()

    if not user:
        return None

    user_id, user_email, hashed_password, role = user

    if not verify_password(
        password,
        hashed_password
    ):
        return None

    return {
    "id": user_id,
    "email": user_email,
    "role": role
}


def create_access_token(
    user_id: int,
    role: str
):
    expiration = (
        datetime.now(timezone.utc)
        + timedelta(hours=8)
    )

    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": expiration
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token