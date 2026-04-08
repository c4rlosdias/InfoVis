# � Oil & Gas Tools - Add-on Blender

Um add-on para Blender que oferece ferramentas especializadas para modelagem e análise de estruturas de Oil & Gas, com suporte a IFC e integração com bSDD.

## 📋 Início Rápido

### Requisitos
- Blender 5.0+
- Python 3.10+
- Git

### Instalação

1. **Obtenha o arquivo zipado com o release:**

   - Abra Blender
   - Acesse Edit > Preferences > Add-ons
   - Clique Install 'AddOn from disk'
   - Selecione o arquivo zip correspondente ao release que deseja instalar

### Criação do release
1. **Execute:**

```
>_ build_realease.bat (Windows)
>_ build_realease.sh (Linux)
```

## 🏗️ Estrutura do Projeto

```
├── operators.py       # Lógica principal (1551 linhas)
├── panels.py         # Interface do usuário (766 linhas)
├── properties.py     # Estrutura de dados (234 linhas)
├── data.py          # Sincronização (613 linhas)
├── resources/       # Arquivos de configuração e dados
├── libs/           # Dependências empacotadas
└── docs/           # Documentação detalhada
```

## 📚 Documentação

- **[Arquitetura](docs/ARCHITECTURE.md)** - Estrutura técnica do projeto
- **[Desenvolvimento](docs/DEVELOPMENT.md)** - Guia para contribuidores
- **Documentação por Módulo:**
  - [operators.py](docs/guides/OPERATORS_DOCUMENTATION.md) - Lógica principal
  - [panels.py](docs/guides/PANELS_DOCUMENTATION.md) - Interface do usuário
  - [properties.py](docs/guides/PROPERTIES_DOCUMENTATION.md) - Estrutura de dados
  - [data.py](docs/guides/DATA_DOCUMENTATION.md) - Sincronização de dados
- **[Glossário](docs/reference/GLOSSARY.md)** - Termos e padrões usados no projeto

## 🚀 Funcionalidades Principais

- **Extração IFC**: Importação e análise de arquivos IFC
- **Visualização de Dados**: Gráficos e estatísticas de estruturas
- **Integração bSDD**: Acesso ao dicionário de dados buildingSMART
- **Gerenciamento de Propriedades**: Controle de propriedades BIM

## 🤝 Contribuindo

1. Leia o [Guia de Desenvolvimento](docs/DEVELOPMENT.md)
2. Consulte a documentação do módulo relevante em `docs/guides/`
3. Siga os padrões definidos no [Glossário](docs/reference/GLOSSARY.md)

## 📄 Licença

Consulte o arquivo LICENSE para mais informações.

```
README.md                            # Este arquivo
docs/
│
├── ARCHITECTURE.md                  # Arquitetura técnica profunda
├── DEVELOPMENT.md                   # Guia de desenvolvimento
│
├── guides/                          # Guias por Módulo
│   ├── OPERATORS_DOCUMENTATION.md       # operators.py (1551 linhas)
│   ├── PANELS_DOCUMENTATION.md          # panels.py (766 linhas)
│   ├── PROPERTIES_DOCUMENTATION.md      # properties.py (234 linhas)
│   └── DATA_DOCUMENTATION.md            # data.py (613 linhas)
│
├── reference/                   # Referência Rápida
│   ├── GLOSSARY.md              # Glossário e padrões
│   └── INDICE_COMPLETO.md       # Índice de todos os documentos
│
└── extra/                       # Documentos Adicionais
    ├── SUMARIO_EXECUTIVO.md     # Resumo para gestão
    ├── PROXIMOS_PASSOS.md       # Ações pós-documentação
    └── DOCUMENTACAO_CONCLUIDA.md # Verificação final
```

## 🗺️ Como Navegar

### Começando
1. **Raiz do projeto** → `DOCUMENTATION.md` (visão geral)
2. **Raiz do projeto** → `README_DOCUMENTATION.md` (índice central)

### Por Objetivo

**"Quero usar o software"**
- Consulte: [DOCUMENTATION.md](./doc/DOCUMENTATION.md)

**"Quero aprender arquitetura"**
- Leia: `ARCHITECTURE.md` (este diretório)

**"Quero desenvolver"**
- Leia: `DEVELOPMENT.md` (este diretório)
- Depois: `guides/` (módulo específico)

**"Preciso de referência rápida"**
- Consulte: `reference/GLOSSARY.md`


**"Qual é o próximo passo?"**
- Veja: `extra/PROXIMOS_PASSOS.md`

## 📖 Documentos Principais (Raiz)

Mantenha na raiz do projeto:
- ✅ `../DOCUMENTATION.md` - Visão geral técnica
- ✅ `../README_DOCUMENTATION.md` - Índice central
- ✅ `../README.md` - README padrão do projeto

## 📦 Documentação por Módulo

Na pasta `guides/`:
- `OPERATORS_DOCUMENTATION.md` - Lógica principal
- `PANELS_DOCUMENTATION.md` - Interface do usuário
- `PROPERTIES_DOCUMENTATION.md` - Estrutura de dados
- `DATA_DOCUMENTATION.md` - Sincronização

## 🔍 Referência Rápida

Na pasta `reference/`:
- `GLOSSARY.md` - Termos, padrões e debugging
- `INDICE_COMPLETO.md` - Lista completa de documentos

## 📊 Documentos Adicionais

Na pasta `extra/`:
- `SUMARIO_EXECUTIVO.md` - Para stakeholders
- `MAPA_MENTAL.md` - Trilhas de aprendizado
- `PROXIMOS_PASSOS.md` - Publicação e manutenção
- `DOCUMENTACAO_CONCLUIDA.md` - Verificação

---

**Total: 13 documentos em 4 pastas + 2 na raiz**

