#!/usr/bin/env bash
# Espera a instalação dos pacotes terminar (se ainda estiver rodando) e renderiza o site.
cd "$(dirname "$0")/.." || exit 1
LOG="_work/render.log"

while pgrep -f "Rscript -e" > /dev/null; do sleep 15; done
echo "=== pacotes instalados em .Rlib: $(ls .Rlib | wc -l) ==="
tail -20 /tmp/r_install3.log | tr '\r' '\n' | tail -14

echo "=== quarto render ==="
quarto render 2>&1 | tail -80
echo "EXIT_RENDER=${PIPESTATUS[0]}"
