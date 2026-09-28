# SharePoint Server Subscription Edition — CU Knowledge Base

**Coverage:** July 2025 CU → September 2026 CU
**Generated:** 2026-09-28
**Sources:** Stefan Goßner's blog (blog.stefan-gossner.com), Microsoft Support KB articles, Microsoft Download Center.

---

## 1. Overview

- SharePoint Server Subscription Edition (SPSE) ships a single **"uber" CU** every month (language-independent + language-dependent bundled).
- Starting with **August 2025 CU**, every monthly SPSE CU is also flagged as a **security update** (Microsoft recommends installing the full CU over individual security fixes).
- Stefan Goßner (Microsoft Senior Escalation Engineer) publishes the authoritative community commentary, including **known/trending issues** and upgrade guidance.
- Feature Update **25H2** shipped inside the September 2025 CU. Feature Update **26H1** shipped inside the June 2026 CU.
- **SharePoint Server 2016 and 2019 reached end of support on 2026-07-14/15** (MS Learn deprecations page says 2026-07-14; Stefan's own post is titled "July 15, 2026" — treat as the same cutover). **August 2026 CU was the final CU released for SharePoint 2016/2019** — no further CU/security posts for those versions appear in Stefan's archive after August 2026. SPSE remains the only actively-patched on-prem version going forward.

### How to use this document

- Section 3 (Current recommendation) tells you *what to install right now*.
- Section 4 lists every CU chronologically with build number, KB, fixes, regressions, and Stefan's verdict.
- Section 5 is a cross-CU issue index — find an issue once and see where it was introduced/fixed.
- Section 6 is the upgrade matrix — the exact path to take from any starting CU.

---

## 2. Build number / KB quick reference

| CU | Release | Build (16.0.x.y) | KB | Also security? |
|---|---|---|---|---|
| **Sep 2026** | 2026-09-09 | 16.0.20326.20136 | KB5002908 | Yes |
| Aug 2026 | 2026-08-11 | 16.0.19725.20522 | KB5002893 | Yes |
| Jul 2026 | 2026-07-14 | 16.0.19725.20434 | KB5002882 | Yes |
| Jun 2026 | 2026-06-09 | 16.0.19725.20384 | KB5002873 | Yes — ships **26H1** feature update |
| May 2026 | 2026-05-12 | 16.0.19725.20280 | KB5002863 | Yes |
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

Note the build-number jump from `16.0.19725.x` (May–Aug 2026) to `16.0.20326.x` (Sep 2026) — a larger jump than the usual monthly increment. Not called out as anything unusual by Stefan; recorded here for administrators tracking build baselines.

---

## 3. Current recommendation (as of 2026-09-28)

**Target: September 2026 CU (KB5002908, build 16.0.20326.20136).**

Reasons:
1. Latest available monthly security rollup (also flagged as a security update, as every CU has been since Aug 2025); specific CVE list not captured from the source post — consult KB5002908 for the CVE table.
2. No install-blocking caution banner from Stefan for the CU itself; the one trending issue introduced by this CU (InfoPath Forms + SP2010 workflows, **I-27**) has an interim fix already published (**KB5002927**) and does not block the core install.
3. Rolls up the permanent fix Stefan indicated for the Aug 2026 Distributed Cache regression (**I-23**) — not independently re-confirmed in the Sep 2026 CU post itself, so verify in your environment.
4. Every monthly CU since Aug 2025 is also a security update; skipping CUs leaves CVEs unpatched.

**Still open at time of writing (carry-forward risk, does not block installing Sep 2026 CU):**
- **I-24** — BCS `BCSAllowedTypeNames` allowlist restriction (introduced Aug 2026 CU) — explicitly *not resolved* as of the latest Sep 2026 comments.
- **I-25** — Document ID Service no longer returns Document ID values for existing Document Sets (introduced Aug 2026 CU) — no fix confirmed.
- **I-17** — `QueryLogJobDefinition` SQL connection pool exhaustion — open since Mar 2025 CU, still no official fix.

**If you use InfoPath Forms Services with SharePoint 2010 workflows:** after installing Sep 2026 CU, also apply **KB5002927** (interim fix) and follow the 3-step mitigation in **I-27**. Note publishing **new** SP2010 workflows is permanently disabled going forward regardless of the fix — migrate to SP2013 workflows or Power Automate.

**Prerequisites when the source farm is Sep 2025 CU:** run
[`Fix-SeptemberCU-Permission-Problem.ps1`](https://aka.ms/stefangossner/Fix-SeptemberCU-Permission-Problem.ps1)
*before* applying any subsequent CU, or else the install fails with "future SharePoint fixes cannot be installed". Alternatively remove `NT Authority\system` from `WSS_WPG` and `IIS_IUSRS` local groups on every SharePoint machine. **This prereq is still called out in every monthly post through Sep 2026** — it has not expired.

**Do NOT install:** the Mar 2026 CU **on top of** Jan 2026 CU without the Feb 2026 CU intermediate (see Upgrade Matrix §6).

---

## 4. Per-CU details (newest first)

### September 2026 CU — KB5002908 — build 16.0.20326.20136 — 2026-09-09
- **Verdict (Stefan):** recommended — routine security rollup; one trending issue surfaced 12 days after release, interim fix already shipped.
- **Highlights:** Monthly security rollup (specific CVE list not captured from source post — consult KB5002908). Build number jumps to the `16.0.20326.x` baseline (from `16.0.19725.x`).
- **Fixes:** Permanent fix for the Aug 2026 CU Distributed Cache "cannot add service instance" regression (**I-23**) — per Stefan's Aug 2026 post, which stated a permanent fix was planned for this CU; not independently re-confirmed in the Sep 2026 post itself.
- **Known issues introduced:** InfoPath Forms Services + SP2010 workflow failures (**I-27**) — interim fix KB5002927 published between the Sep and (expected) Oct 2026 CU.
- **Open issues carried forward, not fixed by this CU:** BCS allowlist restriction (**I-24**), Document ID Service regression (**I-25**), QueryLogJobDefinition SQL pool exhaustion (**I-17**).
- **Prereq:** if farm is still on Sep 2025 CU, apply `Fix-SeptemberCU-Permission-Problem.ps1` first — banner still present in this month's post. Configuration Wizard must be run on each farm machine after install.
- **Sources:**
  - https://blog.stefan-gossner.com/2026/09/09/september-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/
  - https://blog.stefan-gossner.com/2026/09/09/sharepoint-security-fixes-released-with-september-2026-pu-and-offered-through-microsoft-update/
  - https://blog.stefan-gossner.com/2026/09/21/trending-issue-infopath-forms-issues-with-sp2010-workflows-after-september-2026-cu/
  - KB: https://support.microsoft.com/en-us/kb/5002908

### August 2026 CU — KB5002893 — build 16.0.19725.20522 — 2026-08-11
- **Verdict (Stefan):** recommended with caveats — install, but be aware of four issues below; this was the **final CU released for SharePoint Server 2016/2019** (both reached end of support 2026-07-14/15).
- **Highlights:** Monthly security rollup (CVE list not captured from source post).
- **Fixes:** OOS/SP2016 WOPI 401 integration failure from July 2026 CU (**I-21**); workflow status link double-encoding from July 2026 CU (**I-22**).
- **Known issues introduced:**
  - Distributed Cache: cannot add new distributed cache service instances (**I-23**) — temporary workaround via server debug flag; permanent fix planned for Sep 2026 CU.
  - BCS type allowlist restriction blocks BCS models/external content types using non-allowlisted .NET types, e.g. `Nullable\`1` (**I-24**) — **still open as of Sep 2026**.
  - Document ID Service regression: existing Document Sets stop returning Document ID values; affected assemblies must be added to the farm allowlist (**I-25**) — no fix confirmed.
  - Remote Event Receivers without app identifiers are blocked from registering — by design; migrate to provider-hosted SharePoint Add-ins (**I-26**).
- **Prereq:** if farm is still on Sep 2025 CU, apply `Fix-SeptemberCU-Permission-Problem.ps1` first.
- **Sources:**
  - https://blog.stefan-gossner.com/2026/08/11/august-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/
  - https://blog.stefan-gossner.com/2026/08/11/sharepoint-security-fixes-released-with-august-2026-pu-and-offered-through-microsoft-update/
  - https://blog.stefan-gossner.com/2026/08/14/trending-issue-bcs-type-is-not-in-the-bcsallowedtypenames-generic-list-after-august-2026-cu/
  - https://blog.stefan-gossner.com/2026/08/14/resolved-trending-issue-invalid-workflowinstanceid-parameter-in-url-after-july-2026-cu-for-sharepoint/
  - https://blog.stefan-gossner.com/2026/08/14/resolved-trending-issue-office-online-server-oos-integration-with-sp2016-fails-after-installing-july-2026-cu/
  - https://blog.stefan-gossner.com/2026/07/15/sharepoint-end-of-support-what-changed-on-july-15-2026/
  - KB: https://support.microsoft.com/en-us/kb/5002893

### July 2026 CU — KB5002882 — build 16.0.19725.20434 — 2026-07-14
- **Verdict (Stefan):** install with awareness — three known issues surfaced this month, two fixed the following month.
- **Highlights:** Monthly security rollup (CVE list not captured from source post). **2026-07-14/15: SharePoint Server 2016 and 2019 reach end of support** (this CU shipped the same week).
- **Fixes:** Complete fix for the June 2026 CU SP2010 workflow failure (**I-19**), landed for 2016/2019/SE.
- **Known issues introduced:**
  - SP2010 workflows still fail post-fix in some cases — stricter XOML type validation requires additional web.config allowlist entries (`Fix-SystemCodeDom.ps1` provided) (**I-20**) — not stated as fixed in a later CU.
  - Office Online Server integration with SP2016 fails with WOPI 401 errors — fail-open→fail-closed token validation hardening (**I-21**) — fixed Aug 2026 CU.
  - Workflow status links (`WrkStat.aspx`) double-encode the `WorkflowInstanceID` parameter, breaking workflow history access; same issue affects InfoPath task forms (`WrkTaskIP.aspx`) (**I-22**) — fixed Aug 2026 CU.
- **Prereq:** if farm is still on Sep 2025 CU, apply `Fix-SeptemberCU-Permission-Problem.ps1` first.
- **Sources:**
  - https://blog.stefan-gossner.com/2026/07/14/july-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/
  - https://blog.stefan-gossner.com/2026/07/14/sharepoint-security-fixes-released-with-july-2026-pu-and-offered-through-microsoft-update/
  - https://blog.stefan-gossner.com/2026/07/17/trending-issue-sharepoint-2010-workflows-are-failing-after-installing-july-2026-cu/
  - https://blog.stefan-gossner.com/2026/07/17/trending-issue-office-online-server-oos-integration-with-sp2016-fails-after-installing-july-2026-cu/
  - https://blog.stefan-gossner.com/2026/07/22/trending-issue-invalid-workflowinstanceid-parameter-in-url-after-july-2026-cu-for-sharepoint/
  - https://blog.stefan-gossner.com/2026/07/15/sharepoint-end-of-support-what-changed-on-july-15-2026/
  - KB: https://support.microsoft.com/en-us/kb/5002882

### June 2026 CU — KB5002873 — build 16.0.19725.20384 — 2026-06-09
- **Verdict (Stefan):** install with awareness — ships a feature update; SP2010 workflow regression fixed the following month.
- **Highlights:** Ships Feature Update **26H1**. Monthly security rollup (CVE list not captured from source post).
- **Fixes:** none carried in from prior open issues (none pending at the time).
- **Known issues introduced:** SP2010-style workflows fail with "Failed to Start" / "Potentially malicious" XOML errors — stricter workflow-code validation flags legitimate constructs (**I-19**) — fixed July 2026 CU. Temporary workaround (`$farm.EnablePreParseSecurityCheckForWorkflow = $false`) disables a large set of workflow security fixes and should be reverted once patched.
- **Prereq:** if farm is still on Sep 2025 CU, apply `Fix-SeptemberCU-Permission-Problem.ps1` first.
- **Sources:**
  - https://blog.stefan-gossner.com/2026/06/09/june-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/
  - https://blog.stefan-gossner.com/2026/06/09/feature-update-26h1-for-sharepoint-server-subscription-edition-has-been-released-today/
  - https://blog.stefan-gossner.com/2026/06/09/sharepoint-security-fixes-released-with-june-2026-pu-and-offered-through-microsoft-update/
  - https://blog.stefan-gossner.com/2026/06/12/trending-issue-sharepoint-2010-workflows-fail-after-june-2026-cu/
  - KB: https://support.microsoft.com/en-us/kb/5002873

### May 2026 CU — KB5002863 — build 16.0.19725.20280 — 2026-05-12
- **Verdict (Stefan):** recommended — no caution banner; no trending-issue posts published as of 2026-05-18.
- **Highlights:** Monthly security rollup. Patches **two Critical RCE CVEs** (CVE-2026-40365, CVE-2026-40367) and four Important RCEs (CVE-2026-33110, CVE-2026-33112, CVE-2026-35439, CVE-2026-40357) across SharePoint 2016/2019/SE.
- **Known issues introduced:** none identified at time of writing.
- **I-15 / I-17 status:** Text web part read-only regression (I-15) and QueryLogJobDefinition SQL pool exhaustion (I-17) are **still open** — not fixed in this CU.
- **Prereq:** if farm is still on Sep 2025 CU, apply `Fix-SeptemberCU-Permission-Problem.ps1` first. Farms on Jul 2025 CU (or later) can upgrade directly to May 2026 CU (confirmed by Stefan in post comments).
- **Sources:**
  - https://blog.stefan-gossner.com/2026/05/12/may-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/
  - https://blog.stefan-gossner.com/2026/05/12/sharepoint-security-fixes-released-with-may-2026-pu-and-offered-through-microsoft-update/
  - KB: https://support.microsoft.com/en-us/kb/5002863
  - Download: https://www.microsoft.com/en-us/download/details.aspx?id=108655

### April 2026 CU — KB5002853 — build 16.0.19725.20210 — 2026-04-14
- **Verdict (Stefan):** recommended.
- **Highlights:** Complete fix for the Jan→Mar upgrade `SAFE_NOTIFICATION_DATA` regression. Monthly security rollup.
- **Known issues introduced:** none from the CU itself, but the **April 14, 2026 Windows Update** (CVE-2026-20833 hardening) ships the same day and breaks Kerberos for farms whose service accounts lack AES encryption flags in AD — see **I-18**.
- **Prereq:** if farm is still on Sep 2025 CU, apply `Fix-SeptemberCU-Permission-Problem.ps1` first.
- **Sources:**
  - https://blog.stefan-gossner.com/2026/04/14/april-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/
  - Trending issue (Kerberos): https://blog.stefan-gossner.com/2026/04/23/trending-issues-kerberos-failures-in-sharepoint-and-other-applications-starting-april-2026/
  - MS Learn (Kerberos AES config): https://learn.microsoft.com/en-us/troubleshoot/sharepoint/security/configuration-to-support-kerberos-aes-encryption
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
- **I-17 still present:** New community reports of `QueryLogJobDefinition` SQL connection pool exhaustion surfaced specifically after this CU (Mar 2026). Microsoft confirmed no official fix as of Apr 2026.
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
- **Known issue carried forward (I-17):** `QueryLogJobDefinition` SQL connection pool exhaustion — introduced Mar 2025 CU, still present through Apr 2026 CU with no official fix. Manifests as Event ID 6399 critical errors a few days after server restart. See Section 5 for details and workarounds.
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
| I-15 | Modern UI | Text web part read-only while "Text and table formatting" pane open | Medium | Jan 2026 CU | *Not yet fixed at 2026-05-18* — monitor | Close formatting pane before editing text |
| I-16 | Upgrade / DB | `Invalid column name 'SAFE_NOTIFICATION_DATA'` when psconfig upgrades Jan 2026 schema to Mar 2026 CU | Critical (blocks upgrade) | Mar 2026 CU | Apr 2026 CU (complete fix) | Install Feb 2026 CU **first**, run Config Wizard, *then* Mar/Apr 2026 CU; or open MS support ticket if already broken |
| I-18 | Kerberos / AD / Windows Update | **Kerberos authentication failures after April 2026 Windows Update (CVE-2026-20833).** April 14, 2026 Windows Update removes RC4 fallback from KDC. SharePoint service/app-pool accounts without AES encryption flags in AD cannot complete Kerberos handshake. ULS errors: `A call to SSPI failed` / `The encryption type requested is not supported by the KDC`. Affects Central Admin access, Search Admin, User Profile Sync, and other service applications. Not a SPSE CU regression — caused by OS-level security hardening. | High | Windows Apr 2026 Update (external) | N/A — fix is in AD | Enable "AES 128 bit" and "AES 256 bit encryption" on every SharePoint service and app-pool account in AD Users and Computers → Account tab → Account Options. Then run `iisreset` and restart affected services. Ref: KB 5073381, CVE-2026-20833. MS Learn: [SharePoint Kerberos AES config](https://learn.microsoft.com/en-us/troubleshoot/sharepoint/security/configuration-to-support-kerberos-aes-encryption). |
| I-19 | Workflows | SP2010 workflows fail ("Failed to Start" / "Potentially malicious" XOML) — stricter workflow-code validation | High | Jun 2026 CU | Jul 2026 CU | Temp: `$farm.EnablePreParseSecurityCheckForWorkflow = $false` (revert once patched — disables many workflow security fixes) |
| I-20 | Workflows | SP2010 workflows still fail after Jul 2026 CU fix — additional types need allowlisting in web.config (XOML type validation) | High | Jul 2026 CU | *Not stated as fixed* — monitor | Add `System.CodeDom`, `Microsoft.SharePoint.WorkflowActions`, `Microsoft.Office.Workflow.Actions` to web.config authorizedType entries; automatable via `Fix-SystemCodeDom.ps1`. Temp: same `EnablePreParseSecurityCheckForWorkflow` flag as I-19 |
| I-21 | Office Online Server | OOS integration with SP2016 fails — WOPI 401 Unauthorized (fail-closed token validation hardening) | High | Jul 2026 CU | Aug 2026 CU | Register farm's own STS as a trusted issuer via `New-SPTrustedSecurityTokenIssuer`, then `iisreset` on every server |
| I-22 | Workflows | Workflow status links (`WrkStat.aspx`) double-encode `WorkflowInstanceID`, breaking workflow history; same bug affects InfoPath task forms (`WrkTaskIP.aspx`) | High | Jul 2026 CU | Aug 2026 CU | Manually fix double-encoded `%25`→`%` in URLs; access via ellipsis menu → Workflows; or URL Rewrite rule per KB5122408 |
| I-23 | Distributed Cache | Cannot add new distributed cache service instances | High | Aug 2026 CU | Sep 2026 CU (planned per Stefan's Aug post; not independently re-confirmed) | Temporary: `$farm.ServerDebugFlags.Add(59052)` |
| I-24 | BCS | Business Connectivity Services blocks types (e.g. `Nullable\`1`) not in the `BCSAllowedTypeNames` allowlist | High | Aug 2026 CU | **Not fixed — open as of Sep 2026** | Manually add required types via PowerShell, sourced from ULS event `36px6` entries; 14+ entries needed in some search-crawl scenarios |
| I-25 | Document ID Service | Existing Document Sets no longer return Document ID values | High | Aug 2026 CU | *Not confirmed fixed* — monitor | Add affected assemblies to the farm allowlist (new security restriction enforcement) |
| I-26 | Remote Event Receivers | RERs without app identifiers blocked from registering | Medium (by design) | Aug 2026 CU | *By design* — no fix planned | Migrate to provider-hosted SharePoint Add-in model |
| I-27 | InfoPath / Workflows | InfoPath Forms Services + SP2010 workflows fail (rendering/compatibility errors) | High | Sep 2026 CU | Interim fix: **KB5002927** (between Sep and Oct 2026 CU) | Install KB5002927 (no Config Wizard) → run PowerShell to set debug flag 5023 + enable browser rendering → run Config Wizard. **Publishing new SP2010 workflows remains permanently disabled** regardless — migrate to SP2013 workflows or Power Automate |
| I-17 | Search / Timer Jobs | **QueryLogJobDefinition SQL connection pool exhaustion** — `QueryLogJobDefinition` fails with Event 6399: *"Timeout expired. The timeout period elapsed prior to obtaining a connection from the pool"*. Timer job leaks SQL connections on every run; pool (max 100) fills up after a few days causing cascading timer job failures. ULS signature: `QueryLogProcessor: AssignDocIdsToResults error: The method 'EndExecuteReader' cannot be called`. **Still present after Mar 2026 CU (KB5002843), Apr 2026 CU (KB5002853), and May 2026 CU (KB5002863) — no official fix published as of May 2026.** Not independently re-verified against Jun–Sep 2026 CUs during this update pass (no new Stefan post or MS Q&A activity surfaced); treat as still open until confirmed otherwise. Microsoft confirmed investigating but no KB article or fix released. | High | Mar 2025 CU (regression) | **Not fixed — open as of 2026-09 (last independently confirmed May 2026)** | (1) Disable the **Query Logging Timer Job** in Central Admin (most effective). (2) Schedule a nightly restart of `SPTimerV4` to clear the pool every 48–72 hrs. (3) Increase SQL pool size as short-term delay: add `Max Pool Size=200` to the Search connection string. Sources: [Oct 2025 Q&A](https://learn.microsoft.com/en-us/answers/questions/5583482/many-critical-events-in-sharepoint-se-after-july-2) · [Mar 2026 Q&A #1](https://learn.microsoft.com/en-us/answers/questions/5816641/querylogjobdefinition-may-be-exhausting-the-sql-co) · [Mar 2026 Q&A #2](https://learn.microsoft.com/en-us/answers/questions/5849106/search-service-sql-connection-pool-exhaustion-afte) · **Monitored** by `weekly_check.py` (3 answers as of 2026-05-18; new answers trigger GitHub issue) |

---

## 6. Upgrade matrix (recommended paths → latest = September 2026 CU)

| From | Recommended path to Sep 2026 CU | Intermediate stops | Rationale / blockers |
|---|---|---|---|
| **≤ Jun 2025 CU** (pre-ToolShell) | Jun → Sep 2026 CU directly | None technically required | You skip all Sep 2025 CU regressions because you never installed Sep 2025 CU. Verify BDC LobSystem deprecation impact (I-03). Rotate machine keys + hunt for `spinstall0.aspx` before patching. |
| **Jul 2025 CU** | Jul → Sep 2026 CU directly | None | Confirmed by Stefan in May 2026 CU comments. Cleanly jumps over the Sep 2025 perm regression. Run `Test-DefenderAndAmsiWorkProperly` post-install. |
| **Aug 2025 CU** | Aug → Sep 2026 CU directly | None | Clean path; never touched the Sep 2025 perm damage. |
| **Sep 2025 CU** (on Windows Server 2022) | **Remediate → Sep 2026 CU** | *Must* run `Fix-SeptemberCU-Permission-Problem.ps1` OR remove `NT Authority\system` from `WSS_WPG`/`IIS_IUSRS` before installing any CU | Without remediation the CU install fails silently (I-06). Also update SPWFM to Aug 2025 SPWFM CU or later (I-04). This prereq banner is *still* present in the Sep 2026 CU post. |
| **Sep 2025 CU** (on Windows Server 2025) | Remediate perms → Sep 2026 CU | Same as above plus pick up SPAdminV4 WS2025 fix (shipped Mar 2026 CU) | SPAdminV4 stays broken until Mar 2026 CU is applied (I-07); Sep 2026 CU carries that fix forward. |
| **Oct 2025 CU** | Oct → Sep 2026 CU directly | None | No blockers. |
| **Nov 2025 CU** | Nov → Sep 2026 CU directly | None | |
| **Dec 2025 CU** | Dec → Sep 2026 CU directly | None | Carries w3wp 0xC0000409 / 0xC06D007E risk until installed (I-13, I-14); expedite. |
| **Jan 2026 CU** | Jan → **Feb 2026 CU** (run Config Wizard) → Sep 2026 CU | **Feb 2026 CU mandatory** | Skipping Feb causes the `SAFE_NOTIFICATION_DATA` upgrade failure (I-16). Apr 2026 CU onward also contains the complete fix, but Stefan's documented workaround is via Feb first. |
| **Feb 2026 CU** | Feb → Sep 2026 CU directly | None | |
| **Mar 2026 CU (successful install from Feb 2026 CU)** | Mar → Sep 2026 CU directly | None | |
| **Mar 2026 CU (installed on top of Jan 2026 CU — farm broken)** | Open Microsoft Support ticket | MS engineering has a documented remediation | Do not attempt self-repair of the schema. |
| **Apr 2026 CU** | Apr → Sep 2026 CU directly | None | |
| **May 2026 CU** | May → Sep 2026 CU directly | None | |
| **Jun 2026 CU** | Jun → Sep 2026 CU directly | None | Picks up the Jul 2026 CU fix for the SP2010 "Failed to Start" workflow regression (I-19) along the way. |
| **Jul 2026 CU** | Jul → Sep 2026 CU directly | None | Picks up Aug 2026 CU fixes for OOS/SP2016 WOPI 401 (I-21) and workflow-status double-encoding (I-22) along the way. I-20 (SP2010 workflow allowlist) remains open — plan the web.config/`Fix-SystemCodeDom.ps1` workaround regardless of target CU. |
| **Aug 2026 CU** | Aug → Sep 2026 CU directly | None | Distributed Cache regression (I-23) has its planned permanent fix in Sep 2026 CU. BCS allowlist (I-24) and Document ID Service (I-25) issues remain open after upgrading — plan workarounds. If on SharePoint 2016/2019: **Aug 2026 was the final CU for those versions** — there is no upgrade path to Sep 2026 CU on 2016/2019; migrate to SPSE. |

**Note on SharePoint 2016/2019 farms:** with end of support 2026-07-14/15 and August 2026 CU being the last release for those versions, any farm still on SP2016/2019 has no further CU path — plan a migration to SPSE rather than an in-place upgrade.

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
- SharePoint Server 2016/2019 end of support: 2026-07-14/15 — https://blog.stefan-gossner.com/2026/07/15/sharepoint-end-of-support-what-changed-on-july-15-2026/
- 26H1 feature update: https://blog.stefan-gossner.com/2026/06/09/feature-update-26h1-for-sharepoint-server-subscription-edition-has-been-released-today/

## 8. Source log (fetch date: 2026-09-28)

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
| kerberos-apr2026 | https://blog.stefan-gossner.com/2026/04/23/trending-issues-kerberos-failures-in-sharepoint-and-other-applications-starting-april-2026/ |
| mslearn-kerberos-aes-sp | https://learn.microsoft.com/en-us/troubleshoot/sharepoint/security/configuration-to-support-kerberos-aes-encryption |
| spse-2026-05-cu | https://blog.stefan-gossner.com/2026/05/12/may-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/ |
| spse-2026-05-pu | https://blog.stefan-gossner.com/2026/05/12/sharepoint-security-fixes-released-with-may-2026-pu-and-offered-through-microsoft-update/ |
| sep2025-issue-summary | https://blog.stefan-gossner.com/2025/09/25/summary-and-status-of-issues-identified-with-september-2025-cu-for-sharepoint/ |
| mar2026-psconfig-issue | https://blog.stefan-gossner.com/2026/03/12/trending-issue-spse-configuration-wizard-will-fail-for-upgrades-from-january-2026-cu-to-march-2026-cu/ |
| mslearn-critical-events-july2025 | https://learn.microsoft.com/en-us/answers/questions/5583482/many-critical-events-in-sharepoint-se-after-july-2 |
| mslearn-querylog-pool-5816641 | https://learn.microsoft.com/en-us/answers/questions/5816641/querylogjobdefinition-may-be-exhausting-the-sql-co |
| mslearn-querylog-pool-mar2026 | https://learn.microsoft.com/en-us/answers/questions/5849106/search-service-sql-connection-pool-exhaustion-afte |
| exploit-protection-owstimer | https://blog.stefan-gossner.com/2025/09/16/trending-issue-sptimerv4-fails-to-start-on-windows-server-2025-after-installing-september-2025-cu/ |
| spse-2026-06-cu | https://blog.stefan-gossner.com/2026/06/09/june-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/ |
| feature-26h1 | https://blog.stefan-gossner.com/2026/06/09/feature-update-26h1-for-sharepoint-server-subscription-edition-has-been-released-today/ |
| jun2026-workflow-issue | https://blog.stefan-gossner.com/2026/06/12/trending-issue-sharepoint-2010-workflows-fail-after-june-2026-cu/ |
| spse-2026-07-cu | https://blog.stefan-gossner.com/2026/07/14/july-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/ |
| jul2026-workflow-issue | https://blog.stefan-gossner.com/2026/07/17/trending-issue-sharepoint-2010-workflows-are-failing-after-installing-july-2026-cu/ |
| jul2026-oos-sp2016-issue | https://blog.stefan-gossner.com/2026/07/17/trending-issue-office-online-server-oos-integration-with-sp2016-fails-after-installing-july-2026-cu/ |
| jul2026-workflowid-issue | https://blog.stefan-gossner.com/2026/07/22/trending-issue-invalid-workflowinstanceid-parameter-in-url-after-july-2026-cu-for-sharepoint/ |
| sp2016-2019-eos | https://blog.stefan-gossner.com/2026/07/15/sharepoint-end-of-support-what-changed-on-july-15-2026/ |
| spse-2026-08-cu | https://blog.stefan-gossner.com/2026/08/11/august-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/ |
| aug2026-bcs-issue | https://blog.stefan-gossner.com/2026/08/14/trending-issue-bcs-type-is-not-in-the-bcsallowedtypenames-generic-list-after-august-2026-cu/ |
| aug2026-oos-resolved | https://blog.stefan-gossner.com/2026/08/14/resolved-trending-issue-office-online-server-oos-integration-with-sp2016-fails-after-installing-july-2026-cu/ |
| aug2026-workflowid-resolved | https://blog.stefan-gossner.com/2026/08/14/resolved-trending-issue-invalid-workflowinstanceid-parameter-in-url-after-july-2026-cu-for-sharepoint/ |
| spse-2026-09-cu | https://blog.stefan-gossner.com/2026/09/09/september-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/ |
| spse-2026-09-pu | https://blog.stefan-gossner.com/2026/09/09/sharepoint-security-fixes-released-with-september-2026-pu-and-offered-through-microsoft-update/ |
| sep2026-infopath-issue | https://blog.stefan-gossner.com/2026/09/21/trending-issue-infopath-forms-issues-with-sp2010-workflows-after-september-2026-cu/ |

This 2026-09-28 update was performed manually (GitHub Actions workflow `weekly-check.yml` remains disabled — `if: false` — per prior user request) using direct `WebFetch` against Stefan Goßner's blog, since the context-mode MCP sandbox used for prior updates was unavailable this session. `.weekly-state.json` was left untouched by this update; it still reflects the last automated-check baseline (May 2026 CU) and does not track Jun–Sep 2026.

All content in this knowledge base was indexed into the local context-mode sandbox (not stored verbatim in this file). Re-query via `ctx_search` against the listed source labels for verbatim quotes.
