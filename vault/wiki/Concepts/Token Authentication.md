---
type: concept
description: "Signing in by receiving a short-lived signed token that each service can verify"
reviewed: true
---

# Token Authentication

After sign-in, the user receives a signed, short-lived token. Any service that knows the issuer's public key can verify it without trusting the browser.

## Related concepts

- [[Row Level Security]] — the verified token is what lets Postgres know which rows belong to the user.

## Appears in

- [[Card Catalog Networking Tracker]] — Neon Managed Better Auth tokens expire after about 15 minutes and are forwarded from the API to Postgres.
