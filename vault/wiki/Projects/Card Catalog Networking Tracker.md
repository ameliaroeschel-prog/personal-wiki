---
type: source-note
source_id: networking-tracker-readme
source_path: raw/networking-tracker-readme.md
source_sha256: 2e401653ff1da865
description: "Assignment 1: a private networking-contacts app (React + Express + Neon Postgres) where the database enforces ownership"
generated_by: mlx-community/gemma-4-e2b-it-4bit
ingested: 2026-09-27
reviewed: true
review_notes: "Renamed from 'Card Catalog Tracker'. Replaced Gemma's force-fit concept links (Corpus, Evaluation Suite) with concepts the source actually discusses."
---

# Card Catalog Networking Tracker

Assignment 1: "Card Catalog", a private tracker for the people Amelia wants to stay connected with at Berkeley. Each contact is an index card with a follow-up cadence, and the app lists who is overdue each week. Ownership of every card is enforced by Postgres Row Level Security, not by app code.

## Key details

- Contacts store name, company, role, where you met, notes and priority; priority is limited to high/medium/low by the database (§ Features).
- A "Reach out this week" list and month calendar are driven by each contact's cadence: monthly, quarterly, annually or custom (§ Features).
- Stack: React 18 + Vite frontend, Node + Express 5 API, Neon Postgres, Neon Managed Better Auth, hosted on Vercel (§ Technology stack).
- The browser only talks to the Express API, giving a trusted place to validate and a reusable API (§ Why the frontend and backend are separate).
- Sign-in issues a signed token that expires after about 15 minutes; the API verifies it and forwards it so Postgres can check it too (§ Authentication and ownership).
- Row Level Security has a separate policy per operation, and `user_id` is stamped by the database, never sent by the browser (§ Database schema, § The ownership rule).
- Validation happens three times: in the browser, the API, and the database (§ Validation happens three times).

## Related concepts

- [[Row Level Security]] — the core design decision: the database, not the app, decides who owns a row.
- [[Token Authentication]] — short-lived signed tokens let both the API and Postgres verify the user.

## Sources

- Original: [[raw/networking-tracker-readme.md]] (unchanged copy in `vault/raw/`)
