#!/bin/sh
set -e
# clear ready flag
rm -f /tmp/ready

ollama serve &

# start ollama, wait for it to serve
echo "Starting Ollama..."
until curl -s http://localhost:11434/api/tags >/dev/null; do
  sleep 2
done

# all the models to install
MODELS="mistral"

for MODEL in $MODELS; do
  if ! ollama list | grep -q "$MODEL"; then
    ollama pull "$MODEL"
  else
    echo "⛳️ Model '$MODEL' already present."
  fi
done

if command -v nvidia-smi &> /dev/null; then
  echo "✅ GPU detected, enabling acceleration"
  export OLLAMA_GPU=1
else
  echo "⚙️ No GPU found, running on CPU"
  export OLLAMA_GPU=0
fi

# set container as ready
touch /tmp/ready

# start nginx
nginx -g "daemon off;"
