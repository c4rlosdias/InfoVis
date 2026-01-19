# Módulo: data.py

## 📌 Visão Geral

Este módulo gerencia dados, callbacks, eventos e funcionalidades de integração com IFC e bSDD. Coordena sincronização entre a cena Blender e as estruturas de dados da aplicação.

**Linhas de Código**: 613

---

## 🔧 Variáveis Globais

### `last_active`
```python
last_active = None
```

**Propósito**: Rastreia qual objeto estava selecionado
**Uso**: Detectar mudanças de seleção
**Tipo**: Object ou None

---

## 📞 Funções de Callback

### `call_back()`
Callback simples que dispara carregamento de propriedades.

```python
def call_back():
    bpy.ops.props.load_properties()
```

**Acionado por**: Mudança em cena/objeto
**Ação**: Executa operador `props.load_properties`

### `on_active_object_change(scene)`
Detecta quando o objeto ativo muda e atualiza propriedades.

```python
def on_active_object_change(scene):
    global last_active
    obj = bpy.context.view_layer.objects.active
    if obj != last_active:
        last_active = obj        
        bpy.ops.props.load_properties()
```

**Gatilho**: `bpy.app.handlers.depsgraph_update_post`
**Lógica**:
1. Obtém objeto ativo atual
2. Compara com `last_active`
3. Se mudou, carrega propriedades
4. Atualiza `last_active`

**Propósito**: Atualizar painel quando usuário seleciona outro objeto

---

## 🔄 Funções de Atualização (Refresh)

### `refresh(context)`
Filtra classes de `props.classes` e popula `props.classes_shown`.

```python
def refresh(context):
    props = context.scene.og_props
    props.classes_shown.clear()
    for classe in props.classes:
        if not classe.is_hidden:
            new_item = props.classes_shown.add()
            new_item.code = classe.code
            new_item.name = classe.name
            new_item.description = classe.description
            new_item.level_index = classe.level_index
            new_item.uri = classe.uri
            new_item.index = classe.index
            new_item.has_children = classe.has_children
            new_item.is_expanded = classe.is_expanded
            new_item.is_hidden = classe.is_hidden
            new_item.type = classe.type
```

**Propósito**: Sincronizar dados visíveis com filtros
**Ação**:
1. Limpa `classes_shown`
2. Itera sobre `classes`
3. Copia apenas não-ocultas
4. Mantém todas as propriedades

**Uso**: Após expandir/contrair classe

### `refresh_products(context)`
Similar a `refresh()` mas para produtos.

```python
def refresh_products(context):
    props = context.scene.og_props
    props.products_show.clear()
    for classe in props.products:
        if not classe.is_hidden:
            new_item = props.products_show.add()
            # Copia propriedades...
```

**Diferença**: Copia de `products` para `products_show`

### `refresh_types(context)`
Similar para tipos de elementos.

```python
def refresh_types(context):
    props = context.scene.og_props
    props.types_show.clear()
    for classe in props.types:
        if not classe.is_hidden:
            new_item = props.types_show.add()
            # Copia propriedades...
```

### `refresh_container(context)`
Atualiza containers de elementos.

```python
def refresh_container(context):
    props = context.scene.og_props
    props.containers_show.clear()
    for classe in props.elements_containers:
        # Filtra e copia...
```

---

## 🔍 Padrão de Refresh

Todos os `refresh_*()` seguem o mesmo padrão:

```
1. Obter props = context.scene.og_props
2. Limpar coleção visível (clear())
3. Para cada item em coleção completa:
   a. Se não está oculto (is_hidden == False):
      - Criar novo item em coleção visível
      - Copiar todas as propriedades
4. Resultado: Apenas items visíveis na coleção exibida
```

**Vantagem**: Separação entre dados completos e dados exibidos

---

## 📊 Estrutura de Dados IFC

### Integração com IfcStore
```python
from bonsai.bim.ifc import IfcStore
```

IfcStore é o gerenciador central de arquivos IFC no Blender.

### Funções de Seletor IFC
```python
import ifcopenshell.util.selector as selector
```

Permite seleção de elementos por critério (tipo, propriedade, etc).

### Processamento de Dados
```python
import ifcopenshell
import numpy as np
import pandas as pd
```

- **ifcopenshell**: Manipulação IFC
- **numpy**: Operações matriciais
- **pandas**: Análise tabular

---

## 🌐 Integração bSDD

### Classe `bSDD`
```python
from .data import bSDD
```

**Métodos:**
```python
bSDD.is_loaded           # Property: carregado?
bSDD.load_dictionaries()  # Método: carrega do servidor
bSDD.data_dic            # Property: dados em dicionário
```

**Funcionamento:**
1. Primeiro acesso tenta carregar
2. Cache em variável de módulo
3. Próximos acessos usam cache
4. Pode recarregar manualmente

