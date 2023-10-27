from flask             import *
from flask_cors        import CORS
from flask_sqlalchemy  import SQLAlchemy
from flask_login       import UserMixin

from dotenv    import load_dotenv
from io        import StringIO

from qbittorrent import Client
from bs4         import BeautifulSoup
from bs4.element import Tag
from ftplib      import FTP
from tqdm        import tqdm

import hashlib
import bencode
import requests

import os
import json
import dataclasses
import time
import threading
