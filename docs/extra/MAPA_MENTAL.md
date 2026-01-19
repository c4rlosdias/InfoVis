# 🗺️ Mapa Mental - Oil & Gas Tools

## Estrutura Visual da Documentação

```
📚 OIL & GAS TOOLS DOCUMENTATION
│
├─ 🎯 COMEÇAR AQUI
│  ├─ README_DOCUMENTATION.md (Índice Principal)
│  ├─ SUMARIO_EXECUTIVO.md (Overview Rápido)
│  └─ GLOSSARY.md (Termos & Referência)
│
├─ 📖 FUNDAMENTOS
│  ├─ DOCUMENTATION.md
│  │  ├─ Visão Geral
│  │  ├─ Arquitetura
│  │  ├─ Módulos Principais
│  │  ├─ Dependências
│  │  ├─ Fluxo de Dados
│  │  └─ Como Usar
│  │
│  └─ ARCHITECTURE.md
│     ├─ Camadas da Aplicação
│     ├─ Fluxos de Dados
│     ├─ Estrutura de Dados
│     ├─ Integração com Blender
│     ├─ Padrões de Design
│     └─ Recursos Externos
│
├─ 🔧 DESENVOLVIMENTO
│  └─ DEVELOPMENT.md
│     ├─ Setup de Ambiente
│     ├─ Adicionar Funcionalidades
│     ├─ Fluxos Comuns
│     ├─ Testes & Debugging
│     ├─ Performance
│     ├─ Boas Práticas
│     └─ Git Workflow
│
├─ 📦 MÓDULOS (Código-Fonte)
│  ├─ OPERATORS_DOCUMENTATION.md (operators.py - 1551 linhas)
│  │  ├─ Visão Geral
│  │  ├─ Gerenciamento de Dados
│  │  ├─ Construção de Hierarquias
│  │  ├─ Controle de Visibilidade
│  │  ├─ Operadores IFC
│  │  ├─ Análise e Visualização
│  │  ├─ Validação IDS
│  │  └─ Debugging
│  │
│  ├─ PANELS_DOCUMENTATION.md (panels.py - 766 linhas)
│  │  ├─ Funções Auxiliares
│  │  ├─ Panel_Connect
│  │  ├─ List UI Items
│  │  ├─ Operadores Conectados
│  │  ├─ Propriedades Usadas
│  │  ├─ Fluxo de Interação
│  │  ├─ Padrões de Código
│  │  └─ Debugging
│  │
│  ├─ PROPERTIES_DOCUMENTATION.md (properties.py - 234 linhas)
│  │  ├─ Funções de Callback
│  │  ├─ Ifc_properties
│  │  ├─ Class_info
│  │  ├─ Class_type
│  │  ├─ Relacionamentos
│  │  ├─ Fluxo de Atualização
│  │  ├─ Registro
│  │  ├─ Persistência
│  │  ├─ Debugging
│  │  └─ Armadilhas
│  │
│  └─ DATA_DOCUMENTATION.md (data.py - 613 linhas)
│     ├─ Variáveis Globais
│     ├─ Funções de Callback
│     ├─ Funções de Atualização
│     ├─ Estrutura IFC
│     ├─ Integração bSDD
│     ├─ Fluxo de Eventos
│     ├─ Filtragem e Busca
│     ├─ Debugging
│     └─ Armadilhas
│
└─ 📚 REFERÊNCIA RÁPIDA
   └─ GLOSSARY.md
      ├─ Glossário de Termos
      ├─ Referência de Código
      ├─ Padrões Comuns
      ├─ Estrutura de Dados
      ├─ Convenções de Nomenclatura
      ├─ Debugging Rápido
      ├─ Checklist
      ├─ Comandos Úteis
      ├─ Problemas Comuns
      └─ Exercícios
```

---

## 🎯 Guias por Objetivo

### Objetivo: "Quero usar o software"
```
1. Ler: SUMARIO_EXECUTIVO.md (2 min)
   ↓
2. Ler: DOCUMENTATION.md - "Como Usar" (5 min)
   ↓
3. Instalar e testar (10 min)
   ↓
4. Usar interface (prático)
```

### Objetivo: "Quero aprender a arquitetura"
```
1. Ler: README_DOCUMENTATION.md (índice)
   ↓
2. Ler: DOCUMENTATION.md (overview)
   ↓
3. Ler: ARCHITECTURE.md (design profundo)
   ↓
4. Consultar módulos específicos conforme necessário
```

### Objetivo: "Quero adicionar uma funcionalidade"
```
1. Ler: DEVELOPMENT.md - "Adicionar nova funcionalidade"
   ↓
2. Estudar: Módulo relevante (operators.py, panels.py, etc)
   ↓
3. Consultar: GLOSSARY.md para padrões
   ↓
4. Implementar e testar
   ↓
5. Documentar mudanças
```

### Objetivo: "Preciso debugar um problema"
```
1. Consultar: DEVELOPMENT.md - "Debugging"
   ↓
2. Consultar: Módulo relevante - seção Debugging
   ↓
3. Usar: GLOSSARY.md - "Debugging Rápido"
   ↓
4. Inspecionar: Console do Blender (Shift+F4)
```

### Objetivo: "Quero entender um padrão"
```
1. Buscar: GLOSSARY.md - "Padrões Comuns"
   ↓
2. Ou buscar: Documentação de módulo específico
   ↓
3. Ou consultar: ARCHITECTURE.md - "Padrões de Design"
```

---

## 📊 Matriz de Conteúdo

| Tópico | DOCUMENTATION | ARCHITECTURE | DEVELOPMENT | Módulos | GLOSSARY |
|--------|---|---|---|---|---|
| **Overview** | ✅ | ✅ | ✅ | - | ✅ |
| **Instalação** | ✅ | - | ✅ | - | - |
| **Como Usar** | ✅ | - | - | - | - |
| **Arquitetura** | ✅ | ✅✅ | ✅ | ✅ | - |
| **Módulos** | ✅ | - | - | ✅✅ | ✅ |
| **Código** | - | - | - | ✅ | ✅ |
| **Padrões** | - | ✅ | ✅ | ✅ | ✅ |
| **Debugging** | - | - | ✅ | ✅ | ✅ |
| **Desenvolvimento** | - | - | ✅✅ | ✅ | ✅ |
| **Glossário** | - | - | - | - | ✅✅ |

---

## 🔄 Fluxos de Leitura Recomendados

### Para Iniciantes
```
Semana 1:
├─ Dia 1: README_DOCUMENTATION.md (orientação)
├─ Dia 2: SUMARIO_EXECUTIVO.md (overview)
├─ Dia 3: DOCUMENTATION.md (fundamentos)
├─ Dia 4: Instalar e testar
└─ Dia 5: GLOSSARY.md (referência)

Semana 2:
├─ Dia 1-2: ARCHITECTURE.md (fundação teórica)
├─ Dia 3-4: Estudar código-fonte
└─ Dia 5: Praticar com exercícios
```

### Para Intermediários
```
├─ Rever ARCHITECTURE.md (aprofundar)
├─ Ler documentação de módulos específicos
├─ Estudar padrões em DEVELOPMENT.md
└─ Começar pequenas contribuições
```

### Para Avançados
```
├─ Código-fonte (estudo profundo)
├─ Otimizações em DEVELOPMENT.md - "Performance"
├─ Arquitetura em ARCHITECTURE.md - "Integração com Blender"
└─ Desenvolvimento de features complexas
```

---

## 🗂️ Índice de Tópicos

### Análise de Dados
- OPERATORS_DOCUMENTATION.md - "Análise e Visualização"
- GLOSSARY.md - matplotlib, pandas, scipy

### Blender Integration
- ARCHITECTURE.md - "Integração com Blender"
- DEVELOPMENT.md - "Ambiente de Desenvolvimento"

### Callbacks
- PROPERTIES_DOCUMENTATION.md - "Funções de Callback"
- DATA_DOCUMENTATION.md - "Funções de Callback"
- GLOSSARY.md - "Callbacks"

### Debugging
- Todos os módulos têm seção "Debugging"
- GLOSSARY.md - "Debugging Rápido"
- DEVELOPMENT.md - "Debugging"

### Estrutura de Dados
- PROPERTIES_DOCUMENTATION.md - "Property Groups Principais"
- ARCHITECTURE.md - "Estrutura de Dados"
- GLOSSARY.md - "Estrutura de Dados Padrão"

### Eventos
- DATA_DOCUMENTATION.md - "Fluxo de Eventos"
- ARCHITECTURE.md - "Fluxo de Inicialização"

### Fluxo de Dados
- DOCUMENTATION.md - "Fluxo de Dados"
- ARCHITECTURE.md - "Fluxos de Dados"
- DATA_DOCUMENTATION.md - "Fluxo de Eventos"

### IFC/bSDD
- OPERATORS_DOCUMENTATION.md - "Operadores IFC"
- DATA_DOCUMENTATION.md - "Integração bSDD"
- GLOSSARY.md - Termos IFC

### Operadores
- OPERATORS_DOCUMENTATION.md (completo)
- DEVELOPMENT.md - "Adicionar uma nova funcionalidade"
- ARCHITECTURE.md - "Operators Layer"

### Painéis
- PANELS_DOCUMENTATION.md (completo)
- DEVELOPMENT.md - "Adicionar Novo Painel"
- ARCHITECTURE.md - "UI Layer"

### Performance
- DEVELOPMENT.md - "Performance"
- ARCHITECTURE.md - "Integração com Blender"

### PropertyGroups
- PROPERTIES_DOCUMENTATION.md (completo)
- GLOSSARY.md - "Property Groups"
- ARCHITECTURE.md - "Properties Layer"

### Validação
- OPERATORS_DOCUMENTATION.md - "Validação com IDS"
- GLOSSARY.md - "IDS"

---

## 🎓 Cursos e Trilhas de Aprendizado

### Trilha: Usuário Final
**Objetivo**: Usar o software efetivamente
**Duração**: 1-2 horas
```
1. SUMARIO_EXECUTIVO.md (20 min)
2. DOCUMENTATION.md - "Como Usar" (20 min)
3. Exploração prática (30-60 min)
```