---

## 📡 Fluxo de Eventos

```
┌─────────────────────────────────┐
│ Usuário seleciona objeto Blender│
└────────────────┬────────────────┘
                 │
    ┌────────────▼─────────────┐
    │ Handler disparado:       │
    │ depsgraph_update_post    │
    └────────────┬─────────────┘
                 │
    ┌────────────▼─────────────────┐
    │ on_active_object_change()   │
    │ (detecta mudança)           │
    └────────────┬─────────────────┘
                 │
    ┌────────────▼──────────────────┐
    │ bpy.ops.props.load_properties()│
    │ (carrega dados IFC)            │
    └────────────┬──────────────────┘
                 │
    ┌────────────▼──────────────┐
    │ refresh()                 │
    │ (atualiza listas visíveis)│
    └────────────┬──────────────┘
                 │
    ┌────────────▼──────────────┐
    │ Painel redesenhado       │
    │ (props.classes_shown)    │
    └──────────────────────────┘
```

---

## 🔧 Registrando Handlers

No `__init__.py` ao ativar o add-on:

```python
bpy.app.handlers.depsgraph_update_post.append(on_active_object_change)
```

Ao desativar:

```python
bpy.app.handlers.depsgraph_update_post.remove(on_active_object_change)
```

---

## 🔍 Funções de Filtragem e Busca

### Buscar por URI
```python
def find_class_by_uri(context, target_uri):
    props = context.scene.og_props
    for classe in props.classes:
        if classe.uri == target_uri:
            return classe
    return None
```

### Buscar por Nome
```python
def find_classes_by_name(context, name_pattern):
    props = context.scene.og_props
    results = []
    for classe in props.classes:
        if name_pattern.lower() in classe.name.lower():
            results.append(classe)
    return results
```

### Filtrar por Nível
```python
def get_top_level_classes(context):
    props = context.scene.og_props
    return [c for c in props.classes if c.level_index == 1]
```

---

## 📝 Boas Práticas

### 1. Sempre Limpar Antes de Popular
```python
props.classes_shown.clear()  # Limpar primeiro
for item in data:
    new = props.classes_shown.add()
    # Popular...
```

### 2. Verificar Estado Antes de Processar
```python
if props.classes_loaded:
    # Usar dados
else:
    # Carregamento necessário
```

### 3. Usar Generators para Grandes Datasets
```python
def find_all_pipes(context):
    for classe in context.scene.og_props.classes:
        if "pipe" in classe.name.lower():
            yield classe
```

### 4. Evitar Loops de Callback
```python
# Usar flag para evitar recursão
self.updating = True
# ... fazer mudanças ...
self.updating = False
```

---

## 🐛 Debugging

### Verificar Handlers Registrados
```python
print(bpy.app.handlers.depsgraph_update_post)
print(len(bpy.app.handlers.depsgraph_update_post))
```

### Rastrear Mudanças
```python
def on_active_object_change(scene):
    global last_active
    obj = bpy.context.view_layer.objects.active
    print(f"Objeto anterior: {last_active}")
    print(f"Objeto atual: {obj}")
    if obj != last_active:
        print("Mudança detectada!")
```

### Inspecionar Propriedades
```python
props = bpy.context.scene.og_props
print(f"Classes: {len(props.classes)}")
print(f"Classes visíveis: {len(props.classes_shown)}")
print(f"Taxa de filtragem: {len(props.classes_shown) / len(props.classes) * 100:.1f}%")
```

---

## ⚠️ Armadilhas

### 1. Modificar Coleção Durante Iteração
❌ Evite:
```python
for item in props.classes:
    props.classes.remove(0)  # Índices mudam!
```

✅ Melhor:
```python
to_remove = [i for i, item in enumerate(props.classes) if condition]
for i in reversed(to_remove):
    props.classes.remove(i)
```

### 2. Handlers Duplicados
❌ Evite:
```python
# Registrar múltiplas vezes sem remover
bpy.app.handlers.depsgraph_update_post.append(callback)
bpy.app.handlers.depsgraph_update_post.append(callback)
```

✅ Melhor:
```python
if callback not in bpy.app.handlers.depsgraph_update_post:
    bpy.app.handlers.depsgraph_update_post.append(callback)
```

### 3. Acessar Context Fora de contexto
❌ Evite:
```python
def funcao():
    context.scene  # Erro se chamar sem context!
```

✅ Melhor:
```python
def funcao(context):
    context.scene  # OK
```

---

## 🔗 Integração com Outros Módulos

- **operators.py**: Usa `refresh()` para atualizar após operações
- **panels.py**: Exibe dados de `classes_shown`, `products_show`, etc
- **properties.py**: Define as PropertyGroups manipuladas aqui
- **__init__.py**: Registra os handlers de eventos

