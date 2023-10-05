FROM itzg/minecraft-server

COPY ./data.zip /data.zip
COPY ./entry /entry

ENV MAX_MEMORY=8G
ENV RCON_CMDS_ON_CONNECT="team join player @a[team=]"

ENV VERSION=1.20.1
ENV EULA=true
EXPOSE 25565
ENTRYPOINT ["/entry"]
