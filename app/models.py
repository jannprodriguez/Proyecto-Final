from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Carga un usuario desde su ID, necesario para el sistema de sesiones de Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Role(db.Model):
    __tablename__ = 'role'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    # Relación inversa opcional (para ver usuarios asociados al rol)
    users = db.relationship('User', backref='role', lazy=True)

# Modelo de usuarios del sistema
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)  # Asegura suficiente espacio para el hash
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    
    tickets_creados = db.relationship(
        'Ticket',
        foreign_keys='Ticket.usuario_id',
        backref='usuario',
        lazy=True,
    )

    tickets_asignados = db.relationship(
        'Ticket',
        foreign_keys='Ticket.tecnico_id',
        backref='tecnico',
        lazy=True,
    )

    def set_password(self, password: str):
        """
        Genera y guarda el hash de la contraseña.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Verifica si la contraseña ingresada es válida comparando con el hash.
        """
        return check_password_hash(self.password_hash, password)

# Modelo de tickets
class Ticket(db.Model):
    __tablename__ = 'ticket'

    id = db.Column(db.Integer, primary_key=True)

    asunto = db.Column(db.String(150), nullable=False)

    descripcion = db.Column(db.Text, nullable=False)

    prioridad = db.Column(
        db.Enum('Baja', 'Media', 'Alta'),
        nullable=False
    )

    estado = db.Column(
        db.Enum('Abierto', 'En proceso', 'Cerrado'),
        nullable=False,
        default='Abierto'
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    tecnico_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=True
    )

    fecha_creacion = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )
