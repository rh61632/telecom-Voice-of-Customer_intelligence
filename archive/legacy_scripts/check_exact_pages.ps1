param([string]$Path = "paper/Telecom_VoC_Intelligence_JBA_Manuscript.docx")
$fullPath = Resolve-Path $Path
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open($fullPath.Path)
    $pages = $doc.ComputeStatistics(2) # 2 = wdStatisticPages
    $words = $doc.ComputeStatistics(0) # 0 = wdStatisticWords
    Write-Host "Exact Pages in Word: $pages"
    Write-Host "Exact Words in Word: $words"
    $doc.Close([ref]$false)
} finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}
