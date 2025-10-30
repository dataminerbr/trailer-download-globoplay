import json, time, subprocess
from pathlib import Path
from InquirerPy import inquirer



#######CONFIG#######
F_PROFILE = 'PROFILE.default-release'            # Aqui vai o nome da pasta do profile firefox.
FOLDER = ''                                      # Vazio cria uma pasta downloads.
FORMATO = 'mp4'                                  # Formato original é MP4, se quser criar Metadados, mude para MKV.
LOGS = False
####################
INVERTER_EPS = False                             # Isto corrige a ordem invertida se necessário.
DELAY = 10                                       # Delay apra proteger o cookie
THREADS = 2                                      # Use 2 a 4. Se aumentar mais que '2', aumente o tempo de delay.
HLS_NATIVE = True                                # Istomuda o script para usar HLS do YT-DLP nativo e não o FFMPEG.
CHECK_SEGS = True                                # Só funciona com HLS Nativo, True só deixa remuxar se não faltar segmentos.
RESET_SEGS = False                               # Se ativada, quando um segmento falhar irá recomeçar o download do segmento zero.
RETRY_SEGS = 10                                  # Se o segmento falhar, tenta baixar ele novamente por 10x.
RETRY_VIDE = 5                                   # Se o video falhar, ele tenta novamente por 5x.
####################



# Caminho do JSON
json_path = Path("globoplay_trailers.json")

# Lê o arquivo
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Pasta de destino
output_dir = Path(FOLDER or "downloads")
output_dir.mkdir(parents=True, exist_ok=True)

# Série e episódios
serie_title = data.get("serie_title", "Sem título")
episodios = data.get("episodios", [])
if not episodios:
    print("❌ Nenhum episódio encontrado no JSON.")
    exit()

# Inverte números se ativado
if INVERTER_EPS:
    total_eps = len(episodios)
    for i, ep in enumerate(episodios):
        ep["numero"] = str(total_eps - i).zfill(3)

# --- Cria lista para o menu ---
choices = []

# Opção "Selecionar todos [N]"
quantidade = len(episodios)
selecionar_todos_texto = f"Selecionar todos [{quantidade}]" if quantidade else "Selecionar todos"
choices.append({"name": selecionar_todos_texto, "value": "ALL"})

# Adiciona os episódios
for ep in episodios:
    nome = f"{serie_title} - {ep.get('numero','???')} - {ep.get('titulo','Sem título')}"
    choices.append({"name": nome, "value": ep})

# --- Menu de seleção múltipla ---
selecionados = inquirer.checkbox(
    message=f"Selecione os episódios de '{serie_title}' para baixar:",
    choices=choices,
    instruction="(↑↓ navega, Espaço marca, Enter confirma, Ctrl+I inverte)"
).execute()

# --- Se marcou "Selecionar todos", substitui por todos os episódios ---
if "ALL" in selecionados:
    selecionados = episodios

if not selecionados:
    print("❌ Nenhum episódio selecionado. Encerrando.")
    exit()

print(f"\n🎬 Série: {serie_title}")
print(f"📦 Episódios selecionados: {len(selecionados)}\n")

# --- ⬇️ Baixa cada episódio selecionado ---
for ep in selecionados:
    numero = ep.get("numero", "sem_numero")
    titulo = ep.get("titulo", "sem_titulo").replace("/", "-").replace(" ", "_")
    url = ep.get("link")

    if not url:
        print(f"❌ Episódio {numero} sem link, pulando.")
        continue

    saida = str(output_dir / f"{serie_title} - {numero} - {titulo}.%(ext)s")
    print(f"⬇️ Baixando: {nome}")

    # Comando yt-dlp — baixa melhor vídeo e áudio
    cmd = [
        "yt-dlp",
        "--cookies-from-browser", f"firefox:{F_PROFILE}",
        "-S", "acodec:ec-3,acodec:aac,abr",
        "-f", "bv*+ba/b",
        "--merge-output-format", FORMATO,
        "--concurrent-fragments", str(THREADS),
        "--add-header", "Referer: https://globoplay.globo.com/",
        "--add-header", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "-o", saida,
        url,
    ]

    if HLS_NATIVE:
        cmd.append("--hls-prefer-native")

        # só faz sentido se for HLS nativo
        if CHECK_SEGS:
            cmd.append("--abort-on-unavailable-fragment")

    if RESET_SEGS:
        cmd.extend(["--no-continue", "--no-part"])

    # podem sempre ser usados juntos, ou isolados
    if RETRY_SEGS:
        cmd.extend(["--fragment-retries", str(RETRY_SEGS)])
    if RETRY_VIDE:
        cmd.extend(["--retries", str(RETRY_VIDE)])

    if LOGS is False:
        cmd.extend(["-q", "--no-warnings", "--progress"])

    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Episódio {nome} baixado com sucesso!\n")
        # Delay
        print(f"\033[33mAguardando {DELAY} Segundos\033[0m")
        time.sleep(DELAY)
    except subprocess.CalledProcessError as e:
        if LOGS is False:
            print(f"⚠️ Erro ao baixar: {nome}\n")
        else:
            print(f"⚠️ Erro ao baixar {nome}: {e}\n")
