@echo off & title TikTokDownload update By JohnserfSeed
 
::����Ҫ���ص��ļ����ӣ���֧��httpЭ�顣��д�
set Url=https://github.com/Johnserf-Seed/TikTokDownload/releases/download/v1.2.5/TikTokMulti.exe
set Url2=https://github.com/Johnserf-Seed/TikTokDownload/releases/download/v1.2.5/TikTokDownload.exe

::�����ļ�����Ŀ¼������������ǰĿ¼��������
set Save=.\dist
if exist %Save% (echo ����λ�ã�%Save%) else (mkdir %Save% & echo �Ѵ�����%Save%)
if not exist ".\dist\TikTokMulti.exe" (
del ".\dist\TikTokMulti.exe"
del ".\dist\TikTokDownload.exe"
echo ��ɾ���ɰ汾
)

for %%a in ("%Url%") do set "FileName=%%~nxa"
if not defined Save set "Save=%cd%"
(echo Download Wscript.Arguments^(0^),Wscript.Arguments^(1^)
echo Sub Download^(url,target^)
echo   Const adTypeBinary = 1
echo   Const adSaveCreateOverWrite = 2
echo   Dim http,ado
echo   Set http = CreateObject^("Msxml2.ServerXMLHTTP"^)
echo   http.open "GET",url,False
echo   http.send
echo   Set ado = createobject^("Adodb.Stream"^)
echo   ado.Type = adTypeBinary
echo   ado.Open
echo   ado.Write http.responseBody
echo   ado.SaveToFile target, 2
echo   ado.Close
echo End Sub)>DownloadFile.vbs

DownloadFile.vbs "%Url%" ".\dist\TikTokMulti.exe"
echo TikTokMulti�������
DownloadFile.vbs "%Url2%" ".\dist\TikTokDownload.exe"
echo TikTokDownload�������
::������ɾ�����ɵ�vbs�ļ�
del DownloadFile.vbs
pause