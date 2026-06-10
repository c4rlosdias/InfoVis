import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

# ── Configurações ─────────────────────────────────────────────────
FIG_W, FIG_H = 18, 22
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
ax.set_xlim(0, FIG_W)
ax.set_ylim(0, FIG_H)
ax.axis('off')
fig.patch.set_facecolor('#0f1117')

# ── Helpers ───────────────────────────────────────────────────────
def box(ax, x, y, w, h, fc, ec, lw=1.5, ls='-', radius=0.3, zorder=2):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad=0,rounding_size={radius}",
                       facecolor=fc, edgecolor=ec, linewidth=lw,
                       linestyle=ls, zorder=zorder)
    ax.add_patch(p)

def txt(ax, x, y, s, size=9, color='#e0e0e0', ha='center', va='center',
        weight='normal', zorder=3, wrap=False, style='normal'):
    ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va,
            fontweight=weight, zorder=zorder, fontstyle=style,
            fontfamily='monospace')

def arrow(ax, x1, y1, x2, y2, color='#555555', lw=1.5, zorder=2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color,
                                lw=lw, connectionstyle='arc3,rad=0'))

def arrow_label(ax, x, y, s, color='#666666'):
    txt(ax, x, y, s, size=7, color=color, ha='center')

# ── Paleta ────────────────────────────────────────────────────────
BG       = '#0f1117'
C_BLU_D  = '#1a2a3a'
C_BLU_E  = '#3a7bd5'
C_GRN_D  = '#1a2a1a'
C_GRN_E  = '#4caf50'
C_PUR_D  = '#2a1a2a'
C_PUR_E  = '#9c27b0'
C_RED_D  = '#2a1a1a'
C_RED_E  = '#f44336'
C_ORG_D  = '#1a1a2a'
C_ORG_E  = '#ff9800'
C_CYN_D  = '#1a2a2a'
C_CYN_E  = '#00bcd4'
C_YEL_D  = '#1f1f10'
C_YEL_E  = '#f0a500'

TXT_LGT  = '#e0e0e0'
TXT_MED  = '#aaaaaa'
TXT_DIM  = '#666666'

# ══════════════════════════════════════════════════════════════════
# TÍTULO
# ══════════════════════════════════════════════════════════════════
txt(ax, FIG_W/2, 21.5, 'InfoVis — Arquitetura do Add-on',
    size=16, color='#f0a500', weight='bold')
txt(ax, FIG_W/2, 21.1, 'Blender 5.0 + Bonsai/BIM  ·  v0.1.1',
    size=9, color='#888888')

# ══════════════════════════════════════════════════════════════════
# 1. BLENDER HOST
# ══════════════════════════════════════════════════════════════════
Y_BLND = 20.2
box(ax,  0.4, Y_BLND, 17.2, 0.65, '#16202a', C_BLU_E, lw=2)
txt(ax,  1.2, Y_BLND+0.32, '[B]', size=14, ha='left', weight='bold')
txt(ax,  2.1, Y_BLND+0.42, 'Blender 5.0 + Bonsai/BIM', size=11,
    color='#61dafb', ha='left', weight='bold')
txt(ax,  2.1, Y_BLND+0.18, 'Ambiente host  ·  View3D > "O&G Tools" tab',
    size=8, color='#888888', ha='left')

# ══════════════════════════════════════════════════════════════════
# 2. PAINÉIS UI
# ══════════════════════════════════════════════════════════════════
Y_PNL = 18.35
panels = [
    ('[UI]', 'Panel_Connect',        'Subsea Classes\nbSDD browser'),
    ('[D]', 'Panel_Decompositions', 'IFC hierarchy\ntree view'),
    ('[C]', 'Panel_Catalog',        'Type catalog\nproducts JSON'),
    ('[P]', 'Panel_Properties',     'IFC Psets\ngraphs · docs'),
    ('[S]', 'Panel_Settings/Info',  'Configurações\ne informações'),
]
pw = 3.3
gap = 0.1
x0 = 0.4
for i, (icon, name, desc) in enumerate(panels):
    px = x0 + i * (pw + gap)
    box(ax, px, Y_PNL, pw, 1.55, C_BLU_D, C_BLU_E, radius=0.2)
    txt(ax, px + pw/2, Y_PNL + 1.25, icon,    size=14)
    txt(ax, px + pw/2, Y_PNL + 0.95, name,    size=8.5, color='#61dafb', weight='bold')
    txt(ax, px + pw/2, Y_PNL + 0.55, desc,    size=7.5, color='#8ab4cc')

