# 📚 Oil & Gas Tools - Índice de Documentação

Bem-vindo à documentação completa do **Oil & Gas Tools**, um add-on Blender para visualização e análise de projetos de óleo e gás.

---

## 🗺️ Guias Disponíveis

### 📖 Documentação Geral
- **[DOCUMENTATION.md](../../DOCUMENTATION.md)** - Visão geral completa da aplicação
  - Arquitetura do projeto
  - Módulos principais
  - Dependências
  - Funcionalidades principais
  - Fluxo de dados
  - Como usar

### 🏗️ Arquitetura
- **[ARCHITECTURE.md](../ARCHITECTURE.md)** - Arquitetura técnica profunda
  - Visão geral das camadas
  - Padrões de design
  - Fluxos de dados detalhados
  - Estrutura de dados
  - Integração com Blender
  - Dependências entre módulos

### 👨‍💻 Guia de Desenvolvimento
- **[DEVELOPMENT.md](../DEVELOPMENT.md)** - Instruções para desenvolvedores
  - Setup de ambiente
  - Como adicionar funcionalidades
  - Padrões de código
  - Testes
  - Debugging
  - Boas práticas
  - Git workflow

---

## 📦 Documentação por Módulo

### [operators.py](../guides/OPERATORS_DOCUMENTATION.md) - 1551 linhas
**Lógica principal e operadores**

Principais tópicos:
- Gerenciamento de dados JSON
- Construção de hierarquias (`build_classes`, `build_products`)
- Controle de visibilidade
- Operadores IFC
- Análise e visualização (matplotlib, scipy, pandas)
- Validação com IDS

👉 [Ver documentação completa](../guides/OPERATORS_DOCUMENTATION.md)

---

### [panels.py](../guides/PANELS_DOCUMENTATION.md) - 766 linhas
**Interface do usuário e componentes visuais**

Principais tópicos:
- Funções auxiliares de UI
- Panel_Connect - Subsea Classes
- Templates de listas
- Propriedades usadas
- Fluxo de interação
- Padrões de código
- Debugging de UI

👉 [Ver documentação completa](../guides/PANELS_DOCUMENTATION.md)

---

### [properties.py](../guides/PROPERTIES_DOCUMENTATION.md) - 234 linhas
**Propriedades customizadas e estrutura de dados**

Principais tópicos:
- Funções de callback
- PropertyGroup: Ifc_properties
- PropertyGroup: Class_info
- PropertyGroup: Class_type
- Relações entre grupos
- Fluxo de atualização
- Persistência de dados
- Debugging

👉 [Ver documentação completa](../guides/PROPERTIES_DOCUMENTATION.md)

---

### [data.py](../guides/DATA_DOCUMENTATION.md) - 613 linhas
**Manipulação de dados e integração**

Principais tópicos:
- Variáveis globais
- Funções de callback
- Funções de atualização (refresh)
- Estrutura de dados IFC
- Integração bSDD
- Fluxo de eventos
- Funções de filtragem e busca
- Debugging

👉 [Ver documentação completa](../guides/DATA_DOCUMENTATION.md)

---

### [__init__.py](../../DOCUMENTATION.md#initialization-layer) - 124 linhas
**Inicialização do add-on**

Contém informações em DOCUMENTATION.md na seção "Módulos Principais"

---

## 🔍 Busca Rápida

### Por Tarefa

