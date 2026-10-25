param([string]$Root='D:\MLWork\tariff_scope_20261007\revision_20261023')
$ErrorActionPreference='Stop'
$env:TEMP=Join-Path $Root 'temp'
$env:TMP=$env:TEMP
$poppler='C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe'
$names=@('Tariff_Evidence_Audit_20261023','Tariff_Evidence_Audit_Supplement_20261023')
foreach($name in $names) {
    $docxPath=Join-Path $Root ('deliverables\'+$name+'.docx')
    $qaPath=Join-Path $Root ('verification\rendered\'+$name)
    New-Item -ItemType Directory -Force -Path $qaPath | Out-Null
    $pdfPath=Join-Path $qaPath ($name+'.pdf')
    $wordApp=$null
    $wordDoc=$null
    $ownsEmptyInstance=$false
    $priorAlerts=$null
    try {
        $wordApp=New-Object -ComObject Word.Application
        $ownsEmptyInstance=($wordApp.Documents.Count -eq 0)
        $priorAlerts=$wordApp.DisplayAlerts
        if($ownsEmptyInstance) { $wordApp.Visible=$false; $wordApp.DisplayAlerts=0 }
        $wordDoc=$wordApp.Documents.Open($docxPath,$false,$true)
        $wordDoc.Repaginate()
        $pages=$wordDoc.ComputeStatistics(2)
        $wordDoc.ExportAsFixedFormat($pdfPath,17)
        [ordered]@{renderer='Word compatible COM';version=$wordApp.Version;pages=$pages;pdf=$pdfPath;source=$docxPath;read_only=$true;owns_empty_instance=$ownsEmptyInstance;packaged_renderer_limitation='Use only after diagnosing missing soffice.exe in current packaged render_docx.py run'} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $qaPath 'render_metadata.json') -Encoding utf8
        Write-Output ('Rendered '+$name+' '+$pages+' pages')
    } finally {
        if($null -ne $wordDoc) { $wordDoc.Close(0); [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($wordDoc) }
        if($null -ne $wordApp) {
            if($ownsEmptyInstance -and $wordApp.Documents.Count -eq 0) {
                try { $wordApp.Quit(0) } catch { if(-not (Test-Path -LiteralPath $pdfPath)) { throw } }
            } elseif($null -ne $priorAlerts) { $wordApp.DisplayAlerts=$priorAlerts }
            [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($wordApp)
        }
    }
    Get-ChildItem -LiteralPath $qaPath -Filter 'page-*.png' -ErrorAction SilentlyContinue | Remove-Item -Force
    & $poppler -png -r 150 $pdfPath (Join-Path $qaPath 'page')
    if($LASTEXITCODE -ne 0) { throw 'Page rasterization failed' }
}
