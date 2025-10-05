HelpDesk Mini — Submission README

This README is a concise guide for recruiters / hackathon judges to quickly evaluate the HelpDesk Mini project. It contains the submission checklist, API summary with sample requests and credentials, seed data, notes on pagination/idempotency/rate limits, and a short architecture note.

## Submission Checklist

- Ensure these endpoints are live & return correct JSON:
  - GET /api/health/ → { "status": "ok" }
  - GET /api/\_meta/ → project metadata (name, version, author, status)
  - GET /.well-known/hackathon.json → hackathon metadata (should be present at this path)
- API list + sample requests, credentials and seed data are documented below.
- Notes on pagination, idempotency, and rate limits are documented below.
- Short architecture note included (100–200 words).

---

## Quick Project Summary

A role-based Helpdesk Ticket Management System built with Django + Django REST Framework. Supports Users, Agents and Admins with features like ticket creation, SLA tracking, threaded comments, pagination, idempotency, optimistic locking, and rate limiting.

## Authentication & Roles (high level)

- user: register, login, create/view tickets, add comments — routes: /tickets, /tickets/new, /tickets/:id
- agent: view assigned tickets, update status, add comments — /dashboard/agent (frontend)
- admin: full access — /dashboard/admin (frontend)

## Test Credentials

- Admin: admin / admin
- Agent: agent1 / agent123
- User: user / user123

These accounts are seeded in the local/dev database for evaluation.

## API Endpoints (summary + sample requests)

1. Health Check

Endpoint: GET /api/health/

Response:

```json
{ "status": "ok" }
```

Sample (powershell):

```powershell
Invoke-RestMethod -Uri http://localhost:8000/api/health/
```

2. Meta Information

Endpoint: GET /api/\_meta/

Response example:

```json
{
  "name": "Helpdesk Ticket Management System",
  "version": "1.0.0",
  "description": "A Django-based ticketing system with role-based dashboards for users, agents, and admins.",
  "author": "Ajay",
  "status": "running"
}
```

3. Register

Endpoint: POST /api/register/

Body:

```json
{
  "username": "user",
  "email": "user@gmail.com",
  "password": "user123",
  "role": "user"
}
```

Response: user object with id, username, email, role.

4. Login

Endpoint: POST /api/login/

Body:

```json
{
  "username": "user",
  "password": "user123"
}
```

Response:

```json
{
  "token": "JWT_or_session_token_here",
  "user": { "id": 1, "username": "user", "role": "user" }
}
```

5. Create Ticket (idempotent POST)

Endpoint: POST /api/tickets/

Headers:

- Idempotency-Key: <unique-key> (recommended for clients) — server middleware deduplicates identical requests by this key.

Body:

```json
{
  "title": "Wi-Fi not working",
  "description": "Internet connectivity is down since morning"
}
```

Response (201 Created): ticket object

```json
{
  "id": 1,
  "title": "Wi-Fi not working",
  "description": "Internet connectivity is down since morning",
  "status": "open",
  "created_by": "user",
  "assigned_to": null,
  "sla_deadline": "2025-10-06T09:00:00Z"
}
```

6. Get Tickets (paginated)

Endpoint: GET /api/tickets/?limit=5&offset=0

Response example:

```json
{
  "items": [
    {
      "id": 1,
      "title": "Wi-Fi not working",
      "status": "open",
      "created_by": "user"
    }
  ],
  "next_offset": 5
}
```

7. Get Ticket by ID

Endpoint: GET /api/tickets/1/

Response: ticket with comments array

8. Update Ticket (Agent / Admin only)

Endpoint: PATCH /api/tickets/1/

Body:

```json
{ "status": "resolved" }
```

Response: updated ticket. If optimistic locking detects a stale version, server returns 409 Conflict with:

```json
{
  "error": {
    "code": "STALE_VERSION",
    "message": "Ticket was modified by another user"
  }
}
```

9. Add Comment

Endpoint: POST /api/tickets/1/comments/

Body:

```json
{ "content": "The issue has been fixed. Please confirm." }
```

Response: comment object with id, user, content, created_at.

10. Rate Limit Example

If a user exceeds 60 requests/minute:

```json
{ "error": { "code": "RATE_LIMIT" } }
```

---

## Seed Data (already applied)

Example seeded tickets (IDs present in the development DB):

1. Wi-Fi not working — open — created by user1
2. AC not cooling — in_progress — created by user1
3. Printer jam — open — created by user2
   ...
4. App login error — resolved — created by user3

## Notes on Pagination, Idempotency, and Rate Limits

- Pagination: The API uses limit/offset style pagination. Responses for list endpoints return an `items` array and a `next_offset` value. Clients can request fewer or more items by changing `limit` and move through pages using `offset`.
- Idempotency: POST endpoints that create resources (notably /api/tickets/) support an `Idempotency-Key` header. When present, the server stores the key and deduplicates repeated requests with the same key to avoid double-creation. Use a UUID per unique client intent.
- Rate limits: Per-user rate limiting is enforced (example policy: 60 requests/minute). When exceeded, the API returns a 429-like payload {"error":{"code":"RATE_LIMIT"}}. Implement exponential backoff on client retries.

## Short Architecture Note (120 words)

HelpDesk Mini follows a modular Django + DRF architecture emphasizing separation of concerns. The accounts app provides a custom user model with role support (user, agent, admin) and authentication endpoints. The tickets app handles ticket lifecycle, threaded comments, SLA deadlines, and optimistic locking via a version field to prevent lost updates. The core app centralizes cross-cutting concerns: idempotency middleware for safe repeated POSTs, DRF-based throttling for rate limiting, and a shared pagination component. Frontend templates provide role-aware dashboards. This layout makes features testable, easy to extend, and suitable for small teams while keeping API contracts stable for clients.

## How to run (quick)

1. Create a virtualenv and install deps from `requirements.txt`.
2. Run migrations: `python manage.py migrate`.
3. (If needed) load initial seed data or run provided fixtures.
4. Start dev server: `python manage.py runserver` (defaults to http://localhost:8000).

Sample health check once running (powershell):

```powershell
Invoke-RestMethod -Uri http://localhost:8000/api/health/
```

## Verification for judges

- Confirm `/api/health/` and `/api/_meta/` return the JSON described above.
- Confirm `/.well-known/hackathon.json` is present and accessible (used by some hackathons to pick up metadata).
- Use seeded credentials to exercise flows: login, create ticket (with `Idempotency-Key`), add comments, list tickets with pagination, and attempt rapid requests to see rate limiting.

## Contact

Author: Ajay

---

Thank you for reviewing HelpDesk Mini
