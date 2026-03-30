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

| Arquivo | Responsabilidade | Linhas |
|---------|------------------|--------|
| `operators.py` | Lógica principal e operações | 1551 |
| `panels.py` | Interface do usuário | 766 |
| `properties.py` | Estrutura de dados | 234 |
| `data.py` | Sincronização e callbacks | 613 |
| `__init__.py` | Registro do add-on | - |

## Adicionando Funcionalidades

### Novo Operador

**1. Crie em `operators.py`:**
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

**2. Registre em `__init__.py`:**
```python
classes = [
    # ... classes existentes ...
    Operator_meu_novo,  # <- Adicione
]
```

**3. Adicione botão em `panels.py`:**
```python
layout.operator("og.meu_novo", text="Clique Aqui")
```

### Novo Painel

**Em `panels.py`:**
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

**Em `properties.py`:**
```python
class MinhaPropertyGroup(PropertyGroup):
    meu_campo: StringProperty(name="Campo")
    
    def update_funcao(self, context):
        # Chamado quando valor muda
        pass
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
from oil_gas_addon import operators

# Veja operadores disponíveis
print([x for x in dir(operators) if 'Operator' in x])

# Acesse propriedades
props = bpy.context.scene.og_props
print(f"Classes carregadas: {len(props.classes)}")
```

## Padrões do Projeto

- **PropertyGroups** mantêm dados sincronizados com UI
- **Operadores** herdam de `bpy.types.Operator`
- **Painéis** herdam de `bpy.types.Panel`
- **Callbacks** executam código quando propriedades mudam

## Documentação Detalhada

- **[Arquitetura](ARCHITECTURE.md)** - Estrutura técnica
- **[operators.py](guides/OPERATORS_DOCUMENTATION.md)** - Todas as operações
- **[panels.py](guides/PANELS_DOCUMENTATION.md)** - Interface
- **[properties.py](guides/PROPERTIES_DOCUMENTATION.md)** - Dados
- **[data.py](guides/DATA_DOCUMENTATION.md)** - Sincronização
- **[Glossário](reference/GLOSSARY.md)** - Termos e FAQ

