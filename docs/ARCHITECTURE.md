# Arquitetura do InfoVis

## Visao Geral

O InfoVis e um add-on para Blender estruturado como um pacote Python modular. A aplicacao se apoia em tres blocos principais:

- `__init__.py`: ponto de entrada, metadados do add-on, preferencias, autenticacao e ciclo de registro
- `modules/`: UI, operadores e estruturas de dados expostas ao Blender
- `data/`: funcoes de suporte para IFC, bSDD, catalogo, CDE e refresh de arvores

O registro das classes Blender acontece a partir de `modules.get_classes()`, preservando a ordem exigida pelo Blender: tipos auxiliares, `PropertyGroup`s, `OG_Properties`, operadores e paineis.

## Mapa de Componentes

```text
Blender
  |
  |-- __init__.py
  |    |-- bl_info
  |    |-- OilGasAddonPreferences
  |    |-- OG_OT_Login / OG_OT_Logout
  |    `-- register() / unregister()
  |
  |-- modules/
  |    |-- __init__.py
  |    |-- og_properties.py
  |    |-- common/
  |    |-- dictionary/
  |    |-- decomposition/
  |    |-- catalog/
  |    |-- connections/
  |    |-- props/
  |    |-- types/
  |    `-- settings/
  |
  |-- data/
  |    |-- bsdd.py
  |    |-- catalog.py
  |    |-- cde.py
  |    |-- ifc_utils.py
  |    `-- tree.py
  |
  |-- auth.py
  |-- resources/
  |-- libs311/
  `-- libs313/
```

## Responsabilidades por Camada

### Entrada e ciclo de vida

`__init__.py` concentra o que o Blender precisa para carregar o add-on:

- define `bl_info`
- ajusta `sys.path` para bibliotecas empacotadas no Windows
- instala dependencias faltantes em Linux e macOS quando necessario
- declara preferencias do add-on e operadores de autenticacao
- cria `Scene.og_props`
- registra handlers e subscriber de `bpy.msgbus`
- ativa e desativa overlays da viewport

### Modulos Blender

`modules/` organiza a funcionalidade por dominio. Cada dominio agrupa operadores, paineis e, quando necessario, `PropertyGroup`s.

#### `modules/common/`

Utilitarios compartilhados entre paineis e operadores, como expansao de arvores, selecao e mensagens de erro.

#### `modules/dictionary/`

Fluxos de consulta ao bSDD: classes, propriedades, detalhes de classe e exportacao relacionada a IDS.

#### `modules/decomposition/`

Visualizacao da decomposicao IFC, selecao de elementos, ordenacao e navegacao em estruturas hierarquicas.

#### `modules/catalog/`

Carregamento de produtos, tipos e camadas, com apoio ao filtro e selecao de elementos no modelo.

#### `modules/connections/`

Operacoes de criacao, remocao e selecao de conexoes entre objetos no contexto IFC.

#### `modules/props/`

Inspecao e edicao de propriedades, documentos associados e visualizacoes graficas.

#### `modules/types/`

Painel dedicado a tipos exibidos no add-on.

#### `modules/settings/`

Controles de configuracao e gerenciamento dos atributos exibidos como labels IFC.

#### `modules/og_properties.py`

Define `OG_Properties`, o agregador central de estado do add-on. Ele concentra colecoes e flags utilizadas por varios paineis e operadores.

## Camada de Dados

`data/` encapsula operacoes que nao pertencem diretamente a UI do Blender.

- `bsdd.py`: chamadas HTTP para consulta ao bSDD
- `catalog.py`: leitura de catalogo, tipos e apoio ao carregamento IFC
- `cde.py`: integracao com a API de CDE
- `ifc_utils.py`: utilitarios para elementos, propriedades, documentos e conexoes IFC
- `tree.py`: refresh de estruturas em arvore e callback associado a mudanca de objeto ativo

Essa separacao evita que a logica de negocio fique espalhada nos paineis e reduz acoplamento com o ciclo de desenho da interface.

## Registro de Classes

`modules/__init__.py` funciona como registro central. A funcao `get_classes()` retorna todas as classes Blender em ordem estavel.

Sequencia atual:

1. utilitarios compartilhados
2. `PropertyGroup`s especializados
3. `IFC_Label_Attribute`
4. `OG_Properties`
5. operadores por dominio
6. paineis e `UIList`s

