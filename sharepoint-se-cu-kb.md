# SharePoint Server Subscription Edition — CU Knowledge Base

**Coverage:** January 2026 CU → April 2026 CU
**Generated:** 2026-04-18 (refreshed from Apr CU comments 2026-04-18)
**Sources:** Stefan Goßner's blog, Microsoft Support KB articles, Microsoft Download Center.

---

## 1. Overview

- SPSE ships a single unified "uber" CU every month.
- Every SPSE monthly CU in this window is also a security update.
- Stefan Goßner (Microsoft Senior Escalation Engineer) is the authoritative reviewer.
- Standing warning across all four posts: farms still on September 2025 CU must run `Fix-SeptemberCU-Permission-Problem.ps1` (or remove `NT Authority\system` from `WSS_WPG` and `IIS_IUSRS`) before installing any CU in this window.

---

## 2. Build number / KB quick reference

| CU | Release | Build | KB | Security? |
|---|---|---|---|---|
| **Apr 2026** | 2026-04-14 | 16.0.19725.20210 | KB5002853 | Yes |
| Mar 2026 | 2026-03-10 | 16.0.19127.20xxx¹ | KB5002843 | Yes — **CAUTION** |
| Feb 2026 | 2026-02-10 | 16.0.19127.20518 | KB5002833 | Yes |
| Jan 2026 | 2026-01-13 | 16.0.19127.20442 | KB5002822 | Yes |

¹ Not captured from blog preview; see KB5002843.

---

## 3. Current recommendation (as of 2026-04-18)

**Target: April 2026 CU (KB5002853, build 16.0.19725.20210).**

Reasons:
1. Ships the **complete fix** for the Mar 2026 CU `SAFE_NOTIFICATION_DATA` psconfig upgrade regression (I-01).
2. No outstanding caution banner from Stefan.
3. Security rollup for April.