txt(ax, FIG_W/2, Y_PNL + 1.72, 'CAMADA DE INTERFACE  (panels.py)',
    size=7.5, color=TXT_DIM, weight='bold')

# seta UI -> Operators
arrow(ax, FIG_W/2, Y_PNL - 0.02, FIG_W/2, Y_PNL - 0.55, color='#3a7bd5')
arrow_label(ax, FIG_W/2 + 0.5, Y_PNL - 0.27, 'dispara')

# ══════════════════════════════════════════════════════════════════
# 3. OPERATORS
# ══════════════════════════════════════════════════════════════════
Y_OPS = 15.95
box(ax, 0.4, Y_OPS, 17.2, 2.1, C_GRN_D, C_GRN_E, lw=2)
txt(ax, FIG_W/2, Y_OPS + 1.88, 'CAMADA DE LÓGICA  (operators.py)',
    size=7.5, color=TXT_DIM, weight='bold')
txt(ax, 1.0, Y_OPS + 1.6, 'Operators', size=11, color='#66bb6a',
    ha='left', weight='bold')

ops = [
    'get_classes', 'get_properties', 'get_prop_info', 'get_class_info',
    'load_decomposition', 'load_products', 'props_load', 'props_graph',
    'props_edit', 'add_properties', 'export_ids (IDS)', 'expand / contract',
    'decomposition_move', 'catalog_select_type', 'document_load / open', 'show_table',
]
cols = 4
col_w = 17.2 / cols
for i, op in enumerate(ops):
    col = i % cols
    row = i // cols
    ox = 0.4 + col * col_w + 0.25
    oy = Y_OPS + 1.25 - row * 0.38
    box(ax, ox - 0.15, oy - 0.14, col_w - 0.35, 0.3,
        '#1b5e20', '#2e7d32', radius=0.1, lw=1)
    txt(ax, ox + (col_w - 0.55)/2, oy + 0.01, op,
        size=7, color='#a5d6a7', ha='center')

# seta Operators -> camada inferior
arrow(ax, FIG_W/2, Y_OPS - 0.02, FIG_W/2, Y_OPS - 0.55, color='#4caf50')
arrow_label(ax, FIG_W/2 + 0.8, Y_OPS - 0.27, 'lê / escreve')

# ══════════════════════════════════════════════════════════════════
# 4. TRÊS COLUNAS: Estado | Dados | IFC
# ══════════════════════════════════════════════════════════════════
Y_MID = 12.35
col_h = 3.35

# — OG_Properties —
box(ax, 0.4, Y_MID, 5.5, col_h, C_PUR_D, C_PUR_E, lw=2)
txt(ax, 0.4 + 5.5/2, Y_MID + col_h - 0.22,
    'ESTADO GLOBAL  (properties.py)', size=7, color=TXT_DIM, weight='bold')
txt(ax, 0.4 + 5.5/2, Y_MID + col_h - 0.55,
    'OG_Properties', size=11, color='#ce93d8', weight='bold')
txt(ax, 0.4 + 5.5/2, Y_MID + col_h - 0.82,
    'Scene.og_props', size=8, color='#ce93d8', style='italic')
props_items = [
    'classes / classes_shown',
    'ifc_prop',
    'prop_metadata (Psets)',
    'elements_containers',
    'containers_show',
    'products / types / types_show',
    'class_info / class_prop_info',
    'OG_Properties → PropertyGroup',
]
for i, p in enumerate(props_items):
    txt(ax, 0.8, Y_MID + col_h - 1.2 - i*0.3, '•  ' + p,
        size=7.5, color='#bbaacc', ha='left')

