# SharePoint Server Subscription Edition — CU Knowledge Base

**Coverage:** July 2025 CU → April 2026 CU
**Generated:** 2026-04-18
**Sources:** Stefan Goßner's blog (blog.stefan-gossner.com), Microsoft Support KB articles, Microsoft Download Center.

---

## 1. Overview

- SharePoint Server Subscription Edition (SPSE) ships a single **"uber" CU** every month (language-independent + language-dependent bundled).
- Starting with **August 2025 CU**, every monthly SPSE CU is also flagged as a **security update** (Microsoft recommends installing the full CU over individual security fixes).
- Stefan Goßner (Microsoft Senior Escalation Engineer) publishes the authoritative community commentary, including **known/trending issues** and upgrade guidance.
- Feature Update **25H2** shipped inside the September 2025 CU.

### How to use this document

- Section 3 (Current recommendation) tells you *what to install right now*.
- Section 4 lists every CU chronologically with build number, KB, fixes, regressions, and Stefan's verdict.
- Section 5 is a cross-CU issue index — find an issue once and see where it was introduced/fixed.
- Section 6 is the upgrade matrix — the exact path to take from any starting CU.

---

## 2. Build number / KB quick reference

| CU | Release | Build (16.0.x.y) | KB | Also security? |
|---|---|---|---|---|
| **Apr 2026** | 2026-04-14 | 16.0.19725.20210 | KB5002853 | Yes |
| Mar 2026 | 2026-03-10 | 16.0.19127.20xxx¹ | KB5002843 | Yes — **CAUTION** |
| Feb 2026 | 2026-02-10 | 16.0.19127.20518 | KB5002833 | Yes |
| Jan 2026 | 2026-01-13 | 16.0.19127.20442 | KB5002822 | Yes |
| Dec 2025 | 2025-12-09 | 16.0.19127.20378 | KB5002815 | Yes |
| Nov 2025 | 2025-11-11 | 16.0.19127.20338 | KB5002800 | Yes |
| Oct 2025 | 2025-10-14 | 16.0.19127.20262 | KB5002786 | Yes |
| **Sep 2025** | 2025-09-09 | 16.0.19127.20100 | KB5002784 | Yes — **high regression risk** (25H2 feature update) |
| Aug 2025 | 2025-08-12 | 16.0.18526.20518 | KB5002773 | Yes |
| Jul 2025 | 2025-07-08 | 16.0.18526.20424 | KB5002751 | Partial (see ToolShell) |

¹ Exact March 2026 build not captured in blog header (post emphasised the psconfig blocker); consult KB5002843.

---

## 3. Current recommendation (as of 2026-04-18)

**Target: April 2026 CU (KB5002853, build 16.0.19725.20210).**

Reasons:
1. Supersedes the **March 2026 CU `SAFE_NOTIFICATION_DATA` psconfig-fail** regression — Apr 2026 is the first CU with a **complete fix** for the Jan→Mar upgrade break.
2. Supersedes every resolved September-2025-CU side-effect (solution deployment fail, SP2010 workflows, classic WFM, SPAdminV4 on WS2025, Secure Store group-claim validation, w3wp 0xC0000409 / 0xC06D007E crashes, Text web part read-only — see Section 5).
3. Every monthly CU since Aug 2025 is also a security update; skipping CUs leaves CVEs unpatched.

