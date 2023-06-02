from enum import Enum

from fastapi import FastAPI
import models
from config import engine
from pydantic import BaseModel

app = FastAPI()

