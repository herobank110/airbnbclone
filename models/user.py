#!/usr/bin/python3
"""user class, subclass of BaseModel
"""

from models.utils import BaseModel, Field


class User(BaseModel):
    '''representation of a customer'''

    email = Field("")
    password = Field("")
    first_name = Field("")
    last_name = Field("")
