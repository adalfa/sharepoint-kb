# SharePoint Server Subscription Edition — CU Knowledge Base

**Coverage:** July 2025 CU → October 2026 CU
**Generated:** 2026-09-28 · **Comment-analysis revision:** 2026-10-21 (incremental on top of 2026-09-29 full pass and 2026-09-30 delta; all 37 posts + all 1,465 comments dated after 2026-06-01 pulled via REST API; the 168 comments dated 2026-09-30 → 2026-10-21 read in full; see §5A.7)
**Sources:** Stefan Goßner's blog (blog.stefan-gossner.com) — posts **and reader comments** (Stefan's replies are treated as authoritative, unreplied reader reports as *unconfirmed*) — plus Microsoft Support KB articles and Microsoft Download Center.

---

## 1. Overview

- SharePoint Server Subscription Edition (SPSE) ships a single **"uber" CU** every month (language-independent + language-dependent bundled).
- Starting with **August 2025 CU**, every monthly SPSE CU is also flagged as a **security update** (Microsoft recommends installing the full CU over individual security fixes).
- Stefan Goßner (Microsoft Senior Escalation Engineer) publishes the authoritative community commentary, including **known/trending issues** and upgrade guidance.
- Feature Update **25H2** shipped inside the September 2025 CU. Feature Update **26H1** shipped inside the June 2026 CU. Feature Update **26H2** shipped inside the **October 2026 CU** (AMSI body scan "Full mode" default and People-Picker "Everyone" claim exclusion promoted to Standard ring; opt-in People Picker search throttling added in Early ring).
- **Deprecation timeline (see §5A.2):** SP2010 workflows + InfoPath Forms Services EoS 2026-07-14 → disabled by default in the **Sep 2026 CU**; SP2013 workflows were *announced* for the **Oct 2026 CU** but Stefan's source-code check (2026-10-15) shows they are **NOT disabled in the Oct 2026 CU** — date now unannounced; orphaned Remote Event Receivers blocked in the **Nov 2026 CU**; Office Online Server retirement 2026-12-31.
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
| **Oct 2026** | 2026-10-14 | 16.0.20326.20190 | KB5002927² | Yes — ships **26H2** feature update |
| Sep 2026 + COD hotfix | 2026-09-21 | 16.0.20326.20158 | *no KB article* (Download Center entry reused "5002927"²) | Critical-on-demand fix (InfoPath/SP2010 re-enable). Do *not* run Config Wizard until the script has run. Superseded by Oct 2026 CU |
| Sep 2026 | 2026-09-09 | 16.0.20326.20136 | KB5002908 | Yes |
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

² **KB5002927 names two different packages** (correction 2026-10-21). The mid-Sep COD hotfix (build .20158) had no KB article; the Download Center required a KB number and someone entered the number reserved for the next official CU. The Oct 2026 CU (build **.20190**) is the *real* KB5002927. Stefan 2026-10-14/15: *"The two packages are different."* Always verify by **build number**, not KB number. Earlier revisions of this KB wrongly described KB5002927 as the Sep hotfix.

Related Oct 2026 builds: Office Online Server Oct 2026 CU = **16.0.10417.20228** (KB5002928; Stefan 2026-10-15 — Microsoft stopped printing OOS builds on the KB page since July); SharePoint Workflow Manager Oct 2026 CU = KB5002926, client build 16.0.20326.20190.

Note the build-number jump from `16.0.19725.x` (May–Aug 2026) to `16.0.20326.x` (Sep 2026) — a larger jump than the usual monthly increment. Not called out as anything unusual by Stefan; recorded here for administrators tracking build baselines.

---

## 3. Current recommendation (as of 2026-10-21 — updated: Oct 2026 CU released)

**Target: October 2026 CU (KB5002927, build 16.0.20326.20190) — with the pre-flight checklist below. Cumulative: farms on Aug 2026 CU or older may jump straight to Oct and skip Sep (Stefan, 2026-10-15). If you are on the Sep 2026 CU (or its COD hotfix, build .20158) you can move to Oct directly.**

Reasons:
1. Latest monthly security rollup and a **security update** (Microsoft: "evaluate and install as soon as possible"). Stefan 2026-10-16 said the Oct fixes include two Critical CVEs; the PU post was then regenerated (2026-10-19) after readers pointed out that the CVE pages list **14 Critical** — always trust the CVE pages over the blog table. CVE-2026-108452 was initially omitted from the MSRC list and is fixed by the Oct update (informational revision; no extra patch).
2. **Fixes confirmed in Oct CU:** the Sep 2026 CU regression where **subsite / publishing-web creation fails on sites provisioned in SharePoint 2013 (stale v15 `Microsoft.Office.DocumentManagement` event receivers — I-35)**: Stefan (2026-10-15): *"the code change to fix this was included in October 2026 CU"*. This is a code-side tolerance fix — **community testing not yet reported**; still repair stale registrations (script in §5A.3). The Oct CU does **not** appear to remove the need for the InfoPath settings (reader who skipped the COD hotfix and installed Oct had the same InfoPath web-part error until the Sep trending-post settings were applied — I-27).
3. **New regressions introduced by the Oct CU (all reader-reported, see I-44…I-47):** declarative workflows such as the OOB *Page Approval* and event-driven workflows blocked by the new `SPDeclarativeWorkflowRulesValidator` (engineering workaround: `ServerDebugFlags 60751`), HTML special-character encoding change in multi-line text fields (MS case open), Health Analyzer ULS noise, and a PSConfig flighting-assembly failure (single reporter). None carries an official Stefan banner.
4. **SP2013 workflows are NOT disabled by the Oct 2026 CU** (Stefan 2026-10-15, from source code; readers confirm 2013 workflows still run). The earlier "Oct disables SP2013 workflows" expectation was wrong. `Enable-SPWorkflow2013` is therefore not yet a hard pre-flight item, but run it anyway if you want to be forward-safe; a future CU will do it with notice.
5. **Distributed Cache (I-23) — still not confirmed fixed.** The Oct CU post lists no fix list and no commenter reports a verdict; the `59052` debug-flag workaround remains the only documented route. Treat as open until a comment/Stefan post confirms.
6. Package confusion: do not rely on KB number — see footnote ² in §2. Download packages only after the KB article is live; the Sep package was re-uploaded after first publication (I-41).

**Sep 2026 CU (KB5002908) remains valid but is now one CU behind.** Everything in the Sep 2026 notes below still applies to the Oct CU because the Oct CU contains it.

