#!/bin/sh

ZIP=$1

# criar pasta
mkdir -p ./releases/InfoVis

# copiar arquivos
cp ./__init__.py ./releases/InfoVis/
cp ./auth.py ./releases/InfoVis/

# copiar pastas
cp -r ./modules ./releases/InfoVis/
cp -r ./data ./releases/InfoVis/
cp -r ./libs311 ./releases/InfoVis/
cp -r ./libs313 ./releases/InfoVis/
cp -r ./resources ./releases/InfoVis/

# criar zip
cd ./releases || exit
zip -r "${ZIP}.zip" InfoVis

echo "ZIP criado com sucesso!"
printf "Pressione Enter para continuar"
read _