# — data.py —
box(ax, 6.25, Y_MID, 5.5, col_h, C_RED_D, C_RED_E, lw=2)
txt(ax, 6.25 + 5.5/2, Y_MID + col_h - 0.22,
    'CAMADA DE DADOS  (data.py)', size=7, color=TXT_DIM, weight='bold')
txt(ax, 6.25 + 5.5/2, Y_MID + col_h - 0.55,
    'bSDD', size=11, color='#ef9a9a', weight='bold')
bsdd_items = [
    'load_dictionaries()',
    'load_classes(version)',
    'load_properties(version)',
    'get_class(uri)',
    'get_class_prop(uri)',
    'get_property(uri)',
]
for i, p in enumerate(bsdd_items):
    txt(ax, 6.5, Y_MID + col_h - 1.05 - i*0.3, '↳  ' + p,
        size=7.5, color='#ffaaaa', ha='left')
txt(ax, 6.25 + 5.5/2, Y_MID + 0.85,
    'PropTempl', size=10, color='#ef9a9a', weight='bold')
txt(ax, 6.5, Y_MID + 0.55, '↳  template EPset_OG.ifc',
    size=7.5, color='#ffaaaa', ha='left')
txt(ax, 6.5, Y_MID + 0.25, '↳  add_pset_template()',
    size=7.5, color='#ffaaaa', ha='left')

# — ifcopenshell —
box(ax, 12.1, Y_MID, 5.5, col_h, C_CYN_D, C_CYN_E, lw=2)
txt(ax, 12.1 + 5.5/2, Y_MID + col_h - 0.22,
    'BIM / IFC', size=7, color=TXT_DIM, weight='bold')
txt(ax, 12.1 + 5.5/2, Y_MID + col_h - 0.55,
    'ifcopenshell + Bonsai', size=10, color='#80deea', weight='bold')
ifc_items = [
    'IfcStore — modelo IFC ativo',
    'tool.Ifc — acesso ao modelo',
    '',
    'ifcopenshell.api.pset',
    'ifcopenshell.api.nest',
    'ifcopenshell.api.aggregate',
    'ifcopenshell.api.spatial',
    'ifcopenshell.util.element',
    'ifcopenshell.util.unit',
    '',
    'ifctester — export IDS',
]
for i, p in enumerate(ifc_items):
    prefix = '  ' if p == '' else ('→  ' if 'ifc' in p.lower() or 'bonsai' in p.lower() else '•  ')
    txt(ax, 12.35, Y_MID + col_h - 1.0 - i*0.28, prefix + p,
        size=7.2, color='#88ddee', ha='left')

# setas laterais entre colunas
arrow(ax, 5.9,  Y_MID + col_h/2, 6.25, Y_MID + col_h/2, color='#888')
arrow(ax, 11.75, Y_MID + col_h/2, 12.1, Y_MID + col_h/2, color='#888')

# ── BLOCO EXTERNO: bSDD API ────────────────────────────────────
Y_EXT = 9.6
box(ax, 6.25, Y_EXT, 5.5, 2.4, '#1a1a2a', C_ORG_E, lw=2)
txt(ax, 6.25 + 5.5/2, Y_EXT + 2.18,
    'EXTERNO / REMOTO', size=7, color=TXT_DIM, weight='bold')
txt(ax, 6.25 + 5.5/2, Y_EXT + 1.82,
    'bSDD REST API', size=10.5, color='#ffcc80', weight='bold')
txt(ax, 6.25 + 5.5/2, Y_EXT + 1.52,
    'api.bsdd.buildingsmart.org', size=8, color='#ff9800')
txt(ax, 6.5, Y_EXT + 1.18, '• /api/Dictionary/v1',       size=7.5, color='#ddaa66', ha='left')
txt(ax, 6.5, Y_EXT + 0.88, '• /api/Dictionary/v1/Classes', size=7.5, color='#ddaa66', ha='left')
txt(ax, 6.5, Y_EXT + 0.58, '• /api/Class/v1',             size=7.5, color='#ddaa66', ha='left')
txt(ax, 6.5, Y_EXT + 0.28, '• /api/Property/v4',          size=7.5, color='#ddaa66', ha='left')

