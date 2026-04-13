#!/bin/bash

ZIP=$1

# criar pasta
mkdir -p ./releases/OG_Tools

# copiar arquivos
cp ./__init__.py ./releases/OG_Tools/
cp ./panels.py ./releases/OG_Tools/
cp ./operators.py ./releases/OG_Tools/
cp ./properties.py ./releases/OG_Tools/
cp ./data.py ./releases/OG_Tools/

# copiar pastas
cp -r ./libs ./releases/OG_Tools/
cp -r ./resources ./releases/OG_Tools/

# criar zip
cd ./releases || exit
zip -r "${ZIP}.zip" OG_Tools

echo "ZIP criado com sucesso!"
read -p "Pressione Enter para continuar"