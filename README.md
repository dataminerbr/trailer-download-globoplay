# trailer-download-globoplay
Projeto para baixar trailers do site globoplay.
<hr>

Para o uso é necessario ter o aplicativo 'yt-dlp' na pasta do projeto ou no PATH do sistema.
<pre>https://github.com/yt-dlp/yt-dlp</pre>
<hr>
Também é necessário criar um arquivo de cookies no formato Netscape. O arquivo deve estar em:
<pre>cookies/default.txt</pre>
Para obter os cookies do Globoplay, você pode usar extensões do navegador como "Get cookies.txt LOCALLY" ou "cookies.txt" que exportam cookies no formato Netscape. Basta logar no Globoplay e exportar os cookies para o arquivo <code>cookies/default.txt</code>.
<hr>
E se quiser pegar os conteudos do '.JSON' que contém dados do Trailer, você precisará de Tampermonkey no seu navegador.
<hr>
Eu não me responsabilizo pelo uso errado!!!

<hr>
Montagem:

<pre>trailer-download-globoplay/
├── main.py
├── globoplay_trailers.json
├── cookies/
│   └── default.txt (arquivo de cookies no formato Netscape)
├── yt-dlp.exe (opcional / pode usar do PATH)
└── requirements.txt</pre>

<hr>
Configuração:

<pre>#######CONFIG#######
COOKIES_FILE = 'cookies/default.txt'            # Arquivo de cookies no formato Netscape.
P_FOLDER = ''                                    # Vazio cria uma pasta downloads.
S_FOLDER = True                                  # Se ativado, cria uma subpasta com o nome da serie.
####################
INVERTER_EPS = False                             # Isto corrige a ordem invertida se necessário.
HLS_NATIVE = True                                # Istomuda o script para usar HLS do YT-DLP nativo e não o FFMPEG. ISto serve para usar o Checar segmentos, e mantem o formato do video origianl da plataforma, não o remuxa.
CHECK_SEGS = True                                # Só funciona com HLS Nativo, True só deixa remuxar se não faltar segmentos.
RESET_SEGS = False                               # Se ativada, quando um segmento falhar irá recomeçar o download do segmento zero.
FORMATO = 'mp4'                                  # Formato original é MP4, se quser criar Metadados, mude para MKV. Só funciona com "HLS_NATIVE = False" (no caso, não irá checar os segmentos)
RETRY_SEGS = 10                                  # Se o segmento falhar, tenta baixar ele novamente por 10x.
RETRY_VIDE = 5                                   # Se o video falhar, ele tenta novamente por 5x.
DELAY = 10                                       # Delay apra proteger o cookie
THREADS = 2                                      # Use 2 a 4. Se aumentar mais que '2', aumente o tempo de delay.
LOGS = False                                     # Imprime LOGS durante o Download.
####################</pre>
