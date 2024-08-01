from langchain_core.pydantic_v1 import BaseModel, Field


class DialogContext(BaseModel):
    """Create a unique dialog context between two characters."""
    context: str = Field(description="Unique dialog's context. Describe briefly the situation.")
    user: str = Field(description="User's role in the dialog.")
    ai: str = Field(description="AI's role in the dialog.")

class GenderClassifier(BaseModel):
    """Find the role's gender. Return 0 for female, 1 otherwise."""
    gender:int = Field(description="0 or 1")

class EnglishBinaryClassifier(BaseModel):
    """Result of the binary classifier. If an error (grammar, English verbs, vocabulary) is found in the user's response, return_value must be 1, otherwise 0. You must ignore spaces, punctuation or capitalization errors)."""
    return_value: int = Field(description="1 or 0. 1 if an english error is found, 0 otherwise. You must ignore spaces, punctuation or capitalization errors.")

class EnglishCorrector(BaseModel):
    """Correct the user's sentence."""
    corrected_sentence: str = Field(description="Corrected sentence.")
    why: str = Field(description="Explanation of the correction.")
