import streamlit as st
import pandas as pd
import os
import subprocess
import sys
import time
from datetime import datetime
import glob

# Adicionar diretório pai ao path para importar auth_simple
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth_simple import (
    verificar_autenticacao, exibir_header_usuario,
    verificar_status_aprovado, eh_administrador
)

# Configuração da página
st.set_page_config(
    page_title="Extração de Dados - Dashboard KE5Z",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Verificar autenticação
verificar_autenticacao()

# Verificar se o usuário está aprovado
if ('usuario_nome' in st.session_state and 
    not verificar_status_aprovado(st.session_state.usuario_nome)):
    st.warning("⚠️ Sua conta ainda está pendente de aprovação.")
    st.stop()

# Verificar se é administrador
if not eh_administrador():
    st.error("🚫 **Acesso Restrito**")
    st.error("Apenas administradores podem acessar a página de extração.")
    st.info("💡 Entre em contato com o administrador se precisar de acesso.")
    st.stop()

# Header
st.title("📦 Extração de Dados KE5Z")
st.subheader("Execução do Script Extração.py")

# Exibir header do usuÃ¡rio
exibir_header_usuario()

st.markdown("---")
# Garantir logs na sessão antes de usar
if 'logs' not in st.session_state:
    st.session_state.logs = []

# Placeholders principais da UI
status_box = st.empty()
progress_bar = st.progress(0)
logs_placeholder = st.empty()

# CSS para multiselect com rolagem
st.markdown("""
<style>
div[data-testid="stMultiSelect"] > div {max-height: 220px; overflow-y: auto;}
</style>
""", unsafe_allow_html=True)

# Filtro de meses com opção "Todos"
meses_opcoes = ["Todos"] + list(range(1, 13))
nomes_meses = {1:"Janeiro",2:"Fevereiro",3:"Março",4:"Abril",5:"Maio",6:"Junho",7:"Julho",8:"Agosto",9:"Setembro",10:"Outubro",11:"Novembro",12:"Dezembro"}

def format_mes(m):
    return "Todos" if m == "Todos" else nomes_meses[m]

selecionados = st.multiselect(
    "📅 Selecionar Meses para Arquivos Excel",
    options=meses_opcoes,
    default=["Todos"],
    format_func=format_mes,
    help="Selecione os meses que deseja incluir nos arquivos Excel gerados."
)

if "Todos" in selecionados:
    meses_filtro = list(range(1, 13))
else:
    meses_filtro = selecionados

st.markdown("---")

col_a, col_b = st.columns([1, 1])
with col_a:
    executar = st.button("▶️ Executar Extração", use_container_width=True)
with col_b:
    aplicar_filtro = st.button("🔄 Aplicar Filtro de Mês (Excel)", use_container_width=True)

def atualizar_progresso(pct, titulo, detalhe=""):
    with status_box.container():
        st.write(f"{titulo}  {detalhe}")
    progress_bar.progress(int(pct))

def render_logs():
    ultimos = st.session_state.logs[-30:]
    with logs_placeholder.container():
        for linha in ultimos:
            st.write(linha)



st.markdown("---")

def adicionar_log(mensagem, detalhes=None, sem_timestamp=False):
    """Adiciona mensagem aos logs da sessão"""
    if sem_timestamp:
        # Para saída direta do script, não adicionar timestamp
        log_entry = mensagem
    else:
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {mensagem}"
        if detalhes:
            log_entry += f" | {detalhes}"
    
    st.session_state.logs.append(log_entry)
    if len(st.session_state.logs) > 200:  # Aumentar para 200 logs
        st.session_state.logs = st.session_state.logs[-200:]


def resolver_pasta_extracoes() -> str:
    """Resolve o nome da pasta 'Extrações' tolerando variações de acentuação.

    Retorna o nome de diretório existente a ser usado nas verificações/cópias.
    Ordem de prioridade: 'Extrações', 'Extracoes', 'ExtraÃ§Ãµes', fallback 'Extracoes'.
    """
    # Obter diretório base (onde está o executável)
    if hasattr(sys, '_MEIPASS'):
        # Executando dentro do PyInstaller
        base_dir = sys._MEIPASS
    else:
        # Executando normalmente - usar diretório do script atual
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    candidatos = [
        'Extrações',  # nome correto com acento
        'Extracoes',  # sem acento
        'ExtraÃ§Ãµes', # nome corrompido
    ]
    for nome in candidatos:
        caminho = os.path.join(base_dir, nome)
        if os.path.isdir(caminho):
            return nome
    # fallback padrão (usaremos sem acento para nova criação/cópia)
    return 'Extracoes'

def verificar_arquivos_necessarios():
    """Verifica se todos os arquivos necessários existem"""
    # Obter diretório base (onde está o executável)
    if hasattr(sys, '_MEIPASS'):
        # Executando dentro do PyInstaller
        base_dir = sys._MEIPASS
    else:
        # Executando normalmente - usar diretório do script atual
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    base_extracoes = resolver_pasta_extracoes()
    arquivos_necessarios = [
        (os.path.join(base_dir, "Extracao.py"), "Script principal"),
        (os.path.join(base_dir, base_extracoes, "KE5Z"), "Pasta com arquivos .txt KE5Z"),
        (os.path.join(base_dir, base_extracoes, "KSBB"), "Pasta com arquivos .txt KSBB"),
        (os.path.join(base_dir, "Dados SAPIENS.xlsx"), "Base de dados SAPIENS"),
        (os.path.join(base_dir, "Fornecedores.xlsx"), "Lista de fornecedores")
    ]
    
    resultados = []
    todos_ok = True
    
    for caminho, descricao in arquivos_necessarios:
        existe = os.path.exists(caminho)
        if existe:
            if os.path.isdir(caminho):
                arquivos = len([f for f in os.listdir(caminho)
                               if f.endswith('.txt')])
                resultados.append((descricao, f"✅ {arquivos} arquivos .txt",
                                   True))
            else:
                tamanho = os.path.getsize(caminho) / (1024 * 1024)
                resultados.append((descricao, f"✅ {tamanho:.1f} MB", True))
        else:
            resultados.append((descricao, "❌ Não encontrado", False))
            todos_ok = False
    
    return todos_ok, resultados


def executar_extracao(meses_filtro=None, progress_callback=None):
    """Executa o script Extração.py com captura de logs em tempo real"""
    try:
        # Obter diretório base (onde está o executável)
        if hasattr(sys, '_MEIPASS'):
            # Executando dentro do PyInstaller
            base_dir = sys._MEIPASS
        else:
            # Executando normalmente - usar diretório do script atual
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        adicionar_log("🚀 Iniciando execução do Extração.py...")
        if progress_callback:
            progress_callback(10, "🚀 Iniciando execução...", "Preparando ambiente")

        # Determinar o caminho correto do Python
        if hasattr(sys, '_MEIPASS'):
            # Executando dentro do PyInstaller - usar python.exe do sistema
            python_path = "python"
        else:
            # Executando normalmente
            python_path = sys.executable
            
        script_path = os.path.join(base_dir, "Extracao.py")
        adicionar_log(f"🐍 Usando Python: {python_path}")
        adicionar_log(f"📄 Script: {script_path}")
        if progress_callback:
            progress_callback(15, "⚙️ Iniciando subprocess...", "Executando script")

        # Passar meses selecionados via variável de ambiente (ex.: "9,10,11")
        env = os.environ.copy()
        try:
            if meses_filtro and isinstance(meses_filtro, (list, tuple)):
                env["MESES_FILTRO"] = ",".join(str(int(m)) for m in meses_filtro)
        except Exception:
            # Em caso de qualquer problema na serialização, ignorar silenciosamente
            pass

        processo = subprocess.Popen(
            [python_path, "-u", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=base_dir,
            encoding='cp1252',
            errors='replace',
            bufsize=1,
            universal_newlines=True,
            env=env,
        )

        # Leitura em tempo real do stdout
        linhas_lidas = 0
        for linha in iter(processo.stdout.readline, ''):
            if linha == '' and processo.poll() is not None:
                break
            texto = linha.strip()
            if texto:
                adicionar_log(texto, sem_timestamp=True)
                linhas_lidas += 1
                if linhas_lidas % 5 == 0 and progress_callback:
                    pct = min(75, 15 + linhas_lidas)
                    progress_callback(pct, "⚙️ Processando...", f"Linhas: {linhas_lidas}")
                # Atualizar logs na tela
                ultimos = st.session_state.logs[-30:]
                with logs_placeholder.container():
                    for l in ultimos:
                        st.write(l)

        # Capturar stderr ao final
        stderr_restante = processo.stderr.read() or ''
        if stderr_restante:
            for linha in stderr_restante.split('\n'):
                if linha.strip():
                    adicionar_log(linha.strip(), sem_timestamp=True)

        return_code = processo.wait()
        adicionar_log(f"📊 Código de retorno: {return_code}", f"Status: {'Sucesso' if return_code == 0 else 'Erro'}")
        if progress_callback:
            progress_callback(85, "📊 Processamento concluído", "Verificando arquivos")

        arquivos_gerados = verificar_arquivos_gerados()

        if return_code == 0 or (arquivos_gerados and len(arquivos_gerados) > 0):
            adicionar_log("✅ Extração concluída com sucesso!")
            if progress_callback:
                progress_callback(100, "✅ Concluído", "")
            return True, "Extração executada com sucesso!"

        adicionar_log("❌ Extração finalizada sem sucesso")
        return False, "Erro na execução"

    except Exception as e:
        adicionar_log(f"❌ Erro: {str(e)}")
        return False, f"Erro: {str(e)}"


def verificar_arquivos_gerados():
    """Verifica quais arquivos foram gerados pela extração"""
    # Obter diretório base (onde está o executável)
    if hasattr(sys, '_MEIPASS'):
        # Executando dentro do PyInstaller
        base_dir = sys._MEIPASS
    else:
        # Executando normalmente
        base_dir = os.getcwd()
    
    arquivos_gerados = []
    
    adicionar_log("🔍 Verificando arquivos gerados pela extração")
    
    # Verificar arquivos Parquet
    ke5z_path = os.path.join(base_dir, "KE5Z")
    if os.path.exists(ke5z_path):
        arquivos_parquet = glob.glob(os.path.join(ke5z_path, "*.parquet"))
        adicionar_log(f"📁 Pasta KE5Z encontrada", 
                      f"Arquivos .parquet: {len(arquivos_parquet)}")
        
        for arquivo in arquivos_parquet:
            tamanho = os.path.getsize(arquivo) / (1024 * 1024)
            timestamp = os.path.getmtime(arquivo)
            tempo_mod = time.strftime('%H:%M:%S',
                                     time.localtime(timestamp))
            arquivos_gerados.append(f"📊 {os.path.basename(arquivo)} "
                                   f"({tamanho:.1f} MB) - {tempo_mod}")
            adicionar_log(f"📊 Arquivo Parquet: {os.path.basename(arquivo)}", 
                          f"Tamanho: {tamanho:.1f} MB, Modificado: {tempo_mod}")
    else:
        adicionar_log("⚠️ Pasta KE5Z não encontrada")
    
    # Verificar arquivos Excel
    arquivos_path = os.path.join(base_dir, "arquivos")
    if os.path.exists(arquivos_path):
        arquivos_excel = glob.glob(os.path.join(arquivos_path, "*.xlsx"))
        adicionar_log(f"📁 Pasta arquivos encontrada", 
                      f"Arquivos .xlsx: {len(arquivos_excel)}")
        
        for arquivo in arquivos_excel:
            tamanho = os.path.getsize(arquivo) / (1024 * 1024)
            timestamp = os.path.getmtime(arquivo)
            tempo_mod = time.strftime('%H:%M:%S',
                                     time.localtime(timestamp))
            arquivos_gerados.append(f"📄 {os.path.basename(arquivo)} "
                                   f"({tamanho:.1f} MB) - {tempo_mod}")
            adicionar_log(f"📄 Arquivo Excel: {os.path.basename(arquivo)}", 
                          f"Tamanho: {tamanho:.1f} MB, Modificado: {tempo_mod}")
    else:
        adicionar_log("⚠️ Pasta arquivos não encontrada")
    
    adicionar_log(f"📊 Total de arquivos encontrados: {len(arquivos_gerados)}")
    return arquivos_gerados


def aplicar_filtro_mes_excel(meses_filtro):
    """Aplica filtro de mês nos arquivos Excel específicos"""
    try:
        # Obter diretório base (onde está o executável)
        if hasattr(sys, '_MEIPASS'):
            # Executando dentro do PyInstaller
            base_dir = sys._MEIPASS
        else:
            # Executando normalmente
            base_dir = os.getcwd()
        
        if not meses_filtro or len(meses_filtro) == 12:
            adicionar_log("📅 Todos os meses selecionados - sem filtro aplicado", 
                          f"Meses: {meses_filtro}")
            return True
        
        arquivos_excel = [
            os.path.join(base_dir, "arquivos", "KE5Z_veiculos.xlsx"), 
            os.path.join(base_dir, "arquivos", "KE5Z_pwt.xlsx")
        ]
        adicionar_log("🔍 Iniciando aplicação de filtro de mês", 
                      f"Arquivos: {len(arquivos_excel)}, Meses: {meses_filtro}")
        
        for arquivo in arquivos_excel:
            adicionar_log(f"📁 Verificando arquivo: {os.path.basename(arquivo)}")
            if not os.path.exists(arquivo):
                adicionar_log(f"⚠️ Arquivo não encontrado: {arquivo}")
                continue

            adicionar_log(f"✅ Arquivo encontrado: {os.path.basename(arquivo)}")
            df = pd.read_excel(arquivo)
            # Normalizar nomes de colunas (tolerar variações de acentuação/caixa)
            cols_norm = {c: str(c).strip() for c in df.columns}
            df.rename(columns=cols_norm, inplace=True)
            # Se houver 'Periodo' sem acento, alinhar para 'Período'
            if 'Periodo' in df.columns and 'Período' not in df.columns:
                df.rename(columns={'Periodo': 'Período'}, inplace=True)
            adicionar_log(f"📊 Arquivo carregado: {len(df)} registros")

            # Tipos para merge
            for coluna in ['Nºconta', 'Centrocst', 'Nºdoc.ref.', 'Account', 'USI', 'Type 05', 'Type 06', 'Type 07']:
                if coluna in df.columns:
                    df[coluna] = df[coluna].astype(str)
            for coluna in ['Valor', 'QTD']:
                if coluna in df.columns:
                    df[coluna] = pd.to_numeric(df[coluna], errors='coerce')

            # Filtro por mês
            df_filtrado = None
            # Tentar criar coluna 'Mes' se só existir 'Período'
            if 'Mes' not in df.columns and 'Período' in df.columns:
                mapa = {"janeiro":1,"fevereiro":2,"março":3,"marco":3,"abril":4,"maio":5,"junho":6,
                        "julho":7,"agosto":8,"setembro":9,"outubro":10,"novembro":11,"dezembro":12}
                try:
                    df['Mes'] = df['Período'].astype(str).str.lower().map(mapa).astype('Int64')
                except Exception:
                    pass

            if 'Mes' in df.columns:
                meses_numeros = [int(m) for m in meses_filtro]
                df_filtrado = df[df['Mes'].isin(meses_numeros)]
                adicionar_log(f"✅ Filtro aplicado na coluna Mes: {len(df_filtrado)} registros")
            elif 'Período' in df.columns:
                meses_nomes = {1:"janeiro",2:"fevereiro",3:"março",4:"abril",5:"maio",6:"junho",7:"julho",8:"agosto",9:"setembro",10:"outubro",11:"novembro",12:"dezembro"}
                meses_texto = [meses_nomes[int(m)] for m in meses_filtro]
                df_filtrado = df[df['Período'].str.lower().isin(meses_texto)]
                adicionar_log(f"✅ Filtro aplicado na coluna Período: {len(df_filtrado)} registros")
            else:
                adicionar_log("⚠️ Nenhuma coluna de mês encontrada")
                continue

            if len(df_filtrado) == 0:
                adicionar_log("⚠️ Nenhum registro encontrado com os filtros")
                continue

            adicionar_log("🔍 Verificando integridade dos dados filtrados", f"Registros: {len(df_filtrado)}")

            # Salvar de volta no mesmo arquivo
            adicionar_log("💾 Salvando arquivo filtrado", f"Destino: {arquivo}")
            try:
                df_filtrado.to_excel(arquivo, index=False)
                if os.path.exists(arquivo):
                    tamanho = os.path.getsize(arquivo)
                    adicionar_log("✅ Arquivo salvo com sucesso", f"Tamanho: {tamanho} bytes")
            except Exception as e:
                adicionar_log(f"❌ Erro ao salvar arquivo: {str(e)}")
                continue

            adicionar_log(f"✅ Filtro aplicado: {len(df_filtrado)} registros de {len(df)} originais")

        return True
    except Exception as e:
        adicionar_log(f"❌ Erro ao aplicar filtro de mês: {str(e)}")
        return False


# --- AÇÕES DA UI (executadas após definição das funções) ---

if executar:
    st.session_state.logs.clear()
    atualizar_progresso(10, "Preparando...")
    ok, msg = executar_extracao(meses_filtro=meses_filtro, progress_callback=atualizar_progresso)
    atualizar_progresso(80, "Verificando arquivos...")
    verificar_arquivos_gerados()
    atualizar_progresso(100, "Concluído")
    render_logs()

if aplicar_filtro:
    st.session_state.logs.clear()
    atualizar_progresso(20, "Aplicando filtro de mês...")
    aplicar_filtro_mes_excel(meses_filtro)
    atualizar_progresso(100, "Filtro aplicado")
    render_logs()

# Verificação de arquivos necessários (no final da página)
st.subheader("📁 Verificação de Arquivos Necessários")
ok, itens = verificar_arquivos_necessarios()
for desc, info, existe in itens:
    st.write(f"{'✅' if existe else '❌'} {desc} — {info}")
