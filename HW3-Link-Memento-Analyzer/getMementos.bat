@echo off

for /F "tokens=1-2 delims= " %%A in (.\HashURL-Mappings.txt) do (

.\memgator-windows-amd64.exe -c "ODU CS432/532 bbake017@odu.edu" -a https://raw.githubusercontent.com/odu-cs432-websci/public/main/archives.json -F 2 -f JSON %%B > .\mementos\%%A.json
tar -c -f .\mementos\%%A.tar .\mementos\%%A.json
del .\mementos\%%A.json
TIMEOUT /T 10 /NOBREAK
)