### Trilha: Desenvolvedor Iniciante
**Objetivo**: Começar a contribuir
**Duração**: 5-7 horas
```
1. README_DOCUMENTATION.md (30 min)
2. DOCUMENTATION.md (1 hora)
3. ARCHITECTURE.md (1.5 horas)
4. DEVELOPMENT.md - Setup (30 min)
5. Estudar 1 módulo completo (2 horas)
6. Exercício simples (30 min)
```

### Trilha: Desenvolvedor Intermediário
**Objetivo**: Desenvolver novas funcionalidades
**Duração**: 15-20 horas
```
1. Toda trilha iniciante
2. Estudar todos os módulos (5 horas)
3. DEVELOPMENT.md - Fluxos Comuns (2 horas)
4. Implementar 2-3 features (8-10 horas)
5. Otimizações e testes (2 horas)
```

### Trilha: Desenvolvedor Avançado
**Objetivo**: Arquitetura e design
**Duração**: 20-30 horas
```
1. Toda trilha intermediária
2. ARCHITECTURE.md - Estudo profundo (3 horas)
3. Código-fonte linha por linha (5-8 horas)
4. Design e refatoração (5 horas)
5. Documentação e contribuições (5 horas)
```

---

## 📈 Progressão de Conhecimento

```
Usuário
   │
   ├─ Sabe usar (1-2h) ──────────────┐
   │                                 │
   ▼                                 │
Desenvolvedor Iniciante             │
   │ (5-7h)                          │
   ├─ Conhece estrutura              │
   ├─ Pode fazer mudanças simples    │
   │                                 │
   ▼                                 │
Desenvolvedor Intermediário         │
   │ (15-20h)                        │
   ├─ Implementa features            │
   ├─ Entende fluxos                 │
   │                                 │
   ▼                                 │
Desenvolvedor Avançado              │
   │ (20-30h)                        │
   ├─ Projeta arquitetura            │
   ├─ Otimiza performance            │
   ├─ Lidera projeto                 │
   │                                 │
   ▼                                 │
Arquiteto/Mantenedor                │
   │                                 │
   └─────────────────────────────────┘
   (contínuo)
```

---

## 🔗 Ligações Cruzadas

### Ao estudar Operators
→ Veja também: DEVELOPMENT.md, GLOSSARY.md

### Ao estudar Panels
→ Veja também: DEVELOPMENT.md, GLOSSARY.md

### Ao estudar Properties
→ Veja também: ARCHITECTURE.md, GLOSSARY.md

### Ao estudar Data
→ Veja também: ARCHITECTURE.md, GLOSSARY.md

### Ao debugar
→ Veja: Documentação específica do módulo + GLOSSARY.md

### Ao implementar padrão
→ Veja: ARCHITECTURE.md "Padrões" + GLOSSARY.md "Padrões Comuns"

---

## 📚 Contagem de Páginas (Aproximado)

| Documento | Páginas |
|-----------|---------|
| DOCUMENTATION.md | 8 |
| ARCHITECTURE.md | 10 |
| DEVELOPMENT.md | 12 |
| OPERATORS_DOCUMENTATION.md | 8 |
| PANELS_DOCUMENTATION.md | 7 |
| PROPERTIES_DOCUMENTATION.md | 9 |
| DATA_DOCUMENTATION.md | 9 |
| GLOSSARY.md | 10 |
| SUMARIO_EXECUTIVO.md | 8 |
| README_DOCUMENTATION.md | 6 |
| **TOTAL** | **~87 páginas** |

---

## ⏱️ Tempo de Leitura Estimado

| Documento | Tempo |
|-----------|-------|
| SUMARIO_EXECUTIVO.md | 15 min |
| README_DOCUMENTATION.md | 20 min |
| DOCUMENTATION.md | 30 min |
| ARCHITECTURE.md | 45 min |
| DEVELOPMENT.md | 50 min |
| GLOSSARY.md | 30 min |
| Cada módulo | 25-35 min |
| **Mínimo (Overview)** | **~1h** |
| **Padrão (Iniciante)** | **~4h** |
| **Completo (Profundo)** | **~8h** |

---

## ✅ Checklist de Leitura

### Essencial (Todos)
- [ ] SUMARIO_EXECUTIVO.md
- [ ] README_DOCUMENTATION.md
- [ ] DOCUMENTATION.md

### Desenvolvedor
- [ ] ARCHITECTURE.md
- [ ] DEVELOPMENT.md
- [ ] GLOSSARY.md

### Específico por Módulo
- [ ] OPERATORS_DOCUMENTATION.md (se trabalhar com operators)
- [ ] PANELS_DOCUMENTATION.md (se trabalhar com UI)
- [ ] PROPERTIES_DOCUMENTATION.md (se trabalhar com dados)
- [ ] DATA_DOCUMENTATION.md (se trabalhar com eventos)

---

**Mapa Mental completo criado! Use como referência para navegar a documentação. 🗺️**
