# 🚀 Desenvolvimento - Oil & Gas Tools

## Setup Inicial

### Requisitos
- Blender 5.0+
- Python 3.10+
- Git
- VS Code (recomendado)

### Instalação para Desenvolvimento

```bash
# Clone o repositório
git clone <repo-url> oil-gas-addon
cd oil-gas-addon

# Instale dependências
pip install -r requirements.txt

# Copie para pasta de add-ons do Blender
# Windows:
cp -r . "C:\Users\%USERNAME%\AppData\Roaming\Blender\5.0\scripts\addons\oil-gas-addon"
# Linux/Mac:
cp -r . ~/.config/blender/5.0/scripts/addons/oil-gas-addon
```

### Ativar em Blender

1. Abra Blender
2. Edit > Preferences > Add-ons
3. Busque "Oil & Gas"
4. Clique para ativar

## Estrutura de Módulos

O projeto utiliza uma estrutura modular em pacotes Python:

### Raiz
| Arquivo | Responsabilidade |
|---------|------------------|
| `__init__.py` | Registro do add-on, preferences, auth operators |
| `auth.py` | Autenticação por senha (SHA-256) |

### Pacote `data/`
| Módulo | Responsabilidade |
|--------|------------------|
| `bsdd.py` | Cliente REST bSDD |
| `catalog.py` | Import IFC, Catalog, PropTempl |
| `cde.py` | API CDE (mock) |
| `tree.py` | Árvore, refresh, callbacks |
| `ifc_utils.py` | Utilidades IFC, propriedades, conexões |

### Pacote `properties/`
| Módulo | Responsabilidade |
|--------|------------------|
| `types.py` | PropertyGroups individuais (Ifc_properties, Class_info, etc.) |
| `main.py` | OG_Properties + callbacks de atualização |

### Pacote `operators/`
| Módulo | Responsabilidade |
|--------|------------------|
| `common.py` | Utilitários compartilhados (tree expand/contract, save_json, etc.) |
| `dictionary.py` | Operadores bSDD (get classes, properties, export IDS) |
| `decomposition.py` | Decomposição IFC (load, select, move, reorder) |
| `catalog.py` | Catálogo de tipos (load products, layers, select) |
| `connections.py` | Conexões IFC (disconnect, add connect) |
| `properties.py` | Propriedades e gráficos (edit, load, graph) |

### Pacote `panels/`
| Módulo | Responsabilidade |
|--------|------------------|
| `main.py` | Todos os painéis e UILists |

## Adicionando Funcionalidades

### Novo Operador

**1. Crie no submódulo apropriado em `operators/` (ex: `operators/dictionary.py`):**
```python
class Operator_meu_novo(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "og.meu_novo"
    bl_label = "Meu Novo Operador"
    
    def execute(self, context):
        # Sua lógica aqui
        self.report({'INFO'}, "Pronto!")
        return {'FINISHED'}
```

**2. Exporte no `operators/__init__.py`:**
```python
from .dictionary import Operator_meu_novo
```

**3. Registre em `__init__.py` (raiz):**
```python
classes = [
    # ... classes existentes ...
    Operator_meu_novo,  # <- Adicione
]
```

**4. Adicione botão em `panels/main.py`:**
```python
layout.operator("og.meu_novo", text="Clique Aqui")
```

### Novo Painel

**Em `panels/main.py`:**
```python
class Panel_meu_painel(bpy.types.Panel):
    bl_label = "Meu Painel"
    bl_idname = "VIEW3D_PT_meu_painel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "O&G Tools"
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Conteúdo aqui")
```

### Novo PropertyGroup

**Tipos simples em `properties/types.py`, propriedades principais em `properties/main.py`:**
```python
# properties/types.py
class MinhaPropertyGroup(PropertyGroup):
    meu_campo: StringProperty(name="Campo")

# properties/main.py — adicione ao OG_Properties:
minha_prop: PointerProperty(type=MinhaPropertyGroup)
```

## Testando Mudanças

1. Edite o arquivo
2. No Blender: Edit > Preferences > Add-ons
3. Desabilite e reabilite "Oil & Gas Tools"
4. Testes suas mudanças

## Debug

**Console do Blender:** Shift + F4

```python
# Teste imports
import bpy
from oil_gas_addon import operators, data, properties, auth

# Veja operadores disponíveis
print([x for x in dir(operators) if 'Operator' in x])

# Acesse propriedades
props = bpy.context.scene.og_props
print(f"Classes carregadas: {len(props.classes)}")

# Verifique autenticação
print(f"Autenticado: {auth.is_authenticated()}")

# Acesse preferências do addon
prefs = bpy.context.preferences.addons['oil_gas_addon'].preferences
print(f"CDE URL: {prefs.cde_url}")
```

## Padrões do Projeto

- **PropertyGroups** mantêm dados sincronizados com UI
- **Operadores** herdam de `bpy.types.Operator`
- **Painéis** herdam de `bpy.types.Panel`
- **Callbacks** executam código quando propriedades mudam

## Documentação Detalhada

- **[Arquitetura](ARCHITECTURE.md)** - Estrutura técnica
- **[operators/](guides/OPERATORS_DOCUMENTATION.md)** - Todas as operações
- **[panels/](guides/PANELS_DOCUMENTATION.md)** - Interface
- **[properties/](guides/PROPERTIES_DOCUMENTATION.md)** - Dados
- **[data/](guides/DATA_DOCUMENTATION.md)** - Sincronização e dados
- **[Glossário](reference/GLOSSARY.md)** - Termos e FAQ

