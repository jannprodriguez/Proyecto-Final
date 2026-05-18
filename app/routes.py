from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.forms import TicketForm, ChangePasswordForm
from app.models import db, Ticket, User

# Blueprint principal que maneja el dashboard, gestión de cursos y cambio de contraseña
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """
    Página de inicio pública (home).
    """
    return render_template('index.html')

@main.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    """
    Permite al usuario autenticado cambiar su contraseña.
    """
    form = ChangePasswordForm()

    if form.validate_on_submit():
        # Verifica que la contraseña actual sea correcta
        if not current_user.check_password(form.old_password.data):
            flash('Current password is incorrect.')  # 🔁 Traducido
            return render_template('cambiar_password.html', form=form)

        # Actualiza la contraseña y guarda
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('✅ Password updated successfully.')  # 🔁 Traducido
        return redirect(url_for('main.dashboard'))

    return render_template('cambiar_password.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():

    if current_user.role.name == 'Admin':
        tickets = Ticket.query.all()

    elif current_user.role.name == 'Técnico':
        tickets = Ticket.query.all()

    else:
        tickets = Ticket.query.filter_by(usuario_id=current_user.id).all()

    return render_template('dashboard.html', tickets=tickets)

@main.route('/tickets', methods=['GET', 'POST'])
@login_required
def tickets():
    form = TicketForm()

    if form.validate_on_submit():
        ticket = Ticket(
            asunto=form.asunto.data,
            descripcion=form.descripcion.data,
            prioridad=form.prioridad.data,
            estado=form.estado.data,
            usuario_id=current_user.id
        )

        db.session.add(ticket)
        db.session.commit()

        flash("Ticket created successfully.")
        return redirect(url_for('main.dashboard'))

    return render_template('ticket_form.html', form=form)

@main.route('/tickets/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_ticket(id):

    ticket = Ticket.query.get_or_404(id)

    if current_user.role.name not in ['Admin', 'Técnico'] and ticket.usuario_id != current_user.id:
        flash('You do not have permission to edit this ticket.')
        return redirect(url_for('main.dashboard'))

    form = TicketForm(obj=ticket)

    if form.validate_on_submit():
        ticket.asunto = form.asunto.data
        ticket.descripcion = form.descripcion.data
        ticket.prioridad = form.prioridad.data
        ticket.estado = form.estado.data

        db.session.commit()

        flash("Ticket updated successfully.")
        return redirect(url_for('main.dashboard'))

    return render_template('ticket_form.html', form=form, editar=True)

@main.route('/tickets/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_ticket(id):
    ticket = Ticket.query.get_or_404(id)

    if current_user.role.name != 'Admin':
        flash('You do not have permission to delete this ticket.')
        return redirect(url_for('main.dashboard'))

    db.session.delete(ticket)
    db.session.commit()
    flash("Ticket deleted successfully.")
    return redirect(url_for('main.dashboard'))

@main.route('/usuarios')
@login_required
def listar_usuarios():
    if current_user.role.name != 'Admin':
        flash("You do not have permission to view this page.")
        return redirect(url_for('main.dashboard'))

    # Obtener instancias completas de usuarios con sus roles (no usar .add_columns)
    usuarios = User.query.join(User.role).all()

    return render_template('usuarios.html', usuarios=usuarios)

# API REST - Tickets

@main.route('/api/tickets', methods=['GET'])
def api_get_tickets():
    tickets = Ticket.query.all()

    return [{
        "id": ticket.id,
        "asunto": ticket.asunto,
        "descripcion": ticket.descripcion,
        "prioridad": ticket.prioridad,
        "estado": ticket.estado,
        "usuario_id": ticket.usuario_id,
        "tecnico_id": ticket.tecnico_id
    } for ticket in tickets]


@main.route('/api/tickets/<int:id>', methods=['GET'])
def api_get_ticket(id):
    ticket = Ticket.query.get_or_404(id)

    return {
        "id": ticket.id,
        "asunto": ticket.asunto,
        "descripcion": ticket.descripcion,
        "prioridad": ticket.prioridad,
        "estado": ticket.estado,
        "usuario_id": ticket.usuario_id,
        "tecnico_id": ticket.tecnico_id
    }


@main.route('/api/tickets', methods=['POST'])
def api_create_ticket():
    data = request.get_json()

    ticket = Ticket(
        asunto=data.get('asunto'),
        descripcion=data.get('descripcion'),
        prioridad=data.get('prioridad'),
        estado=data.get('estado'),
        usuario_id=data.get('usuario_id', 1),
        tecnico_id=data.get('tecnico_id')
    )

    db.session.add(ticket)
    db.session.commit()

    return {"message": "Ticket created successfully", "id": ticket.id}, 201


@main.route('/api/tickets/<int:id>', methods=['PUT'])
def api_update_ticket(id):
    ticket = Ticket.query.get_or_404(id)
    data = request.get_json()

    ticket.asunto = data.get('asunto', ticket.asunto)
    ticket.descripcion = data.get('descripcion', ticket.descripcion)
    ticket.prioridad = data.get('prioridad', ticket.prioridad)
    ticket.estado = data.get('estado', ticket.estado)
    ticket.tecnico_id = data.get('tecnico_id', ticket.tecnico_id)

    db.session.commit()

    return {"message": "Ticket updated successfully"}


@main.route('/api/tickets/<int:id>', methods=['DELETE'])
def api_delete_ticket(id):
    ticket = Ticket.query.get_or_404(id)

    db.session.delete(ticket)
    db.session.commit()

    return {"message": "Ticket deleted successfully"}