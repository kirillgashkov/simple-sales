from datetime import datetime
from uuid import UUID

import argon2
from asyncpg import Connection
from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from simple_sales.api.dependencies.argon2 import get_password_hasher
from simple_sales.api.dependencies.db import get_db
from simple_sales.db.models import User, Session
from simple_sales.db.queries.sessions import select_session
from simple_sales.db.queries.users import select_user, update_user
from simple_sales.settings import API_SESSION_ID_COOKIE_NAME
