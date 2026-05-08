from flask import Blueprint

api_bp = Blueprint("api", __name__)

from . import health
from .departamento import *
from .empleado import *
from .linea import *
from .proceso import *
from .programacion import *
from .registro import *
from .rol import *
from .rol_ruta import *
from .ruta import *
from .usuario import *
from .usuario_rol import *