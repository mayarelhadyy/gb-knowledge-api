from pydantic import BaseModel, Field


class Document(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    department: str = Field(min_length=2, max_length=50)
    year: int = Field(ge=2020, le=2030)


class SearchRequest(BaseModel):
    question: str = Field(
        min_length=2,
        max_length=500
    )

class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=2,
        max_length=500
    )

    conversation_id: str | None = None

class RegisterRequest(BaseModel):
    email: str = Field(
        ...,
        min_length=5,
        max_length=100
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=100
    )


class LoginRequest(BaseModel):
    email: str
    password: str

