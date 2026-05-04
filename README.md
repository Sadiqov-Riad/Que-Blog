# Que Blog

## Docker setup

### Prerequisites
- Docker Desktop (includes Docker Compose v2)

### Quick start
1. Copy env file:
   - cp .env.example .env
2. Build and start containers:
   - docker compose up --build
3. Run migrations in another terminal:
   - docker compose exec web python manage.py migrate
4. Create an admin user:
   - docker compose exec web python manage.py createsuperuser
5. Open the app:
   - http://localhost:8000

### Useful commands
- Stop containers:
  - docker compose down
- Remove containers and DB volume:
  - docker compose down -v
- Follow web logs:
  - docker compose logs -f web
- Django shell:
  - docker compose exec web python manage.py shell

### Notes
- The Docker setup uses `config.settings.base` so `DJANGO_DEBUG` and `DJANGO_ALLOWED_HOSTS` come from .env.
- If you need access from another device, add your host IP to `DJANGO_ALLOWED_HOSTS`.
