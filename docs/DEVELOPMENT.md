# Desenvolvimento do InfoVis

## Objetivo deste guia

Este documento descreve como preparar o ambiente, iterar no add-on e empacotar releases do InfoVis sem perder aderencia a estrutura atual do repositorio.

## Requisitos

- Blender 5.0 ou superior
- acesso ao Python embarcado do Blender
- Git
- VS Code ou outro editor com suporte a Python

## Estrutura relevante para desenvolvimento

- `__init__.py`: entrada do add-on e registro de classes
- `auth.py`: autenticacao e controle de sessao
- `modules/`: operadores, paineis e `PropertyGroup`s por dominio
- `data/`: integracoes e logica de apoio
- `resources/`: arquivos JSON de apoio
- `Example/`: arquivo IFC para testes manuais
- `build_release.bat` e `build_release.sh`: empacotamento

## Preparacao do ambiente

### Dependencias Python

O arquivo `requirements.txt` lista dependencias de apoio ao projeto. Em ambiente Blender, a execucao depende tambem das bibliotecas embarcadas nas pastas `libs311/` e `libs313/`.

No Windows, o add-on prioriza essas bibliotecas empacotadas. Em Linux e macOS, dependencias ausentes podem ser instaladas dinamicamente pelo proprio add-on quando ele e importado.

### Instalar o add-on para iteracao local

Fluxo recomendado:

1. trabalhe normalmente neste repositorio
2. gere um zip instalavel com o script de build
3. reinstale o zip no Blender quando precisar validar mudancas

Windows:

```powershell
.\build_release.bat dev-local
```

Linux ou macOS:

```bash
./build_release.sh dev-local
```

O pacote gerado fica em `releases/dev-local.zip`.

### Instalar no Blender

1. abra o Blender
2. acesse `Edit > Preferences > Add-ons`
3. clique em `Install from Disk`
4. selecione o zip gerado em `releases/`
5. habilite o add-on `InfoVis`

## Fluxo de trabalho recomendado

1. altere o codigo em `modules/`, `data/`, `auth.py` ou `resources/`
2. gere um novo zip com o script de build
3. reinstale o add-on ou remova e instale novamente no Blender
4. valide os paineis e operadores impactados com um arquivo IFC real
5. repita o ciclo ate estabilizar a funcionalidade

## Onde fazer cada tipo de mudanca

### Novo operador

1. adicione a classe em `modules/<dominio>/operators.py`
2. registre a classe em `modules/__init__.py`
3. exponha a acao no painel apropriado, se necessario
4. use `data/` para encapsular acesso a IFC, bSDD ou CDE

### Novo painel ou UIList

1. implemente em `modules/<dominio>/panels.py`
2. registre em `modules/__init__.py`
3. leia e escreva estado apenas por `context.scene.og_props` ou propriedades Blender relacionadas

### Novo `PropertyGroup`

1. declare o tipo no modulo de dominio correspondente
2. registre o tipo antes de `OG_Properties`
3. adicione a propriedade agregada em `modules/og_properties.py` quando o estado for compartilhado

### Nova integracao ou regra de negocio

Prefira colocar logica fora de `draw()` dos paineis. Se a funcionalidade conversar com APIs, arquivos IFC, catalogos ou transformacao de dados, o destino natural costuma ser `data/`.

## Regras praticas do projeto

- mantenha `modules/__init__.py` como fonte unica da ordem de registro
- nao coloque logica pesada dentro de `Panel.draw()`
- preserve o uso de `OG_Properties` como estado compartilhado entre modulos
- trate dependencias multiplataforma considerando o carregamento de `libs311/` e `libs313/`
- teste no Blender depois de qualquer alteracao que envolva registro, UI ou callbacks

## Validacao manual

Use `Example/C3388.8_UN-31.ifc` como base para verificacoes manuais quando aplicavel.

Checklist minimo:

1. o add-on instala e habilita sem erro
2. os paineis principais aparecem na barra lateral da View3D
3. a selecao de objetos atualiza as informacoes do painel de propriedades
4. operadores alterados executam sem excecao no console do Blender
5. overlays ou listas afetadas refletem o novo estado apos refresh

## Debug no Blender

O console Python do Blender pode ser usado para verificacoes rapidas.

Exemplos uteis:

```python
import bpy
import InfoVis
from InfoVis.modules import get_classes
from InfoVis import auth

props = bpy.context.scene.og_props
print(len(get_classes()))
print(auth.is_authenticated())
print(hasattr(props, "classes"))
```

Se o add-on foi instalado com outro nome de pasta, ajuste o import conforme o nome real do pacote no ambiente Blender.

## Processo de release

Os scripts de build fazem a montagem do pacote em `releases/InfoVis/` e depois geram um zip final.

Conteudo do pacote:

- `__init__.py`
- `auth.py`
- `modules/`
- `data/`
- `libs311/`
- `libs313/`
- `resources/`

Antes de publicar um release:

1. confirme a versao em `bl_info` dentro de `__init__.py`
2. valide a instalacao do zip em um Blender limpo
3. confira se recursos JSON e bibliotecas embarcadas estao incluidos
4. registre as mudancas relevantes na documentacao principal

## Documentacao relacionada

- [ARCHITECTURE.md](ARCHITECTURE.md)
- [guides/OPERATORS_DOCUMENTATION.md](guides/OPERATORS_DOCUMENTATION.md)
- [guides/PANELS_DOCUMENTATION.md](guides/PANELS_DOCUMENTATION.md)
- [guides/PROPERTIES_DOCUMENTATION.md](guides/PROPERTIES_DOCUMENTATION.md)
- [guides/DATA_DOCUMENTATION.md](guides/DATA_DOCUMENTATION.md)
- [reference/GLOSSARY.md](reference/GLOSSARY.md)

