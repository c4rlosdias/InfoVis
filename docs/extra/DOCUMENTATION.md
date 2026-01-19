# Oil & Gas Tools - Documentação Técnica

## 📋 Visão Geral

**Oil & Gas Tools** é um add-on para Blender desenvolvido para acessar e manipular informações de projetos de óleo e gás que seguem especificações PetroBRAS. A aplicação funciona como um visualizador e gerenciador de modelos IFC (Industry Foundation Classes), fornecendo ferramentas de decomposição, catalogação e análise.

### Informações do Projeto
- **Nome**: Oil & Gas Tools
- **Autor**: Carlos Dias
- **Versão**: 0.1.1
- **Compatibilidade**: Blender 5.0+
- **Licença**: GNU General Public License v3
- **Categoria**: Ferramentas de Usuário

---

## 🏗️ Arquitetura do Projeto

### Estrutura de Diretórios

```
oil-gas-addon/
├── __init__.py              # Inicialização do add-on e registro de classes
├── operators.py             # Operadores e funcionalidades principais
├── panels.py                # Painéis da interface do usuário
├── properties.py            # Propriedades customizadas do Blender
├── data.py                  # Manipulação de dados e conexões
├── requirements.txt         # Dependências Python
├── resources/               # Recursos (dados estáticos)
│   ├── ifc_types.json
│   ├── FlexiblePipeStructure.json
│   ├── HangOffCollarType.json
│   ├── TopBendStiffenerType.json
│   ├── BendRestrictorType.ttl
│   └── units.json
├── files/                   # Arquivos de teste IFC
├── libs/                    # Bibliotecas Python incluídas
└── releases/                # Versões compiladas
```

---

## 🔧 Módulos Principais

### 1. **__init__.py** - Inicialização

Responsável pelo registro do add-on e suas classes no Blender.

**Funcionalidades:**
- Definição de metadados do add-on (`bl_info`)
- Importação dinâmica de módulos
- Registro de classes e operadores
- Configuração de propriedades de cena

**Classes Registradas:**
- `Operator_get_properties` - Obtém propriedades do IFC
- `Operator_get_classes` - Recupera classes do bSDD
- `Operator_load_decomposition` - Carrega decomposição
- `Operator_contract_classes` - Contrai hierarquia de classes
- `Operator_expand_classes` - Expande hierarquia de classes
- Painéis e propriedades customizadas

### 2. **operators.py** - Operadores e Lógica Principal (1551 linhas)

Contém a lógica de negócio e operadores do Blender.

**Funcionalidades Principais:**

#### Gerenciamento de Dados JSON
```python
save_json(dados)  # Salva dados em dados.json
get_options()     # Retorna itens dinâmicos
```

#### Construção de Hierarquias
```python
build_classes(context, classe, c, level, parent, hide)
  # Constrói árvore hierárquica de classes
  # Parâmetros:
  #   - context: Contexto do Blender
  #   - classe: Dicionário com dados da classe
  #   - c: Contador de elementos
  #   - level: Nível hierárquico
  #   - parent: Elemento pai
  #   - hide: Estado de visibilidade

build_products(context, classe, c, level, parent, hide, children)
  # Similar para produtos/tipos
```

#### Operadores IFC
- Manipulação de arquivos IFC
- Extração de propriedades e quantidades
- Processamento de geometrias e materiais
- Aplicação de estilos e representações

#### Análise e Visualização
- Geração de gráficos com matplotlib
- Interpolação de dados com scipy
- Processamento com pandas
- Exportação de dados em múltiplos formatos

### 3. **panels.py** - Interface do Usuário (766 linhas)

Define os painéis e elementos visuais no Blender.

**Painéis Principais:**

#### Panel_Connect - Classes Subsea
- **ID**: `VIEW3D_PT_og_connect`
- **Localização**: View 3D > Painel Lateral
- **Funcionalidades**:
  - Conexão com bSDD (buildingSMART Data Dictionary)
  - Listagem de classes
  - Informações detalhadas de classes
  - Extração de propriedades

**Funcionalidades Auxiliares:**
```python
_label_multiline(context, text, parent)
  # Quebra texto em múltiplas linhas na UI

get_properties(ifc_obj)
  # Extrai propriedades do objeto IFC

get_product_attribute(context, index, attribute)
  # Obtém atributo específico do produto
```

