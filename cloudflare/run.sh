 docker run --network ssl -v ./run.yaml:/etc/run.yaml cloudflare/cloudflared:latest tunnel --config /etc/run.yaml --no-autoupdate --loglevel debug run  --token eyJhIjoiOWY1ZjBhMjRjNzEyM2FiODE3MDFhZmRjZDYzY2JhZGIiLCJ0IjoiNjRlODhhZTAtYWNlNi00ZDAzLTgzZjctYWJmZWJhMDYzYmM5IiwicyI6Ik56TTRPVEkyTmpNdFlURTNOaTAwWldWaExXSTBZbUV0TnpoaU16TmhaVGM1TkRZMSJ9 


#   docker run --network ssl -v .:/etc  cloudflare/cloudflared:latest  tunnel info

cloudflared tunnel --overwrite-dns --config /etc/run.yml run --token eyJhIjoiOWY1ZjBhMjRjNzEyM2FiODE3MDFhZmRjZDYzY2JhZGIiLCJ0IjoiNjRlODhhZTAtYWNlNi00ZDAzLTgzZjctYWJmZWJhMDYzYmM5IiwicyI6Ik56TTRPVEkyTmpNdFlURTNOaTAwWldWaExXSTBZbUV0TnpoaU16TmhaVGM1TkRZMSJ9 


docker run -it -v ./run.yml:/etc/run.yml -v ./cert.pem:/usr/local/etc/cloudflared/cert.pem -v ./tunnel.json:/usr/local/etc/cloudflared/tunnel.json cloud bash