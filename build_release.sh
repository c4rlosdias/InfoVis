#!/bin/bash

ZIP=$1

# criar pasta
mkdir -p ./releases/OG_Tools

# copiar arquivos
cp ./__init__.py ./releases/OG_Tools/
cp ./auth.py ./releases/OG_Tools/

# copiar pastas
cp -r ./modules ./releases/OG_Tools/
cp -r ./data ./releases/OG_Tools/
cp -r ./libs ./releases/OG_Tools/
cp -r ./resources ./releases/OG_Tools/

# criar zip
cd ./releases || exit
zip -r "${ZIP}.zip" OG_Tools

echo "ZIP criado com sucesso!"
read -p "Pressione Enter para continuar"