Essa ordem e importante porque o Blender exige que tipos referenciados por propriedades sejam registrados antes de serem usados.

## Fluxo de Inicializacao

```text
Usuario ativa o add-on
  -> Blender executa __init__.py
  -> bibliotecas empacotadas sao adicionadas ao sys.path quando aplicavel
  -> preferencias e operadores basicos sao declarados
  -> modules.get_classes() monta a lista de classes
  -> register() registra classes no Blender
  -> Scene.og_props e WindowManager.* sao criados
  -> msgbus passa a observar o objeto ativo
  -> overlay de labels IFC e registrado
```

Ao abrir um novo arquivo, o handler `_on_load_post` restabelece a assinatura do `msgbus`, mantendo a sincronizacao entre selecao ativa e arvores exibidas nos paineis.

## Gestao de Dependencias

O projeto usa duas estrategias de distribuicao:

- Windows: bibliotecas binarias embarcadas em `libs311/` e `libs313/`
- Linux e macOS: instalacao sob demanda usando o Python do Blender

Esse comportamento e decidido em tempo de importacao com base em `platform.system()` e `sys.version_info`.

## Recursos Estaticos

`resources/` armazena arquivos JSON utilizados pela aplicacao, incluindo definicoes auxiliares de tipos IFC, unidades e datasets de dominio.

## Pacote de Release

Os scripts `build_release.bat` e `build_release.sh` copiam apenas o subconjunto necessario do repositorio para `releases/InfoVis/` e geram um arquivo zip instalavel no Blender.

Conteudo empacotado:

- `__init__.py`
- `auth.py`
- `modules/`
- `data/`
- `libs311/`
- `libs313/`
- `resources/`

Arquivos de documentacao e exemplos nao entram no pacote de instalacao.

## Convencoes Arquiteturais

- os paineis devem delegar trabalho pesado para operadores e funcoes de `data/`
- o estado compartilhado deve ficar em `OG_Properties` ou em `PropertyGroup`s dedicados
- integracoes externas devem ser encapsuladas em `data/` ou em um modulo de infraestrutura claro
- o registro de novas classes deve passar por `modules/__init__.py`

## Documentos Relacionados

- [DEVELOPMENT.md](DEVELOPMENT.md)
- [guides/OPERATORS_DOCUMENTATION.md](guides/OPERATORS_DOCUMENTATION.md)
- [guides/PANELS_DOCUMENTATION.md](guides/PANELS_DOCUMENTATION.md)
- [guides/PROPERTIES_DOCUMENTATION.md](guides/PROPERTIES_DOCUMENTATION.md)
- [guides/DATA_DOCUMENTATION.md](guides/DATA_DOCUMENTATION.md)
- [reference/GLOSSARY.md](reference/GLOSSARY.md)
    │
    ├─ Lê dados atualizados
    ├─ Verifica auth.is_authenticated() para funcionalidades de edição
    ├─ Desenha novamente
    │
    ▼
Usuário vê resultado
```

---

## ⚙️ Configurações e Constantes

### Em `__init__.py`
```python
bl_info = {
    "name": "Oil&Gas Tools",
    "version": (0, 1, 1),
    "blender": (5, 0, 0),
    ...
}
```

### Em `requirements.txt`
```
ifcopenshell==0.8.1
numpy==2.2.4
matplotlib==3.10.5
...
```

### Em `resources/` (dados estáticos)
```
ifc_types.json
FlexiblePipeStructure.json
HangOffCollarType.json
TopBendStiffenerType.json
BendRestrictorType.ttl
units.json
```

---

## 🔐 Segurança e Validação

### Validação IFC
- Verificar se arquivo é válido com `ifcopenshell`
- Testar conformidade com IDS
- Validar estrutura esperada

### Tratamento de Erros
- Try-except em operações de arquivo
- Feedback ao usuário via UI
- Log em console

### Sincronização de Dados
- Evitar loops infinitos de callbacks
- Usar flags para prevenir reprocessamento
- Limpar dados antigos antes de carregar novos

---

## 📚 Recursos Externos

- **Blender Python API**: https://docs.blender.org/api/current/
- **ifcopenshell Docs**: http://docs.ifcopenshell.org/
- **buildingSMART**: https://www.buildingsmart.org/
- **Matplotlib**: https://matplotlib.org/
- **Pandas**: https://pandas.pydata.org/
- **SciPy**: https://scipy.org/