# seta data.py -> bSDD API
arrow(ax, 6.25 + 5.5/2, Y_MID - 0.02,
      6.25 + 5.5/2, Y_EXT + 2.42, color='#ff9800')
arrow_label(ax, 6.25 + 5.5/2 + 0.6, (Y_MID + Y_EXT + 2.42)/2 + 0.1, 'HTTP GET', color='#ff9800')

# ── BLOCO LOCAL: metadata.json ─────────────────────────────────
box(ax, 0.4, Y_EXT, 5.5, 2.4, '#1a1a2a', C_ORG_E, lw=1.5, ls='--')
txt(ax, 0.4 + 5.5/2, Y_EXT + 2.18,
    'ARQUIVO LOCAL', size=7, color=TXT_DIM, weight='bold')
txt(ax, 0.4 + 5.5/2, Y_EXT + 1.82,
    'metadata.json', size=10.5, color='#ffcc80', weight='bold')
txt(ax, 0.4 + 5.5/2, Y_EXT + 1.45,
    'Catálogo local de tipos de produto', size=8, color='#ddaa66')
txt(ax, 0.6, Y_EXT + 1.1,  '• Pipes / Pipe Fittings', size=7.5, color='#ddaa66', ha='left')
txt(ax, 0.6, Y_EXT + 0.8,  '• Valves / Flanges',       size=7.5, color='#ddaa66', ha='left')
txt(ax, 0.6, Y_EXT + 0.5,  '• element_type + description', size=7.5, color='#ddaa66', ha='left')
txt(ax, 0.6, Y_EXT + 0.2,  '→ lido por Operator_load_products', size=7.5, color='#aaa', ha='left')

arrow(ax, 0.4 + 5.5/2, Y_MID - 0.02,
      0.4 + 5.5/2, Y_EXT + 2.42, color='#ff9800', lw=1.2)
arrow_label(ax, 0.4 + 5.5/2 + 0.5, (Y_MID + Y_EXT + 2.42)/2 + 0.1, 'carrega', color='#ff9800')

# ── BLOCO: matplotlib/pandas ───────────────────────────────────
box(ax, 12.1, Y_EXT, 5.5, 2.4, '#1a1a2a', C_ORG_E, lw=1.5, ls='--')
txt(ax, 12.1 + 5.5/2, Y_EXT + 2.18,
    'LIBS PYTHON', size=7, color=TXT_DIM, weight='bold')
txt(ax, 12.1 + 5.5/2, Y_EXT + 1.82,
    'matplotlib · pandas · scipy', size=9.5, color='#ffcc80', weight='bold')
txt(ax, 12.1 + 5.5/2, Y_EXT + 1.45,
    'Geração de gráficos de propriedades', size=8, color='#ddaa66')
txt(ax, 12.3, Y_EXT + 1.1,  '• Curvas interpoladas (scipy.interp1d)', size=7.5, color='#ddaa66', ha='left')
txt(ax, 12.3, Y_EXT + 0.8,  '• Scatter / Line plots (matplotlib)',      size=7.5, color='#ddaa66', ha='left')
txt(ax, 12.3, Y_EXT + 0.5,  '• Tabelas de dados (pandas DataFrame)',    size=7.5, color='#ddaa66', ha='left')
txt(ax, 12.3, Y_EXT + 0.2,  '→ Operator_props_graph',                  size=7.5, color='#aaa', ha='left')

arrow(ax, 12.1 + 5.5/2, Y_MID - 0.02,
      12.1 + 5.5/2, Y_EXT + 2.42, color='#ff9800', lw=1.2)
arrow_label(ax, 12.1 + 5.5/2 + 0.5, (Y_MID + Y_EXT + 2.42)/2 + 0.1, 'usa', color='#ff9800')