### Pre-flight checklist before installing Sep / Oct 2026 CU (from post-June comment analysis)
- [ ] **Enable legacy workflows per site collection *before* patching** (Sep CU disables SP2010 workflows on *all* site collections; Oct CU will do the same for SP2013): `Enable-SPLegacyWorkflow <url>` / `Enable-SPWorkflow2013 <url>` — available once Aug 2026 CU is installed. Sep CU has an *allow-list only* (the Aug `Get-SPLegacyWorkflowDisabledSites` cmdlet no longer exists). See I-38.
- [ ] `Enable-SPToolPane` if editors need classic web-part editing (I-36).
- [ ] Inventory **event receivers registered against old assembly versions** (`Version=15.0.0.0`, `14.0.0.0`, `12.0.0.0`, custom assembly redirects) — these fail to load after Sep CU and break workflow auto-start, subsite creation and third-party solutions (I-35).
- [ ] Pre-seed farm allow-lists: `AllowedDLCAssemblies` (DocumentManagement 15.0.0.0/14.0.0.0 — I-25), `BCSAllowedTypeNames` (I-24), `SPAllowedOutboundHosts` (I-32).
- [ ] Do **not** add/convert Distributed Cache hosts during patching (I-23); use graceful stop (`-ShouldGracefulStopDCache $true`) instead of removing the instance.
- [ ] After installing, confirm the **`System.CodeDom` / `Microsoft.SharePoint.WorkflowActions` / `Microsoft.Office.Workflow.Actions` authorizedType entries are still present in every web.config** (three commenters lost one after the Aug 2026 CU — I-20).
- [ ] If SQL Always On: remove `WSS_Logging` from the AG while PSConfig runs (I-41).
- [ ] **Added 2026-10-21 (Oct CU):** before patching, list SharePoint-2013-era content (`Version=15.0.0.0` / `14.0.0.0` receivers on sites, webs, lists **and content types** — Document Set, Video, System Media Collection — plus the `docid_customProvider_assembly` web property) and repair with an *extended* version of `Update-EventReceiverVersionTo16.ps1` (the community script only covers list receivers — Ingo, Chandu, Peter v.d. Berg, Abu; see §5A.7).
- [ ] **Added 2026-10-21:** keep the workflow `authorizedTypes` entries for **v14.0.0.0** (`Microsoft.SharePoint.WorkflowActions`, `Microsoft.Office.Workflow.Actions`, `…WorkflowActions.WithKey`, `System.CodeDom` 2.0.0.0 *and* 4.0.0.0) — OOB *Page Approval* needs them. Stefan: **add lines, never edit existing version numbers**; read the ULS `4letu … Block the namespace:` entry to learn exactly what to allow-list. One farm found the Sep CU had *removed* an entry added earlier; `SP2010-WORKFIX-WEBCONFIG-Fix-SystemCodeDom.ps1` reported "Modification already exists" (false positive) — verify web.config by hand after patching.
- [ ] **Added 2026-10-21:** after the Oct CU, if OOB Page Approval / event-driven workflows stop with `SPDeclarativeWorkflowRulesValidator: BLOCKED … ROOT.rules` apply the engineering workaround `$farm=Get-SPFarm; $farm.ServerDebugFlags.Add(60751); $farm.Update()` (I-44). Debug flags are short-term mitigations that **may be removed without notice** (Stefan 2026-10-19).
- [ ] **Added 2026-10-21:** Workflow Manager farms — install the matching Workflow Manager **Client** (16.0.20326.20190) on *every* SharePoint **and** WFM server; add outbound hosts to the WFM farm allow-list `WorkflowServiceAllowedOutboundHosts` (I-47).
- [ ] **Added 2026-10-21:** stop all processes that keep SharePoint DLLs loaded (IIS, scheduled tasks, PowerShell, SPCache) before installing — otherwise the MSI hangs with `hr=80070005 RemoveDirectoryAndChildren` (Stefan 2026-10-19).

**Still open at time of writing (carry-forward risk, does not block installing Oct 2026 CU):** *(I-44…I-47 are new Oct-CU items, see §5A.7)*
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

### October 2026 CU — KB5002927 — build 16.0.20326.20190 — 2026-10-14
- **Verdict (Stefan):** no banner; recommended with caveats (my assessment) — contains a code fix for the Sep-CU subsite-creation regression (I-35) but introduces new workflow-validator and encoding reports (I-44, I-45).
- **Highlights:** Monthly security rollup + **Feature Update 26H2** (AMSI Body Scan defaults to *Full mode*; config to exclude the "Everyone" claim in the People Picker — both promoted to Standard ring; opt-in People Picker search throttling — Early ring). Features still in Early ring from 26H1: JWE-encrypted tokens from Entra ID, drag-and-drop of web parts in publishing sites, AMSI option for document virus check, Text web part enhancements. PU post (2026-10-14, edited 2026-10-19) lists ≈ 90 CVEs, **14 Critical** after regeneration (CVE-2026-108452 added afterwards as an informational revision). Cite KB5002927 for the CVE list.
- **Fixes confirmed:** subsite/publishing-web creation on SP2013-provisioned sites that carry stale v15 event receivers (Stefan 2026-10-15, I-35) — *untested by readers at 10-21*.
- **Not in this CU (despite earlier expectations):** SP2013 workflow disablement (Stefan: not enabled in source); a confirmed Distributed Cache fix (I-23 — no statement).
- **Known issues introduced / reported:** I-44 (declarative workflow rules validator blocks OOB Page Approval + event-driven workflows; workaround ServerDebugFlags 60751), I-45 (HTML special characters re-encoded in multi-line text fields), I-46 (Health Analyzer ULS "rule not found in RuleExecutionParameters" — benign per Stefan, also seen on Aug CU; PSConfig `Microsoft.Skype.ECS.Client` not found — single reporter), I-47 (Workflow Manager Oct CU: outbound allow-list + client GAC not updating), Document-ID generation stopped (single reporter 10-20, see I-25).
- **Prereq:** Sep 2025 CU farms still need `Fix-SeptemberCU-Permission-Problem.ps1` (banner present in Oct post). PSConfig on every machine.
- **Package/KB note:** KB5002927 was also (mis)used for the unrelated Sep COD hotfix — see §2 footnote ².
- **Sources:**
  - https://blog.stefan-gossner.com/2026/10/14/october-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/
  - https://blog.stefan-gossner.com/2026/10/14/sharepoint-security-fixes-released-with-october-2026-pu-and-offered-through-microsoft-update/
  - https://blog.stefan-gossner.com/2026/10/14/feature-update-26h2-for-sharepoint-server-subscription-edition-has-been-released/
  - https://blog.stefan-gossner.com/2026/10/14/october-2026-cu-for-sharepoint-workflow-manager-is-available-for-download/
  - https://blog.stefan-gossner.com/2026/10/14/october-2026-cu-for-office-online-server-is-available-for-download/
  - KB: https://support.microsoft.com/en-us/kb/5002927

