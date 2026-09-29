# SharePoint Server Subscription Edition — CU Knowledge Base

**Coverage:** July 2025 CU → September 2026 CU
**Generated:** 2026-09-28 · **Comment-analysis revision:** 2026-09-29 (all posts + all comments after 2026-06-01 re-read; see §5A)
**Sources:** Stefan Goßner's blog (blog.stefan-gossner.com) — posts **and reader comments** (Stefan's replies are treated as authoritative, unreplied reader reports as *unconfirmed*) — plus Microsoft Support KB articles and Microsoft Download Center.

---

## 1. Overview

- SharePoint Server Subscription Edition (SPSE) ships a single **"uber" CU** every month (language-independent + language-dependent bundled).
- Starting with **August 2025 CU**, every monthly SPSE CU is also flagged as a **security update** (Microsoft recommends installing the full CU over individual security fixes).
- Stefan Goßner (Microsoft Senior Escalation Engineer) publishes the authoritative community commentary, including **known/trending issues** and upgrade guidance.
- Feature Update **25H2** shipped inside the September 2025 CU. Feature Update **26H1** shipped inside the June 2026 CU.
- **Deprecation timeline (see §5A.2):** SP2010 workflows + InfoPath Forms Services EoS 2026-07-14 → disabled by default in the **Sep 2026 CU**; SP2013 workflows disabled by default in the **Oct 2026 CU**; orphaned Remote Event Receivers blocked in the **Nov 2026 CU**; Office Online Server retirement 2026-12-31.
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
| Sep 2026 + KB5002927 | 2026-09-21 | 16.0.20326.20158 | KB5002927 | Intermediate fix (supersedes Sep CU; InfoPath/SP2010 re-enable). Do *not* run Config Wizard until the script has run |
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

## 3. Current recommendation (as of 2026-09-29)

**Target: September 2026 CU (KB5002908, build 16.0.20326.20136) — with the pre-flight checklist below. If you use SP2010 workflows or InfoPath Forms, install the intermediate fix KB5002927 (build 16.0.20326.20158, includes the Sep 2026 CU) instead, then run the InfoPath script (I-27).**

Reasons:
1. Latest available monthly security rollup (also flagged as a security update, as every CU has been since Aug 2025). Skipping CUs leaves CVEs unpatched; CUs are cumulative, so no intermediate CU is ever required (Stefan, Jul 2026 comments) — except the Jan→Feb 2026 chain (I-16).
2. Stefan has issued no install-blocking banner for the CU, **but the Sep 2026 CU is the most behaviour-changing CU in the window**: it disables SP2010 workflows, InfoPath Forms Services and the web-part ToolPane by default and breaks event receivers registered against old assembly versions. It is safe to install *only after* the pre-flight checklist. Comments show the June 2026 → Sep 2026 CUs were each a "landmine" release (see §5A.1).
3. **Correction to the previous revision:** the Sep 2026 CU does **not** contain the fix for the Aug 2026 Distributed Cache regression (**I-23**). Stefan (2026-09-09): *"this fix is still in development"*; a commenter says it is targeted for the Oct 2026 CU (unofficial). The `59052` debug-flag workaround is still required to provision new DCache hosts.
4. The 2026-09-09 package was **re-uploaded** after first publication; a package downloaded before the KB article went live fails PSConfig with `SPMissingAttributeException … RegisterInfoPathDeprecationHttpModule`. Verify the installed build is exactly **16.0.20326.20136** (or `.20158` for KB5002927) in Central Admin → Patch status; re-download otherwise (I-41).

### Pre-flight checklist before installing Sep 2026 CU (from post-June comment analysis)
- [ ] **Enable legacy workflows per site collection *before* patching** (Sep CU disables SP2010 workflows on *all* site collections; Oct CU will do the same for SP2013): `Enable-SPLegacyWorkflow <url>` / `Enable-SPWorkflow2013 <url>` — available once Aug 2026 CU is installed. Sep CU has an *allow-list only* (the Aug `Get-SPLegacyWorkflowDisabledSites` cmdlet no longer exists). See I-38.
- [ ] `Enable-SPToolPane` if editors need classic web-part editing (I-36).
- [ ] Inventory **event receivers registered against old assembly versions** (`Version=15.0.0.0`, `14.0.0.0`, `12.0.0.0`, custom assembly redirects) — these fail to load after Sep CU and break workflow auto-start, subsite creation and third-party solutions (I-35).
- [ ] Pre-seed farm allow-lists: `AllowedDLCAssemblies` (DocumentManagement 15.0.0.0/14.0.0.0 — I-25), `BCSAllowedTypeNames` (I-24), `SPAllowedOutboundHosts` (I-32).
- [ ] Do **not** add/convert Distributed Cache hosts during patching (I-23); use graceful stop (`-ShouldGracefulStopDCache $true`) instead of removing the instance.
- [ ] After installing, confirm the **`System.CodeDom` / `Microsoft.SharePoint.WorkflowActions` / `Microsoft.Office.Workflow.Actions` authorizedType entries are still present in every web.config** (three commenters lost one after the Aug 2026 CU — I-20).
- [ ] If SQL Always On: remove `WSS_Logging` from the AG while PSConfig runs (I-41).

**Still open at time of writing (carry-forward risk, does not block installing Sep 2026 CU):**
- **I-23** — Distributed Cache host provisioning (Aug 2026 CU) — fix *not* in Sep 2026 CU.
- **I-33** — Search topology / admin component not healthy after patch (reported since Apr 2026 CU) — Stefan (2026-08-13): *"this has been reported already starting with April CU. No, this was not fixed."*
- **I-43** — HTTP throttling / 503 on User Profile cache endpoints after Jun 2026 CU — no root cause; support cases open.
- **I-17** — `QueryLogJobDefinition` SQL connection pool exhaustion — open since Mar 2025 CU, still no official fix.
- **I-42** — several single-reporter modern-UI/JSOM regressions (see §5A.5), unacknowledged.

