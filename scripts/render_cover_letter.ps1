param([string]$Root='D:\MLWork\tariff_scope_20261007\revision_20261023')
$ErrorActionPreference='Stop'
$docx=Join-Path $Root 'deliverables\Cover_Letter_Tariff_Evidence_Audit.docx'
$pdf=Join-Path $Root 'deliverables\Cover_Letter_Tariff_Evidence_Audit.pdf'
$wordApp=$null; $wordDoc=$null
try {
    $wordApp=New-Object -ComObject Word.Application
    $wordApp.Visible=$false; $wordApp.DisplayAlerts=0
    $wordDoc=$wordApp.Documents.Open($docx,$false,$true)
    $wordDoc.Repaginate()
    $pages=$wordDoc.ComputeStatistics(2)
    $wordDoc.ExportAsFixedFormat($pdf,17)
    Write-Output ('Rendered cover letter '+$pages+' pages -> '+$pdf)
} finally {
    if($null -ne $wordDoc) { $wordDoc.Close(0); [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($wordDoc) }
    if($null -ne $wordApp) { $wordApp.Quit(0); [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($wordApp) }
}
$poppler='C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe'
$qa=Join-Path $Root 'verification\rendered\Cover_Letter'
New-Item -ItemType Directory -Force -Path $qa | Out-Null
& $poppler -png -r 110 $pdf (Join-Path $qa 'page')
if($LASTEXITCODE -ne 0) { throw 'rasterization failed' }
Write-Output 'pages rasterized'
