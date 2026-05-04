from app.core.security import hash_password, verify_password, create_access_token
from app.db.repositories.user_repo import UserRepository
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserUpdate


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def register(self, data: UserCreate) -> User:
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise ValueError("Email already registered")
        return await self.repo.create(
            email=data.email,
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
        )

    async def authenticate(self, email: str, password: str) -> Token:
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")
        if not user.is_active:
            raise ValueError("Account is disabled")
        return Token(access_token=create_access_token(subject=user.id))

    async def update(self, user: User, data: UserUpdate) -> User:
        updates: dict = {}
        if data.full_name is not None:
            updates["full_name"] = data.full_name
        if data.password is not None:
            updates["hashed_password"] = hash_password(data.password)
        return await self.repo.update(user, **updates)
