# Módulo: operators.py

## 📌 Visão Geral

Este é o módulo mais extenso da aplicação (1551 linhas) e contém a lógica principal de negócio. Implementa operadores Blender que manipulam dados IFC, realizam análises e gerenciam a decomposição de projetos de óleo e gás.

---

## 🔧 Funcionalidades Principais

### 1. Gerenciamento de Dados JSON

#### `save_json(dados)`
```python
def save_json(dados):
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "dados.json")
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(dados, file, ensure_ascii=False, indent=4)
```
**Propósito**: Salva dados em formato JSON no arquivo `dados.json` local
**Uso**: Persistência de configurações e cache de resultados

---

### 2. Construção de Hierarquias

#### `build_classes(context, classe, c, level, parent, hide)`
Constrói recursivamente a hierarquia de classes na propriedade `classes`.

**Parâmetros:**
- `context`: Contexto do Blender
- `classe`: Dicionário com dados da classe (código, nome, descrição, URI)
- `c`: Contador/índice do elemento
- `level`: Nível de profundidade na hierarquia
- `parent`: Nome da classe pai
- `hide`: Se deve ocultar inicialmente (True/False)

**Lógica:**
1. Cria novo item `Class_info` em `props.classes`
2. Preenche propriedades: código, nome, descrição, URI, tipo
3. Define índice, nível e relação de parentesco
4. Se tem filhos, marca como expandível e processa recursivamente
5. Define visibilidade com `set_hide_class()`

**Exemplo:**
```python
classe_dict = {
    "code": "001",
    "name": "Pipe",
    "descriptionPart": "Tubulação subsuperficial",
    "uri": "http://bsdd.buildingsmart.org/...",
    "classType": "IfcPipeSegment",
    "children": [...]
}
build_classes(context, classe_dict, 0, 1, "", False)
```

#### `build_products(context, classe, c, level, parent, hide, children)`
Similar a `build_classes` mas para tipos de produtos/elementos IFC.

**Diferenças:**
- Adiciona em `props.types` em vez de `props.classes`
- Usa `element_type` em vez de `classType`
- Parametro adicional `children`

---

### 3. Controle de Visibilidade Hierárquica

#### `set_hide_class(context, index, is_hidden)`
Oculta/mostra recursivamente todas as subclasses de um item.

**Algoritmo:**
```
Para cada classe após o índice:
  Se nível > nível do índice:
    Aplica o estado is_hidden
  Se nível <= nível do índice:
    Para (limite alcançado)
```

#### `set_hide_product(context, index, is_hidden)`
Versão para produtos com mesma lógica.

---

### 4. Operadores IFC

#### Importação e Configuração
```python
import ifcopenshell.util.element as element
import ifcopenshell.util.representation as representation
import ifcopenshell.util.selector as selector
import ifcopenshell.api.root.create_entity as create_entity
import ifcopenshell.api.material as material
import ifcopenshell.api.geometry as geometry
import ifcopenshell.api.style as style
```

**Funcionalidades:**
- **element**: Manipulação de elementos (obter propriedades, valores)
- **representation**: Gerenciar representações geométricas
- **selector**: Selecionar elementos por critério
- **create_entity**: Criar novos objetos IFC
- **material**: Associar materiais
- **geometry**: Manipular geometrias
- **style**: Aplicar estilos visuais

#### Integração Bonsai/Blender
```python
import bonsai.core
import bonsai.core.geometry
import bonsai.core.material
import bonsai.core.type
import bonsai.tool as tool
from bonsai.bim import import_ifc
```

Usa a biblioteca Bonsai para integração profunda com BlenderBIM.

---

### 5. Análise e Visualização de Dados

#### Bibliotecas
```python
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib
import numpy as np
from scipy.interpolate import interp1d
```

#### Capacidades
- **Pandas**: Processamento de dados tabulares, cálculos estatísticos
- **Matplotlib**: Geração de gráficos 2D/3D
- **NumPy**: Operações vetorizadas em arrays
- **SciPy**: Interpolação de curvas, algoritmos científicos

#### Exemplos de Uso
```python
# Interpolação de dados
f = interp1d(x_values, y_values, kind='cubic')
y_interpolated = f(x_new)

# Gráficos com matplotlib
plt.figure(figsize=(10, 6))
plt.plot(x, y)
plt.xlabel('Distância (m)')
plt.ylabel('Pressão (bar)')
plt.show()
```

---

### 6. Validação com IDS

#### Importação
```python
from ifctester import ids
```

#### Uso
- Validar se arquivo IFC atende especificações IDS
- Testar conformidade com PetroBRAS
- Gerar relatórios de conformidade

---

### 7. Função `get_options(self, context)`

**Propósito**: Callback para propriedades enum que usam `dynamic_items`

```python
dynamic_items = []  # Lista global

def get_options(self, context):    
    return dynamic_items
```

**Uso**: Permite opções dinâmicas em dropdowns da UI

---

## 🔄 Fluxo Típico

```
1. Usuário seleciona arquivo IFC ou clica em botão
   │
2. Callback ou operador disparado
   │
3. Extrai dados com ifcopenshell
   │
4. Processa com pandas/numpy se necessário
   │
5. Constrói hierarquias com build_classes/build_products
   │
6. Atualiza propriedades (properties.py)
   │
7. Renderiza na UI (panels.py)
   │
8. Salva dados em dados.json se necessário
```

---

## 📦 Estruturas de Dados

### Classe JSON esperada
```json
{
  "code": "001",
  "name": "Flexible Pipe",
  "descriptionPart": "Descrição",
  "uri": "http://bsdd.buildingsmart.org/...",
  "classType": "IfcPipeSegmentFlexible",
  "children": [
    {
      "code": "001.001",
      "name": "Tensioner",
      ...
    }
  ]
}
```

### Dicionário de Produto
```json
{
  "id": 123,
  "name": "Product Name",
  "description": "Descrição",
  "element_type": "IfcPipeSegment"
}
```

---

## ⚙️ Configurações

### Caminho de Dados
```python
path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "dados.json")
# Salva no mesmo diretório do script
```

### Encoding
```python
encoding='utf-8'  # Suporta caracteres especiais (português)
ensure_ascii=False
```

---

## 🐛 Debugging

### Imprimir Classes
```python
props = context.scene.og_props
for classe in props.classes:
    print(f"{classe.name} (level: {classe.level_index})")
```

### Validar IFC
```python
import ifcopenshell
ifc_file = ifcopenshell.open("path/file.ifc")
print(f"Entidades: {len(ifc_file)}")
```

### Inspecionar Propriedades
```python
element_obj = ifc_file[123]  # Por GlobalId
props_dict = element.get_psets(element_obj)
```

---

## 📝 Boas Práticas

1. **Sempre validar** entrada IFC antes de processar
2. **Usar try-except** em operações de arquivo
3. **Limpar dados** dinâmicos antes de recarregar
4. **Usar tqdm** para feedback em operações longas
5. **Documentar** callbacks e eventos

---

## 🔗 Integração com Outros Módulos

- **properties.py**: Define estruturas usadas aqui (`Class_info`, `Class_type`)
- **panels.py**: Consome dados construídos aqui
- **data.py**: Complementa com funcionalidades de integração
- **__init__.py**: Registra operadores para Blender

