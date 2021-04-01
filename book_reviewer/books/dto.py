from pydantic import BaseModel, Field
from typing import Optional


class CreateReviewDto(BaseModel):
    title: str = Field(min_length=5, max_length=50)
    review_text: str = Field(max_length=500)
    category: Optional[str] = Field(max_length=50)