**Resolved since previous revision:** **I-15** (Text web part read-only) was fixed in the **June 2026 CU** (Stefan's "resolved trending issue" post, 2026-07-02) — the earlier "not yet fixed" status was stale. **I-25** (Document ID) has a confirmed root cause and fix (allow-list `AllowedDLCAssemblies`). **I-28/I-29/I-31** (Jul 2026 actor-token, session-cookie/DCache, PictureURL) were fixed by the Aug 2026 CU.

**Prerequisites when the source farm is Sep 2025 CU:** run
[`Fix-SeptemberCU-Permission-Problem.ps1`](https://aka.ms/stefangossner/Fix-SeptemberCU-Permission-Problem.ps1)
*before* applying any subsequent CU, or else the install fails with "future SharePoint fixes cannot be installed" (MSI error 1603). Alternatively remove `NT Authority\system` from `WSS_WPG` and `IIS_IUSRS` local groups on every SharePoint machine. **This prereq is still called out in every monthly post through Sep 2026** — it has not expired. It is *not* needed for farms that never installed Sep 2025 CU (Stefan, 2026-07-19). For **new** farms: RTM + language packs → latest CU; *skip* Sep 2025 CU (Stefan, 2026-06-10).

**Do NOT install:** the Mar 2026 CU **on top of** Jan 2026 CU without the Feb 2026 CU intermediate (see Upgrade Matrix §6).

---

## 4. Per-CU details (newest first)

### September 2026 CU — KB5002908 — build 16.0.20326.20136 — 2026-09-09
- **Verdict (Stefan):** recommended — routine security rollup; one trending issue surfaced 12 days after release, interim fix already shipped.
- **Highlights:** Monthly security rollup (specific CVE list not captured from source post — consult KB5002908). Build number jumps to the `16.0.20326.x` baseline (from `16.0.19725.x`).
- **Fixes:** none carried over from prior open issues. *(The previous revision wrongly listed the Aug 2026 Distributed Cache fix (I-23) here; Stefan confirmed on 2026-09-09 that it is still in development.)*
- **Known issues introduced:** InfoPath Forms Services + SP2010 workflow failures (**I-27**) — interim fix KB5002927 published between the Sep and (expected) Oct 2026 CU.
- **Open issues carried forward, not fixed by this CU:** Distributed Cache provisioning (**I-23**), BCS allow-list (**I-24**, by design), Document ID allow-list (**I-25**, by design), RER blocking (**I-26**), search topology (**I-33**), QueryLogJobDefinition SQL pool exhaustion (**I-17**).
- **Prereq:** if farm is still on Sep 2025 CU, apply `Fix-SeptemberCU-Permission-Problem.ps1` first — banner still present in this month's post. Configuration Wizard must be run on each farm machine after install.
- **Fix-list correction (2026-09-29 revision):** the Sep 2026 CU does **not** roll up the Distributed Cache fix (I-23) — see §3.
- **Additional behaviour changes / regressions found in the 120 comments (all after release):** SP2010 workflows + InfoPath Forms Services + ToolPane **disabled by default** (I-27, I-36, I-38); event receivers registered against old assembly versions no longer load → workflow auto-start, subsite creation and third-party solutions break (**I-35**, not in KB, no PG fix); Document-ID assembly allow-list blocks site provisioning on old site collections (I-25); RER outbound host allow-list (I-26/I-32); `Get-SPLegacyWorkflowDisabledSites` removed (allow-list only); package re-uploaded after first publish (I-41a); Update Catalog delayed ~1 day; modern **Check-In** menu item missing, custom tiles across web apps, empty navigation managed properties on new pages (I-42).
- **Intermediate fix:** **KB5002927 = build 16.0.20326.20158** (2026-09-21) supersedes the Sep CU for InfoPath/SP2010-workflow users; no dedicated KB page.
- **Stefan's statements worth keeping:** build jump `16.0.19725 → 16.0.20326` does **not** mean 26H2 — forks are not mapped to feature updates (2026-09-23). Microsoft will not publish a separate article on the workflow enable-only behaviour. Ask for InfoPath reinstatement is out of scope (support ended 2026-07-14).
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
- **Fixed in this CU (confirmed in comments):** Jul 2026 CU issues **I-28** (actor-token property removed — revert the flag), **I-29** (session-cookie / DCache re-auth), **I-31** (PictureURL), **I-21**, **I-22**. **Not fixed:** search topology (**I-33**), Nintex/third-party SP2010 workflow issues.
- **Additional issues found in the 124 comments:** DCache **role-conversion** bug not in the KB (I-23; Stefan: "identified after the fix was released"); RER **new registrations already blocked** (I-26); `AllowedDLCAssemblies` (I-25); OData/WCF BCS outbound-host allow-list (I-32); BCS crawl / term-store / friendly-URL search loss (I-24); sandbox-solution activation blocked (I-37); SP2013 workflow AD-group access denied (I-39); one `System.CodeDom` web.config line reported dropped by the CU (I-20); PSConfig vs Always On `WSS_Logging` (I-41); SQL 18452 (I-41h); PnP 401 (I-42).
- **New cmdlets:** `Enable-SPLegacyWorkflow`, `Enable-SPWorkflow2013`, `Disable-SPLegacyWorkflow`, `Get-SPLegacyWorkflowEnabledSites`, `Get-SPWorkflow2013EnabledSites`, `Get-SPOrphanedRemoteEventReceiver` (I-38, I-26).
- **Final CU for SharePoint 2016/2019** — reconfirmed by Stefan 2026-08-14/-18 and 2026-09-01 ("No further updates are planned"); reason: large backlog of critical security fixes, released for all versions at once so the fixes could not be reverse-engineered on unpatched 2016/2019 servers.
- **Security:** CVE-2026-65665 (Critical) was fixed in this CU although the Sep PU table lists 16 vs the Sep KB's 17 CVEs (Sep KB repeats it). Readers asked whether **CVE-2026-55040** (Critical JWT auth-bypass) is covered — *unanswered on the blog; check MSRC*, and note that `DisableActorTokenAudienceValidation` (Jul) only disables a defense-in-depth check.
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
- **Required post-PSConfig step documented only in the KB *Known issues* section (easy to miss):** `$farm.DisableActorTokenAudienceValidation = $true; $farm.Update()` once per farm (**I-28**) — otherwise OOS and SP2013 workflows fail. Property removed by Aug 2026 CU.
- **Additional issues found in the 120 comments (Stefan-acknowledged):** session-cookie/Distributed-Cache re-authentication on multi-WFE Forms/Trusted-provider farms (**I-29**, fixed Aug); PictureURL commit failure (**I-31**, flag 53534; fixed Aug); DataFormParameter/SPD forms and app safe-control failures (**I-30**); WCF-BCS outbound host allow-list (**I-32**); iFrame/CSP frame-ancestors (**I-34**); `IniWrkflIP` session-cookie error (**I-40**). **Unacknowledged/single reporters:** JSOM `ValidateFormDigest` access denied + redirect loops, UPS profile picture, modern list paging, search "All query processing components Failed" (I-33/I-42).
- **Workflow (I-20) field experience from 111 comments on the July trending post:** the fix needs *three* authorizedType groups (System.CodeDom, Microsoft.SharePoint.WorkflowActions, Microsoft.Office.Workflow.Actions[.WithKey]); `Fix-SystemCodeDom.ps1` adds only one; must be run from SharePoint Management Shell; Nintex works after entries are complete; OWSTIMER config must have none. Workaround from Jun (`EnablePreParseSecurityCheckForWorkflow=$false`) should be reverted once entries are in place (Stefan 2026-07-20/-22).
- **CU-skipping:** CUs are cumulative — June is not required before July (Stefan 2026-07-17).
- **Stefan on EoS behaviour:** SP2010 workflows are "unsupported – not necessarily removed … there is a good chance that it will be removed without further notice" when the next vulnerability appears (2026-07-15).
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
- **Fixes:** Text web part read-only regression (**I-15**, introduced Jan 2026 CU).
- **Known issues introduced:** SP2010-style workflows fail with "Failed to Start" / "Potentially malicious" XOML errors — stricter workflow-code validation flags legitimate constructs (**I-19**) — fixed July 2026 CU. Temporary workaround (`$farm.EnablePreParseSecurityCheckForWorkflow = $false`) disables a large set of workflow security fixes and should be reverted once patched.
- **Prereq:** if farm is still on Sep 2025 CU, apply `Fix-SeptemberCU-Permission-Problem.ps1` first.
- **Correction:** the June 2026 CU **fixed I-15** (Text web part read-only) — the resolved post is dated 2026-07-02.
- **Package quality:** SHA256 and build number in the KB did not match the downloadable `uber-subscription-kb5002873-fullfile-x64-glb.exe` (real build 16.0.19725.20384); MS updated the KB the next day. Learn "SharePoint updates" and 26H1 pages were stale for days (Learn maintenance).
- **Additional issues found in the 48 comments + 34 on the trending post:** Nintex breaks (publish + fire; needs the `System.CodeDom` sub-type authorizedTypes in web.config **and** in `owstimer.exe.config` according to one reader) — scheduled/timer-run workflows broke even with web.config edits (**I-19/I-20**); Search topology/admin component broken on *all* farms of two readers (**I-33**); FedAuth cookies lost when routed to certain WFEs behind F5 (**I-29**, cause unproven); UPS `FeedCacheService`/`ProfileDBCacheService` 503 throttling (**I-43**); Yes/No calculated column (**I-42**); the "Workflow" timer job running for hours after the flag was cleared (I-41).
- **Feature update 26H1 reception (19 comments):** readers criticise that the only new *early-release* feature is the People-Picker "exclude Everyone claim" config; SPFx toolchain is still 1.4.1/1.5.0; modern branding limits. Stefan (2026-07-02/03): the product group asks that customers file **Design Change Requests via a support case** with quantified business impact — this is the main input for future feature updates.
- **Stefan on risk trade-off (2026-06-29):** safest is to install the CU and *not* apply the workflow workaround; but June CU has 30+ fixes incl. 2 critical — for SP2010-workflow-dependent farms it is a risk assessment.
- **Fresh install guidance (2026-06-10):** RTM + language packs → latest CU; skip Sep 2025 CU.
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
| I-15 | Modern UI | Text web part read-only while "Text and table formatting" pane open | Medium | Jan 2026 CU | **Jun 2026 CU** (Stefan's resolved-issue post, 2026-07-02) | Close formatting pane before editing text (until Jun 2026 CU) |
| I-16 | Upgrade / DB | `Invalid column name 'SAFE_NOTIFICATION_DATA'` when psconfig upgrades Jan 2026 schema to Mar 2026 CU | Critical (blocks upgrade) | Mar 2026 CU | Apr 2026 CU (complete fix) | Install Feb 2026 CU **first**, run Config Wizard, *then* Mar/Apr 2026 CU; or open MS support ticket if already broken |
| I-18 | Kerberos / AD / Windows Update | **Kerberos authentication failures after April 2026 Windows Update (CVE-2026-20833).** April 14, 2026 Windows Update removes RC4 fallback from KDC. SharePoint service/app-pool accounts without AES encryption flags in AD cannot complete Kerberos handshake. ULS errors: `A call to SSPI failed` / `The encryption type requested is not supported by the KDC`. Affects Central Admin access, Search Admin, User Profile Sync, and other service applications. Not a SPSE CU regression — caused by OS-level security hardening. | High | Windows Apr 2026 Update (external) | N/A — fix is in AD | Enable "AES 128 bit" and "AES 256 bit encryption" on every SharePoint service and app-pool account in AD Users and Computers → Account tab → Account Options. Then run `iisreset` and restart affected services. Ref: KB 5073381, CVE-2026-20833. MS Learn: [SharePoint Kerberos AES config](https://learn.microsoft.com/en-us/troubleshoot/sharepoint/security/configuration-to-support-kerberos-aes-encryption). |
| I-19 | Workflows | SP2010 workflows fail ("Failed to Start" / "Potentially malicious" XOML; "This feature has been temporarily disabled"; Nintex publish fails) — stricter workflow-code validation. Affects 2016/2019/SE and third-party engines (Nintex) | High | Jun 2026 CU | Jul 2026 CU (code fix; web.config allow-listing still needed, see I-20) | Temp: `$farm.EnablePreParseSecurityCheckForWorkflow = $false` (revert once patched — Stefan: this disables *all* SP2010-workflow security fixes of the last 5 years; risk confined to SP2010 workflows, but June CU carried 30+ fixes incl. 2 critical, so patching + workaround beats staying on May). Scheduled/pause workflows still failed after web.config-only fixes because they run in OWSTIMER (see I-20) |
| I-20 | Workflows | SP2010 workflows still fail after Jul 2026 CU fix — additional types need allowlisting in web.config (XOML type validation). Event tags `4letu` / `c42q0` / `c42q8` in ULS name the missing type | High | Jul 2026 CU | *Not fixed — configuration requirement (by design)* | Add `System.CodeDom`, `Microsoft.SharePoint.WorkflowActions`, **`Microsoft.Office.Workflow.Actions`** (note *Actions*, Stefan's first post had a typo) and sub-namespaces `…WorkflowActions.WithKey` to web.config authorizedTypes in **every web application**; `Fix-SystemCodeDom.ps1` (run in **SharePoint Management Shell, not ISE**) adds *only* `System.CodeDom`. `owstimer.exe.config` must contain **no** authorizedType entries (otherwise web.config entries are ignored — Stefan 2026-08-06). Workflows resumed by the timer (pause/delay) still failed for some until the pre-parse flag was set false. Three commenters found the Aug 2026 CU dropped one web.config line; SPWebConfigModification then reports "Modification already exists" — re-add manually. Nintex: contact Nintex; Nintex Synchronization timer job may fail (only tracks licence usage) |
| I-21 | Office Online Server | OOS integration with SP2016 fails — WOPI 401 Unauthorized (fail-closed token validation hardening) | High | Jul 2026 CU | Aug 2026 CU | Register farm's own STS as a trusted issuer via `New-SPTrustedSecurityTokenIssuer`, then `iisreset` on every server |
| I-22 | Workflows | Workflow status links (`WrkStat.aspx`) double-encode `WorkflowInstanceID`, breaking workflow history; same bug affects InfoPath task forms (`WrkTaskIP.aspx`) | High | Jul 2026 CU | Aug 2026 CU | Manually fix double-encoded `%25`→`%` in URLs; access via ellipsis menu → Workflows; or URL Rewrite rule per KB5122408 |
| I-23 | Distributed Cache | Cannot add new distributed cache service instances / convert a server to the DCache role (`Add-SPDistributedCacheServiceInstance` → "No hosts present in the cluster"; PSConfig `CacheHostInfo is null` / NullReferenceException). Also hits single-server farms. Not documented in the CU KB at release | High | Aug 2026 CU | **Not fixed in Sep 2026 CU** (Stefan 2026-09-09: "still in development"; a commenter says Oct 2026 CU — unofficial) | `$farm.ServerDebugFlags.Add(59052); $farm.Update()` → provision host → **remove the flag** (`ServerDebugFlags.Remove(59052)`). Patching is unaffected if the role is not changed and the DCache is only *gracefully stopped* (Install-SPSE_Fix `-ShouldGracefulStopDCache $true` — Stefan confirmed). Removing/re-joining the server did *not* help. One reader still failed with the flag on a 2-node DCache farm → support case. Community script (Export/Import-SPCacheClusterConfig + re-provision) reported working — unverified |
| I-24 | BCS | Business Connectivity Services blocks types (e.g. `Nullable\`1`, `SecureStoreProvider`) not in the `BCSAllowedTypeNames` allowlist. **Stefan: by design — "a solution, not a workaround"** | High | Aug 2026 CU | *By design* — allow-list required. Unsolved: models whose WCF proxy assembly is **generated at runtime with a random name** (`t0tn0tcs`), reported by two farms, support case open | Add the exact string from ULS `36px6` for every blocked type. Gotchas: use **single quotes** in PowerShell or the backtick in `Nullable\`1` is eaten (`Nullable1`; remove with `RemoveGenericAllowedListValue`); values replicate in seconds but some needed `iisreset`/search-service restart (crawl idle) or a reboot; `SPDuplicateObjectException` on add → remove the list object and re-add. Search crawl of the term store / BCS needs **~14–15 entries** (`TopicPagesConnector`, `System.Object`, `System.Data.IDataReader`, `IDataRecord`, `TaxonomyProperty[]`, …). Missing entries also caused **friendly-URL pages to vanish from the search index** after Aug CU (fixed by the same list). Existing external content type Edit-form/Entity-picker failures ("BDC is configured incorrectly") are this issue |
| I-25 | Document ID Service | Existing Document Sets return null Document ID; `DocIdSettings.aspx` throws `InvalidDocumentIdProviderException`; **Sep 2026 CU also breaks subsite/publishing-web creation** ("Failed to create the 'Images' library") on *older/migrated site collections* | High | Aug 2026 CU (Sep 2026 CU for site creation) | *By design — root cause confirmed by Microsoft support & Stefan* | `$farm.AddGenericAllowedListValue("AllowedDLCAssemblies","Microsoft.Office.DocumentManagement, Version=15.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c")` (also `Version=14.0.0.0` if ULS names it) → `$farm.Update()` → `iisreset`. Root cause: old site collections store a 14/15.0 DocID provider assembly reference in root-web properties; alternative is rewriting `docid_customProvider_assembly` to `Version=16.0.0.0` |
| I-26 | Remote Event Receivers | RERs without an `AppIdentifier` are blocked. **New registrations are blocked already since Aug 2026 CU** (CSOM/PnP/PowerShell → "Access denied … Adding a Remote Event Receiver Definition without an AppIdentifier is blocked"); the KB text only announced blocking of *existing orphaned* RERs for the **Nov 2026 CU** (Health Analyzer rule + `Get-SPOrphanedRemoteEventReceiver`). Sep 2026 CU adds an *outbound host* check on RER calls (`Outbound request blocked: host … is not in SPAllowedOutboundHosts`) | Medium (by design) | Aug 2026 CU | *By design* — PG position (relayed by Stefan 2026-08-19): register through a SharePoint Add-in so the receiver is stamped with an app identity; Stefan 2026-09-15: no change planned | Register via Add-in/app installer or REST with app identity; add RER hosts to `SPAllowedOutboundHosts` (farm property, not web-app). Microsoft support gave a temporary flag `ServerDebugFlags 50008` + `iisreset` for PowerShell registration (community-reported; **reported slow** — 9 large libraries took ~2.5 h; Microsoft could not confirm it survives Nov 2026). Farm-solution ItemEventReceiver that forwards to the .svc endpoint is a viable redesign. Reaction in comments: strongly negative (breaks K2 / air-gapped provisioning) |
| I-27 | InfoPath / Workflows | Sep 2026 CU **disables InfoPath Forms Services and SP2010 workflows by default**. Symptoms: "The specified form template could not be found, or is not compatible with rendering in the browser", "The form cannot be rendered … State Service", manual-start forms (`IniWrkflIP.aspx`, `CstWrkflIP.aspx`, approval workflow start) fail even after `Enable-SPLegacyWorkflow`; `Set-SPInfoPathFormsService -AllowUserFormBrowserRendering $true` throws "no longer supported because InfoPath is deprecated"; new `InfoPathDeprecation` HTTP module in web.config. Affects **all** InfoPath forms, not just workflows | High | Sep 2026 CU | Intermediate fix **KB5002927** (build **16.0.20326.20158**, released 2026-09-21, supersedes the Sep CU; no separate KB page; will be rolled into Oct CU but the script stays mandatory) | Install KB5002927 (*no* Config Wizard yet) → **restart the PowerShell session** → run Stefan's script (debug flag 5023, `AllowUserFormBrowserRendering/Enabling = $true`) → run Config Wizard. Script run once is enough. **Correction 2026-09-24:** Stefan first said publishing new SP2010 workflows stays permanently disabled, then corrected after asking the PG — the hotfix *did* re-enable creating/publishing SP2010 workflows, but *do not read this as a long-term commitment*; InfoPath Forms Services and SP2010 workflows are expected to be **removed in a future CU** (a KB will precede removal). Nintex workflows can be published only where `Enable-SPLegacyWorkflow` was run. Older, community-reported DLL-swap trick did *not* work for others |
| I-28 | Auth / Tokens | **Actor-token audience validation** ("defense-in-depth feature under development") → Office Online Server integration and **SP2013 workflows (WFM↔SharePoint) fail** with 401/403 ("You do not have permissions to open this file in the browser", "Un-whitelisted client sent us an OAuth token"). Listed only in the KB *Known issues* section | High | Jul 2026 CU | **Aug 2026 CU** — property `DisableActorTokenAudienceValidation` was *removed*; Stefan: "This issue was fixed and the flag should be reverted" | `$farm.DisableActorTokenAudienceValidation = $true; $farm.Update()` **once per farm** (stored on the SPFarm object) *after PSConfig*. Multi-WFE farms with OOS saw 401s until it was set. Stefan: do not confuse with SP2016 WOPI issue (I-21). A reader still got 403 after setting it ("app principal does not exist") → support case. |
| I-29 | Auth / Distributed Cache | **Session-cookie transform protection** → session token cannot be stored in Distributed Cache (`Session cookie transform was triggered unexpectedly`, `NotSupportedCookieTransform`); users on multi-WFE farms with **Trusted-Provider/Forms auth** are re-prompted for sign-in whenever they hit a different WFE (also seen as FedAuth-cookie loss behind an F5 after Jun 2026 CU). Windows-auth farms not affected | High | Jul 2026 CU (a Jun 2026 CU report exists, unconfirmed) | **Aug 2026 CU** (Stefan 2026-08-12: "checked in for all product versions") | Sticky sessions on the reverse proxy, or single WFE. **Never set `SessionCookieTransformProtectionEnabled=$false`** — Stefan/PG: "very dangerous", exposes servers to significant security risk; PG asked a third-party post recommending it to be removed. |
| I-30 | SharePoint Designer / Safe controls | Custom SPD forms and apps stop rendering (`Unsafe control … DataFormParameter … property traversal char`, `Re-definition of tag … maintaining consistency of attributes`, `WebPartPageUserException`, apps failing `SafeControls.IsSafeControl`) | Medium | Jun/Jul 2026 CU (`xsl:template` tag issue traced by Stefan to **Jan 2026 CU**) | *By design* — configuration | Add web.config `<SafeControl Assembly="Microsoft.SharePoint, Version=16.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c" Namespace="Microsoft.SharePoint.WebPartPages" TypeName="DataFormParameter" Safe="True" AllowPropertiesTraversal="True" />` (post with `[ ]` for angle brackets — the blog strips them). Plus `$farm.AddGenericAllowedListValue("AllowedTagPrefixesWhichAreNotWebControlsList","xsl:template")`. `$farm.PreserveAttributeConsistency=$false` is the alternative when the SafeControl entry is absent; the "Re-definition of tag" ULS message is *expected, not an error* (Stefan). Some apps also needed `SkipUpdateWebConfigPermission`/WSS_WPG rights on web.config (Stefan: only if app code touches web.config). |
| I-31 | User Profile | `UserProfile.Commit` / `Update-SPProfilePhotoStore` fail: "Url is not safe … `SPServiceContext.Current is null`" when setting `PictureURL` from PowerShell | Medium | Jul 2026 CU | **Aug 2026 CU** (readers confirm flag no longer needed) | `$f.ServerDebugFlags.Add(53534); $f.Update()` (iisreset not needed) → do the update → **remove** the flag |
| I-32 | Outbound host allow-list | New enforcement of `SPAllowedOutboundHosts`: WCF-BCS (Jul), OData-BCS crawl (Aug: `Host … not in allowlist … for property 'ODataServiceUrl'`), Remote Event Receivers (Sep). Symptom for WCF BCS: Entity picker/Edit form "Business Data Connectivity is configured incorrectly" while Display form still shows stored values | High | Jul 2026 CU (expanded Aug, Sep) | *By design* — farm allow-list | `$farm.AddGenericAllowedListValue("SPAllowedOutboundHosts","host")` per host (farm property, **not** web-app). Escape hatch (unsafe): `DisableWcfBdcHostAllowlistEnforcement` = debug flag **115** (message text from ULS). One farm needed a **server reboot** before the value was read. |
| I-33 | Search | After patching (reported since **Apr 2026 CU**, every CU since, incl. Jun/Jul): CA shows "Unable to retrieve topology component health states … admin component is not up", crawl/incremental crawl hangs or "Paused for: External request", "All query processing components are in 'Failed' status", ULS `Failed to synchronize legacy admin … Failed to connect to system manager`, CSS connector failures. Also seen after Windows Updates (Benjamin F., 14 farms: 9 affected) | High | Apr 2026 CU (per Stefan) | **Not fixed** (Stefan 2026-08-13). Not reproducible → PG has no fix | In order of invasiveness: (1) restart `SPSearchHostController` (wait 3-4 min, restart again if needed) and `OSearch16`; (2) `sc.exe config SPSearchHostController start=delayed-auto` + `sc.exe config OSearch16 start=delayed-auto`, reboot (Stefan; worked for several, not all; keep permanently is fine); (3) `$ssa.ForceResume($ssa.IsPaused())` after stopping the host controller for 3-4 min; (4) `iisreset` for CSS connector errors; (5) last resort: rebuild topology (one reader loses ~2.5 days of crawl per incident). One reader observed it depends on the search service account's local-admin membership. Several readers *stay on Apr 2026 CU* because of it — a security trade-off. Separate: SearchAdmin DB migrated from 2019 fails psconfig with missing `proc_MSS_*` stored procedures (unresolved). |
| I-34 | iFrame / CSP | `AppWebProxy.aspx`/app-authorize pages now send `Content-Security-Policy: frame-ancestors 'self' teams…` and `X-Frame-Options: SAMEORIGIN` → provider-hosted add-ins, SP2019 News app, Office Online preview from Search Center on a different URL fail to frame | Medium | Jul 2026 CU | *By design* — configuration (Stefan: worth investigating; product group not confirmed as bug) | `$farm.EnableCSPHeaderForPage = $true` **and** `$farm.AddGenericAllowedListValue("AllowIframeAppAuthorizePageDomains","<host of the framing app>")` (hosts of the *external app / OOS*, not SharePoint web apps; wildcards allowed) → app-pool recycle on WFEs. If a custom CSP header is needed, disable SharePoint's injection per Stefan's 2024-03 article. |
| I-35 | Event receivers / assembly binding | **Sep 2026 CU stops honouring assembly-version redirects for event receivers**: `LoadEventReceiverTypeSafe: Failed to load type … Version=15.0.0.0 …` (also 7.0.0.0→8.0.0.0 custom redirects, third-party v12/v14 references, `ReflectionOnly … has not been preloaded`). Consequences: SP2010/SP2013 workflows created before migration no longer **auto-start** (manual start works), multi-step approval workflows stall after step 1 (`ContentSubscriptionEventReceiver`), subsite creation fails on old site collections (`STS#0`, publishing `Images` library), third-party (Nintex Forms web-part tests, Aderant HSListGuru) | High | Sep 2026 CU | **Not fixed** (no PG statement; Stefan 2026-09-18: "currently the only solution is to update the event receiver registration"). Not in KB | (1) Re-point registrations to `Version=16.0.0.0` with a script (community `Update-EventReceiverVersionTo16.ps1` — confirmed working by 3 readers; Stefan pointed to the same approach); (2) allow `Microsoft.Office.DocumentManagement 15.0.0.0` in `AllowedDLCAssemblies` (see I-25) for site creation; (3) reader-reported (unofficial, exposes a security check) `ServerDebugFlags.Add(59025)` + `iisreset` fixed three DEV/TEST farms. 3rd-party binaries compiled against 12.0/14.0 have no workaround except vendor recompile. |
| I-36 | Editing UI | **ToolPane feature disabled by default** — web parts cannot be edited in the browser after Sep 2026 CU | Medium (by design) | Sep 2026 CU | *By design* — KB Known/Notice section | `Enable-SPToolPane` |
| I-37 | Solutions / Workflows | WSP activation blocked: "Activation of solutions with sandboxed code has been disabled" for packages that contain a Feature with `ReceiverAssembly=Microsoft.SharePoint.WorkflowServices` (`SPWorkflowPackageFeatureReceiver`), i.e. declarative SP2013 workflows | Medium | Aug 2026 CU | **Not fixed**; reporter opened a support case | Reader workaround: remove `ReceiverAssembly`/`ReceiverClass` attributes from `Feature.xml` in the WSP. Stefan: open case. |
| I-38 | Legacy workflow platforms | **Policy/behaviour timeline**: SP2010 workflows disabled by default with **Sep 2026 CU** (all site collections, including existing, unless allow-listed); SP2013 workflows disabled by default with **Oct 2026 CU**. Rationale (Stefan): reduce attack surface. SP2013 workflows + SPWFM remain supported (Stefan 2026-09-07/-24: no plan to drop) | High (change mgmt) | Aug 2026 CU (cmdlets) / Sep 2026 CU (SP2010 off) / Oct 2026 CU (SP2013 off) | n/a — policy | `Enable-SPLegacyWorkflow <site-collection-url>`, `Enable-SPWorkflow2013 <url>`, `Disable-SPLegacyWorkflow`, `Get-SPLegacyWorkflowEnabledSites`, `Get-SPWorkflow2013EnabledSites`, `Get-Command *SPLegacyWorkflow*`. Run in SharePoint Management Shell **on an SPSE server with Aug CU or later**. Needed once per site collection, **also for every new site collection** (provisioning scripts must call it) and again after a 2019→SPSE database attach. Stefan (2026-09-03): the Aug 2026 CU itself did *not* disable workflows (a few readers reported engines disabled after Aug — unconfirmed). SP2010 list-retention policies tied to SP2010 workflows have no SP2013 equivalent. |
| I-39 | SP2013 workflows / SPWFM | Workflows start then fail `HTTP 401/403` back into SharePoint: (a) Jul 2026 actor-token (I-28); (b) **Aug 2026**: workflow fires as *Access denied* when the initiating user got permissions **through an AD security group** (works with direct user grants; "actor token has no AppIdAcr claim"); (c) SP2013→SPSE migrations: `invalid_client` 401 from SPWFM callbacks; (d) SP2013 workflow calling an SP2010 workflow (`InteropService.StartWorkflow` Unauthorized) | High | Jul/Aug 2026 CU | *Not acknowledged*; Stefan → support case (Aug/Sep). SPWFM Aug CU KB5002864 did **not** help the reporter | (b) Add the individual users in addition to the group; watch the *primary-group* pitfall. SPWFM min version: Stefan clarified the KB text is misleading — **KB5002799 (Nov 2025) is the *minimum***, newer is recommended; SPWFM Sep 2026 fix (KB5002925) was released 2026-09-11 out-of-band although the KB says 09-08. |
| I-40 | InfoPath / session | `IniWrkflIP.aspx`: "form cannot be displayed … session cookies have been disabled" after Jul 2026 CU (also Aug, new farms) | Medium | Jul 2026 CU | Unknown — not on Stefan's list (Stefan 2026-08-20) | Setting `httpOnlyCookies="false"` in web.config makes it work (readers) — security trade-off; superseded by I-27 after Sep 2026 CU. |
| I-41 | Patching / PSConfig | Install/upgrade anomalies: **(a)** Sep 2026 package first published was wrong → `SPMissingAttributeException … RegisterInfoPathDeprecationHttpModule requires To and From build information` — re-download (build 16.0.20326.20136). **(b)** Jun 2026 KB hash and build number in KB did not match the download (fixed by MS within a day); Aug OOS KB text pointed to wrong KB/duplicate file. **(c)** MSI **1603** on a *new* farm (Feb 2026 build) with the Install-SPSE_Fix script → clearing `%TEMP%`, installing Jun CU + PSConfig first, then Jul worked. **(d)** PSConfig `MergeWebConfig … NullReferenceException` where web.config had *partial InfoPath merge state* (Sep). **(e)** `RECONFIGURE` permission error on Secure Store DB → temporarily `GRANT ALTER SETTINGS`/sysadmin to setup account. **(f)** `Get-SPServer … NeedsUpgrade` inconsistent between two servers → clear config cache (keep `Cache.ini`, set to `1`). **(g)** PSConfig fails on `WSS_Logging` when it is in a SQL Always On AG (must be removed while PSConfig runs). **(h)** `Login failed … untrusted domain (18452)` after OS updates — Stefan: AD/SPN/NTLM problem, "SharePoint is a victim" (see Kerberos I-18). **(i)** timer job "Workflow" running for hours after the pre-parse flag was cleared — clear timer cache/restart SPTimerV4. **(j)** LOGS folder permissions for `WSS_ADMIN_WPG`/`WSS_WPG` lost after patch → usage-import jobs fail with access denied. **(k)** SharePoint update auto-installed by BigFix/WSUS unexpectedly re-triggered the workflow break. **(l)** Sep 2026 packages missing from Update Catalog for ~1 day (fixed). | Medium | Jun–Sep 2026 CU | Varies (see text) | See each item. Stefan: SharePoint updates cannot be uninstalled → validate every CU in a test farm against business-critical features. |
| I-42 | Modern UI / JSOM / misc (single reporters, **unacknowledged**) | Yes/No **calculated column** no longer recognised as Boolean (Jun/Jul); JSOM `ValidateFormDigest` access denied + "too many redirects" on custom CSS/JS (Jul); modern list paging/item count broken (SP2019, Jul); **Check-In missing in modern library menu** on 4 farms (Sep — classic view fine); display-template check-in no longer updates `.js` (Sep); `?contents=1` web-part diagnostic param broken (Aug); custom tiles across web apps need DB rights for the MySite app-pool account (Sep); new publishing pages get empty `owstaxidNavigation`/`Tags` managed properties (Sep); Windows Server 2025 + Sep CU "Server Error" on every site (ULS needed); `PnP Connect/Invoke-PnPQuery` 401/403 (Aug/Sep — Stefan: PnP not supported/tested) | Low–Medium | Jun–Sep 2026 CU | Unknown | Open a support case where business-critical; no acknowledged fix. |
| I-43 | Performance / UPS | Recurring HTTP throttling / **503 Server Busy**, growing request queue; long-running calls to `FeedCacheService.svc` / `ProfileDBCacheService.svc`; IIS pool recycling only helps for minutes. Two farms confirm (Belen, Andy D.) | High | Jun 2026 CU | **Not acknowledged** — Stefan: open MS support case (2026-07-10) | Mitigate by pulling WFEs from LB + recycling pools; one farm resolved a related "0.3 s → 80 s response time" by re-running PSConfig after Windows Updates. |
| I-17 | Search / Timer Jobs | **QueryLogJobDefinition SQL connection pool exhaustion** — `QueryLogJobDefinition` fails with Event 6399: *"Timeout expired. The timeout period elapsed prior to obtaining a connection from the pool"*. Timer job leaks SQL connections on every run; pool (max 100) fills up after a few days causing cascading timer job failures. ULS signature: `QueryLogProcessor: AssignDocIdsToResults error: The method 'EndExecuteReader' cannot be called`. **Still present after Mar 2026 CU (KB5002843), Apr 2026 CU (KB5002853), and May 2026 CU (KB5002863) — no official fix published as of May 2026.** Not independently re-verified against Jun–Sep 2026 CUs during this update pass (no new Stefan post or MS Q&A activity surfaced); treat as still open until confirmed otherwise. Microsoft confirmed investigating but no KB article or fix released. | High | Mar 2025 CU (regression) | **Not fixed — open as of 2026-09 (last independently confirmed May 2026)** | (1) Disable the **Query Logging Timer Job** in Central Admin (most effective). (2) Schedule a nightly restart of `SPTimerV4` to clear the pool every 48–72 hrs. (3) Increase SQL pool size as short-term delay: add `Max Pool Size=200` to the Search connection string. Sources: [Oct 2025 Q&A](https://learn.microsoft.com/en-us/answers/questions/5583482/many-critical-events-in-sharepoint-se-after-july-2) · [Mar 2026 Q&A #1](https://learn.microsoft.com/en-us/answers/questions/5816641/querylogjobdefinition-may-be-exhausting-the-sql-co) · [Mar 2026 Q&A #2](https://learn.microsoft.com/en-us/answers/questions/5849106/search-service-sql-connection-pool-exhaustion-afte) · **Monitored** by `weekly_check.py` (3 answers as of 2026-05-18; new answers trigger GitHub issue) |

---

## 5A. Post-June 2026 deep analysis — posts + all comments (revision 2026-09-29)

**Method.** Every Stefan Goßner post dated 2026-06-01 → 2026-09-28 (32 posts: SPSE, SP2016, SP2019, OOS, Workflow Manager, PU summaries, trending/resolved issues, EoS, 26H1) was downloaded, and **all 1,181 reader comments** were pulled through the blog's WordPress REST API (the RSS comment feeds only expose the newest 20). SPSE-relevant threads were read in full (≈ 700 comments); SP2016/2019/OOS/SPWFM threads were read where they contained SPSE-relevant or cross-version content. **Trust model:** Stefan's replies = authoritative; another reader's fix that Stefan or a second reader confirmed = *confirmed*; a single reader's claim = *unconfirmed*. Comment counts (2026-09-29): Jun SPSE CU 48 · Jul SPSE CU 120 · Aug SPSE CU 124 · Sep SPSE CU 120 · SP2010 WF Jun-issue 34 (+82 on the "resolved" repost) · Jul WF issue 111 · BCS 32 · "Are you using SP2010/2013 workflows" 78 · InfoPath 27.

### 5A.1 What the comments changed (corrections to earlier revisions)
| # | Earlier statement | Corrected by |
|---|---|---|
| 1 | I-15 Text web part "not yet fixed" | Fixed in **Jun 2026 CU** (Stefan's resolved post, 2026-07-02) |
| 2 | Sep 2026 CU rolls up the DCache fix (I-23) | Stefan 2026-09-09: fix "still in development"; workaround still needed |
| 3 | I-24 BCS "not fixed" (a bug) | **By design**; allow-list is the *solution* (Stefan 2026-08-15). Only runtime-generated proxy assemblies are unsolved |
| 4 | I-25 Document ID "no fix confirmed" | Root cause + fix known (`AllowedDLCAssemblies`); same root cause breaks Sep CU site creation |
| 5 | I-26 RERs blocked "in Nov 2026" | **New registrations blocked since Aug 2026 CU**; Nov only affects existing orphaned RERs |
| 6 | I-27 "publishing new SP2010 workflows permanently disabled" | Stefan retracted 2026-09-24: KB5002927 re-enables publishing (no long-term promise) |
| 7 | I-20 "not stated as fixed" | Config requirement (not a defect); need 3 authorizedType groups; OWSTIMER rule |
| 8 | Jul 2026 CU known issues = 3 | Actually ≥ 9 (actor token, session cookie/DCache, PictureURL, DataFormParameter, outbound hosts, CSP/iFrame, …) — see I-28…I-34 |
| 9 | Aug 2026 "four issues" | ≥ 12 incl. DCache role conversion, sandbox activation, AD-group workflow denial, search allow-lists |

### 5A.2 Deprecation / behaviour-change timeline
| Date / CU | Change | Action |
|---|---|---|
| 2026-07-14/15 | EoS: SP2016, SP2019, Project Server 2016/2019, **SP2010 workflows (incl. Nintex etc.)**, **InfoPath Forms Services**, Basic auth, SPD 2013, Classic Workflow Manager. Support cases can be opened to 07-14 | Migrate; Stefan: options = SP2013 workflows (VS 2022 package, supported to 2032), Power Automate (needs internet/on-prem gateway), third-party. SPSE supported at least to 2035 |
| Jun 2026 CU | Workflow pre-parse validation (I-19); 26H1 | web.config allow-list |
| Jul 2026 CU | Actor-token, session-cookie, outbound-host, CSP, DataFormParameter hardening (I-28…I-34) | Known-issues script, allow-lists |
| Aug 2026 CU | Last SP2016/2019 CU; BCS type allow-list; `AllowedDLCAssemblies`; RER without AppIdentifier blocked; workflow enable cmdlets | Pre-seed allow-lists; **run `Enable-*` cmdlets before Sep/Oct** |
| **Sep 2026 CU** | **SP2010 workflows, InfoPath Forms Services, ToolPane disabled by default**; event-receiver assembly binding tightened; SP2010 allow-list only (no deny-list) | KB5002927 + script; `Enable-SPToolPane`; re-register receivers at v16 |
| **Oct 2026 CU** (expected 2026-10-13) | **SP2013 workflows disabled by default** (`Enable-SPWorkflow2013`); DCache fix targeted (unofficial) | Enable per site collection before installing |
| **Nov 2026 CU** | **Orphaned RERs (no AppIdentifier) blocked** | `Get-SPOrphanedRemoteEventReceiver`; migrate to add-in/farm solution |
| Future CU (undated) | SP2010 workflows + InfoPath Forms Services **removed** (KB to precede) | Finish migration |
| 2026-12-31 | Office Online Server retirement (separate product/lifecycle; Stefan: unrelated to SPSE support) | Plan replacement |

### 5A.3 Remediation cookbook (all verified in comments or by Stefan unless marked)
```powershell
# --- Sep 2026 pre-flight (SharePoint Management Shell, NOT ISE; Aug 2026 CU+ required for the cmdlets)
Enable-SPLegacyWorkflow  http://site-collection-url     # per site collection, incl. NEW ones; re-run after 2019->SPSE attach
Enable-SPWorkflow2013    http://site-collection-url     # before Oct 2026 CU
Get-SPLegacyWorkflowEnabledSites ; Get-SPWorkflow2013EnabledSites ; Get-Command *SPLegacyWorkflow*
Enable-SPToolPane                                       # web-part editing after Sep CU

# --- Farm allow-lists (one server; values replicate in seconds; some need iisreset / reboot)
$farm = Get-SPFarm
$farm.AddGenericAllowedListValue("AllowedDLCAssemblies","Microsoft.Office.DocumentManagement, Version=15.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c")   # + Version=14.0.0.0 if ULS says so
$farm.AddGenericAllowedListValue("BCSAllowedTypeNames",'Assembly=mscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089|Namespace=System|TypeName=Nullable`1')  # SINGLE quotes!
$farm.AddGenericAllowedListValue("SPAllowedOutboundHosts","host.fqdn")            # WCF/OData BCS + RER hosts
$farm.AddGenericAllowedListValue("AllowIframeAppAuthorizePageDomains","app.fqdn")  # + $farm.EnableCSPHeaderForPage = $true
$farm.AddGenericAllowedListValue("AllowedTagPrefixesWhichAreNotWebControlsList","xsl:template")
$farm.Update()
$farm.GetGenericAllowedListValues("BCSAllowedTypeNames")                          # verify
```
```xml
<!-- SP2010 workflows: in EVERY web application web.config (and NONE in owstimer.exe.config) -->
<System.Workflow.ComponentModel.WorkflowCompiler><authorizedTypes><targetFx version="v4.0">
  <authorizedType Assembly="System, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089" Namespace="System.CodeDom" TypeName="*" Authorized="True" />
  <authorizedType Assembly="Microsoft.SharePoint.WorkflowActions, Version=16.0.0.0, Culture=neutral, PublicKeyToken=null" Namespace="Microsoft.SharePoint.WorkflowActions" TypeName="*" Authorized="True" />
  <authorizedType Assembly="Microsoft.SharePoint.WorkflowActions, Version=16.0.0.0, Culture=neutral, PublicKeyToken=null" Namespace="Microsoft.SharePoint.WorkflowActions.WithKey" TypeName="*" Authorized="True" />
  <authorizedType Assembly="Microsoft.Office.Workflow.Actions, Version=16.0.0.0, Culture=neutral, PublicKeyToken=null" Namespace="Microsoft.Office.Workflow.Actions" TypeName="*" Authorized="True" />
</targetFx></authorizedTypes></WorkflowCompiler>
<!-- Derive further entries from ULS events 4letu / c42q0 / c42q8; a missing "s" in "Actions" cost one reader two weeks. -->
```
| Debug flag / property | Purpose | Status |
|---|---|---|
| `EnablePreParseSecurityCheckForWorkflow=$false` | Disable SP2010 workflow pre-parse validation (I-19) | Temp only — revert after entries added; disables 5 years of SP2010-workflow security fixes |
| `DisableActorTokenAudienceValidation=$true` | Jul 2026 known issue (I-28) | Property **gone** after Aug CU |
| `SessionCookieTransformProtectionEnabled=$false` | Not a fix for I-29 | **Do not use** (Stefan: security risk) |
| `PreserveAttributeConsistency=$false` | SPD form "re-definition of tag" (I-30) | Alternative to SafeControl entry |
| `ServerDebugFlags 59052` | Provision DCache host (I-23) | Remove after provisioning |
| `ServerDebugFlags 53534` | PictureURL (I-31) | Not needed after Aug CU |
| `ServerDebugFlags 5023` | InfoPath re-enable (I-27) | Set by Stefan's script; stays |
| `ServerDebugFlags 50008` | PowerShell RER registration without AppIdentifier (I-26) | Reader-reported from MS support; slow; may stop working Nov 2026 |
| `ServerDebugFlags 59025` | Event-receiver assembly redirect (I-35) | Reader-reported, **unofficial** |
| `ServerDebugFlags 115` (`DisableWcfBdcHostAllowlistEnforcement`) | WCF-BCS host allow-list off (I-32) | Named in ULS text; weakens security |
| `EnableCSPHeaderForPage` | Control CSP header injection (I-34) | Per Stefan's 2024-03 article |

**Search recovery ladder (I-33):** restart `SPSearchHostController` → `sc.exe config SPSearchHostController start=delayed-auto` and `OSearch16` (reboot) → stop host controller 3-4 min, start, `$ssa.ForceResume($ssa.IsPaused())` → `iisreset` → rebuild topology. Note: the `Install-SPSE_Fix.ps1` snippet circulated in comments had `-eq "Running"` where `-ne "Running"` is required (Stefan confirmed the bug is in an *older* script version).

**Event-receiver re-registration (I-35):** update each `SPEventReceiverDefinition` whose `Assembly` contains `Version=15.0.0.0` to `Version=16.0.0.0` (community script `Update-EventReceiverVersionTo16.ps1`; confirmed working by three readers) then `iisreset`; verify workflows auto-start and subsites can be created.

**Config-cache reset for `NeedsUpgrade` mismatch:** on both servers delete everything in `%ProgramData%\Microsoft\SharePoint\Config\<GUID>` except `Cache.ini`, set `Cache.ini` content to `1`.

### 5A.4 Stefan's positions & process guidance (from replies)
- **Cumulative:** never install an intermediate CU; fresh farm = RTM + language packs → newest CU; skip Sep 2025 CU.
- **Why so many regressions:** "a need to push a very large number of security fixes into several consecutive CUs in a very short time… testing all side effects of 30+ fixes … is challenging" (2026-08-12). Updates cannot be uninstalled → test farm first.
- **Third-party (Nintex, K2, PnP, Aderant):** not supported/tested by Microsoft → vendor/PnP community. Nintex Sync job only tracks licence usage.
- **Feature requests:** open an SPSE support case, label it "design change request", quantify impact; product group commits to invest based on these.
- **SharePoint Workflow Manager:** min version KB5002799; SP2013 workflows will stay (limited investment; SPD unsupported; VS 2026 deprecates SharePoint workflow tooling → use **VS 2022**, supported to 2032).
- **SPWFM patching multi-server:** no official best-practice article (a reader asked; unanswered).
- **Support-case hygiene:** SP2016/2019 cases only until 07-14; for AD/SQL authentication issues raise the case against AD/SQL, not SharePoint.

### 5A.5 Unacknowledged / single-reporter observations (watch-list)
Nintex Forms broken after Jul/Aug/Sep (vendor); Nintex Convert Document action; SPD 2013 "Delay/pause" SP2010 workflows fail after Aug (silent, user report 2026-09-15/18 — tried re-enabling, permission fixes); K2 workflow engine + RER; `BDC` custom WCF; `New-SPWeb STS#0` fails on old site collections (= I-35/I-25); modern "Check-In" missing; friendly-URL crawl (= I-24 fix); custom-tiles DB rights; SP2019 FBA new users cannot log in after Jul (SP2019, not SPSE); SP2019 timer/logs permissions (I-41j); OOS Excel paste/fill-range failure after Sep OOS CU (fixed by OOS 2026-09-22 update KB4461632 per reader; verify); Sep OOS post download link pointed to Aug (fixed).

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
| **Jun 2026 CU** | Jun → Sep 2026 CU directly | None | Picks up Jul (SP2010 workflow code fix, I-19) and Aug fixes on the way; **still add the web.config authorizedTypes (I-20) and pre-flight the Sep behaviour changes** (§3). Stefan (2026-07-20): a farm hit by the June security regression can go straight to the latest CU, no restore needed. |
| **Jul 2026 CU** | Jul → Sep 2026 CU directly | None | Picks up Aug fixes for actor-token (I-28; property removed — revert the flag), session-cookie/DCache (I-29), PictureURL (I-31), OOS/WOPI (I-21) and workflow-status double-encoding (I-22; the URL-rewrite rule can be removed). I-20 web.config entries remain your responsibility. |
| **Aug 2026 CU** | Aug → Sep 2026 CU directly | None | **Before** installing: run `Enable-SPLegacyWorkflow` / `Enable-SPWorkflow2013` on required site collections, pre-seed `AllowedDLCAssemblies`/`SPAllowedOutboundHosts`, inventory event receivers on old assembly versions (I-35). Sep 2026 CU does **not** fix the DCache issue (I-23) — do not change DCache roles while patching. BCS (I-24), Document ID (I-25) are allow-list tasks, not defects. If on SP2016/2019: Aug 2026 was the **final** CU — no upgrade path to Sep 2026 CU; migrate to SPSE. |
| **Sep 2026 CU** (16.0.20326.20136) | Sep → **KB5002927 (16.0.20326.20158)** if you use SP2010 workflows/InfoPath forms → Oct 2026 CU | Optional intermediate fix (skip Config Wizard until the InfoPath script has run) | Oct 2026 CU disables **SP2013 workflows** by default → run `Enable-SPWorkflow2013` first. Expect the DCache fix in Oct (unofficial). Nov 2026 CU blocks orphaned RERs. |

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

## 8. Source log (fetch dates: 2026-09-28; comment-analysis pass 2026-09-29)

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
| stefan-2026-06-…-09 comments (REST API) | https://blog.stefan-gossner.com/wp-json/wp/v2/comments?post=<id>&per_page=100 — all 32 post-June threads (1,181 comments) |
| spse-2026-06-comments | https://blog.stefan-gossner.com/2026/06/09/june-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/#comments |
| resolved-text-webpart | https://blog.stefan-gossner.com/2026/07/02/resolved-trending-issue-text-web-part-cannot-be-edited-while-text-and-table-formatting-pane-is-open/ |
| resolved-jun2026-workflow | https://blog.stefan-gossner.com/2026/07/14/resolved-trending-issue-sharepoint-2010-workflows-fail-after-june-2026-cu/ |
| spse-2026-07-pu | https://blog.stefan-gossner.com/2026/07/14/sharepoint-security-fixes-released-with-july-2026-pu-and-offered-through-microsoft-update/ |
| spse-2026-08-pu | https://blog.stefan-gossner.com/2026/08/11/sharepoint-security-fixes-released-with-august-2026-pu-and-offered-through-microsoft-update/ |
| workflows-disabled-default | https://blog.stefan-gossner.com/2026/08/14/are-you-using-sp2010-or-sp2013-workflows-in-your-sharepoint-farms-this-post-is-for-you/ |
| jul2026-kb-known-issues | https://support.microsoft.com/en-us/servicing/office/update/2026/5002882 |
| sep2026-hotfix | KB5002927 — "Fix to support reenabling InfoPath Forms Services" (linked from the InfoPath trending post) |
| spwfm-aug-2026 / sep-2026 | KB5002864 (Aug), KB5002925 (Sep, released 2026-09-11) |
| oos-sep-fix | https://support.microsoft.com/en-us/servicing/office/hotfix/4461632 (as quoted by a reader) |

This 2026-09-29 comment-analysis revision was also performed manually — **no GitHub Actions** (`weekly-check.yml` remains disabled, `if: false`). Posts were fetched with `curl` and the blog's public WordPress REST API (context-mode MCP unavailable). `.weekly-state.json` was left untouched.

This 2026-09-28 update was performed manually (GitHub Actions workflow `weekly-check.yml` remains disabled — `if: false` — per prior user request) using direct `WebFetch` against Stefan Goßner's blog, since the context-mode MCP sandbox used for prior updates was unavailable this session. `.weekly-state.json` was left untouched by this update; it still reflects the last automated-check baseline (May 2026 CU) and does not track Jun–Sep 2026.

All content in this knowledge base was indexed into the local context-mode sandbox (not stored verbatim in this file). Re-query via `ctx_search` against the listed source labels for verbatim quotes.