### 4. **properties.py** - Propriedades Customizadas (234 linhas)

Define as propriedades que armazenam dados na cena do Blender.

**Classes de Propriedades:**

#### `Ifc_properties`
```python
- name: StringProperty        # Nome do elemento
- code: StringProperty        # Código
- description: StringProperty # Descrição
- uri: StringProperty         # Identificador único
- is_selected: BoolProperty   # Estado de seleção
```

#### `Class_info`
```python
- code, name, description     # Identificação
- uri, propertyset            # Referências
- has_children: BoolProperty  # Estrutura hierárquica
- is_hidden, is_expanded      # Estados de UI
- index, parent, level_index  # Posição na hierarquia
- type: StringProperty        # Tipo de classe
```

#### `Class_type`
```python
- id: IntProperty             # Identificador numérico
- name, description           # Identificação
- element_type: StringProperty # Tipo de elemento
- (campos hierárquicos similares a Class_info)
```

**Callbacks de Mudança:**
- `active_prop_changed()` - Atualiza quando propriedade muda
- `active_class_changed()` - Atualiza quando classe muda
- `active_product_changed()` - Atualiza quando produto muda
- `active_type_changed()` - Atualiza quando tipo muda

### 5. **data.py** - Manipulação de Dados (613 linhas)

Gerencia dados, IFC e conexões externas.

**Funções de Callback e Eventos:**
```python
on_active_object_change(scene)  # Detecta mudança de objeto ativo
callback()                      # Carrega propriedades automaticamente
refresh(context)                # Atualiza lista de classes visíveis
refresh_products(context)       # Atualiza lista de produtos
refresh_types(context)          # Atualiza lista de tipos
refresh_container(context)      # Atualiza containers
```

**Funções de Filtro e Busca:**
- Filtragem de classes por atributos
- Busca de elementos em estrutura IFC
- Seleção de produtos por critérios

**Integração com Biblioteca bSDD:**
- Carregamento de dicionários
- Consulta de definições
- Mapeamento de propriedades

---

## 📦 Dependências

### Python Packages (requirements.txt)

| Pacote | Versão | Propósito |
|--------|--------|----------|
| ifcopenshell | 0.8.1 | Leitura e manipulação de arquivos IFC |
| ifctester | 0.8.1 | Validação de IDS (Information Delivery Specification) |
| numpy | 2.2.4 | Computação numérica e arrays |
| matplotlib | 3.10.5 | Visualização de dados e gráficos |
| scipy | 1.16.2 | Algoritmos científicos (interpolação, etc) |
| pandas | (implícito) | Manipulação de dados tabulares |
| fake-bpy-module-4.3 | 20250130 | Stubs para autocompletar do Blender |
| shapely | 2.0.7 | Operações geométricas |
| lark | 1.2.2 | Parser para linguagens |
| rdflib | 7.1.4 | Processamento de RDF (incluído) |

---

## 🎯 Funcionalidades Principais

### 1. **Conexão com bSDD (buildingSMART Data Dictionary)**
- Recuperação de dicionários de classes internacionais
- Consulta de propriedades e definições
- Mapeamento de tipos de elementos conforme PetroBRAS

### 2. **Gerenciamento de Decomposição**
- Carregamento de estrutura hierárquica
- Expansão/contração de classes e produtos
- Visualização em árvore na interface

### 3. **Extração de Propriedades IFC**
- Leitura de propriedades customizadas
- Extração de quantidades (QTO - Quantity Takeoff)
- Acesso a materiais e estilos

### 4. **Análise e Visualização**
- Geração de gráficos de dados
- Interpolação de curvas
- Exportação de relatórios

### 5. **Validação com IDS**
- Validação de conformidade com especificações
- Teste de integridade de dados

---

## 🔄 Fluxo de Dados

