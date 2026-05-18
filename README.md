# Sistema de Gestión de Tickets

## Descripción
Este proyecto es un sistema web de gestión de tickets desarrollado con Flask y MySQL.  
El sistema permite a los usuarios registrarse, iniciar sesión, crear tickets de soporte, editar tickets, eliminar tickets y administrar información dependiendo del rol del usuario.

La aplicación incluye autenticación, manejo de roles, operaciones CRUD, endpoints REST API e integración con base de datos MySQL.

---

# Tecnologías Utilizadas

- Python
- Flask
- Flask-Login
- Flask-WTF
- SQLAlchemy
- MySQL
- HTML
- Bootstrap 5
- Jinja2
- REST Client (.rest)

---

# Funcionalidades

## Autenticación
- Registro de usuarios
- Inicio de sesión
- Cierre de sesión
- Cambio de contraseña

## Roles
- Admin
- Usuario
- Técnico

## Gestión de Tickets
- Crear tickets
- Ver tickets
- Editar tickets
- Eliminar tickets

## REST API
El proyecto incluye endpoints REST API para operaciones CRUD:

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/tickets` | Obtener todos los tickets |
| GET | `/api/tickets/<id>` | Obtener un ticket por ID |
| POST | `/api/tickets` | Crear un nuevo ticket |
| PUT | `/api/tickets/<id>` | Actualizar un ticket |
| DELETE | `/api/tickets/<id>` | Eliminar un ticket |

---

# Base de Datos

Nombre de la base de datos:

```sql
seguimiento_tickets
```

Tablas principales:
- role
- user
- ticket

---

# Instalación

## 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
```

---

## 2. Abrir la carpeta del proyecto

```bash
cd final_project
```

---

## 3. Crear entorno virtual

```bash
python -m venv venv
```

Activar entorno virtual:

### Windows
```bash
venv\Scripts\activate
```

---

## 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 5. Configurar MySQL

Crear la base de datos:

```sql
CREATE DATABASE seguimiento_tickets;
```

Importar el archivo SQL desde:

```text
database_schema/
```

---

## 6. Ejecutar la aplicación

```bash
py run.py
```

El servidor correrá en:

```text
http://127.0.0.1:5000
```

---

# Pruebas REST API

Las pruebas CRUD REST API fueron realizadas utilizando archivos `.rest` dentro de:

```text
pruebas/
```

Archivos utilizados:
- create.rest
- read.rest
- read-a-row.rest
- update.rest
- delete.rest

---

# Capturas de Pantalla

El proyecto incluye capturas de:
- Login
- Registro
- Dashboard
- Crear ticket
- Editar ticket
- Eliminar ticket
- Pruebas REST API

---

# Autor

Jann P Rodriguez Santiago

---

# Conclusión

Este proyecto demuestra el desarrollo de una aplicación web completa utilizando Flask y MySQL, incluyendo autenticación, manejo de roles, operaciones CRUD, integración REST API y administración de base de datos.