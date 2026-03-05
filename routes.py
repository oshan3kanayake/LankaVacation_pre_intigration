{% extends "base.html" %}
{% block title %}Ticket #{{ ticket.id }}{% endblock %}

{% block head %}
{{ super() }}
<style>
  .message-card {
    background: var(--cream);
    border-left: 4px solid var(--green);
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1rem;
  }
  .reply-card {
    background: white;
    border-left: 4px solid var(--orange);
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1rem;
  }
  .meta {
    font-size: 0.85rem;
    color: var(--gray);
  }
  .status-badge {
    display: inline-block;
    padding: 0.3rem 1rem;
    border-radius: 50px;
    font-size: 0.8rem;
    font-weight: 600;
  }
  .status-open { background: #fff3e0; color: var(--orange); }
  .status-closed { background: #e8f5e9; color: var(--green); }
  .status-resolved { background: #e3f2fd; color: #1976d2; }
  .btn-back {
    background: transparent;
    border: 2px solid var(--green);
    color: var(--green);
    padding: 0.5rem 1.5rem;
    border-radius: 40px;
    font-weight: 600;
    transition: all 0.3s ease;
    text-decoration: none;
    display: inline-block;
  }
  .btn-back:hover {
    background: var(--green);
    color: white;
  }
</style>
{% endblock %}

{% block body %}
<div class="container py-5">
  <div class="d-flex justify-content-between align-items-center mb-4">
    <h2 style="color: var(--green); font-family: 'Playfair Display', serif;">Ticket #{{ ticket.id }}: {{ ticket.subject }}</h2>
    <span class="status-badge status-{{ ticket.status }}">{{ ticket.status|upper }}</span>
  </div>

  <div class="message-card">
    <div class="d-flex justify-content-between">
      <strong>You ({{ ticket.user.name }})</strong>
      <span class="meta">{{ ticket.created_at.strftime('%d %b %Y, %H:%M') }}</span>
    </div>
    <p class="mt-2">{{ ticket.message }}</p>
  </div>

  {% for reply in ticket.replies %}
  <div class="reply-card">
    <div class="d-flex justify-content-between">
      <strong>Support Team</strong>
      <span class="meta">{{ reply.created_at.strftime('%d %b %Y, %H:%M') }}</span>
    </div>
    <p class="mt-2">{{ reply.reply }}</p>
  </div>
  {% else %}
  <p class="text-muted">No replies yet.</p>
  {% endfor %}

  <div class="mt-4">
    <a href="{{ url_for('tickets.my_tickets') }}" class="btn-back">← Back to My Tickets</a>
  </div>
</div>
{% endblock %}