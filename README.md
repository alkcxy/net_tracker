# net_tracker
simple python script to track local ip via mqtt

under the [ips] section of the config.ini you can assign a name at each ip you want to be tracked

foo=192.168.0.5
bar=192.168.0.10
and so on

under [mqtt] section you should configure the connection to your mqtt server
host=
user=
pwd= 

How to build a docker image for arm64

```bash
    docker buildx build --platform linux/arm64 -t alkcxy/net_tracker:0.0.2-arm64 -f Dockerfile.arm64 .
```