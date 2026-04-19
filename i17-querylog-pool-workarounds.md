# I-17 Workarounds — QueryLogJobDefinition SQL Connection Pool Exhaustion

**Issue:** QueryLogJobDefinition timer job leaks SQL connections; pool (default max 100) exhausts in 48–72h causing Event 6399 cascading failures.
**Status:** Open as of Apr 2026 — no official fix in any CU through KB5002853.

---

## Script 1 — Update Max Pool Size in all web app web.config files

Run from **SharePoint Management Shell** on one server (reads/writes via UNC paths):

```powershell
Add-PSSnapin Microsoft.SharePoint.PowerShell -ErrorAction SilentlyContinue

$newMaxPoolSize = 200

foreach ($webApp in Get-SPWebApplication -IncludeCentralAdministration) {
    $webConfigPath = $webApp.IisSettings[[Microsoft.SharePoint.Administration.SPUrlZone]::Default].Path.FullName + "\web.config"
    if (Test-Path $webConfigPath) {
        [xml]$xml = Get-Content $webConfigPath
        $changed = $false
        foreach ($cs in $xml.configuration.connectionStrings.add) {
            if ($cs.connectionString -notmatch "Max Pool Size") {
                $cs.connectionString = $cs.connectionString.TrimEnd(';') + ";Max Pool Size=$newMaxPoolSize"
                $changed = $true
            }
        }
        if ($changed) {
            $xml.Save($webConfigPath)
            Write-Host "Updated: $webConfigPath"
        }
    }
}

iisreset /noforce
Write-Host "IISReset complete."
```

> **Note:** This covers IIS worker processes only. The timer service (OWSTIMER.EXE) reads connection strings from the SharePoint config database, not web.config. See Script 2 for the timer service.

---

## Script 2 — Update Max Pool Size on Search Service Application databases

Targets the databases accessed by the timer service, where QueryLogJobDefinition runs:

```powershell
Add-PSSnapin Microsoft.SharePoint.PowerShell -ErrorAction SilentlyContinue

$ssa = Get-SPEnterpriseSearchServiceApplication
if (-not $ssa) {
    Write-Error "No Search Service Application found."
    exit 1
}

$searchDbs = @(
    $ssa.SearchAdminDatabase,
    $ssa.LinksDatabase,
    $ssa.AnalyticsReportingDatabase
)

foreach ($db in $searchDbs) {
    if ($db -ne $null) {
        $cs = $db.DatabaseConnectionString
        if ($cs -notmatch "Max Pool Size") {
            $db.DatabaseConnectionString = $cs.TrimEnd(';') + ";Max Pool Size=200"
            $db.Update()
            Write-Host "Updated connection string for: $($db.Name)"
        } else {
            Write-Host "Already has Max Pool Size: $($db.Name)"
        }
    }
}

Write-Host "Done. Restarting SPTimerV4..."
Restart-Service SPTimerV4
Write-Host "SPTimerV4 restarted."
```

---

## Script 3 — Scheduled nightly SPTimerV4 restart (Workaround 2)

Register a Windows Scheduled Task to restart the timer service every night at 02:00.
Run once from an **elevated PowerShell** session on each SharePoint server:

```powershell
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-NonInteractive -Command `"Restart-Service SPTimerV4; Write-EventLog -LogName Application -Source 'SPTimerV4-Restart' -EntryType Information -EventId 9999 -Message 'Scheduled SPTimerV4 restart completed.'`""

$trigger = New-ScheduledTaskTrigger -Daily -At "02:00"

$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Minutes 10) -StartWhenAvailable

Register-ScheduledTask -TaskName "SharePoint - Nightly SPTimerV4 Restart" `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Settings $settings `
    -Description "Workaround for I-17: clears leaked SQL connections in QueryLogJobDefinition before pool exhaustion." `
    -Force

Write-Host "Scheduled task registered. Next run: $(Get-ScheduledTask -TaskName 'SharePoint - Nightly SPTimerV4 Restart' | Get-ScheduledTaskInfo | Select-Object -ExpandProperty NextRunTime)"
```

To remove the task when Microsoft ships a fix:
```powershell
Unregister-ScheduledTask -TaskName "SharePoint - Nightly SPTimerV4 Restart" -Confirm:$false
```

---

## Recommended value for Max Pool Size

| Farm size | Value |
|---|---|
| Single-server / dev | 200 |
| Small multi-server | 200–300 |
| Large production | 300–500 |

Before increasing, verify SQL Server can handle additional connections:
```sql
SELECT @@MAX_CONNECTIONS        -- SQL Server hard limit
SELECT COUNT(*) FROM sys.dm_exec_sessions  -- current active sessions
```

---

## Caveats

- `Max Pool Size` changes in web.config **survive server reboots** but may be **overwritten by CU installs** — recheck after patching.
- Search database connection string changes via PowerShell are stored in the SharePoint config DB and persist across reboots.
- Increasing the pool delays exhaustion but does not stop the leak — combine Script 2 + Script 3 for best coverage.
- **Disable the Query Logging Timer Job** (Workaround 1) remains the most effective option if query analytics are not required.

---

## References

- [Many critical events in SharePoint SE after July 2025 updates — MS Q&A](https://learn.microsoft.com/en-us/answers/questions/5583482/many-critical-events-in-sharepoint-se-after-july-2)
- [QueryLogJobDefinition may be exhausting the SQL connection pool — MS Q&A (Mar 2026)](https://learn.microsoft.com/en-us/answers/questions/5816641/querylogjobdefinition-may-be-exhausting-the-sql-co)
- [Search service SQL connection pool exhaustion after the March 2026 update — MS Q&A (Apr 2026)](https://learn.microsoft.com/en-us/answers/questions/5849106/search-service-sql-connection-pool-exhaustion-afte)
- [How to change Max Pool Size in SharePoint SE — MS Q&A](https://learn.microsoft.com/en-us/answers/questions/5578539/how-can-i-change-the-max-pool-size-with-the-sharep)
- [Tuning Max Pool Size in SharePoint SE — SilverPC Blog](https://blog.silverpc.hu/2025/10/22/tuning-for-performance-how-to-change-the-max-pool-size-with-the-sharepoint-server-subscription-edition-to-avoid-errors/)
