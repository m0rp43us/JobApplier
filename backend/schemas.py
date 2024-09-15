from pydantic import BaseModel

class UserLogin(BaseModel):
    email: str
    password: str

class JobSearchQuery(BaseModel):
    search_term: str
    location: str
