$word = New-Object -ComObject Word.Application
$word.Visible = $false
$docPath = (Resolve-Path "paper/journal_manuscript/Telecom_VoC_Intelligence_JBA_Manuscript.docx").Path
$doc = $word.Documents.Open($docPath)
$pages = $doc.ComputeStatistics(2)
$words = $doc.ComputeStatistics(0)
$doc.Close([ref]$false)
$word.Quit()
Write-Host "EXACT Word Document Pages: $pages, Words: $words"

