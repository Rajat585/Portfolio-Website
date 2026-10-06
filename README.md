# Rajat Verma — Portfolio (Full Project)

## 🎥 Demo Video

[![Watch the demo](https://img.youtube.com/vi/4qG4Gj1ByxU/0.jpg)](https://youtu.be/4qG4Gj1ByxU)

Click the image above to watch a full walkthrough of the portfolio.

This zip contains everything from the 6-part brief: design, frontend,
backend, project integration, SEO/recruiter optimization, and deployment.

## What's inside

```
rajat-portfolio/
├── frontend-preview/   ← open index.html directly in any browser, no setup needed
└── backend/            ← full Django + MySQL project (see backend/README.md)
```

### 1. Just want to see the design?
Open `frontend-preview/index.html` in a browser (double-click it). Everything
— hero, projects, certifications, internship, testimonials, blog, contact
form, animations — works as static HTML/CSS/JS with Bootstrap 5. The contact
form will open your email app if it can't reach a backend (that's expected
here — it's for the live Django version).

### 2. Want the real, working site (database, admin, email/WhatsApp on
contact form, deployable)?
Go into `backend/` and follow `backend/README.md` — local setup, then
deployment to Render or a VPS (Nginx + Gunicorn), both fully scripted.

## Quick facts

- **Design**: Charcoal Noir / Cloud Veil / Royal Blue / Emerald Green
  palette, Inter + JetBrains Mono type, signature "IDE hero" section styled
  as a live code editor window.
- **Frontend**: Bootstrap 5, jQuery, scroll-reveal animations, fully
  responsive, resume download, all 6 social links wired to what you sent
  (LinkedIn, GitHub, Telegram, Instagram, WhatsApp, Facebook).
- **Backend**: Django 5 + DRF + MySQL, models for Projects/Certifications/
  Internship/Testimonials/Blog/Contact, admin panel, email + WhatsApp
  automation on the contact form, rate limiting, optional reCAPTCHA.
- **Content**: pre-filled from your resume (3 projects, 2 certifications,
  SarthMandi internship) via `backend/core/fixtures/seed_data.json`.
- **SEO**: meta tags, Open Graph, JSON-LD (Person + Project schema),
  robots.txt, sitemap.xml.
- **Deployment**: Render build/start commands, VPS guide (Gunicorn +
  systemd + Nginx + Let's Encrypt), GitHub Actions CI/CD.

## Things you'll want to replace before going live

- Testimonials are placeholder quotes — swap for real ones via the admin.
- Blog posts are placeholder cards — add real ones via the admin, or wire
  the frontend JS to `/api/blog/` (the endpoint already exists).
- "Live Demo" buttons on projects point to `#` — add real hosted links once
  the projects are deployed somewhere.
- Certification logos use a generic badge icon (Mantra Institute / COPA
  logos weren't provided) — upload real ones in the admin, they'll render
  in place of the icon automatically.
- `rajatverma.dev` is a placeholder domain throughout (SEO tags, CORS,
  Nginx config) — swap in your real domain once you have one.
