# SQL Server imajını genişlet ve sqlcmd aracını yükle
FROM mcr.microsoft.com/mssql/server:2019-latest

USER root
RUN apt-get update \
    && apt-get install -y curl apt-transport-https gnupg2 \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list \
        > /etc/apt/sources.list.d/mssql-tools.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y mssql-tools unixodbc-dev \
    && ln -s /opt/mssql-tools/bin/sqlcmd /usr/bin/sqlcmd \
    && rm -rf /var/lib/apt/lists/*

# Başlangıç betiği ve SQL şema dosyasını kopyala
WORKDIR /usr/src/app
COPY database/schema.sql /usr/src/app/schema.sql
COPY init.sh /usr/src/app/init.sh
RUN chmod +x /usr/src/app/init.sh

# mssql kullanıcısına geri dön
USER mssql

# Özel entrypoint ile SQL Server'ı başlat ve şemayı oluştur
ENTRYPOINT ["/usr/src/app/init.sh"]