**Prerequisites when the source farm is Sep 2025 CU:** run
[`Fix-SeptemberCU-Permission-Problem.ps1`](https://aka.ms/stefangossner/Fix-SeptemberCU-Permission-Problem.ps1)
*before* applying any subsequent CU, or else the install fails with "future SharePoint fixes cannot be installed". Alternatively remove `NT Authority\system` from `WSS_WPG` and `IIS_IUSRS` local groups on every SharePoint machine.

**Do NOT install:** the Mar 2026 CU **on top of** Jan 2026 CU without the Feb 2026 CU intermediate (see Upgrade Matrix §6).

---

## 4. Per-CU details (newest first)

### April 2026 CU — KB5002853 — build 16.0.19725.20210 — 2026-04-14
- **Verdict (Stefan):** recommended.
- **Highlights:** Complete fix for the Jan→Mar upgrade `SAFE_NOTIFICATION_DATA` regression. Monthly security rollup.
- **Known issues introduced:** none reported at time of writing.
- **Prereq:** if farm is still on Sep 2025 CU, apply `Fix-SeptemberCU-Permission-Problem.ps1` first.
- **Sources:**
  - https://blog.stefan-gossner.com/2026/04/14/april-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/
  - KB: https://support.microsoft.com/en-us/kb/5002853
  - Download: https://www.microsoft.com/en-us/download/details.aspx?id=108607

### March 2026 CU — KB5002843 — 2026-03-10 — ⚠ CAUTION
- **Verdict (Stefan):** *do not* install directly on top of Jan 2026 CU.
- **Regression:** Running psconfig after upgrading databases from **Jan 2026 schema** to Mar 2026 fails with
  `Invalid column name 'SAFE_NOTIFICATION_DATA'` in Upgrade-*.log.
  Affected only when DB schema was updated to Jan 2026 CU level.
- **Workarounds:**
  - *Scenario 1 (Mar not yet applied):* install Feb 2026 CU → run Configuration Wizard → then Mar 2026 CU.
  - *Scenario 2 (Mar already applied):* open a Microsoft Support ticket; engineering has guidance.
- **Fixes this CU delivers:** SPAdminV4 fail on Windows Server 2025 (Sep 2025 regression); Secure Store group-claim validation after Sep 2025 CU.
- **Sources:**
  - Main post: https://blog.stefan-gossner.com/2026/03/10/march-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/
  - Trending issue: https://blog.stefan-gossner.com/2026/03/12/trending-issue-spse-configuration-wizard-will-fail-for-upgrades-from-january-2026-cu-to-march-2026-cu/
  - Text-webpart regression report: https://blog.stefan-gossner.com/2026/03/11/trending-issue-text-web-part-cannot-be-edited-while-text-and-table-formatting-pane-is-open/

### February 2026 CU — KB5002833 — build 16.0.19127.20518 — 2026-02-10
- **Verdict:** recommended (stable).
- **Fixes:** w3wp worker process crash **0xC0000409** (owssvr.dll, Sep 2025 regression); w3wp crash **0xC06D007E / 0xE0434352** race condition; SP2010 workflows failing on SPSE (Sep 2025 regression).
- **Known issues:** none new; carries forward the Text-webpart modern-UI regression introduced in Jan 2026 CU.
- **Sources:** https://blog.stefan-gossner.com/2026/02/10/february-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/ · KB5002833.

### January 2026 CU — KB5002822 — build 16.0.19127.20442 — 2026-01-13
- **Verdict:** install only as stepping-stone to later CUs; do **not** dwell on it because:
  - Mar 2026 CU cannot upgrade its DB schema directly (see §6).
  - Introduced **Text web part** modern-UI regression: content area becomes read-only while "Text and table formatting" pane is open.
- **Sources:** https://blog.stefan-gossner.com/2026/01/13/january-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/ · KB5002822.

### December 2025 CU — KB5002815 — build 16.0.19127.20378 — 2025-12-09
- **Verdict:** rolling security. Documented follow-up to ongoing Sep-2025-CU w3wp crash investigations.
- **Known issues:** w3wp **0xC0000409** and **0xC06D007E/0xE0434352** crashes documented (fix arrives Feb 2026 CU).
- **Sources:** https://blog.stefan-gossner.com/2025/12/09/december-2025-cu-for-sharepoint-server-subscription-edition-is-available-for-download/ · KB5002815.

### November 2025 CU — KB5002800 — build 16.0.19127.20338 — 2025-11-11
- **Verdict:** routine security CU; recommended if coming from Oct 2025 CU or earlier.
- **Prereq banner:** same "remove NT Authority\system from WSS_WPG/IIS_IUSRS" prereq for farms still on Sep 2025 CU.
- **Sources:** https://blog.stefan-gossner.com/2025/11/11/november-2025-cu-for-sharepoint-server-subscription-edition-is-available-for-download/ · KB5002800.

### October 2025 CU — KB5002786 — build 16.0.19127.20262 — 2025-10-14
- **Verdict:** first "rescue" CU after Sep 2025 CU — **strongly recommended** for anyone stuck on Sep 2025.
- **Fixes (Sep 2025 regressions):**
  - Solution deployment failure.
  - SP 2013 workflows + classic Workflow Manager failure.
  - Future SharePoint fixes fail to install (WSS_WPG / IIS_IUSRS perm regression) — **fix present but the existing perm damage on Sep 2025 farms must still be remediated** via `Fix-SeptemberCU-Permission-Problem.ps1`.
  - Health rule falsely flagging WSS_WPG elevated permissions.
- **Sources:** https://blog.stefan-gossner.com/2025/10/14/october-2025-cu-for-sharepoint-server-subscription-edition-is-available-for-download/ · KB5002786.

### September 2025 CU — KB5002784 — build 16.0.19127.20100 — 2025-09-09 — ⚠ HIGH REGRESSION RISK
- **Includes:** Feature Update **25H2**.
- **New security features (by design):**
  - **AMSI enabled for all web applications** (all supported SP versions).
  - **Automatic machine-key rotation timer job** (ASP.NET machine keys rotated periodically for viewstate integrity).
  - **Test-DefenderAndAmsiWorkProperly** cmdlet.
  - New Windows Exploit Protection on OWSTIMER.EXE (blocks child-process creation).
  - `_LAYOUTS` directory write-hardening — removes WSS_WPG / IIS_IUSRS write access.
- **Regressions introduced (see Section 5 for fix locations):**
  1. SP2013 workflows + Classic Workflow Manager break (hardening requires latest SPWFM).
  2. Solution deployment fails.
  3. Future SharePoint fixes cannot be installed (NT Authority\system in WSS_WPG/IIS_IUSRS).
  4. SPAdminV4 fails to start on **Windows Server 2025** (Exploit Protection side-effect).
  5. SharePoint Health rule false-positive on WSS_WPG.
  6. SharePoint admin tools (PSCONFIG, Mgmt Shell) fail when run under Farm Service Account — documented as *by design*.
  7. SP2010 workflows fail (CSC.exe child-process blocked) — **Nintex workflows are also affected by the same CSC.exe Exploit Protection block** (reported by community user in Stefan's Sep 2025 issue-summary comments after KB5002784 + KB5002786; fix arrives Feb 2026 CU, workaround: relax Exploit Protection on OWSTIMER.EXE).
  8. Secure Store: group claim validation fails / stored credentials no longer decryptable (new encryption algo).
  9. w3wp crash **0xC0000409** (owssvr.dll).
  10. w3wp crash **0xC06D007E / 0xE0434352** race.
- **Verdict (Stefan):** install **only with awareness** of the 10 issues above; prefer Oct 2025 CU or later. If already on Sep 2025 CU, do NOT install any later CU without first running `Fix-SeptemberCU-Permission-Problem.ps1`.
- **Sources:**
  - Main: https://blog.stefan-gossner.com/2025/09/09/september-2025-cu-for-sharepoint-server-subscription-edition-is-available-for-download/
  - Summary of issues: https://blog.stefan-gossner.com/2025/09/25/summary-and-status-of-issues-identified-with-september-2025-cu-for-sharepoint/
  - Security features: https://blog.stefan-gossner.com/2025/09/09/new-security-features-released-with-september-2025-cu-for-all-supported-sharepoint-versions/
  - KB5002784.

### August 2025 CU — KB5002773 — build 16.0.18526.20518 — 2025-08-12
- **Verdict:** recommended — first clean security rollup after the July emergency.
- **Notes:**
  - From this CU onward every SPSE monthly CU is also a security update.
  - Side-topic: SharePoint **Workflow Manager** Aug 2025 CU switched from `System.Data.SqlClient` to `Microsoft.Data.SqlClient`; bare SPWFM machines (without SPSE installed) hit `System.Memory.dll` missing errors — additional assemblies were added in Stefan's 2025-08-21 update.
  - BDC LobSystem types `DotNetAssembly` and `WebService` remain disabled (disabled since June 2025 CU; no new BDC models since Sep 2024 CU) — re-enable guidance documented.
- **Sources:** https://blog.stefan-gossner.com/2025/08/12/august-2025-cu-for-sharepoint-server-subscription-edition-is-available-for-download/ · KB5002773.

### July 2025 CU — KB5002751 — build 16.0.18526.20424 — 2025-07-08
- **Verdict:** **MUST install or go higher** — baseline for **ToolShell** remediation.
- **Security context:**
  - Active, in-the-wild attacks targeting on-prem SharePoint (2016/2019/SE) exploiting vulns *partially* addressed by July Security Update. Admin IoC: presence of `spinstall0.aspx` in `…\16\TEMPLATE\LAYOUTS` = machine likely compromised.
  - Customers who were on July 2025 CU only were still vulnerable to follow-on variants — **install at least Aug 2025 CU**, preferably later, for full coverage.
- **Functional fixes (per Stefan Q&A in comments):** Query Logging Job timeout (actually fixed in June 2025 CU); User Profile Language Synchronization Job failure planned for Aug 2025 CU — so July CU did **not** cover those two as some customers believed.
- **Known issue carried forward (I-17):** `QueryLogJobDefinition` SQL connection pool exhaustion — introduced Mar 2025 CU, still present in Jul and Aug 2025 CU. Manifests as Event ID 6399 critical errors a few days after server restart. See Section 5 for details and workaround.
- **Sources:**
  - Main: https://blog.stefan-gossner.com/2025/07/08/july-2025-cu-for-sharepoint-server-subscription-edition-is-available-for-download/
  - ToolShell advisory: https://blog.stefan-gossner.com/2025/07/21/important-active-attacks-targeting-on-premises-sharepoint-server-customers/
  - AMSI clarifications: https://blog.stefan-gossner.com/2025/07/23/clarifying-common-questions-around-amsi-in-sharepoint/
  - KB5002751.

---

## 5. Cross-CU issue index

| # | Component | Summary | Severity | Introduced | Fixed in | Workaround |
|---|---|---|---|---|---|---|
| I-01 | Security / whole farm | ToolShell active exploitation (`spinstall0.aspx`) | Critical | pre-Jul 2025 | Jul 2025 CU (partial); Aug 2025 CU (full) | Scan LAYOUTS for `spinstall0.aspx`; rotate machine keys; enable AMSI |
| I-02 | SPWFM | `System.Memory.dll` missing after Aug 2025 SPWFM CU on non-SPSE hosts | Medium | Aug 2025 SPWFM CU | Updated assembly list (2025-08-21 note) | Deploy listed assemblies manually |
| I-03 | BDC | LobSystem `DotNetAssembly` / `WebService` disabled | Medium | Disabled Jun 2025 CU (deprecated Sep 2024) | *By design* | Re-enable via documented farm property |
| I-04 | Workflows | SP2013 workflows + Classic Workflow Manager fail | High | Sep 2025 CU | Oct 2025 CU | Update SPWFM to Aug 2025 SPWFM CU (required before 2026-07-14 EoS anyway) |
| I-05 | Solutions | Solution deployment fails | High | Sep 2025 CU | Oct 2025 CU | None — install Oct 2025 CU |
| I-06 | Patching | Future SharePoint fixes fail to install (WSS_WPG / IIS_IUSRS perm) | High | Sep 2025 CU | Oct 2025 CU (code) but existing farms must remediate | Run `Fix-SeptemberCU-Permission-Problem.ps1` *or* remove `NT Authority\system` from `WSS_WPG` + `IIS_IUSRS` |
| I-07 | Services | SPAdminV4 fails on Windows Server 2025 | High | Sep 2025 CU | Mar 2026 CU | Downgrade Exploit Protection setting on OWSTIMER.EXE (doc'd) |
| I-08 | Health analyzer | False-positive: WSS_WPG elevated permissions | Low | Sep 2025 CU | Oct 2025 CU | Ignore rule |
| I-09 | Admin tools | PSCONFIG / Management Shell fail under Farm Service Account | Medium | Sep 2025 CU | *By design — do not use FSA interactively* | Use a dedicated admin account |
| I-10 | Web apps | AMSI enabled by default for all web apps | N/A (feature) | Sep 2025 CU | By design | Known "Module SPRequestFilterModule could not be found" with legacy customisations — see Oct 2023 CU trending-issue post |
| I-11 | Workflows | SP2010 workflows fail (CSC.EXE child-process blocked by Exploit Protection) — **also affects Nintex workflows** (same root cause, confirmed in Stefan's blog comments) | High | Sep 2025 CU | Feb 2026 CU | Temporarily relax Exploit Protection on OWSTIMER.EXE (doc'd) |
| I-12 | Secure Store | Group claim validation fails; stored creds can't be decrypted (new encryption algo) | High | Sep 2025 CU | Mar 2026 CU | Re-enter credentials / re-create target applications |
| I-13 | Worker process | w3wp crash `0xC0000409` in `owssvr.dll` | High | Sep 2025 CU | Feb 2026 CU | None effective; apply Feb 2026 CU |
| I-14 | Worker process | w3wp crash `0xC06D007E` / `0xE0434352` (KERNELBASE race) | High | Sep 2025 CU | Feb 2026 CU | None effective; apply Feb 2026 CU |
| I-15 | Modern UI | Text web part read-only while "Text and table formatting" pane open | Medium | Jan 2026 CU | *Not yet fixed at 2026-04-18* — monitor | Close formatting pane before editing text |
| I-16 | Upgrade / DB | `Invalid column name 'SAFE_NOTIFICATION_DATA'` when psconfig upgrades Jan 2026 schema to Mar 2026 CU | Critical (blocks upgrade) | Mar 2026 CU | Apr 2026 CU (complete fix) | Install Feb 2026 CU **first**, run Config Wizard, *then* Mar/Apr 2026 CU; or open MS support ticket if already broken |
| I-17 | Search / Timer Jobs | **QueryLogJobDefinition SQL connection pool exhaustion** — `QueryLogJobDefinition` fails with Event 6399: *"Timeout expired. The timeout period elapsed prior to obtaining a connection from the pool"*. Timer job leaks SQL connections on every run; pool (max 100) fills up after a few days causing cascading timer job failures. ULS signature: `QueryLogProcessor: AssignDocIdsToResults error: The method 'EndExecuteReader' cannot be called`. Reproducible on SPSE / SQL 2022 / WS2025 single-server farm. | High | Mar 2025 CU (regression) | Not fixed as of Oct 2025 (still open in Jul + Aug 2025 CU comments) | Disable the **Query Logging Timer Job** in Central Admin to stop connection leak. Restarting SPTimerV4 temporarily clears the pool. Source: [MS Q&A thread](https://learn.microsoft.com/en-us/answers/questions/5583482/many-critical-events-in-sharepoint-se-after-july-2) |

---

## 6. Upgrade matrix (recommended paths → latest = April 2026 CU)

| From | Recommended path to Apr 2026 CU | Intermediate stops | Rationale / blockers |
|---|---|---|---|
| **≤ Jun 2025 CU** (pre-ToolShell) | Jun → Apr 2026 CU directly | None technically required | You skip all Sep 2025 CU regressions because you never installed Sep 2025 CU. Verify BDC LobSystem deprecation impact (I-03). Rotate machine keys + hunt for `spinstall0.aspx` before patching. |
| **Jul 2025 CU** | Jul → Apr 2026 CU directly | None | Same as above; you cleanly jump over the Sep 2025 perm regression. Run `Test-DefenderAndAmsiWorkProperly` post-install. |
| **Aug 2025 CU** | Aug → Apr 2026 CU directly | None | Clean path; never touched the Sep 2025 perm damage. |
| **Sep 2025 CU** (on Windows Server 2022) | **Remediate → Apr 2026 CU** | *Must* run `Fix-SeptemberCU-Permission-Problem.ps1` OR remove `NT Authority\system` from `WSS_WPG`/`IIS_IUSRS` before installing any CU | Without remediation the CU install fails silently (I-06). Also update SPWFM to Aug 2025 SPWFM CU or later (I-04). |
| **Sep 2025 CU** (on Windows Server 2025) | Remediate perms → Apr 2026 CU | Same as above plus pick up SPAdminV4 WS2025 fix (shipped Mar 2026 CU) | SPAdminV4 stays broken until Mar 2026 CU is applied (I-07); Apr 2026 CU carries that fix. |
| **Oct 2025 CU** | Oct → Apr 2026 CU directly | None | No blockers. |
| **Nov 2025 CU** | Nov → Apr 2026 CU directly | None | |
| **Dec 2025 CU** | Dec → Apr 2026 CU directly | None | Carries w3wp 0xC0000409 / 0xC06D007E risk until installed (I-13, I-14); expedite. |
| **Jan 2026 CU** | Jan → **Feb 2026 CU** (run Config Wizard) → Apr 2026 CU | **Feb 2026 CU mandatory** | Skipping Feb causes the `SAFE_NOTIFICATION_DATA` upgrade failure (I-16). Alt: Jan → Apr 2026 CU directly is also safe (the complete fix ships in Apr 2026 CU), but Stefan's documented workaround is via Feb. |
| **Feb 2026 CU** | Feb → Apr 2026 CU directly | None | |
| **Mar 2026 CU (successful install from Feb 2026 CU)** | Mar → Apr 2026 CU directly | None | |
| **Mar 2026 CU (installed on top of Jan 2026 CU — farm broken)** | Open Microsoft Support ticket | MS engineering has a documented remediation | Do not attempt self-repair of the schema. |

### General SPSE patching procedure (all paths)

1. Read the target CU's Stefan post for last-minute blockers.
2. Back up all content + config DBs.
3. Install binaries on all SharePoint machines (any order).
4. Run **SharePoint Products Configuration Wizard** (`PSConfigUI.exe`) — Stefan recommends the UI over `psconfig.exe`.
5. After install, run `Test-DefenderAndAmsiWorkProperly` (Sep 2025+).
6. Verify machine-key rotation timer job is healthy (Sep 2025+).

---

## 7. Microsoft Learn & official references

- Product servicing policy: https://learn.microsoft.com/en-us/sharepoint/product-servicing-policy/updated-product-servicing-policy-for-sharepoint-server-se
- Servicing FAQ: https://learn.microsoft.com/en-us/sharepoint/product-servicing-policy/faq/faq-subscription-edition
- 25H2 feature update: https://learn.microsoft.com/en-us/SharePoint/what-s-new/new-and-improved-features-in-sharepoint-server-subscription-edition-25h1-release *(page also covers 25H2)*
- Deprecations (SP2010 workflows EoS 2026-07-14): https://learn.microsoft.com/en-us/sharepoint/what-s-new/what-s-deprecated-or-removed-from-sharepoint-server-subscription-edition#sharepoint-2010-workflows
- Office Online Server retirement: 2026-12-31 (announced Oct 2025).

## 8. Source log (fetch date: 2026-04-18)

| Label | URL |
|---|---|
| stefan-gossner-home | https://blog.stefan-gossner.com/ |
| stefan-2025-07 … stefan-2026-04 | Monthly archive pages |
| spse-2025-07-cu | https://blog.stefan-gossner.com/2025/07/08/july-2025-cu-for-sharepoint-server-subscription-edition-is-available-for-download/ |
| spse-2025-08-cu | https://blog.stefan-gossner.com/2025/08/12/august-2025-cu-for-sharepoint-server-subscription-edition-is-available-for-download/ |
| spse-2025-09-cu | https://blog.stefan-gossner.com/2025/09/09/september-2025-cu-for-sharepoint-server-subscription-edition-is-available-for-download/ |
| spse-2025-10-cu | https://blog.stefan-gossner.com/2025/10/14/october-2025-cu-for-sharepoint-server-subscription-edition-is-available-for-download/ |
| spse-2025-11-cu | https://blog.stefan-gossner.com/2025/11/11/november-2025-cu-for-sharepoint-server-subscription-edition-is-available-for-download/ |
| spse-2025-12-cu | https://blog.stefan-gossner.com/2025/12/09/december-2025-cu-for-sharepoint-server-subscription-edition-is-available-for-download/ |
| spse-2026-01-cu | https://blog.stefan-gossner.com/2026/01/13/january-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/ |
| spse-2026-02-cu | https://blog.stefan-gossner.com/2026/02/10/february-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/ |
| spse-2026-03-cu | https://blog.stefan-gossner.com/2026/03/10/march-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/ |
| spse-2026-04-cu | https://blog.stefan-gossner.com/2026/04/14/april-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/ |
| sep2025-issue-summary | https://blog.stefan-gossner.com/2025/09/25/summary-and-status-of-issues-identified-with-september-2025-cu-for-sharepoint/ |
| mar2026-psconfig-issue | https://blog.stefan-gossner.com/2026/03/12/trending-issue-spse-configuration-wizard-will-fail-for-upgrades-from-january-2026-cu-to-march-2026-cu/ |
| mslearn-critical-events-july2025 | https://learn.microsoft.com/en-us/answers/questions/5583482/many-critical-events-in-sharepoint-se-after-july-2 |
| exploit-protection-owstimer | https://blog.stefan-gossner.com/2025/09/16/trending-issue-sptimerv4-fails-to-start-on-windows-server-2025-after-installing-september-2025-cu/ |

All content in this knowledge base was indexed into the local context-mode sandbox (not stored verbatim in this file). Re-query via `ctx_search` against the listed source labels for verbatim quotes.
