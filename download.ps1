$urls = @(
    "https://maps.app.goo.gl/Gb6Vd1PfoHceBWCA6",
    "https://maps.app.goo.gl/9vaYQLtGdBdCeStw8",
    "https://maps.app.goo.gl/9yK2zktgQpjoA7oW8",
    "https://maps.app.goo.gl/3xSpVmzghYaxFeWU6",
    "https://maps.app.goo.gl/gy6dETssHytWMmKB8",
    "https://maps.app.goo.gl/tGcv3UpD73ddFLuPA",
    "https://maps.app.goo.gl/4EJ6T7ioDTbUjfZLA"
)

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$i = 1
foreach ($url in $urls) {
    try {
        $response = Invoke-WebRequest -Uri $url -UseBasicParsing -UserAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        $html = $response.Content
        
        $imgUrl = $null
        if ($html -match '<meta\s+property="og:image"\s+content="([^"]+)"') {
            $imgUrl = $matches[1]
        } elseif ($html -match '<meta\s+content="([^"]+)"\s+property="og:image"') {
             $imgUrl = $matches[1]
        } elseif ($html -match '<meta\s+content="([^"]+)"\s+itemprop="image"') {
             $imgUrl = $matches[1]
        }
        
        if ($null -ne $imgUrl) {
            $imgUrl = $imgUrl -replace '&amp;', '&'
            if ($imgUrl -match 'googleusercontent.com') {
                $imgUrl = $imgUrl -replace '=w\d+-h\d+-[a-zA-Z0-9\-]+', '=s0'
            }
            Write-Host "[$i] Downloading $imgUrl..."
            Invoke-WebRequest -Uri $imgUrl -OutFile "C:\Users\Syed Anas\OneDrive\Desktop\PLAZA PARTY HALL\images\img$i.jpg"
            Write-Host "[$i] Saved img$i.jpg"
        } else {
            Write-Host "[$i] No meta tag found for $url"
        }
    } catch {
        Write-Host "[$i] Error fetching url " $url
    }
    $i++
}
