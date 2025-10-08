# 🚀 GUIA COMPLETO: EMPACOTAMENTO STREAMLIT PARA EXECUTÁVEL DESKTOP

## 📋 ÍNDICE
1. [Pré-requisitos](#pré-requisitos)
2. [Preparação do Projeto](#preparação-do-projeto)
3. [Instalação das Ferramentas](#instalação-das-ferramentas)
4. [Estrutura de Arquivos](#estrutura-de-arquivos)
5. [Configuração dos Caminhos](#configuração-dos-caminhos)
6. [Processo de Empacotamento](#processo-de-empacotamento)
7. [Verificação e Testes](#verificação-e-testes)
8. [Distribuição](#distribuição)
9. [Solução de Problemas](#solução-de-problemas)
10. [Checklist Final](#checklist-final)

---

## 1. PRÉ-REQUISITOS

### Sistema Operacional
- **Windows 10/11** (64-bit)
- **Python 3.8+** instalado (apenas para desenvolvimento)
- **Git** (opcional, para controle de versão)

### Projeto Streamlit
- Aplicação Streamlit funcional
- Estrutura de pastas organizada
- Dependências listadas em `requirements.txt`

---

## 2. PREPARAÇÃO DO PROJETO

### 2.1 Estrutura de Pastas Recomendada
```
projeto/
├── app.py                    # Aplicação principal Streamlit
├── auth_simple.py           # Sistema de autenticação
├── requirements.txt         # Dependências Python
├── pages/                   # Páginas do Streamlit
│   ├── 1_Dash_Mes.py
│   ├── 2_IUD_Assistant.py
│   └── ...
├── dados/                   # Dados do projeto
│   ├── usuarios.json
│   ├── dados_equipe.json
│   └── arquivos.xlsx
├── Extracoes/              # Dados brutos
│   ├── KE5Z/
│   └── KSBB/
└── scripts/                # Scripts auxiliares
    └── Extracao.py
```

### 2.2 Verificação de Dependências
```bash
# Verificar se todas as dependências estão no requirements.txt
pip freeze > requirements.txt
```

### 2.3 Teste da Aplicação
```bash
# Testar se a aplicação funciona corretamente
streamlit run app.py
```

---

## 3. INSTALAÇÃO DAS FERRAMENTAS

### 3.1 Instalar streamlit-desktop-app
```bash
# Instalar a ferramenta de empacotamento
pip install streamlit-desktop-app
```

### 3.2 Verificar Instalação
```bash
# Verificar se foi instalado corretamente
streamlit-desktop-app --help
```

---

## 4. ESTRUTURA DE ARQUIVOS

### 4.1 Arquivos Principais (Raiz)
- **app.py**: Aplicação principal Streamlit
- **auth_simple.py**: Sistema de autenticação
- **requirements.txt**: Dependências Python
- **usuarios.json**: Dados de usuários
- **dados_equipe.json**: Configurações da aplicação

### 4.2 Pastas de Dados
- **pages/**: Páginas do Streamlit
- **dados/**: Dados processados
- **Extracoes/**: Dados brutos para processamento
- **scripts/**: Scripts auxiliares

### 4.3 Arquivos de Configuração
- **usuarios_padrao.json**: Usuários padrão
- ***.xlsx**: Arquivos Excel de dados

---

## 5. CONFIGURAÇÃO DOS CAMINHOS

### 5.1 Padronização de Caminhos Relativos

**IMPORTANTE**: Todos os caminhos devem ser relativos à pasta principal do projeto.

#### Exemplo em `Extracao.py`:
```python
import sys
import os

# Obter diretório base (onde está o executável)
if hasattr(sys, '_MEIPASS'):
    # Executando dentro do PyInstaller
    base_dir = sys._MEIPASS
    print(f"Executando dentro do PyInstaller: {base_dir}")
else:
    # Executando normalmente - usar diretório do script atual
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Executando normalmente: {base_dir}")

# ================== CAMINHOS PADRONIZADOS ==================
# Pasta raiz do projeto
ROOT_DIR = base_dir

# Pastas de entrada
DIR_EXTRACOES = os.path.join(ROOT_DIR, "Extracoes")
DIR_KE5Z_IN = os.path.join(DIR_EXTRACOES, "KE5Z")
DIR_KSBB_IN = os.path.join(DIR_EXTRACOES, "KSBB")

# Arquivos auxiliares de entrada
ARQ_SAPIENS = os.path.join(ROOT_DIR, "Dados SAPIENS.xlsx")
ARQ_FORNECEDORES = os.path.join(ROOT_DIR, "Fornecedores.xlsx")

# Pastas/arquivos de saída
DIR_KE5Z_OUT = os.path.join(ROOT_DIR, "KE5Z")
DIR_ARQUIVOS_OUT = os.path.join(ROOT_DIR, "arquivos")
# ============================================================
```

### 5.2 Verificação de Arquivos Necessários

#### Exemplo em `pages/6_Extracao_Dados.py`:
```python
def verificar_arquivos_necessarios():
    """Verifica se todos os arquivos necessários existem"""
    # Obter diretório base (onde está o executável)
    if hasattr(sys, '_MEIPASS'):
        # Executando dentro do PyInstaller
        base_dir = sys._MEIPASS
    else:
        # Executando normalmente - usar diretório do script atual
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    arquivos_necessarios = [
        (os.path.join(base_dir, "Extracao.py"), "Script principal"),
        (os.path.join(base_dir, "Extracoes", "KE5Z"), "Pasta com arquivos .txt KE5Z"),
        (os.path.join(base_dir, "Extracoes", "KSBB"), "Pasta com arquivos .txt KSBB"),
        (os.path.join(base_dir, "Dados SAPIENS.xlsx"), "Base de dados SAPIENS"),
        (os.path.join(base_dir, "Fornecedores.xlsx"), "Lista de fornecedores")
    ]
    
    # Verificar cada arquivo...
```

---

## 6. PROCESSO DE EMPACOTAMENTO

### 6.1 Comando de Empacotamento
```bash
# Navegar para a pasta do projeto
cd C:\caminho\para\seu\projeto

# Executar o empacotamento
streamlit-desktop-app build
```

### 6.2 Estrutura Gerada
Após o empacotamento, será criada a pasta `dist/` com:
```
dist/
└── NomeDoProjeto/
    ├── NomeDoProjeto.exe          # Executável principal
    ├── _internal/                 # Arquivos internos do PyInstaller
    │   ├── python313.dll         # Python runtime
    │   ├── libcrypto-3.dll       # OpenSSL
    │   ├── libssl-3.dll          # OpenSSL
    │   ├── app.py                # Aplicação principal
    │   ├── auth_simple.py        # Sistema de autenticação
    │   ├── pages/                # Páginas do Streamlit
    │   ├── Extracao.py           # Scripts auxiliares
    │   ├── Dados SAPIENS.xlsx    # Dados auxiliares
    │   ├── Fornecedores.xlsx     # Dados auxiliares
    │   └── Extracoes/            # Dados brutos
    │       ├── KE5Z/
    │       └── KSBB/
    ├── usuarios.json             # Dados de usuários (acessível)
    ├── dados_equipe.json         # Configurações (acessível)
    ├── Dados SAPIENS.xlsx        # Dados auxiliares (acessível)
    ├── Fornecedores.xlsx         # Dados auxiliares (acessível)
    ├── KE5Z/                     # Dados processados (acessível)
    ├── arquivos/                 # Arquivos gerados (acessível)
    └── Extracoes/                # Dados brutos (acessível)
```

---

## 7. VERIFICAÇÃO E TESTES

### 7.1 Verificação de Arquivos Críticos
```bash
# Verificar se todos os arquivos necessários estão presentes
cd dist/NomeDoProjeto

# Verificar executável
dir NomeDoProjeto.exe

# Verificar arquivos em _internal
dir _internal\*.py
dir _internal\*.xlsx

# Verificar pastas de dados
dir _internal\Extracoes\KE5Z
dir _internal\Extracoes\KSBB
```

### 7.2 Teste de Execução
```bash
# Testar execução do aplicativo
cd dist/NomeDoProjeto
NomeDoProjeto.exe
```

### 7.3 Verificação de Funcionalidades
1. **Login**: Testar sistema de autenticação
2. **Navegação**: Testar todas as páginas
3. **Extração**: Testar processamento de dados
4. **Download**: Testar geração de arquivos
5. **Filtros**: Testar filtros de dados

---

## 8. DISTRIBUIÇÃO

### 8.1 Preparação para Distribuição
```bash
# Criar arquivos de instrução
echo "Para executar o aplicativo, clique duas vezes em NomeDoProjeto.exe" > COMO_USAR.txt
echo "Ou execute ABRIR_DASHBOARD.bat" >> COMO_USAR.txt
```

### 8.2 Script de Abertura (Opcional)
```batch
@echo off
echo Iniciando Dashboard...
start NomeDoProjeto.exe
pause
```

### 8.3 Documentação
Criar arquivos de documentação:
- **README.md**: Instruções gerais
- **COMO_USAR.txt**: Instruções de uso
- **INSTRUCOES_DISTRIBUICAO.txt**: Instruções para distribuição

---

## 9. SOLUÇÃO DE PROBLEMAS

### 9.1 Erro: "ModuleNotFoundError"
**Problema**: Módulos Python não encontrados
**Solução**: 
```bash
# Copiar arquivos Python para _internal
copy auth_simple.py dist/NomeDoProjeto/_internal/
xcopy pages dist/NomeDoProjeto/_internal/pages/ /E /I /Y
```

### 9.2 Erro: "Arquivo não encontrado"
**Problema**: Arquivos de dados não encontrados
**Solução**:
```bash
# Copiar arquivos de dados para _internal
copy "Dados SAPIENS.xlsx" dist/NomeDoProjeto/_internal/
copy "Fornecedores.xlsx" dist/NomeDoProjeto/_internal/
xcopy Extracoes dist/NomeDoProjeto/_internal/Extracoes/ /E /I /Y
```

### 9.3 Erro: "IndentationError"
**Problema**: Erro de indentação no código
**Solução**: Verificar e corrigir indentação em todos os arquivos Python

### 9.4 Erro: "RecursionError"
**Problema**: Recursão infinita em funções
**Solução**: Verificar lógica das funções e evitar chamadas recursivas incorretas

---

## 10. CHECKLIST FINAL

### ✅ **ANTES DO EMPACOTAMENTO**
- [ ] Aplicação Streamlit funcionando corretamente
- [ ] Todos os caminhos padronizados como relativos
- [ ] Dependências listadas em requirements.txt
- [ ] Arquivos de dados organizados
- [ ] Scripts auxiliares funcionando

### ✅ **DURANTE O EMPACOTAMENTO**
- [ ] Comando `streamlit-desktop-app build` executado
- [ ] Pasta `dist/` criada com sucesso
- [ ] Executável gerado sem erros

### ✅ **APÓS O EMPACOTAMENTO**
- [ ] Executável principal presente
- [ ] Arquivos Python em `_internal/`
- [ ] Dados auxiliares em `_internal/`
- [ ] Pastas de dados em `_internal/`
- [ ] Arquivos de configuração na raiz (acessíveis)

### ✅ **VERIFICAÇÃO DE FUNCIONALIDADES**
- [ ] Executável inicia sem erros
- [ ] Sistema de login funcionando
- [ ] Todas as páginas acessíveis
- [ ] Extração de dados funcionando
- [ ] Filtros de dados funcionando
- [ ] Download de arquivos funcionando

### ✅ **PREPARAÇÃO PARA DISTRIBUIÇÃO**
- [ ] Arquivos de documentação criados
- [ ] Script de abertura criado (opcional)
- [ ] Teste em PC sem Python instalado
- [ ] Verificação de portabilidade

---

## 🎯 **DICAS IMPORTANTES**

### 1. **Caminhos Relativos**
- **SEMPRE** use caminhos relativos à pasta principal
- Use `sys._MEIPASS` para detectar execução em PyInstaller
- Teste em diferentes locais do sistema

### 2. **Arquivos de Dados**
- Mantenha dados acessíveis na raiz para o usuário
- Copie arquivos críticos para `_internal/` para o executável
- Use duplicação estratégica quando necessário

### 3. **Dependências**
- Inclua todas as dependências no `requirements.txt`
- Teste em ambiente limpo antes do empacotamento
- Verifique se todas as DLLs estão incluídas

### 4. **Testes**
- Teste em PC sem Python instalado
- Teste em diferentes versões do Windows
- Verifique todas as funcionalidades

### 5. **Documentação**
- Crie instruções claras para o usuário
- Documente requisitos do sistema
- Inclua solução de problemas comuns

---

## 📝 **EXEMPLO DE COMANDOS COMPLETOS**

```bash
# 1. Preparação
cd C:\caminho\para\projeto
pip install streamlit-desktop-app

# 2. Empacotamento
streamlit-desktop-app build

# 3. Verificação
cd dist/NomeDoProjeto
dir
dir _internal

# 4. Correção de arquivos (se necessário)
copy "Extracao.py" _internal/
copy "Dados SAPIENS.xlsx" _internal/
copy "Fornecedores.xlsx" _internal/
xcopy Extracoes _internal/Extracoes/ /E /I /Y

# 5. Teste
NomeDoProjeto.exe
```

---

## 🚀 **RESULTADO FINAL**

Após seguir este guia, você terá:
- ✅ **Executável independente** (não precisa de Python)
- ✅ **Todas as funcionalidades** preservadas
- ✅ **Dados acessíveis** para o usuário
- ✅ **Portabilidade** entre PCs Windows
- ✅ **Fácil distribuição** e instalação

**O aplicativo estará pronto para distribuição!** 🎉

---

*Guia criado em: 08/10/2025*  
*Versão: 1.0*  
*Compatível com: Windows 10/11, Python 3.8+, Streamlit*
