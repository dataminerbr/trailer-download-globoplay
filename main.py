import json, time, subprocess
from pathlib import Path
from InquirerPy import inquirer



#######CONFIG#######
FORMATO = 'mp4'                               # Formato original é MP4, se quser criar Metadados, mude para MKV.
FOLDER = ''                                   # Vazio cria uma pasta downloads.
F_PROFILE = 'PROFILE.default-release'         # Aqui vai o nome da pasta do profile firefox.
INVERTER_EPS = False                          # Isto corrige a ordem invertida se necessário.
DELAY = 10                                    # Delay apra proteger o cookie
THREADS = 2                                   # Use 2 a 4. Se aumentar mais que '2', aumente o tempo de delay.
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
    print(f"⬇️ Baixando: {saida.replace('.%(ext)s', f'.{FORMATO}')}")

    # Comando yt-dlp — baixa melhor vídeo e áudio
    cmd = [
        "yt-dlp",
        "--cookies-from-browser", f"firefox:{F_PROFILE}",
        "-S", "acodec:ec-3,acodec:aac,abr",
        "-f", "bv*+ba/b",
        "--merge-output-format", FORMATO,
        "--concurrent-fragments", str(THREADS),
        #"--download-sections", "*00:00:05-01:10:00",
        "-o", saida,
        url,
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Episódio {saida.replace('.%(ext)s', f'.{FORMATO}')} baixado com sucesso!\n")
        # Renomear
        subprocess.run(["powershell", "-File", "Renomear.ps1", saida])
        # Delay
        print(f"\033[33mAguardando {DELAY} Segundos\033[0m")
        time.sleep(DELAY)
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Erro ao baixar {saida.replace('.%(ext)s', f'.{FORMATO}')}: {e}\n")
