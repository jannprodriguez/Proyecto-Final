from flask import Blueprint, request, jsonify
from app.models import db, Ticket

# Blueprint solo con endpoints de prueba para tickets
main = Blueprint('main', __name__)


@main.route('/')
@main.route('/dashboard')
def index():
    """
    Página de inicio pública para modo de prueba.
    """
    return '<h1>Corriendo en Modo de Prueba - Sistema de Tickets</h1>'


@main.route('/api/tickets', methods=['GET'])
def listar_tickets():
    """
    Retorna una lista de tickets en formato JSON.
    """
    tickets = Ticket.query.all()

    data = [
        {
            'id': ticket.id,
            'asunto': ticket.asunto,
            'descripcion': ticket.descripcion,
            'prioridad': ticket.prioridad,
            'estado': ticket.estado,
            'usuario_id': ticket.usuario_id,
            'tecnico_id': ticket.tecnico_id
        }
        for ticket in tickets
    ]

    return jsonify(data), 200


@main.route('/api/tickets/<int:id>', methods=['GET'])
def listar_un_ticket(id):
    """
    Retorna un solo ticket por su ID en formato JSON.
    """
    ticket = Ticket.query.get_or_404(id)

    data = {
        'id': ticket.id,
        'asunto': ticket.asunto,
        'descripcion': ticket.descripcion,
        'prioridad': ticket.prioridad,
        'estado': ticket.estado,
        'usuario_id': ticket.usuario_id,
        'tecnico_id': ticket.tecnico_id
    }

    return jsonify(data), 200


@main.route('/api/tickets', methods=['POST'])
def crear_ticket():
    """
    Crea un ticket usando datos JSON.
    Espera JSON con asunto, descripcion, prioridad, estado y usuario_id.
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    ticket = Ticket(
        asunto=data.get('asunto'),
        descripcion=data.get('descripcion'),
        prioridad=data.get('prioridad'),
        estado=data.get('estado'),
        usuario_id=data.get('usuario_id'),
        tecnico_id=data.get('tecnico_id')
    )

    db.session.add(ticket)
    db.session.commit()

    return jsonify({
        'message': 'Ticket creado',
        'id': ticket.id,
        'usuario_id': ticket.usuario_id,
        'tecnico_id': ticket.tecnico_id
    }), 201


@main.route('/api/tickets/<int:id>', methods=['PUT'])
def actualizar_ticket(id):
    """
    Actualiza un ticket usando datos JSON.
    """
    ticket = Ticket.query.get_or_404(id)
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    ticket.asunto = data.get('asunto', ticket.asunto)
    ticket.descripcion = data.get('descripcion', ticket.descripcion)
    ticket.prioridad = data.get('prioridad', ticket.prioridad)
    ticket.estado = data.get('estado', ticket.estado)
    ticket.usuario_id = data.get('usuario_id', ticket.usuario_id)
    ticket.tecnico_id = data.get('tecnico_id', ticket.tecnico_id)

    db.session.commit()

    return jsonify({
        'message': 'Ticket actualizado',
        'id': ticket.id
    }), 200


@main.route('/api/tickets/<int:id>', methods=['DELETE'])
def eliminar_ticket(id):
    """
    Elimina un ticket por su ID.
    """
    ticket = Ticket.query.get_or_404(id)

    db.session.delete(ticket)
    db.session.commit()

    return jsonify({
        'message': 'Ticket eliminado',
        'id': id
    }), 200