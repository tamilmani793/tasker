# Daily Tracker

A personal daily habits and task tracker with Google login, auto-sync via Supabase, and import/export backup.

## How it works

Credentials are **never hardcoded**. GitHub Actions injects them at deploy time from your repository variables and secrets, so the source code is safe to keep public.

```
GitHub Repo Variables/Secrets
        │
        ▼
GitHub Actions (deploy.yml)
        │  sed replaces __SUPABASE_URL__ and __SUPABASE_ANON_KEY__
        ▼
Built index.html → deployed to GitHub Pages
```

---

## Setup (one time, ~15 minutes)

### Step 1 — Fork or create this repo

Push all files to a GitHub repository.

### Step 2 — Create a free Supabase project

1. Go to [supabase.com](https://supabase.com) → New project
2. Choose a name and region, wait ~2 minutes

### Step 3 — Create the tasks table

In your Supabase project → **SQL Editor** → run:

```sql
create table tasks (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references auth.users not null,
  name text not null,
  cat text not null,
  time text default '',
  days integer[] not null,
  done jsonb default '{}'::jsonb,
  created_at timestamptz default now()
);

alter table tasks enable row level security;

create policy "Users own tasks" on tasks
  for all using (auth.uid() = user_id)
  with check (auth.uid() = user_id);
```

### Step 4 — Enable Google login in Supabase

1. Supabase → **Authentication → Providers → Google** → toggle on
2. Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a project → APIs & Services → Credentials
   - Create OAuth 2.0 Client ID (Web application)
   - Add Authorised redirect URI: `https://YOUR-PROJECT-REF.supabase.co/auth/v1/callback`
3. Copy the Client ID and Client Secret back into Supabase Google provider settings

### Step 5 — Add GitHub repository variables and secrets

Go to your GitHub repo → **Settings → Secrets and variables → Actions**

#### Repository Variables (Settings → Variables tab)
| Name | Value |
|------|-------|
| `SUPABASE_URL` | `https://xxxxxxxxxxxx.supabase.co` |

#### Repository Secrets (Settings → Secrets tab)
| Name | Value |
|------|-------|
| `SUPABASE_ANON_KEY` | `eyJh...` (your anon/public key) |

> **Why split?** The URL is not sensitive (it's a public endpoint) so it goes in Variables. The anon key is safe to expose in frontend code but keeping it in Secrets means it never appears in logs or diffs.

Get both values from: Supabase → **Project Settings → API**

### Step 6 — Enable GitHub Pages

Repo → **Settings → Pages → Source** → select `GitHub Actions`

### Step 7 — Add the Supabase redirect URL

Once GitHub Pages deploys, copy your Pages URL (e.g. `https://yourusername.github.io/daily-tracker`).

Add it in two places:
1. **Supabase → Authentication → URL Configuration → Site URL** → paste your Pages URL
2. **Supabase → Authentication → URL Configuration → Redirect URLs** → add your Pages URL
3. **Google Cloud Console → OAuth Client** → add to Authorised JavaScript origins and Authorised redirect URIs

### Step 8 — Deploy

Push any change to `main` (or trigger manually via Actions → Run workflow). GitHub Actions will inject your credentials and deploy automatically.

---

## Repository structure

```
├── index.html              # Full app — uses __SUPABASE_URL__ and __SUPABASE_ANON_KEY__ placeholders
├── .github/
│   └── workflows/
│       └── deploy.yml      # Injects secrets and deploys to GitHub Pages
└── README.md
```

## Features

- ✅ Google login via Supabase Auth
- ✅ Auto-sync — every task change saves to Supabase instantly
- ✅ Works on any device — just sign in with the same Google account
- ✅ Export backup as `.json` file
- ✅ Import from backup file (merges, no duplicates)
- ✅ Demo mode — works without login, stores locally
- ✅ Dark mode support
- ✅ Stats dashboard with weekly and monthly charts
- ✅ Task-wise filter on stats
- ✅ Activity streak tracker

## Credentials are never in code

The `index.html` source file contains only:
```js
const SUPABASE_URL = "__SUPABASE_URL__";
const SUPABASE_ANON_KEY = "__SUPABASE_ANON_KEY__";
```

These placeholders are replaced by `sed` inside GitHub Actions before deployment. Your actual credentials never appear in any committed file.
