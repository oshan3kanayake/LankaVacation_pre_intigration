{% extends "base.html" %}
{% block title %}My Tickets{% endblock %}

{% block head %}
{{ super() }}
<style>
    .page-header {
        background: linear-gradient(135deg, var(--green), #1e3f1f);
        color: white;
        padding: 3rem 0 2rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .page-header h1 {
        font-size: 2.5rem;
        font-family: 'Playfair Display', serif;
        font-weight: 700;
    }
    .tickets-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
        gap: 1.5rem;
        margin-bottom: 3rem;
    }
    .ticket-card {
        background: white;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        overflow: hidden;
        border: 1px solid rgba(0,0,0,0.05);
        display: flex;
        flex-direction: column;
        height: 100%;
        position: relative;
    }
    .ticket-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 20px 40px rgba(44, 95, 45, 0.15);
    }
    .ticket-header {
        background: linear-gradient(135deg, var(--green), #1e3f1f);
        color: white;
        padding: 1.2rem 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .ticket-header h3 {
        margin: 0;
        font-size: 1.2rem;
        font-weight: 600;
        flex: 1;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        padding-right: 1rem;
    }
    .status-badge {
        padding: 0.4rem 1.2rem;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        background: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .status-open {
        color: var(--orange);
        border: 1px solid var(--orange);
    }
    .status-closed {
        color: var(--green);
        border: 1px solid var(--green);
    }
    .status-resolved {
        color: #1976d2;
        border: 1px solid #1976d2;
    }
    .ticket-body {
        padding: 1.5rem;
        flex: 1;
    }
    .ticket-message {
        color: var(--gray);
        margin-bottom: 1.5rem;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    .ticket-meta {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        font-size: 0.85rem;
        color: #888;
        border-top: 1px solid #eee;
        padding-top: 1rem;
    }
    .ticket-meta-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .ticket-meta-item i {
        color: var(--green);
        width: 18px;
        font-size: 1rem;
    }
    .ticket-footer {
        background: #f8f9fa;
        padding: 1rem 1.5rem;
        display: flex;
        justify-content: flex-end;
        gap: 0.75rem;
        border-top: 1px solid #eee;
    }
    .btn-action {
        padding: 0.5rem 1.5rem;
        border-radius: 40px;
        font-weight: 600;
        font-size: 0.85rem;
        transition: all 0.2s ease;
        border: none;
        cursor: pointer;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }
    .btn-view {
        background: var(--green);
        color: white;
    }
    .btn-view:hover {
        background: #1e4f1f;
        transform: translateY(-2px);
        color: white;
    }
    .btn-edit {
        background: var(--orange);
        color: white;
    }
    .btn-edit:hover {
        background: #e67e22;
        transform: translateY(-2px);
    }
    .btn-delete {
        background: #dc3545;
        color: white;
    }
    .btn-delete:hover {
        background: #b02a37;
        transform: translateY(-2px);
    }
    .create-button {
        background: var(--green);
        border: none;
        border-radius: 50px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        color: white;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }
    .create-button:hover {
        background: var(--orange);
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(44, 95, 45, 0.3);
    }
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        background: var(--cream);
        border-radius: 30px;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    .empty-state h3 {
        color: var(--green);
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    .empty-state p {
        color: var(--gray);
        margin-bottom: 2rem;
    }
    .empty-icon {
        font-size: 4rem;
        color: var(--orange);
        margin-bottom: 1.5rem;
        opacity: 0.5;
    }
    @media (max-width: 768px) {
        .tickets-grid {
            grid-template-columns: 1fr;
        }
        .ticket-header {
            flex-direction: column;
            align-items: flex-start;
            gap: 0.5rem;
        }
        .ticket-header h3 {
            white-space: normal;
        }
    }
</style>
{% endblock %}

{% block body %}
<div class="page-header">
    <div class="container">
        <h1 data-aos="fade-up">My Support Tickets</h1>
        <p class="lead" data-aos="fade-up" data-aos-delay="100">Track and manage your requests</p>
    </div>
</div>

<div class="container py-4">
    <div class="row mb-5">
        <div class="col-12 d-flex justify-content-end">
            <a href="{{ url_for('tickets.create_ticket') }}" class="create-button">
                <i class="bi bi-plus-circle"></i> Create New Ticket
            </a>
        </div>
    </div>

    {% if tickets %}
    <div class="tickets-grid">
        {% for ticket in tickets %}
        <div class="ticket-card" data-aos="fade-up" data-aos-delay="{{ loop.index * 50 }}">
            <div class="ticket-header">
                <h3>{{ ticket.subject }}</h3>
                <span class="status-badge
                        {% if ticket.status == 'open' %}status-open
                        {% elif ticket.status == 'closed' %}status-closed
                        {% else %}status-resolved{% endif %}">
                        {{ ticket.status }}
                    </span>
            </div>
            <div class="ticket-body">
                <div class="ticket-message">
                    {{ ticket.message[:150] }}{% if ticket.message|length > 150 %}...{% endif %}
                </div>
                <div class="ticket-meta">
                    <div class="ticket-meta-item">
                        <i class="bi bi-calendar3"></i>
                        <span>Created: {{ ticket.created_at.strftime('%d %b %Y, %H:%M') }}</span>
                    </div>
                    {% if ticket.updated_at and ticket.updated_at != ticket.created_at %}
                    <div class="ticket-meta-item">
                        <i class="bi bi-pencil-square"></i>
                        <span>Updated: {{ ticket.updated_at.strftime('%d %b %Y, %H:%M') }}</span>
                    </div>
                    {% endif %}
                    <div class="ticket-meta-item">
                        <i class="bi bi-chat-dots"></i>
                        <span>{{ ticket.replies|length }} reply(ies)</span>
                    </div>
                </div>
            </div>
            <div class="ticket-footer">
                <a href="{{ url_for('tickets.ticket_detail', ticket_id=ticket.id) }}" class="btn-action btn-view">
                    <i class="bi bi-eye"></i> View
                </a>
                <a href="{{ url_for('tickets.edit_ticket', ticket_id=ticket.id) }}" class="btn-action btn-edit">
                    <i class="bi bi-pencil"></i> Edit
                </a>
                <form method="POST" action="{{ url_for('tickets.delete_ticket', ticket_id=ticket.id) }}" style="display: inline;" onsubmit="return confirm('Delete this ticket? This action cannot be undone.');">
                    <button type="submit" class="btn-action btn-delete">
                        <i class="bi bi-trash"></i> Delete
                    </button>
                </form>
            </div>
        </div>
        {% endfor %}
    </div>
    {% else %}
    <div class="empty-state" data-aos="fade-up">
        <div class="empty-icon">
            <i class="bi bi-ticket"></i>
        </div>
        <h3>No Tickets Yet</h3>
        <p>You haven't created any support tickets. Need help? Create one now!</p>
        <a href="{{ url_for('tickets.create_ticket') }}" class="create-button">
            <i class="bi bi-plus-circle"></i> Create Your First Ticket
        </a>
    </div>
    {% endif %}
</div>
{% endblock %}