**Prerequisite — if source farm is September 2025 CU:** run [`Fix-SeptemberCU-Permission-Problem.ps1`](https://aka.ms/stefangossner/Fix-SeptemberCU-Permission-Problem.ps1) first, else install fails.

**Do NOT install:** Mar 2026 CU directly on top of Jan 2026 CU without Feb 2026 CU as an intermediate (see §6).

---

## 4. Per-CU details (newest first)

### April 2026 CU — KB5002853 — build 16.0.19725.20210 — 2026-04-14
- **Verdict (Stefan):** strongly_recommended.
- **Highlights:** complete fix for I-01 (`SAFE_NOTIFICATION_DATA`); addresses **CVE-2026-32201** (listed in CISA KEV as actively exploited — accelerate patching).
- **Known issues introduced:** one unconfirmed report (I-03) — see issue index.
- **Prereq:** if on Sep 2025 CU, run `Fix-SeptemberCU-Permission-Problem.ps1` first.
- **Sources:**
  - https://blog.stefan-gossner.com/2026/04/14/april-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/
  - https://support.microsoft.com/en-us/kb/5002853
  - https://www.microsoft.com/en-us/download/details.aspx?id=108607

### March 2026 CU — KB5002843 — build 16.0.19127.20xxx — 2026-03-10 — ⚠ CAUTION
- **Verdict (Stefan):** caution — banner at top of post.
- **Issue introduced (I-01):** psconfig upgrade fails with `Invalid column name 'SAFE_NOTIFICATION_DATA'` when the farm's current schema is from Jan 2026 CU. Mar 2026 CU's installer is the failing actor.
- **Workaround (before install):** install Feb 2026 CU → run Configuration Wizard → then install Mar 2026 CU.
- **Workaround (already broken):** open Microsoft Support ticket; engineering has documented remediation.
- **Fixes this CU delivers:** SPAdminV4 failure on Windows Server 2025 (Sep 2025 CU regression); Secure Store group-claim validation after Sep 2025 CU.
- **Sources:**
  - https://blog.stefan-gossner.com/2026/03/10/march-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/
  - https://blog.stefan-gossner.com/2026/03/12/trending-issue-spse-configuration-wizard-will-fail-for-upgrades-from-january-2026-cu-to-march-2026-cu/
  - https://support.microsoft.com/en-us/kb/5002843

### February 2026 CU — KB5002833 — build 16.0.19127.20518 — 2026-02-10
- **Verdict (Stefan):** must_install_or_higher — mandatory intermediate between Jan and Mar CUs.
- **Fixes:** w3wp crash `0xC0000409` (owssvr.dll), w3wp crash `0xC06D007E / 0xE0434352` race, SP2010 workflow CSC.EXE failure — all three are Sep 2025 CU regressions.
- **Known issues:** none new; carries forward I-02 (Text web part regression introduced by Jan 2026 CU).
- **Sources:**
  - https://blog.stefan-gossner.com/2026/02/10/february-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/
  - https://support.microsoft.com/en-us/kb/5002833

### January 2026 CU — KB5002822 — build 16.0.19127.20442 — 2026-01-13
- **Verdict (Stefan):** caution.
- **Known issues introduced:** I-02 — Text web part content area becomes read-only while the "Text and table formatting" pane is open (modern UI regression; still unfixed as of 2026-04-18).
- **Regression trap:** Jan 2026 CU's schema is incompatible with Mar 2026 CU's installer (see I-01 in Mar 2026 CU entry). Do not jump directly from Jan 2026 CU to Mar 2026 CU — install Feb 2026 CU first (or skip to Apr 2026 CU).
- **Sources:**
  - https://blog.stefan-gossner.com/2026/01/13/january-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/
  - https://support.microsoft.com/en-us/kb/5002822

---

## 5. Cross-CU issue index

| # | Component | Summary | Severity | Introduced | Fixed in | Workaround |
|---|---|---|---|---|---|---|
| I-01 | Upgrade / psconfig | `Invalid column name 'SAFE_NOTIFICATION_DATA'` when Mar 2026 CU tries to upgrade a Jan 2026 CU schema | critical | **2026-03** (Mar 2026's installer is the failing actor) | 2026-04 | Install Feb 2026 CU + run Config Wizard before Mar, or jump straight to Apr 2026 CU |
| I-02 | Modern UI / Text web part | Text web part read-only while "Text and table formatting" pane is open | medium | 2026-01 | not yet fixed (2026-04-18) | Close formatting pane before editing text |
| I-03 ⚠ **unconfirmed** | Search / psconfig | After Apr 2026 CU, Configuration Wizard upgrade of `SearchAdminDatabase` fails with `Cannot find the object 'proc_MSS_GetCrawlErrorOrWarningCounts'`. Single community report on Stefan's Apr CU post, no Stefan response yet; could be environment-specific. | potentially high | 2026-04 (unconfirmed) | n/a | Snapshot Search Admin DB before install. If hit: do not self-repair — open Microsoft Support ticket |

Carryover from outside window (farms still on Sep 2025 CU):

| # | Component | Summary | Severity | Introduced | Fixed in | Workaround |
|---|---|---|---|---|---|---|
| X-01 | Patching / perms | Future SharePoint fixes fail to install due to `NT Authority\system` in `WSS_WPG`/`IIS_IUSRS` | high | 2025-09 | code fix in 2025-10; existing farms must remediate | Run `Fix-SeptemberCU-Permission-Problem.ps1` |

---

## 6. Upgrade matrix (to April 2026 CU)

| From | Recommended path | Intermediate required | Rationale / blockers |
|---|---|---|---|
| ≤ 2025-12 (pre-window) | → Apr 2026 CU | No | Clean jump. Run `Fix-SeptemberCU-Permission-Problem.ps1` first if farm was ever on Sep 2025 CU. |
| 2026-01 | → Feb 2026 CU (run Config Wizard) → Apr 2026 CU | **Yes — Feb mandatory** | Skipping Feb triggers I-01 if you later try Mar. Alt: Jan → Apr 2026 CU direct is also safe (Apr contains the complete fix). |
| 2026-02 | → Apr 2026 CU | No | Feb schema is compatible with Apr's installer. |
| 2026-03 (installed cleanly from Feb) | → Apr 2026 CU | No | Mar schema is compatible with Apr's installer. |
| **2026-03-broken** (Mar installed on top of Jan — psconfig failing) | Open Microsoft Support ticket | N/A | Engineering-guided remediation only; do not self-repair schema. |
| 2026-04 | *(already current)* | — | Target. |

### General SPSE patching procedure
1. Read target CU's Stefan post for last-minute blockers.
2. Back up all content + config DBs.
3. Install binaries on all SharePoint machines.
4. Run SharePoint Products Configuration Wizard (`PSConfigUI.exe`).
5. Run `Test-DefenderAndAmsiWorkProperly` (available since Sep 2025 CU).
6. Verify machine-key rotation timer job health (since Sep 2025 CU).

---

## 7. Microsoft Learn & official references

- Product servicing policy: https://learn.microsoft.com/en-us/sharepoint/product-servicing-policy/updated-product-servicing-policy-for-sharepoint-server-se
- Servicing FAQ: https://learn.microsoft.com/en-us/sharepoint/product-servicing-policy/faq/faq-subscription-edition
- Feature-update page (25H1/25H2): https://learn.microsoft.com/en-us/SharePoint/what-s-new/new-and-improved-features-in-sharepoint-server-subscription-edition-25h1-release
- Deprecations: https://learn.microsoft.com/en-us/sharepoint/what-s-new/what-s-deprecated-or-removed-from-sharepoint-server-subscription-edition

## 8. Source log (fetch date: 2026-04-18)

| Label | URL |
|---|---|
| spse-2026-01-cu | https://blog.stefan-gossner.com/2026/01/13/january-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/ |
| spse-2026-02-cu | https://blog.stefan-gossner.com/2026/02/10/february-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/ |
| spse-2026-03-cu | https://blog.stefan-gossner.com/2026/03/10/march-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/ |
| spse-2026-04-cu | https://blog.stefan-gossner.com/2026/04/14/april-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/ |
| mar2026-psconfig-issue | https://blog.stefan-gossner.com/2026/03/12/trending-issue-spse-configuration-wizard-will-fail-for-upgrades-from-january-2026-cu-to-march-2026-cu/ |
