# DB Setup
1. Download docker
2. Add to path: `C:\Program Files\Docker\Docker\resources\bin`
3. Run `docker pull mcr.microsoft.com/mssql/server`
4. Run
~~~ 
docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=_nam35685_" -e "MSSQL_PID=Evaluation" -p 1433:1433  --name sqlpreview --hostname sqlpreview -d mcr.microsoft.com/mssql/server:2022-preview-ubuntu-22.04
~~~