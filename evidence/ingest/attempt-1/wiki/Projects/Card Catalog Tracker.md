---
type: source-note
source_id: networking-tracker-readme
source_path: raw/networking-tracker-readme.md
source_sha256: 2e401653ff1da865
description: "This project is a private card catalog designed to track connections, featuring features for adding and editing contacts"
generated_by: mlx-community/gemma-4-e2b-it-4bit
ingested: 2026-09-27
reviewed: false
---

# Card Catalog Tracker

This project is a private card catalog designed to track connections, featuring features for adding and editing contacts. The main result is a secure architecture where the browser communicates with an Express API, which in turn handles communication with the database.

## Key details

- Contacts can be added with details including name, company, role, where they were met, notes, and priority.
- Priority is strictly limited to `high`, `medium`, or `low` and is enforced in the database.
- Users can only edit and delete their own contacts.
- The frontend is built using React 18 + Vite, which builds a plain static site served by Vercel's CDN.
- The architecture separates the browser from the database by routing all requests through an Express API.
- Authentication uses Neon Managed Better Auth, which issues a signed token that expires after about 15 minutes.
- Row Level Security is enabled on the `contacts` table, comparing the row's owner against the signed-in user.

## Related concepts

- [[Corpus]] — The source document details the structure of the card catalog, including fields for contacts.
- [[Evaluation Suite]] — The architecture discusses how different approaches to database connectivity affect security properties.
- [[Learning Rate]] — This concept is not explicitly mentioned in the source document.
- [[Loss]] — This concept is not explicitly mentioned in the source document.

## Sources

- Original: [[raw/networking-tracker-readme.md]] (unchanged copy in `vault/raw/`)