### September 2026 CU — KB5002908 — build 16.0.20326.20136 — 2026-09-09
- **Verdict (Stefan):** recommended — routine security rollup; one trending issue surfaced 12 days after release, interim fix already shipped.
- **Highlights:** Monthly security rollup (specific CVE list not captured from source post — consult KB5002908). Build number jumps to the `16.0.20326.x` baseline (from `16.0.19725.x`).
- **Fixes:** none carried over from prior open issues. *(The previous revision wrongly listed the Aug 2026 Distributed Cache fix (I-23) here; Stefan confirmed on 2026-09-09 that it is still in development.)*
- **Known issues introduced:** InfoPath Forms Services + SP2010 workflow failures (**I-27**) — interim COD hotfix (build .20158, no KB article) published 2026-09-21; superseded by the Oct 2026 CU.
- **Open issues carried forward, not fixed by this CU:** Distributed Cache provisioning (**I-23**), BCS allow-list (**I-24**, by design), Document ID allow-list (**I-25**, by design), RER blocking (**I-26**), search topology (**I-33**), QueryLogJobDefinition SQL pool exhaustion (**I-17**).
- **Prereq:** if farm is still on Sep 2025 CU, apply `Fix-SeptemberCU-Permission-Problem.ps1` first — banner still present in this month's post. Configuration Wizard must be run on each farm machine after install.
- **Fix-list correction (2026-09-29 revision):** the Sep 2026 CU does **not** roll up the Distributed Cache fix (I-23) — see §3.
- **Additional behaviour changes / regressions found in the 120 comments (all after release):** SP2010 workflows + InfoPath Forms Services + ToolPane **disabled by default** (I-27, I-36, I-38); event receivers registered against old assembly versions no longer load → workflow auto-start, subsite creation and third-party solutions break (**I-35**, not in KB, no PG fix); Document-ID assembly allow-list blocks site provisioning on old site collections (I-25); RER outbound host allow-list (I-26/I-32); `Get-SPLegacyWorkflowDisabledSites` removed (allow-list only); package re-uploaded after first publish (I-41a); Update Catalog delayed ~1 day; modern **Check-In** menu item missing, custom tiles across web apps, empty navigation managed properties on new pages (I-42).
- **Intermediate fix:** COD hotfix **build 16.0.20326.20158** (2026-09-21) supersedes the Sep CU for InfoPath/SP2010-workflow users; it has **no KB article** (Download Center entry reused the number 5002927, which is now the Oct 2026 CU — corrected 2026-10-21; Stefan 2026-10-14).
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
| I-25 | Document ID Service | Existing Document Sets return null Document ID; `DocIdSettings.aspx` throws `InvalidDocumentIdProviderException`; **Sep 2026 CU also breaks subsite/publishing-web creation** ("Failed to create the 'Images' library") on *older/migrated site collections* | High | Aug 2026 CU (Sep 2026 CU for site creation) | *By design — root cause confirmed by Microsoft support & Stefan* | `$farm.AddGenericAllowedListValue("AllowedDLCAssemblies","Microsoft.Office.DocumentManagement, Version=15.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c")` (also `Version=14.0.0.0` if ULS names it) → `$farm.Update()` → `iisreset`. Root cause: old site collections store a 14/15.0 DocID provider assembly reference in root-web properties; alternative is rewriting `docid_customProvider_assembly` to `Version=16.0.0.0` | **[2026-10-21 update]** Sep CU: Document-Set `DocumentSetEventReceiver` / `DocIdHandler` v15 (and v14) references on *content types* break provisioning and Document-Set propagation; `AllowedDLCAssemblies` alone did not fix it for several readers (the ReflectionOnly path ignores the allow-list for missing DLLs — I-35). Oct 2026 CU: one reader reports **no Document IDs generated at all** (10-20, unanswered) — repair `docid_customProvider_assembly` on every root web (script posted 10-19, unverified).
| I-26 | Remote Event Receivers | RERs without an `AppIdentifier` are blocked. **New registrations are blocked already since Aug 2026 CU** (CSOM/PnP/PowerShell → "Access denied … Adding a Remote Event Receiver Definition without an AppIdentifier is blocked"); the KB text only announced blocking of *existing orphaned* RERs for the **Nov 2026 CU** (Health Analyzer rule + `Get-SPOrphanedRemoteEventReceiver`). Sep 2026 CU adds an *outbound host* check on RER calls (`Outbound request blocked: host … is not in SPAllowedOutboundHosts`) | Medium (by design) | Aug 2026 CU | *By design* — PG position (relayed by Stefan 2026-08-19): register through a SharePoint Add-in so the receiver is stamped with an app identity; Stefan 2026-09-15: no change planned | Register via Add-in/app installer or REST with app identity; add RER hosts to `SPAllowedOutboundHosts` (farm property, not web-app). Microsoft support gave a temporary flag `ServerDebugFlags 50008` + `iisreset` for PowerShell registration (community-reported; **reported slow** — 9 large libraries took ~2.5 h; Microsoft could not confirm it survives Nov 2026). Farm-solution ItemEventReceiver that forwards to the .svc endpoint is a viable redesign. Reaction in comments: strongly negative (breaks K2 / air-gapped provisioning) | **[2026-10-21]** Health Analyzer rule *"Remote event receivers without application identity"* appears since Sep CU; `Get-SPOrphanedRemoteEventReceiver` also flags **SharePoint webhooks** (`SPWebhookItemEventReceiver`). Stefan (10-02): all RERs without an app identity will be blocked with the **November CU** and webhooks may be hit — open a Microsoft ticket for clarity.
| I-27 | InfoPath / Workflows | Sep 2026 CU **disables InfoPath Forms Services and SP2010 workflows by default**. Symptoms: "The specified form template could not be found, or is not compatible with rendering in the browser", "The form cannot be rendered … State Service", manual-start forms (`IniWrkflIP.aspx`, `CstWrkflIP.aspx`, approval workflow start) fail even after `Enable-SPLegacyWorkflow`; `Set-SPInfoPathFormsService -AllowUserFormBrowserRendering $true` throws "no longer supported because InfoPath is deprecated"; new `InfoPathDeprecation` HTTP module in web.config. Affects **all** InfoPath forms, not just workflows | High | Sep 2026 CU | Intermediate fix **KB5002927** (build **16.0.20326.20158**, released 2026-09-21, supersedes the Sep CU; no separate KB page; will be rolled into Oct CU but the script stays mandatory) | Install KB5002927 (*no* Config Wizard yet) → **restart the PowerShell session** → run Stefan's script (debug flag 5023, `AllowUserFormBrowserRendering/Enabling = $true`) → run Config Wizard. Script run once is enough. **Correction 2026-09-24:** Stefan first said publishing new SP2010 workflows stays permanently disabled, then corrected after asking the PG — the hotfix *did* re-enable creating/publishing SP2010 workflows, but *do not read this as a long-term commitment*; InfoPath Forms Services and SP2010 workflows are expected to be **removed in a future CU** (a KB will precede removal). Nintex workflows can be published only where `Enable-SPLegacyWorkflow` was run. Older, community-reported DLL-swap trick did *not* work for others | **[2026-10-21 update]** KB number 5002927 is now the Oct CU (build .20190); the Sep COD hotfix (.20158) had no KB. A reader who skipped the hotfix and installed Oct had the same InfoPath web-part error → the settings from the trending post are still required on Oct. Setting `httpOnlyCookies="false"` clears the "session cookies disabled" form error but **weakens XSS protection** (Stefan 10-15; customer risk decision). OOB Page Approval workflows need the v14 authorizedTypes (I-20/I-44).
| I-28 | Auth / Tokens | **Actor-token audience validation** ("defense-in-depth feature under development") → Office Online Server integration and **SP2013 workflows (WFM↔SharePoint) fail** with 401/403 ("You do not have permissions to open this file in the browser", "Un-whitelisted client sent us an OAuth token"). Listed only in the KB *Known issues* section | High | Jul 2026 CU | **Aug 2026 CU** — property `DisableActorTokenAudienceValidation` was *removed*; Stefan: "This issue was fixed and the flag should be reverted" | `$farm.DisableActorTokenAudienceValidation = $true; $farm.Update()` **once per farm** (stored on the SPFarm object) *after PSConfig*. Multi-WFE farms with OOS saw 401s until it was set. Stefan: do not confuse with SP2016 WOPI issue (I-21). A reader still got 403 after setting it ("app principal does not exist") → support case. |
| I-29 | Auth / Distributed Cache | **Session-cookie transform protection** → session token cannot be stored in Distributed Cache (`Session cookie transform was triggered unexpectedly`, `NotSupportedCookieTransform`); users on multi-WFE farms with **Trusted-Provider/Forms auth** are re-prompted for sign-in whenever they hit a different WFE (also seen as FedAuth-cookie loss behind an F5 after Jun 2026 CU). Windows-auth farms not affected | High | Jul 2026 CU (a Jun 2026 CU report exists, unconfirmed) | **Aug 2026 CU** (Stefan 2026-08-12: "checked in for all product versions") | Sticky sessions on the reverse proxy, or single WFE. **Never set `SessionCookieTransformProtectionEnabled=$false`** — Stefan/PG: "very dangerous", exposes servers to significant security risk; PG asked a third-party post recommending it to be removed. |
| I-30 | SharePoint Designer / Safe controls | Custom SPD forms and apps stop rendering (`Unsafe control … DataFormParameter … property traversal char`, `Re-definition of tag … maintaining consistency of attributes`, `WebPartPageUserException`, apps failing `SafeControls.IsSafeControl`) | Medium | Jun/Jul 2026 CU (`xsl:template` tag issue traced by Stefan to **Jan 2026 CU**) | *By design* — configuration | Add web.config `<SafeControl Assembly="Microsoft.SharePoint, Version=16.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c" Namespace="Microsoft.SharePoint.WebPartPages" TypeName="DataFormParameter" Safe="True" AllowPropertiesTraversal="True" />` (post with `[ ]` for angle brackets — the blog strips them). Plus `$farm.AddGenericAllowedListValue("AllowedTagPrefixesWhichAreNotWebControlsList","xsl:template")`. `$farm.PreserveAttributeConsistency=$false` is the alternative when the SafeControl entry is absent; the "Re-definition of tag" ULS message is *expected, not an error* (Stefan). Some apps also needed `SkipUpdateWebConfigPermission`/WSS_WPG rights on web.config (Stefan: only if app code touches web.config). |
| I-31 | User Profile | `UserProfile.Commit` / `Update-SPProfilePhotoStore` fail: "Url is not safe … `SPServiceContext.Current is null`" when setting `PictureURL` from PowerShell | Medium | Jul 2026 CU | **Aug 2026 CU** (readers confirm flag no longer needed) | `$f.ServerDebugFlags.Add(53534); $f.Update()` (iisreset not needed) → do the update → **remove** the flag |
| I-32 | Outbound host allow-list | New enforcement of `SPAllowedOutboundHosts`: WCF-BCS (Jul), OData-BCS crawl (Aug: `Host … not in allowlist … for property 'ODataServiceUrl'`), Remote Event Receivers (Sep). Symptom for WCF BCS: Entity picker/Edit form "Business Data Connectivity is configured incorrectly" while Display form still shows stored values | High | Jul 2026 CU (expanded Aug, Sep) | *By design* — farm allow-list | `$farm.AddGenericAllowedListValue("SPAllowedOutboundHosts","host")` per host (farm property, **not** web-app). Escape hatch (unsafe): `DisableWcfBdcHostAllowlistEnforcement` = debug flag **115** (message text from ULS). One farm needed a **server reboot** before the value was read. |
| I-33 | Search | After patching (reported since **Apr 2026 CU**, every CU since, incl. Jun/Jul): CA shows "Unable to retrieve topology component health states … admin component is not up", crawl/incremental crawl hangs or "Paused for: External request", "All query processing components are in 'Failed' status", ULS `Failed to synchronize legacy admin … Failed to connect to system manager`, CSS connector failures. Also seen after Windows Updates (Benjamin F., 14 farms: 9 affected) | High | Apr 2026 CU (per Stefan) | **Not fixed** (Stefan 2026-08-13). Not reproducible → PG has no fix | In order of invasiveness: (1) restart `SPSearchHostController` (wait 3-4 min, restart again if needed) and `OSearch16`; (2) `sc.exe config SPSearchHostController start=delayed-auto` + `sc.exe config OSearch16 start=delayed-auto`, reboot (Stefan; worked for several, not all; keep permanently is fine); (3) `$ssa.ForceResume($ssa.IsPaused())` after stopping the host controller for 3-4 min; (4) `iisreset` for CSS connector errors; (5) last resort: rebuild topology (one reader loses ~2.5 days of crawl per incident). One reader observed it depends on the search service account's local-admin membership. Several readers *stay on Apr 2026 CU* because of it — a security trade-off. Separate: SearchAdmin DB migrated from 2019 fails psconfig with missing `proc_MSS_*` stored procedures (unresolved). |
| I-34 | iFrame / CSP | `AppWebProxy.aspx`/app-authorize pages now send `Content-Security-Policy: frame-ancestors 'self' teams…` and `X-Frame-Options: SAMEORIGIN` → provider-hosted add-ins, SP2019 News app, Office Online preview from Search Center on a different URL fail to frame | Medium | Jul 2026 CU | *By design* — configuration (Stefan: worth investigating; product group not confirmed as bug) | `$farm.EnableCSPHeaderForPage = $true` **and** `$farm.AddGenericAllowedListValue("AllowIframeAppAuthorizePageDomains","<host of the framing app>")` (hosts of the *external app / OOS*, not SharePoint web apps; wildcards allowed) → app-pool recycle on WFEs. If a custom CSP header is needed, disable SharePoint's injection per Stefan's 2024-03 article. |
| I-35 | Event receivers / assembly binding | **Sep 2026 CU stops honouring assembly-version redirects for event receivers**: `LoadEventReceiverTypeSafe: Failed to load type … Version=15.0.0.0 …` (also 7.0.0.0→8.0.0.0 custom redirects, third-party v12/v14 references, `ReflectionOnly … has not been preloaded`). Consequences: SP2010/SP2013 workflows created before migration no longer **auto-start** (manual start works), multi-step approval workflows stall after step 1 (`ContentSubscriptionEventReceiver`), subsite creation fails on old site collections (`STS#0`, publishing `Images` library), third-party (Nintex Forms web-part tests, Aderant HSListGuru) | High | Sep 2026 CU | **Not fixed** (no PG statement; Stefan 2026-09-18: "currently the only solution is to update the event receiver registration"). Not in KB | (1) Re-point registrations to `Version=16.0.0.0` with a script (community `Update-EventReceiverVersionTo16.ps1` — confirmed by 3 readers and **endorsed by Stefan 2026-09-29**, incl. App Catalog upload failure; adjust `$oldAssembly` for v14 / DocumentManagement); (2) allow `Microsoft.Office.DocumentManagement 15.0.0.0` in `AllowedDLCAssemblies` (see I-25) for site creation; (3) reader-reported (unofficial, exposes a security check) `ServerDebugFlags.Add(59025)` + `iisreset` fixed three DEV/TEST farms. 3rd-party binaries compiled against 12.0/14.0 have no workaround except vendor recompile. | **[2026-10-21 update]** Oct 2026 CU contains a code change fixing the *subsite creation* symptom (Stefan 10-15; untested by readers). **Event receivers on content types** (Document Set, Video, System Media Collection) and `docid_customProvider_assembly` are *not* covered by the community script; reader-written scripts are reported working (§5A.7). Debug flag `59025` (RevertEventReceiverValidationFix) = Assembly.Load path — a security bypass, temporary only. Root cause (Ingo): the new validation path calls `Assembly.ReflectionOnlyLoad`, which ignores binding redirects/publisher policy.
| I-36 | Editing UI | **ToolPane feature disabled by default** — web parts cannot be edited in the browser after Sep 2026 CU | Medium (by design) | Sep 2026 CU | *By design* — KB Known/Notice section | `Enable-SPToolPane` |
| I-37 | Solutions / Workflows | WSP activation blocked: "Activation of solutions with sandboxed code has been disabled" for packages that contain a Feature with `ReceiverAssembly=Microsoft.SharePoint.WorkflowServices` (`SPWorkflowPackageFeatureReceiver`), i.e. declarative SP2013 workflows | Medium | Aug 2026 CU | **Not fixed**; reporter opened a support case | Reader workaround: remove `ReceiverAssembly`/`ReceiverClass` attributes from `Feature.xml` in the WSP. Stefan: open case. |
| I-38 | Legacy workflow platforms | **Policy/behaviour timeline**: SP2010 workflows disabled by default with **Sep 2026 CU** (all site collections, including existing, unless allow-listed); SP2013 workflows disabled by default with **Oct 2026 CU**. Rationale (Stefan): reduce attack surface. SP2013 workflows + SPWFM remain supported (Stefan 2026-09-07/-24: no plan to drop) | High (change mgmt) | Aug 2026 CU (cmdlets) / Sep 2026 CU (SP2010 off) / Oct 2026 CU (SP2013 off) | n/a — policy | `Enable-SPLegacyWorkflow <site-collection-url>`, `Enable-SPWorkflow2013 <url>`, `Disable-SPLegacyWorkflow`, `Get-SPLegacyWorkflowEnabledSites`, `Get-SPWorkflow2013EnabledSites`, `Get-Command *SPLegacyWorkflow*`. Run in SharePoint Management Shell **on an SPSE server with Aug CU or later**. Needed once per site collection, **also for every new site collection** (provisioning scripts must call it) and again after a 2019→SPSE database attach. Stefan (2026-09-03): the Aug 2026 CU itself did *not* disable workflows (a few readers reported engines disabled after Aug — unconfirmed). SP2010 list-retention policies tied to SP2010 workflows have no SP2013 equivalent. | **[2026-10-21 correction]** Oct 2026 CU does **not** disable SP2013 workflows (Stefan, source-code check 10-15; Paul C. confirms they still run). No new date announced.
| I-39 | SP2013 workflows / SPWFM | Workflows start then fail `HTTP 401/403` back into SharePoint: (a) Jul 2026 actor-token (I-28); (b) **Aug 2026**: workflow fires as *Access denied* when the initiating user got permissions **through an AD security group** (works with direct user grants; "actor token has no AppIdAcr claim"); (c) SP2013→SPSE migrations: `invalid_client` 401 from SPWFM callbacks; (d) SP2013 workflow calling an SP2010 workflow (`InteropService.StartWorkflow` Unauthorized) | High | Jul/Aug 2026 CU | *Not acknowledged*; Stefan → support case (Aug/Sep). SPWFM Aug CU KB5002864 did **not** help the reporter | (b) Add the individual users in addition to the group; watch the *primary-group* pitfall. SPWFM min version: Stefan clarified the KB text is misleading — **KB5002799 (Nov 2025) is the *minimum***, newer is recommended; SPWFM Sep 2026 fix (KB5002925) was released 2026-09-11 out-of-band although the KB says 09-08. |
| I-40 | InfoPath / session | `IniWrkflIP.aspx`: "form cannot be displayed … session cookies have been disabled" after Jul 2026 CU (also Aug, new farms) | Medium | Jul 2026 CU | Unknown — not on Stefan's list (Stefan 2026-08-20) | Setting `httpOnlyCookies="false"` in web.config makes it work (readers) — security trade-off; superseded by I-27 after Sep 2026 CU. |
| I-41 | Patching / PSConfig | Install/upgrade anomalies: **(a)** Sep 2026 package first published was wrong → `SPMissingAttributeException … RegisterInfoPathDeprecationHttpModule requires To and From build information` — re-download (build 16.0.20326.20136). **(b)** Jun 2026 KB hash and build number in KB did not match the download (fixed by MS within a day); Aug OOS KB text pointed to wrong KB/duplicate file. **(c)** MSI **1603** on a *new* farm (Feb 2026 build) with the Install-SPSE_Fix script → clearing `%TEMP%`, installing Jun CU + PSConfig first, then Jul worked. **(d)** PSConfig `MergeWebConfig … NullReferenceException` where web.config had *partial InfoPath merge state* (Sep). **(e)** `RECONFIGURE` permission error on Secure Store DB → temporarily `GRANT ALTER SETTINGS`/sysadmin to setup account. **(f)** `Get-SPServer … NeedsUpgrade` inconsistent between two servers → clear config cache (keep `Cache.ini`, set to `1`). **(g)** PSConfig fails on `WSS_Logging` when it is in a SQL Always On AG (must be removed while PSConfig runs). **(h)** `Login failed … untrusted domain (18452)` after OS updates — Stefan: AD/SPN/NTLM problem, "SharePoint is a victim" (see Kerberos I-18). **(i)** timer job "Workflow" running for hours after the pre-parse flag was cleared — clear timer cache/restart SPTimerV4. **(j)** LOGS folder permissions for `WSS_ADMIN_WPG`/`WSS_WPG` lost after patch → usage-import jobs fail with access denied. **(k)** SharePoint update auto-installed by BigFix/WSUS unexpectedly re-triggered the workflow break. **(l)** Sep 2026 packages missing from Update Catalog for ~1 day (fixed). | Medium | Jun–Sep 2026 CU | Varies (see text) | See each item. Stefan: SharePoint updates cannot be uninstalled → validate every CU in a test farm against business-critical features. |
| I-42 | Modern UI / JSOM / misc (single reporters, **unacknowledged**) | Yes/No **calculated column** no longer recognised as Boolean (Jun/Jul); JSOM `ValidateFormDigest` access denied + "too many redirects" on custom CSS/JS (Jul); modern list paging/item count broken (SP2019, Jul); **Site activity web part empty after Restore/Move (Aug CU)**, **Office 2016 cannot edit (Aug CU)**, **modern file upload fails (Sep CU)**, **Check-In missing in modern library menu** on 4 farms (Sep — classic view fine); display-template check-in no longer updates `.js` (Sep); `?contents=1` web-part diagnostic param broken (Aug); custom tiles across web apps need DB rights for the MySite app-pool account (Sep); new publishing pages get empty `owstaxidNavigation`/`Tags` managed properties (Sep); Windows Server 2025 + Sep CU "Server Error" on every site (ULS needed); `PnP Connect/Invoke-PnPQuery` 401/403 (Aug/Sep — Stefan: PnP not supported/tested) | Low–Medium | Jun–Sep 2026 CU | Unknown | Open a support case where business-critical; no acknowledged fix. |
| I-43 | Performance / UPS | Recurring HTTP throttling / **503 Server Busy**, growing request queue; long-running calls to `FeedCacheService.svc` / `ProfileDBCacheService.svc`; IIS pool recycling only helps for minutes. Two farms confirm (Belen, Andy D.) | High | Jun 2026 CU | **Not acknowledged** — Stefan: open MS support case (2026-07-10) | Mitigate by pulling WFEs from LB + recycling pools; one farm resolved a related "0.3 s → 80 s response time" by re-running PSConfig after Windows Updates. |
| I-44 | Legacy workflows / validator | **Oct 2026 CU:** `SPDeclarativeWorkflowRulesValidator: BLOCKED workflow 'Microsoft.SharePoint.Workflow.ROOT' … ROOT.rules deserialized with N error(s) … type 'Microsoft.SharePoint.WorkflowActions.WorkflowCodeTypeReferenceExpression' could not be resolved` — OOB *Page Approval* (publishing) and event-driven workflows fail to start; SPD list workflows keep working. 3 reporters (Stephan 10-16, Asay 10-19, Blast 10-20) | High | Oct 2026 CU | Not fixed | Stefan (10-20, after talking to engineering): `$farm=Get-SPFarm; $farm.ServerDebugFlags.Add(60751); $farm.Update()` — reporter confirmed it solved the problem. Debug flags are temporary and may be removed without notice. |
| I-45 | Text fields / encoding | **Oct 2026 CU:** HTML in multi-line text fields — special characters now stored encoded (`{"` → `&#123;&quot;`). MS ticket opened by reporter; Stefan asked for updates (10-19). Unconfirmed by PG | Medium | Oct 2026 CU | Unknown | Support case; test custom field renderers/JSON-in-text-field solutions before patching |
| I-46 | Patching / Health Analyzer | **(a)** Oct (and Aug) CU: OWSTIMER logs *"Health rule …StatisticsAreOutOfDate / DatabasesAreFragmented was not found in RuleExecutionParameters"* — rules present and enabled; Stefan: performance-relevant only, then "open a support case" (10-15); seen on Aug 2026 CU too (Sunil 10-16). **(b)** PSConfig on Oct CU fails `TypeInitializationException … SPOnPremFlight … ECSSPFlightDataProvider … Microsoft.Skype.ECS.Client, Version=16.6.0.995 not found` — single reporter, unanswered. | Low / Medium | Aug–Oct 2026 CU | Unknown | (a) none needed; (b) re-run install/repair, support case |
| I-47 | Workflow Manager (SPWFM Oct CU) | **(a)** After the WFM update, 2013-workflows calling REST endpoints fail: `The outbound request destination is not permitted by the Workflow Manager outbound request policy … add its host to the farm-level allow list 'WorkflowServiceAllowedOutboundHosts'`. `Get-WFFarm` shows `SupportedGenericAllowedListNames = WorkflowServiceAllowedOutboundHosts / …Schemes / …Ports / …AttachableMembers` — **no official documentation** of the value format (2 reporters, unanswered). **(b)** WFM Client 16.0.20326.20190 not updating the GAC copy of `Microsoft.Workflow.Common.dll` (stays 16.0.10001.10000) → `TypeLoadException NdcsAllowListSerializationBinder`; reinstall did not help — Stefan: open MS support case. **(c)** No-code sandbox solutions used to deploy SP2013 workflows stopped working after Aug 2026 CU (activities need `ReceiverAssembly`) — unanswered. | High | Oct 2026 SPWFM CU (a,b); Aug 2026 CU (c) | Not fixed | (a) Try `Set-WFFarm`/`Add-WFGenericAllowedListValue`-style cmdlets per `Get-WFFarm` property names (unverified); (b) support case. Verify WFM Client is installed on **all** SP and WFM servers. |
| I-17 | Search / Timer Jobs | **QueryLogJobDefinition SQL connection pool exhaustion** — `QueryLogJobDefinition` fails with Event 6399: *"Timeout expired. The timeout period elapsed prior to obtaining a connection from the pool"*. Timer job leaks SQL connections on every run; pool (max 100) fills up after a few days causing cascading timer job failures. ULS signature: `QueryLogProcessor: AssignDocIdsToResults error: The method 'EndExecuteReader' cannot be called`. **Still present after Mar 2026 CU (KB5002843), Apr 2026 CU (KB5002853), and May 2026 CU (KB5002863) — no official fix published as of May 2026.** Not independently re-verified against Jun–Sep 2026 CUs during this update pass (no new Stefan post or MS Q&A activity surfaced); treat as still open until confirmed otherwise. Microsoft confirmed investigating but no KB article or fix released. | High | Mar 2025 CU (regression) | **Not fixed — open as of 2026-09 (last independently confirmed May 2026)** | (1) Disable the **Query Logging Timer Job** in Central Admin (most effective). (2) Schedule a nightly restart of `SPTimerV4` to clear the pool every 48–72 hrs. (3) Increase SQL pool size as short-term delay: add `Max Pool Size=200` to the Search connection string. Sources: [Oct 2025 Q&A](https://learn.microsoft.com/en-us/answers/questions/5583482/many-critical-events-in-sharepoint-se-after-july-2) · [Mar 2026 Q&A #1](https://learn.microsoft.com/en-us/answers/questions/5816641/querylogjobdefinition-may-be-exhausting-the-sql-co) · [Mar 2026 Q&A #2](https://learn.microsoft.com/en-us/answers/questions/5849106/search-service-sql-connection-pool-exhaustion-afte) · **Monitored** by `weekly_check.py` (3 answers as of 2026-05-18; new answers trigger GitHub issue) |

---

## 5A. Post-June 2026 deep analysis — posts + all comments (revision 2026-10-21)

**Method.** Every Stefan Goßner post dated 2026-06-01 → 2026-09-28 (32 posts: SPSE, SP2016, SP2019, OOS, Workflow Manager, PU summaries, trending/resolved issues, EoS, 26H1) was downloaded, and **all 1,181 reader comments** were pulled through the blog's WordPress REST API (the RSS comment feeds only expose the newest 20). SPSE-relevant threads were read in full (≈ 700 comments); SP2016/2019/OOS/SPWFM threads were read where they contained SPSE-relevant or cross-version content. **Trust model:** Stefan's replies = authoritative; another reader's fix that Stefan or a second reader confirmed = *confirmed*; a single reader's claim = *unconfirmed*. Comment counts (2026-09-29): Jun SPSE CU 48 · Jul SPSE CU 120 · Aug SPSE CU 124 · Sep SPSE CU 120 · SP2010 WF Jun-issue 34 (+82 on the "resolved" repost) · Jul WF issue 111 · BCS 32 · "Are you using SP2010/2013 workflows" 78 · InfoPath 27.

**Revision 2026-09-30 (incremental).** Re-pulled the WordPress REST API for 2026-06-01 → 2026-09-30: still **32 posts** (newest = InfoPath trending post 2026-09-21; nothing new published since) and **1,307 comments** (33 new since the 09-29 pass; last comment 2026-09-30 19:52 UTC). No new CU, hotfix or PG statement. New facts from the 33 comments are in §5A.6.

**Revision 2026-10-21 (incremental).** Re-pulled the REST API for 2026-06-01 → 2026-10-21: **37 posts** (5 new: Oct 2026 SPSE CU, PU summary, Feature Update 26H2, Workflow Manager CU, OOS CU; edited since last pass: 26H1 post on 10-14, PU Oct post on 10-19, Aug trending posts) and **1,465 comments** (the 168 dated ≥ 2026-09-30 were read in full; ≈ 10 older comments no longer returned — deleted/spam-filtered). New facts are in §5A.7; corrections to earlier statements are rows 10–15 below.

### 5A.1 What the comments changed (corrections to earlier revisions)
| # | Earlier statement | Corrected by |
|---|---|---|
| 1 | I-15 Text web part "not yet fixed" | Fixed in **Jun 2026 CU** (Stefan's resolved post, 2026-07-02) |
| 2 | Sep 2026 CU rolls up the DCache fix (I-23) | Stefan 2026-09-09: fix "still in development"; workaround still needed |
| 3 | I-24 BCS "not fixed" (a bug) | **By design**; allow-list is the *solution* (Stefan 2026-08-15). Only runtime-generated proxy assemblies are unsolved |
| 4 | I-25 Document ID "no fix confirmed" | Root cause + fix known (`AllowedDLCAssemblies`); same root cause breaks Sep CU site creation |
| 5 | I-26 RERs blocked "in Nov 2026" | **New registrations blocked since Aug 2026 CU**; Nov only affects existing orphaned RERs |
| 6 | I-27 "publishing new SP2010 workflows permanently disabled" | Stefan retracted 2026-09-24: the COD hotfix (build .20158) re-enables publishing (no long-term promise) |
| 7 | I-20 "not stated as fixed" | Config requirement (not a defect); need 3 authorizedType groups; OWSTIMER rule |
| 8 | Jul 2026 CU known issues = 3 | Actually ≥ 9 (actor token, session cookie/DCache, PictureURL, DataFormParameter, outbound hosts, CSP/iFrame, …) — see I-28…I-34 |
| 9 | Aug 2026 "four issues" | ≥ 12 incl. DCache role conversion, sandbox activation, AD-group workflow denial, search allow-lists |
| 10 | KB5002927 = Sep intermediate fix (build .20158) | KB5002927 is the **Oct 2026 CU (build .20190)**; the Sep COD hotfix had no KB (Stefan 2026-10-14/15). Verify by build number |
| 11 | "Oct 2026 CU disables SP2013 workflows" | **Not enabled in Oct CU** (Stefan, source-code check 2026-10-15); date unannounced |
| 12 | "Oct CU will contain the DCache (I-23) fix (unofficial)" | No statement either way; Oct post has no fix list — remains **unconfirmed/open** |
| 13 | Sep 2026 CU "recommended" with interim fix as alternative | Oct 2026 CU is now the target; the interim fix is superseded |
| 14 | I-35 "no PG fix" | Subsite-creation symptom fixed in code in the Oct CU (Stefan 10-15, unverified by readers); script gap for content types/DocID remains |
| 15 | PU Oct summary "8 Critical CVEs" / "two Critical fixes" | Regenerated 2026-10-19: **14 Critical**; CVE-2026-108452 was omitted at first and is fixed by the Oct update |

### 5A.2 Deprecation / behaviour-change timeline
| Date / CU | Change | Action |
|---|---|---|
| 2026-07-14/15 | EoS: SP2016, SP2019, Project Server 2016/2019, **SP2010 workflows (incl. Nintex etc.)**, **InfoPath Forms Services**, Basic auth, SPD 2013, Classic Workflow Manager. Support cases can be opened to 07-14 | Migrate; Stefan: options = SP2013 workflows (VS 2022 package, supported to 2032), Power Automate (needs internet/on-prem gateway), third-party. SPSE supported at least to 2035 |
| Jun 2026 CU | Workflow pre-parse validation (I-19); 26H1 | web.config allow-list |
| Jul 2026 CU | Actor-token, session-cookie, outbound-host, CSP, DataFormParameter hardening (I-28…I-34) | Known-issues script, allow-lists |
| Aug 2026 CU | Last SP2016/2019 CU; BCS type allow-list; `AllowedDLCAssemblies`; RER without AppIdentifier blocked; workflow enable cmdlets | Pre-seed allow-lists; **run `Enable-*` cmdlets before Sep/Oct** |
| **Sep 2026 CU** | **SP2010 workflows, InfoPath Forms Services, ToolPane disabled by default**; event-receiver assembly binding tightened; SP2010 allow-list only (no deny-list) | COD hotfix (.20158) or Oct CU + script; `Enable-SPToolPane`; re-register receivers at v16 |
| **Oct 2026 CU** (released 2026-10-14, **26H2**) | SP2013 workflow disablement **did NOT ship** (Stefan 10-15, source check); new declarative-rules validator (I-44); WFM outbound allow-list (I-47); AMSI Full-mode default | `ServerDebugFlags 60751` if OOB workflows blocked; keep v14 authorizedTypes; `WorkflowServiceAllowedOutboundHosts` on WFM |
| **Nov 2026 CU** | **Orphaned RERs (no AppIdentifier) blocked** — Health Analyzer rule now warns; webhooks are flagged (Stefan 10-02); **SP2013 workflow disablement possibly with a later CU (unannounced)** | `Get-SPOrphanedRemoteEventReceiver`; migrate to add-in/farm solution; ticket for webhooks |
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

### 5A.6 Delta 2026-09-29 → 2026-09-30 (33 new comments)
- **I-35 widened + Stefan confirms the script.** App Catalog upload fails after Sep CU (Product ID/Title/Metadata Language not read; ULS `LoadEventReceiverTypeSafe … SPCorporateCatalogEventReceiver … Microsoft.SharePoint, Version=15.0.0.0`) = same root cause: event-receiver registrations still pointing to SP2013 assemblies. **Stefan (09-29):** run community `Update-EventReceiverVersionTo16.ps1`; for v14 (SP2010-era) registrations set `$oldAssembly` to `14.0.0.0`; for `Microsoft.Office.DocumentManagement` set old=15.0.0.0 / new=16.0.0.0 explicitly. Script is now **Stefan-endorsed** (was "confirmed by three readers"). **Third-party DLLs:** Stefan — check the required signature with the vendor; a reader whose receiver assembly is a 3rd-party DLL compiled against old Microsoft.SharePoint has **no viable fix** if older Microsoft.SharePoint references are intentionally dropped in the Sep CU (unanswered).
- **I-27 InfoPath — two more causes after the COD hotfix (build .20158).** (a) Stefan (09-29): if the InfoPath script was run *after* the Config Wizard, forms stay broken until **Central Admin → InfoPath Forms Services → "Render form templates that are browser-enabled by users"** is enabled manually. (b) Reader-found (09-30, confirmed working): list **form mappings** for Display/Edit/New pointing at `DispForm.aspx`/`EditForm.aspx`/`NewForm.aspx` instead of the InfoPath form pages — fix the mappings. Stefan knows of no problem with the script itself; Enable-SPLegacyWorkflow per site collection is still required (reader reminder).
- **I-19/I-27 residual:** one more report of `RunWorkflow … This feature has been temporarily disabled` after Sep CU despite `System.CodeDom` authorized and `Enable-SPLegacyWorkflow` (09-29) and a report of SPD workflows with *Delay* failing (09-30) — both unanswered.
- **IIS module loss after PSConfig (known, 2023):** `SPRequestFilterModule` association removed from web apps after PSConfig → sites fail (FREB logs show file/module not found). Stefan (09-30): this is the 2023-10 trending issue; apply the fix from that post (AMSI-related), **do not hand-edit IIS/web.config**. Reader asked why it recurred in 2026 — unanswered. Treat as a post-PSConfig verification step.
- **I-36 ToolPane — Stefan's rationale (09-30):** ToolPane is "the first step of a broader **defense-in-depth initiative**": several features not required by all customers will be disabled by default with a re-enable option, to reduce attack surface; *no known threat vector* tied to the disabled features. Expect more default-off features in coming CUs; also stated in the Sep CU KB article.
- **I-42 additions (unacknowledged/unanswered):** (Aug CU 16.0.19725.20522) modern **Site activity** web part shows "You don't have any recent activity" once recent changes contain a *Restore* or *Move* (prod + QA; Stefan 09-29: not known — open a ticket); **Office 2016 cannot edit documents** from libraries after Aug CU (forced checkout → "cannot be checked out"; otherwise opens read-only; 09-29, unanswered); Sep CU: Modern-view **file upload/replace fails** for some users on UAT after KB5002908 (09-29, unanswered).
- **I-24 (BCS):** reader-confirmed extra `BCSAllowedTypeNames` entries for search crawl of the taxonomy term store (`TopicPagesConnector`, plus `SecureStoreProvider`) — already covered by the allow-list approach; one more reader is opening a ticket about the BDC/BCS trending post (09-30).
- **OOS:** Sep OOS CU KB4461632 page lacks file hash information (reader 09-28; cosmetic).

### 5A.7 Delta 2026-09-30 → 2026-10-21 (168 comments + 5 new posts)
**Facts / Stefan statements**
- **Oct 2026 CU released 2026-10-14**: KB5002927, build **16.0.20326.20190**; Feature Update 26H2; security update. OOS build 16.0.10417.20228; SPWFM CU KB5002926 (client .20190). Post contains no fix list.
- **KB-number reuse** (Gabor, Anis, Paul C.; Stefan 10-14/15): the Sep COD hotfix had no KB; the Download Center forced a number and the Oct CU's reserved number was typed in. Two different packages; Oct CU installs over the hotfix (cumulative — implied, not explicitly confirmed).
- **SP2013 workflows not disabled in Oct CU** (Stefan 10-15; Paul C. 10-14/16).
- **Subsite creation fix in Oct CU** (Stefan 10-15 → Phu V. Huynh, confirmed "yes"). Stefan could not reproduce because his lab has no SP2013-provisioned sites (Sam, Peter v.d. Berg explain the SP2013-origin).
- **Cumulative:** installing Oct while skipping Sep is fine (Stefan, Robi 10-15).
- **PU summary:** severity table regenerated 10-19; CVE-2026-108452 omission = informational (no extra patch).
- **Debug flags:** `59025` (event-receiver validation revert) and `60751` (declarative workflow rules validator) are temporary mitigations, may vanish without notice (Stefan 10-19).
- **ToolPane** may be enabled per web application *and* per site collection (Stefan 09-30) — contradicts earlier "site collection only".
- **Remote event receivers** — Health Analyzer message since Sep CU; webhooks flagged; all RERs without app identity blocked with Nov CU (Stefan 10-02).
- **SP2019 unplanned update** KB5002911 (16.0.10417.20202) was pushed to Microsoft Update for a few hours after Sep CU and pulled (Stefan 10-01) — SP2019 is out of support; ignore. SP2019 admin-component deadlock root cause posted by a reader (10-20: NodeRunner race between `SearchAdminDBLeaserUpdater` and `SPUtility..cctor/GetFarmAllowedTypes`; workaround kill `NodeRunner.exe` of AdminComponent1) — **relevant to I-33** (search admin component not healthy) if SPSE shows the same signature (unverified on SPSE).
- **CSP / frame-ancestors:** SharePoint Add-ins blocked after Aug CU (framing of `*.spapps…` violates default `frame-ancestors`); picture-library URLs from host-named site collections blocked on SP2019 — Stefan: define your own CSP header (2024-03-12 post).
- **Nintex:** `Failed to send notification. Access denied` after applying Nintex's Sep-CU guidance — Stefan: Nintex ticket (MS does not support their internals).
- **Install hang** `hr=80070005 RemoveDirectoryAndChildren` (KB5002908 on Aug farm, installer 'stuck' for hours, `Install-SPSE_Fix.ps1` exit 17302) — processes holding DLLs (Stefan 10-19).
- **PSConfig on Search Admin DB** failing `proc_MSS_*` "does not exist" after Sep CU — resolved by granting the farm account **sysadmin** temporarily (Gustav 10-06).
- **Search host controller** not connecting — `sc.exe config … start=delayed-auto` (Stefan) did **not** help one reporter (10-06); I-33 remains open.
- **Windows Server Oct OS update**: question whether it impacts SPSE (Exchange SE had problems) — unanswered.
- **`UpdateNonceCertificate`** stops updating (reader 10-21, unanswered, likely unrelated).
- **Nightly timer-restart / install scripts:** Stefan cannot reproduce a PowerShell process not restarting (10-18).

**Remediation snippets (reader-reported, not Microsoft-verified)**
- Extended event-receiver repair: delete or re-point `Version=15.0.0.0` receivers at site, web, list **and content-type** level (Chandu 10-01: `$ct.XmlDocuments['http://schemas.microsoft.com/sharepoint/events']` + `SchemaXml` replace, set `ReadOnly=$false` first; Peter v.d. Berg's extended script).
- Document ID provider: loop all sites and set `docid_customProvider_assembly` to `Microsoft.Office.DocumentManagement, Version=16.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c` and `docid_customProvider_class` to `Microsoft.Office.DocumentManagement.Internal.OobProvider` (Abu 10-19).
- authorizedTypes for OOB Page Approval: five lines listed in the Sep 21 trending post comments (Asay 10-01).
- InfoPath: list form mappings must point at `displayifs/editifs/newifs.aspx` (Sandra 09-30); after COD hotfix enable "Render form templates that are browser-enabled by users"; `httpOnlyCookies=false` is a security trade-off.

**Unanswered / watch-list:** Oct HTML encoding (I-45); Oct PSConfig ECS assembly (I-46b); SPWFM allow-list syntax (I-47a); Document-ID generation stopped (10-20); SP2010 workflows remaining broken on a subset of site collections after `Enable-SPLegacyWorkflow` (Vinod 10-20, backup/restore-seeded sites); 500 error after adding v14 authorizedType (vikram 10-20 — Stefan asked for the exception); Sep CU Nintex mail; Windows Server Oct update impact.

---

## 6. Upgrade matrix (recommended paths → latest = October 2026 CU)

> **2026-10-21:** every path below that ends at "Sep 2026 CU" now ends at the **Oct 2026 CU (KB5002927, build .20190)** — the CUs are cumulative, no extra intermediate stop is needed. Apply the Sep/Oct pre-flight checklist in §3. Rows for the Sep 2026 CU and the COD hotfix are at the bottom.

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
| **Sep 2026 CU** (16.0.20326.20136) | Sep → **Oct 2026 CU (KB5002927, .20190)** directly; the COD hotfix (.20158) is no longer needed | None (InfoPath settings from the Sep trending post still apply) | Oct 2026 CU does **not** disable SP2013 workflows (Stefan 10-15). DCache fix (I-23) unconfirmed. Nov 2026 CU blocks orphaned RERs. |

**Note on SharePoint 2016/2019 farms:** with end of support 2026-07-14/15 and August 2026 CU being the last release for those versions, any farm still on SP2016/2019 has no further CU path — plan a migration to SPSE rather than an in-place upgrade.
| **Sep 2026 CU + COD hotfix (build .20158)** | → **Oct 2026 CU (.20190)** | None | Same settings/script as before still needed for InfoPath; re-check workflow authorizedTypes and receivers. Do not confuse KB5002927 (Oct CU) with the hotfix. |
| **Oct 2026 CU** (16.0.20326.20190) | Current target | — | Watch I-44 (workflow validator), I-45 (encoding), I-47 (SPWFM) |

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

## 8. Source log (fetch dates: 2026-09-28; comment-analysis passes 2026-09-29, 2026-09-30, 2026-10-21)

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
| spse-2026-10-cu | https://blog.stefan-gossner.com/2026/10/14/october-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download/ |
| spse-2026-10-pu | https://blog.stefan-gossner.com/2026/10/14/sharepoint-security-fixes-released-with-october-2026-pu-and-offered-through-microsoft-update/ |
| fu-26h2 | https://blog.stefan-gossner.com/2026/10/14/feature-update-26h2-for-sharepoint-server-subscription-edition-has-been-released/ |
| spwfm-2026-10-cu | https://blog.stefan-gossner.com/2026/10/14/october-2026-cu-for-sharepoint-workflow-manager-is-available-for-download/ |
| oos-2026-10-cu | https://blog.stefan-gossner.com/2026/10/14/october-2026-cu-for-office-online-server-is-available-for-download/ |
| comments-rest-api | https://blog.stefan-gossner.com/wp-json/wp/v2/comments?after=2026-06-01T00:00:00&per_page=100&page=N&order=asc |
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
| sep2026-hotfix | COD hotfix build .20158 (no KB; Download Center listed it as 5002927) — "Fix to support reenabling InfoPath Forms Services" (linked from the InfoPath trending post) |
| spwfm-aug-2026 / sep-2026 | KB5002864 (Aug), KB5002925 (Sep, released 2026-09-11) |
| oos-sep-fix | https://support.microsoft.com/en-us/servicing/office/hotfix/4461632 (as quoted by a reader) |

The 2026-09-30 incremental pass (REST API re-pull, 33 new comments) and this 2026-09-29 comment-analysis revision were also performed manually — **no GitHub Actions** (`weekly-check.yml` remains disabled, `if: false`). Posts were fetched with `curl` and the blog's public WordPress REST API (context-mode MCP unavailable). `.weekly-state.json` was left untouched.

This 2026-09-28 update was performed manually (GitHub Actions workflow `weekly-check.yml` remains disabled — `if: false` — per prior user request) using direct `WebFetch` against Stefan Goßner's blog, since the context-mode MCP sandbox used for prior updates was unavailable this session. `.weekly-state.json` was left untouched by this update; it still reflects the last automated-check baseline (May 2026 CU) and does not track Jun–Sep 2026.

All content in this knowledge base was indexed into the local context-mode sandbox (not stored verbatim in this file). Re-query via `ctx_search` against the listed source labels for verbatim quotes.
