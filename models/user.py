"""user class, subclass of BaseModel
"""

from models.utils import BaseModel, Field


class User(BaseModel):
    '''representation of a customer'''

    email = Field(str)
    password = Field(str)
    first_name = Field(str)
    last_name = Field(str)
