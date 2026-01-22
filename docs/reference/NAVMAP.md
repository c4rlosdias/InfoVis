# 🗺️ Mapa de Navegação Rápida

## 👋 "Onde Eu Estou?"

```
                        README.md (raiz)
                              │
                    ┌─────────┼─────────┐
                    │         │         │
            Quero    │    Quero     Quero
            Usar     │   Entender    Dev.
              │      │      │         │
              ▼      ▼      ▼         ▼
          WELCOME.md, ARCHITECTURE, DEVELOPMENT
                │         │              │
                ├─────────┼──────────────┤
                │                        │
                ▼                        ▼
          guides/ (detalhes)      reference/GLOSSARY
```

## 🎯 Navegação por Perfil

### 👤 Usuário (Quer usar o add-on)
```
1. Leia: README.md (raiz)
2. Siga: Seção "Instalação"
3. Pronto: Comece a usar!
```

### 👨‍💻 Desenvolvedor (Quer contribuir)
```
1. Leia: WELCOME.md
2. Leia: DEVELOPMENT.md
3. Escolha módulo em: guides/
4. Dúvida? Consulte: GLOSSARY.md
```

### 🔍 Investigador (Quer entender tudo)
```
1. Leia: WELCOME.md
2. Leia: ARCHITECTURE.md
3. Explore: guides/
4. Aprofunde: extra/
```

### 📊 Stakeholder (Quer relatório executivo)
```
1. Leia: README.md (raiz)
2. Leia: extra/SUMARIO_EXECUTIVO.md
3. Pronto!
```

## 🔍 "Preciso de Informações Sobre..."

| Pergunta | Resposta |
|----------|----------|
| **Como instalo?** | [README.md](../README.md) |
| **Como navego docs?** | [WELCOME.md](WELCOME.md) ou [INDEX.md](reference/INDEX.md) |
| **Como funciona internamente?** | [ARCHITECTURE.md](ARCHITECTURE.md) |
| **Como começo a desenvolver?** | [DEVELOPMENT.md](DEVELOPMENT.md) |
| **Como funcionam os operadores?** | [guides/OPERATORS_DOCUMENTATION.md](guides/OPERATORS_DOCUMENTATION.md) |
| **Como funciona a UI?** | [guides/PANELS_DOCUMENTATION.md](guides/PANELS_DOCUMENTATION.md) |
| **Como funcionam as propriedades?** | [guides/PROPERTIES_DOCUMENTATION.md](guides/PROPERTIES_DOCUMENTATION.md) |
| **Como sincroniza dados?** | [guides/DATA_DOCUMENTATION.md](guides/DATA_DOCUMENTATION.md) |
| **Qual é o significado de X?** | [reference/GLOSSARY.md](reference/GLOSSARY.md) |
| **Preciso de um índice completo** | [reference/INDEX.md](reference/INDEX.md) ou [README.md](README.md) |
| **Qual foi a reorganização?** | [REORGANIZATION.md](REORGANIZATION.md) |

## 📍 Localização de Arquivos

### Raiz do Projeto
```
oil-gas-addon/
├── README.md              ← Visão geral
├── requirements.txt
├── __init__.py
├── operators.py
├── panels.py
├── properties.py
├── data.py
└── docs/
```

### Pasta docs/
```
docs/
├── WELCOME.md             ← Comece aqui
├── README.md              ← Índice
├── ARCHITECTURE.md        ← Como funciona
├── DEVELOPMENT.md         ← Como desenvolver
├── REORGANIZATION.md      ← O que mudou
│
├── guides/
│   ├── OPERATORS_DOCUMENTATION.md
│   ├── PANELS_DOCUMENTATION.md
│   ├── PROPERTIES_DOCUMENTATION.md
│   └── DATA_DOCUMENTATION.md
│
├── reference/
│   ├── GLOSSARY.md        ← Perguntas rápidas
│   └── INDEX.md           ← Este mapa
│
└── extra/
    ├── SUMARIO_EXECUTIVO.md
    ├── MAPA_MENTAL.md
    ├── PROXIMOS_PASSOS.md
    └── DOCUMENTACAO_CONCLUIDA.md
```

## 🚀 Fluxos Rápidos

### "Quero adicionar um novo operador"
```
1. DEVELOPMENT.md → seção "Novo Operador"
2. guides/OPERATORS_DOCUMENTATION.md → exemplos
3. GLOSSARY.md → se tiver dúvida
```

### "Quero adicionar um novo painel"
```
1. DEVELOPMENT.md → seção "Novo Painel"
2. guides/PANELS_DOCUMENTATION.md → exemplos
3. GLOSSARY.md → se tiver dúvida
```

### "Quero entender um fluxo de dados"
```
1. ARCHITECTURE.md → seção "Fluxo de Dados"
2. guides/OPERATORS_DOCUMENTATION.md → detalhes
3. guides/DATA_DOCUMENTATION.md → sincronização
```

### "Encontrei um bug, onde procuro?"
```
1. GLOSSARY.md → seção "Debugging"
2. guides/ → módulo relevante
3. ARCHITECTURE.md → entender fluxo
```

## 💡 Dicas

### Para Encontrar Algo Rápido
- Use **Ctrl+F** em qualquer documento
- Comece pela [referência de índice](reference/INDEX.md)
- Consulte o [GLOSSARY.md](reference/GLOSSARY.md)

### Se Estiver Perdido
1. Leia [WELCOME.md](WELCOME.md)
2. Veja [Este arquivo](reference/INDEX.md)
3. Procure no [GLOSSARY.md](reference/GLOSSARY.md)

### Se Quiser Aprofundar
- Documentação detalhada está em `guides/`
- Complementos estão em `extra/`

## 🎯 Próximos Passos

Escolha seu ponto de entrada:

- **Novo por aqui?** → [WELCOME.md](WELCOME.md)
- **Quer visão geral?** → [README.md](../README.md)
- **Vai desenvolver?** → [DEVELOPMENT.md](DEVELOPMENT.md)
- **Quer saber tudo?** → [ARCHITECTURE.md](ARCHITECTURE.md)
- **Dúvida rápida?** → [GLOSSARY.md](GLOSSARY.md)

---

**Dica Final:** Não é preciso ler tudo! 
Comece pelo nível que você precisa e aprofunde conforme necessário. 😊
