---
type: concept
description: "A Postgres feature where the database itself decides which rows each user may see or change"
reviewed: true
---

# Row Level Security

A Postgres feature that attaches a policy to a table, so every query only sees or changes rows the signed-in user is allowed to — even if the application code has a bug.

## Related concepts

- [[Token Authentication]] — the database needs to know who the user is before it can apply the policy.

## Appears in

- [[Card Catalog Networking Tracker]] — one policy per operation on the contacts table; ownership is stamped by the database.
