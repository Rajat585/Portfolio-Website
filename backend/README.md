# Rajat Verma — Portfolio (Django + MySQL backend)

Recruiter-ready portfolio: Django 5 + Django REST Framework + MySQL backend,
Bootstrap 5 / jQuery frontend, email + WhatsApp contact automation, SEO/JSON-LD,
and deployment configs for both Render and a self-managed VPS.

## 1. Local setup

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env              # then edit .env with your real values
python manage.py migrate
python manage.py loaddata core/fixtures/seed_data.json   # pre-fills projects/certs/internship
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the site and `http://127.0.0.1:8000/admin/`
to manage content (projects, certifications, testimonials, blog posts,
contact messages).

No MySQL server handy? Leave `DATABASE_URL` unset in `.env` and it falls
back to local SQLite automatically — good enough for trying things out.

## 2. Project structure

```
backend/
├── manage.py
├── portfolio_backend/      # settings, urls, wsgi/asgi
├── core/                   # models, admin, DRF serializers/views, migrations, fixtures
├── templates/index.html    # the single-page site (Django template, uses {% static %})
├── static/                 # css/js/img (source files — collected into staticfiles/ on deploy)
├── requirements.txt
├── .env.example
├── Procfile                 # Render/Railway-style start command
├── render.yaml               # Render build/start command reference
├── gunicorn_conf.py          # VPS Gunicorn config
├── deploy/portfolio.service   # systemd unit for Gunicorn on a VPS
├── nginx/portfolio.conf        # Nginx reverse proxy + SSL + gzip
└── .github/workflows/ci-cd.yml # test-then-deploy pipeline
```

## 3. Environment variables

See `.env.example` for the full list. Required for the contact form to
actually send email: `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USER`,
`EMAIL_PASSWORD` (use a Gmail **App Password**, not your normal password).
`WHATSAPP_API_KEY` / `WHATSAPP_API_URL` are optional — leave blank and the
WhatsApp step is skipped silently.

## 4. Deploying to Render

1. Push this repo to GitHub.
2. Create a new **Web Service** on Render, connect the repo.
3. Build command:
   `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
4. Start command:
   `gunicorn portfolio_backend.wsgi:application --bind 0.0.0.0:$PORT --workers 3`
5. Add all variables from `.env.example` under **Environment**, with
   `DEBUG=False` and real values for `SECRET_KEY`, `DATABASE_URL` (Render's
   MySQL/PlanetScale connection string), `ALLOWED_HOSTS`, email, etc.
6. Add a **Persistent Disk** mounted at `/media` if you plan to upload
   certification/internship logos through the admin.

## 5. Deploying to a VPS (Nginx + Gunicorn)

```bash
sudo apt update && sudo apt install -y python3-venv python3-dev libmysqlclient-dev \
  mysql-server nginx certbot python3-certbot-nginx

sudo mkdir -p /var/www/portfolio && cd /var/www/portfolio
git clone <your-repo-url> .
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env      # fill in production values, DEBUG=False
python manage.py migrate
python manage.py collectstatic --noinput

sudo cp deploy/portfolio.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now portfolio

sudo cp nginx/portfolio.conf /etc/nginx/sites-available/portfolio
sudo ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

sudo certbot --nginx -d rajatverma.dev -d www.rajatverma.dev
```

Static files are served straight from `/var/www/portfolio/staticfiles/` by
Nginx (see `nginx/portfolio.conf`); Gunicorn only handles Django requests.

## 6. Security checklist (already wired into settings.py)

- `DEBUG=False`, explicit `ALLOWED_HOSTS` in production
- `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, HSTS
- CSRF protection on all forms; DRF endpoints throttled (`5/min` on
  `/api/contact/`, `20/hour` anonymous elsewhere)
- PBKDF2 password hashing (Django default, kept explicit in settings)
- Optional Google reCAPTCHA on the contact form (set `RECAPTCHA_SECRET_KEY`
  + `RECAPTCHA_SITE_KEY` to turn it on)
- Take regular `mysqldump` backups in production; not automated here since
  it depends on your host

## 7. Scaling this later

- New content type → new Django app under `core/` or a sibling app,
  registered in `INSTALLED_APPS`
- Blog search/tagging → add `django-taggit` + a search view once there are
  enough posts to need it
- Swap the static demo content in `templates/index.html` for live API calls
  to `/api/projects/`, `/api/testimonials/`, etc. (serializers/viewsets are
  already there, just not wired into the frontend JS yet)
- CI/CD in `.github/workflows/ci-cd.yml` runs `manage.py check` on every
  push and can trigger a Render deploy hook on `main`

## 8. Frontend-only preview

If you just want to see the design without setting up Django/MySQL at all,
open `frontend-preview/index.html` (in the project root, outside `backend/`)
directly in a browser — it's the same page with plain relative paths instead
of Django's `{% static %}` tags.