```
┌─────────────────────────────────────────────────────────┐
│         Arquivo IFC Carregado no Blender              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
          ┌──────────────────────────┐
          │ Detectar mudança de cena │
          │ (data.py - callback)     │
          └────────┬─────────────────┘
                   │
                   ▼
        ┌──────────────────────────────┐
        │ Carregar Propriedades IFC    │
        │ (operators.py)               │
        └────────┬─────────────────────┘
                 │
    ┌────────────┴────────────┐
    │                         │
    ▼                         ▼
┌──────────┐         ┌──────────────┐
│ Classes  │         │ Produtos     │
│ (bSDD)   │         │ (IFC Types)  │
└────┬─────┘         └────┬─────────┘
     │                    │
     │    ┌───────────────┘
     │    │
     ▼    ▼
┌─────────────────────────┐
│ properties.py           │
│ PropertyGroups          │
└────────┬────────────────┘
         │
         ▼
┌──────────────────────────┐
│ panels.py                │
│ UI Rendering             │
└──────────────────────────┘
```

---

## 🚀 Como Usar

### Instalação

1. **Clone ou baixe** a pasta `oil-gas-addon`
2. **Copie** para o diretório de add-ons do Blender:
   ```
   %APPDATA%\Blender Foundation\Blender\5.0\scripts\addons\
   ```
3. **Ative** em Blender: Edit > Preferences > Add-ons > Buscar "Oil & Gas"

### Uso Básico

1. **Abra um arquivo IFC** em Blender
2. **Ative o painel** "O&G Tools" na View 3D (lado direito)
3. **Clique em "get classes from bSDD"** para conectar ao dicionário
4. **Selecione classes** da lista para ver informações
5. **Use os operadores** para carregar decomposições e analisar dados

---

## 📊 Estrutura de Dados IFC

### Hierarquia de Projeto
```
Project (IfcProject)
  ├── Site (IfcSite)
  │   ├── Building (IfcBuilding)
  │   │   └── BuildingStorey (IfcBuildingStorey) [Levels]
  │   │       └── Spaces (IfcSpace)
  │   └── Elements (IfcElement)
  │       ├── Walls (IfcWall)
  │       ├── Doors (IfcDoor)
  │       ├── Windows (IfcWindow)
  │       ├── Columns (IfcColumn)
  │       └── ... mais tipos
```

### Propriedades Customizadas
Cada elemento pode ter:
- **Psets**: Property Sets (conjuntos de propriedades)
- **Qsets**: Quantity Sets (conjuntos de quantidades)
- **Materiais**: Material associations
- **Estilos**: Presentation styles

---

## 🔍 Debugging e Troubleshooting

### Verificar Imports
```python
# No console do Blender
import ifcopenshell
import matplotlib
import scipy
import pandas
```

### Validar Arquivo IFC
```python
# Verificar se modelo é válido
import ifcopenshell
ifc_file = ifcopenshell.open("caminho/arquivo.ifc")
print(ifc_file.is_valid())
```

### Logs
- Consulte o console do Blender (Shift + F4) para mensagens
- Arquivo `dados.json` contém últimas consultas

---

## 📝 Convenções de Código

- **Naming**: snake_case para funções, PascalCase para classes
- **Docstrings**: Em português, seguindo padrão Python
- **Indentação**: 4 espaços
- **Imports**: Agrupados (stdlib, third-party, local)

---

## 🤝 Contribuindo

Para adicionar novas funcionalidades:

1. **Operators**: Adicione em `operators.py` herdando de `bpy.types.Operator`
2. **UI**: Adicione painéis em `panels.py` herdando de `bpy.types.Panel`
3. **Propriedades**: Defina em `properties.py` herdando de `PropertyGroup`
4. **Registro**: Adicione à lista `classes` em `__init__.py`

---

## 📚 Recursos Adicionais

- [buildingSMART IFC Schema](https://www.buildingsmart.org/)
- [ifcopenshell Documentation](http://docs.ifcopenshell.org/)
- [Blender Python API](https://docs.blender.org/api/current/)
- [Especificações PetroBRAS](https://www.petrobras.com.br/)

---

## 📄 Licença

Este projeto está sob a Licença GNU General Public License v3. Veja o arquivo LICENSE para mais detalhes.

---

## ✉️ Contato e Suporte

- **Desenvolvedor**: Carlos Dias
- **Versão Atual**: 0.1.1
- **Status**: Em Desenvolvimento