# ══════════════════════════════════════════════════════════════════
# 5. EVENTO AUTOMÁTICO
# ══════════════════════════════════════════════════════════════════
Y_EVT = 8.7
box(ax, 0.4, Y_EVT, 17.2, 0.75, C_YEL_D, C_YEL_E, lw=1.5, ls='--', radius=0.25)
txt(ax, 1.0, Y_EVT + 0.55, '(!)', size=11, ha='left')
txt(ax, 1.8, Y_EVT + 0.55, 'EVENTO AUTOMÁTICO', size=8, color='#f0a500',
    ha='left', weight='bold')
txt(ax, 1.8, Y_EVT + 0.22,
    'bpy.msgbus.subscribe_rna(LayerObjects.active)  →  data.call_back()  →  bpy.ops.props.load_properties()',
    size=8, color='#ccaa44', ha='left')

arrow(ax, FIG_W/2, Y_MID - 0.02, FIG_W/2, Y_EVT + 0.77, color='#f0a500', lw=1.2)

# ══════════════════════════════════════════════════════════════════
# 6. FLUXO PRINCIPAL
# ══════════════════════════════════════════════════════════════════
Y_FLW = 6.4
txt(ax, FIG_W/2, Y_FLW + 1.85,
    'FLUXO PRINCIPAL', size=8, color='#f0a500', weight='bold')

steps = [
    ('1', 'Seleciona\nobjeto',       'Usuário clica\nno Viewport'),
    ('2', 'Carrega\nPsets',          'props_load lê psets\nIFC do objeto'),
    ('3', 'Panel_\nProperties',      'Exibe e permite\neditar propriedades'),
    ('4', 'bSDD /\nCatálogo',        'Consulta API\nou JSON local'),
    ('5', 'Exporta\nIDS / salva',    'Gera IDS ou\nescreve no IFC'),
]
sw = 3.1
sx0 = 0.4
for i, (num, title, desc) in enumerate(steps):
    sx = sx0 + i * (sw + 0.2)
    box(ax, sx, Y_FLW, sw, 1.65, '#161b26', '#2a3040', radius=0.2)
    txt(ax, sx + 0.45, Y_FLW + 1.38, num,  size=20, color='#2a3a5a', weight='bold')
    txt(ax, sx + sw/2, Y_FLW + 0.95, title, size=9,  color='#61dafb', weight='bold')
    txt(ax, sx + sw/2, Y_FLW + 0.42, desc,  size=7.5, color='#888888')
    if i < len(steps) - 1:
        arrow(ax, sx + sw + 0.02, Y_FLW + 0.82,
              sx + sw + 0.18, Y_FLW + 0.82, color='#444')

# ══════════════════════════════════════════════════════════════════
# 7. LEGENDA
# ══════════════════════════════════════════════════════════════════
Y_LEG = 5.3
legend_items = [
    (C_BLU_D, C_BLU_E, 'UI / Painéis'),
    (C_GRN_D, C_GRN_E, 'Operators (lógica)'),
    (C_PUR_D, C_PUR_E, 'Estado (PropertyGroup)'),
    (C_RED_D, C_RED_E, 'Dados / API'),
    (C_CYN_D, C_CYN_E, 'IFC / Bonsai'),
    (C_ORG_D, C_ORG_E, 'Ext / Local / Libs'),
]
lx = 0.4
for i, (fc, ec, label) in enumerate(legend_items):
    llx = lx + i * 2.9
    box(ax, llx, Y_LEG, 0.4, 0.28, fc, ec, radius=0.05, lw=1.2)
    txt(ax, llx + 0.55, Y_LEG + 0.14, label, size=7.5, color='#aaaaaa', ha='left')

# ══════════════════════════════════════════════════════════════════
# SALVAR
# ══════════════════════════════════════════════════════════════════
import os
out = os.path.join(os.path.dirname(__file__), 'diagrama_arquitetura.png')
plt.tight_layout(pad=0)
plt.savefig(out, dpi=150, bbox_inches='tight',
            facecolor='#0f1117', edgecolor='none')
print(f'Salvo em: {out}')
