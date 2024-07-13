#!/bin/bash

# set port number
port=8081

. .venv/bin/activate
set -a && . ./.env && set +a

if hostname -I 2>/dev/null; then
  # display URL for access to the local server.
  host_name="http://$(uname -n).local:$port"
  ip_addr="http://$(hostname -I | awk -F' ' '{print $1}'):$port"

  max_len=${#ip_addr}
  if [ ${#host_name} -gt $max_len ]; then
    max_len=${#host_name}
  fi

  border_len=$(($max_len + 2))

  printf "+"
  printf "%0.s-" $(seq 1 $border_len)
  echo "+"

  printf "| %-${max_len}s |\n" "$host_name"

  printf "| %-${max_len}s |\n" "$ip_addr"

  printf "+"
  printf "%0.s-" $(seq 1 $border_len)
  echo "+"
else
  # on some systems, hostname -I doesn't work. show below message instead.
  echo "failed to get host address. perhaps, http://hostname:$port is host address."
fi

python -m http.server $port
