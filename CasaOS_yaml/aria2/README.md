# Aria2 Docker & CasaOS
## Instructions & docker build
https://hub.docker.com/r/hurlenko/aria2-ariang
Important parts to read `ARIA2RPCPORT`. The environment variable `RPC_SECRET` is not working neither are `BASIC_AUTH_USERNAME` & `BASIC_AUTH_PASSWORD` So we need manually edit `.conf` file
## Docker Compose
Check attached
## Configuration file
First start the docker with the above compose file. After that stop it & overwrite attached `.conf` file. Edit the file settings like `rpc-user` & `rpc-passwd`
## NGinx Proxy
When I configured the webpage as https://aria.ukhan.duckdns.org/ the webUI didn't properly connected with `aria2c`
I have to go to AriaNG Settings & change port from 7443 -> 443 (method is https + Post)
