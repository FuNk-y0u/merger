from flask             import *
from flask_cors        import CORS
from flask_sqlalchemy  import SQLAlchemy
from flask_login       import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from datetime  import datetime, timedelta
from dotenv    import load_dotenv
from functools import wraps
from io        import StringIO
from pprint    import pprint

from bs4         import BeautifulSoup
from qbittorrent import Client

import hashlib
import bencode
import uuid
import jwt
import secrets
import requests

import sys
import json
import time
import dataclasses
import os