**"Quero adicionar um novo botão"**
1. Leia [operators.py - Operadores](../guides/OPERATORS_DOCUMENTATION.md#-operadores-ifc)
2. Leia [panels.py - Painéis Principais](../guides/PANELS_DOCUMENTATION.md#-painéis-principais)
3. Siga [DEVELOPMENT.md - Adicionar nova funcionalidade](../DEVELOPMENT.md#-adicionar-uma-nova-funcionalidade)

**"Quero entender como os dados fluem"**
1. Leia [ARCHITECTURE.md - Fluxos de Dados](../ARCHITECTURE.md#-fluxos-de-dados)
2. Consulte [DOCUMENTATION.md - Fluxo de Dados](../../DOCUMENTATION.md#-fluxo-de-dados)
3. Veja exemplos específicos em cada módulo

**"Quero debugar um problema"**
1. Veja [DEVELOPMENT.md - Debugging](../DEVELOPMENT.md#-debugging)
2. Consulte seção de debugging em cada documentação de módulo:
   - [operators.py debugging](../guides/OPERATORS_DOCUMENTATION.md#-debugging)
   - [panels.py debugging](../guides/PANELS_DOCUMENTATION.md#-debugging-de-ui)
   - [properties.py debugging](../guides/PROPERTIES_DOCUMENTATION.md#-debugging)
   - [data.py debugging](../guides/DATA_DOCUMENTATION.md#-debugging)

**"Quero entender a estrutura de propriedades"**
1. Leia [PROPERTIES_DOCUMENTATION.md](../guides/PROPERTIES_DOCUMENTATION.md)
2. Consulte exemplos em [DOCUMENTATION.md - Estrutura de Dados IFC](../../DOCUMENTATION.md#-estrutura-de-dados-ifc)

**"Quero adicionar um novo painel"**
1. Leia [DEVELOPMENT.md - Adicionar Novo Painel](../DEVELOPMENT.md#-adicionar-novo-painel)
2. Consulte exemplos em [PANELS_DOCUMENTATION.md](../guides/PANELS_DOCUMENTATION.md)

---

## 🎯 Por Nível de Experiência

### Iniciante
Comece com:
1. [DOCUMENTATION.md](../../DOCUMENTATION.md) - Visão geral
2. [ARCHITECTURE.md](../ARCHITECTURE.md) - Entender estrutura
3. [DEVELOPMENT.md - Setup](../DEVELOPMENT.md#-ambiente-de-desenvolvimento)

### Intermediário
Aprofunde em:
1. [Documentação de módulos específicos](#-documentação-por-módulo)
2. [ARCHITECTURE.md - Padrões de Design](../ARCHITECTURE.md#-padrões-de-design)
3. [DEVELOPMENT.md - Fluxos Comuns](../DEVELOPMENT.md#-fluxos-comuns)

### Avançado
Domine:
1. [Código-fonte dos módulos](../../)
2. [ARCHITECTURE.md - Integração com Blender](../ARCHITECTURE.md#-integração-com-blender)
3. [DEVELOPMENT.md - Performance](../DEVELOPMENT.md#-performance)

---

## 📊 Diagrama de Relacionamento

```
DOCUMENTATION.md (Overview)
    │
    ├── ARCHITECTURE.md (Design)
    │   └── DEVELOPMENT.md (How-To)
    │       ├── OPERATORS_DOCUMENTATION.md
    │       ├── PANELS_DOCUMENTATION.md
    │       ├── PROPERTIES_DOCUMENTATION.md
    │       └── DATA_DOCUMENTATION.md
    │
    └── Módulos Específicos
        ├── operators.py
        ├── panels.py
        ├── properties.py
        └── data.py
```

---

## 🔑 Conceitos Principais

### Property Groups
Estruturas de dados customizadas do Blender que persistem com o arquivo.
→ [Aprender mais](../guides/PROPERTIES_DOCUMENTATION.md#-estrutura-de-propertygroups)

### Operadores
Ações que o usuário pode executar (cliques de botão).
→ [Aprender mais](../guides/OPERATORS_DOCUMENTATION.md#-funcionalidades-principais)

### Panels
Interface visual onde o usuário interage.
### Callbacks
Funções disparadas quando dados mudam.
→ [Aprender mais](../guides/PROPERTIES_DOCUMENTATION.md#-funções-de-callback)

### Refresh
Sincronização entre dados completos e dados exibidos.
→ [Aprender mais](../guides/DATA_DOCUMENTATION.md#-funções-de-atualização-refresh)

---

## 🚀 Começar Rapidamente

### Instalação
1. Clone o repositório
2. Copie para pasta de add-ons do Blender
3. Ative em Preferences > Add-ons
→ [Detalhes](../../DOCUMENTATION.md#-como-usar)

### Uso Básico
1. Abra um arquivo IFC em Blender
2. Ative o painel "O&G Tools"
3. Clique em "get classes from bSDD"
4. Explore a estrutura
→ [Detalhes](../../DOCUMENTATION.md#-uso-básico)

### Desenvolvendo
1. Leia DEVELOPMENT.md
2. Configure ambiente
3. Adicione funcionalidade
4. Teste em Blender
→ [Detalhes](../DEVELOPMENT.md)

---

## 📞 Recursos Externos

### Blender
- [Blender Python API](https://docs.blender.org/api/current/)
- [BlenderBIM Documentation](https://blenderbim.org/)

### IFC
- [ifcopenshell Docs](http://docs.ifcopenshell.org/)
- [buildingSMART](https://www.buildingsmart.org/)
- [IFC Specification](https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/HTML/)

### Python Libraries
- [Matplotlib](https://matplotlib.org/) - Gráficos
- [Pandas](https://pandas.pydata.org/) - Análise de dados
- [SciPy](https://scipy.org/) - Computação científica
- [NumPy](https://numpy.org/) - Computação numérica

---

## ❓ FAQ (Perguntas Frequentes)

**P: Onde adiciono um novo botão?**
R: [DEVELOPMENT.md - Adicionar nova funcionalidade](../DEVELOPMENT.md#-adicionar-uma-nova-funcionalidade)

**P: Como debugo um problema?**
R: [DEVELOPMENT.md - Debugging](../DEVELOPMENT.md#-debugging)

**P: Qual é a estrutura de dados?**
R: [PROPERTIES_DOCUMENTATION.md](../guides/PROPERTIES_DOCUMENTATION.md)

**P: Como os dados fluem na aplicação?**
R: [ARCHITECTURE.md - Fluxos de Dados](../ARCHITECTURE.md#-fluxos-de-dados)

**P: Como adiciono uma nova PropertyGroup?**
R: [DEVELOPMENT.md - Adicionar nova PropertyGroup](../DEVELOPMENT.md#-adicionar-nova-propertygroup)

**P: Qual é o padrão de design usado?**
R: [ARCHITECTURE.md - Padrões de Design](../ARCHITECTURE.md#-padrões-de-design)

---

## 📄 Licença

Este projeto e sua documentação estão sob **GNU General Public License v3**.
Veja LICENSE para detalhes.

---

## 🤝 Contribuições

Contribuições são bem-vindas! 

Procedimento:
1. Fork o repositório
2. Crie branch para sua feature
3. Commit mudanças
4. Push para branch
5. Abra Pull Request

→ [Mais detalhes](../DEVELOPMENT.md#-integração-com-git)

---

## 📊 Estatísticas do Projeto

| Métrica | Valor |
|---------|-------|
| Linhas de código | ~3,600+ |
| Módulos | 5 (+ __init__.py) |
| Classes | 20+ |
| Operadores | 15+ |
| Painéis | 5+ |
| Documentação | 7 arquivos |

---

## ⚡ Última Atualização

- **Data**: 19 de Janeiro de 2026
- **Versão**: 0.1.1
- **Versão Blender**: 5.0+

---

## 🎓 Estrutura Recomendada de Aprendizado

```
Dia 1: Fundamentos
  ├─ DOCUMENTATION.md (leitura geral)
  └─ ARCHITECTURE.md (entender estrutura)

Dia 2: Módulos
  ├─ PROPERTIES_DOCUMENTATION.md
  ├─ OPERATORS_DOCUMENTATION.md
  ├─ PANELS_DOCUMENTATION.md
  └─ DATA_DOCUMENTATION.md

Dia 3: Desenvolvimento
  ├─ DEVELOPMENT.md (setup)
  └─ Código-fonte (estudo prático)

Dia 4+: Praticar
  ├─ Adicionar novos operadores
  ├─ Criar novos painéis
  └─ Expandir funcionalidades
```

---

## 💡 Dicas Úteis

1. **Sempre leia docstrings** - Cada função está documentada
2. **Use console Blender** - Shift+F4 para debug
3. **Teste incrementalmente** - Faça mudanças pequenas
4. **Backup antes de editar** - Use Git
5. **Consulte exemplos** - Veja código similar

---

**Bom desenvolvimento! 🚀**

Para dúvidas, consulte a seção relevante ou abra uma issue no repositório.
