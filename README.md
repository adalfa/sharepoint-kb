# SharePoint Server Subscription Edition — CU Knowledge Base

Canonical knowledge base of SPSE Cumulative Updates, built from Stefan Goßner's blog and Microsoft KB articles.

## Files

- [`sharepoint-se-cu-kb.md`](./sharepoint-se-cu-kb.md) — human-readable dossier (per-CU details, cross-CU issue index, upgrade matrix).
- [`sharepoint-se-cu-kb.json`](./sharepoint-se-cu-kb.json) — machine-readable mirror for tooling.

## Current coverage

January 2026 CU → April 2026 CU. Recommended target: **April 2026 CU (KB5002853, build 16.0.19725.20210)**.

## Weekly refresh

A scheduled Claude Code remote agent (`spse-cu-weekly-check`) runs every Monday ~08:17 Europe/Rome:

1. Re-fetches the Stefan Goßner blog homepage and the latest CU post (including its comments).
2. Diffs findings against the KB in this repo.
3. Opens a PR when there are new facts — new CU release, new trending-issue post, a change in an unconfirmed-issue status, newly disclosed CVEs, etc.
4. Exits quietly when nothing has changed.

The agent commits to a branch named `spse-weekly-YYYY-MM-DD` and opens a PR against `main`.

## Attribution rule for cross-CU regressions

When a bug manifests only during an upgrade (e.g. CU N installer fails against CU M's schema), `introduced_in` attributes to **the CU whose installer fails** — the one Stefan's trending-issue post is tagged against — not the earlier CU whose schema was merely incompatible.
