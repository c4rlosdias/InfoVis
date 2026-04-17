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

O projeto utiliza uma **estrutura modular organizada por domínio funcional**. Cada domínio agrupa seus operadores, painéis e propriedades dentro de `modules/`:

### Raiz
| Arquivo | Responsabilidade |
|---------|------------------|
| `__init__.py` | Registro do add-on, preferences, auth operators |
| `auth.py` | Autenticação por senha (SHA-256) |

### Pacote `modules/`
| Módulo | Responsabilidade |
|--------|------------------|
| `__init__.py` | `get_classes()` — registro centralizado de todas as classes |
| `og_properties.py` | OG_Properties (PropertyGroup central) + callbacks |
| `common/operators.py` | Utilitários compartilhados (tree expand/contract, Columns, ErrorMessage) |
| `dictionary/` | Integração bSDD (operators, panels, properties) |
| `decomposition/` | Decomposição IFC (operators, panels, properties) |
| `catalog/` | Catálogo de tipos (operators, panels, properties) |
| `connections/` | Conexões entre elementos (operators, panels) |
| `props/` | Propriedades do objeto (operators, panels, properties) |
| `settings/` | Configurações e informações (panels) |

### Pacote `data/`
| Módulo | Responsabilidade |
|--------|------------------|
| `bsdd.py` | Cliente REST bSDD |
| `catalog.py` | Import IFC, Catalog, PropTempl |
| `cde.py` | API CDE (mock) |
| `tree.py` | Árvore, refresh, callbacks |
| `ifc_utils.py` | Utilidades IFC, propriedades, conexões |

## Adicionando Funcionalidades

### Novo Operador

**1. Crie no submódulo apropriado em `modules/<domínio>/operators.py`:**
```python
# modules/dictionary/operators.py
class Operator_meu_novo(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "og.meu_novo"
    bl_label = "Meu Novo Operador"
    
    def execute(self, context):
        # Sua lógica aqui
        self.report({'INFO'}, "Pronto!")
        return {'FINISHED'}
```

**2. Registre em `modules/__init__.py` na função `get_classes()`:**
```python
def get_classes():
    return [
        # ... classes existentes ...
        _dict_ops.Operator_meu_novo,  # <- Adicione na seção correta
    ]
```

**3. Adicione botão no painel do domínio (`modules/<domínio>/panels.py`):**
```python
layout.operator("og.meu_novo", text="Clique Aqui")
```

### Novo Painel

**Em `modules/<domínio>/panels.py`:**
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

**Crie em `modules/<domínio>/properties.py` e adicione ao OG_Properties:**
```python
# modules/<domínio>/properties.py
class MinhaPropertyGroup(PropertyGroup):
    meu_campo: StringProperty(name="Campo")

# modules/og_properties.py — adicione ao OG_Properties:
minha_prop: CollectionProperty(type=MinhaPropertyGroup)
```

### Novo Módulo de Domínio

Para adicionar uma funcionalidade completamente nova:

1. Crie a pasta `modules/<novo_dominio>/`
2. Crie `__init__.py`, `operators.py`, `panels.py`, `properties.py`
3. Importe os submódulos em `modules/__init__.py`
4. Adicione as classes na função `get_classes()`

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
from oil_gas_addon import modules, data, auth

# Acesse propriedades
props = bpy.context.scene.og_props
print(f"Classes carregadas: {len(props.classes)}")

# Verifique autenticação
print(f"Autenticado: {auth.is_authenticated()}")

# Acesse preferências do addon
prefs = bpy.context.preferences.addons['oil_gas_addon'].preferences
print(f"CDE URL: {prefs.cde_url}")

# Veja todas as classes registradas
from oil_gas_addon.modules import get_classes
print(f"Total de classes: {len(get_classes())}")
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

