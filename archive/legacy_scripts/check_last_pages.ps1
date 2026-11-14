$word = New-Object -ComObject Word.Application
$word.Visible = $false
$docPath = (Resolve-Path "paper/journal_manuscript/Telecom_VoC_Intelligence_JBA_Manuscript.docx").Path
$doc = $word.Documents.Open($docPath)
$lastPage = $doc.ComputeStatistics(2)
for ($pg = 18; $pg -le $lastPage; $pg++) {
    $rStart = $doc.GoTo(1, 1, $pg)
    $rEnd = if ($pg -lt $lastPage) { $doc.GoTo(1, 1, $pg + 1) } else { $doc.Range($doc.Content.End - 1, $doc.Content.End) }
    $pageRange = $doc.Range($rStart.Start, $rEnd.Start)
    $wordsOnPg = $pageRange.ComputeStatistics(0)
    Write-Host "=== Page $pg (Words: $wordsOnPg) ==="
    $lines = $pageRange.Text -split "`r`n|`n|`r"
    foreach ($line in $lines) {
        if ($line.Trim().Length -gt 0) {
            $prev = if ($line.Trim().Length -gt 70) { $line.Trim().Substring(0, 70) + "..." } else { $line.Trim() }
            Write-Host "   $prev"
        }
    }
}
$doc.Close([ref]$false)
$word.Quit()

