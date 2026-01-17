# trailer-download-globoplay
Projeto para baixar trailers do site globoplay.
<hr>

Para o uso é necessario ter o aplicativo 'yt-dlp' na pasta do projeto ou no sistema.
<pre>https://github.com/yt-dlp/yt-dlp</pre>
<hr>
Também é nescessário obter um arquivo de cookies.txt no formato Netscape, ou mais facil, logar com sua conta globoplay no navegador e obter o nome seu profile, que é o nome de uma das pastas dentro de:
<pre>%USERPROFILE%\AppData\Roaming\Mozilla\Firefox\Profiles</pre>
<hr>
E se quiser pegar os conteudos do '.JSON' que contém dados do Trailer, você precisará de Tampermonkey no seu navegador.
<hr>
Eu não me responsabilizo pelo uso errado!!!

<hr>
Montagem:

<pre>trailer-download-globoplay/
├── main.py
├── globoplay_trailers.json
├── yt-dlp.exe (opcional / pode usar do sistema)
├── requirements.txt
└── cookis.txt (opcional)</pre>

<hr>
Configuração:

<pre>#######LOGIN#######
C_PROFILE = 'cookies.txt'                        # Aqui vai o profile do navegador com o cookie (EXs: "firefox:xxxxxxxxxx", "chrome:xxxxxxxxxx"), ou um arquvo de cookies em .txt no formato Netscape.
#######CONFIG#######
P_FOLDER = ''                                    # Vazio cria uma pasta downloads.
S_FOLDER = True                                  # Se ativado, cria uma subpasta com o nome da serie.
####################
INVERTER_EPS = False                             # Isto corrige a ordem invertida se necessário.
HLS_NATIVE = True                                # Isto muda o script para usar HLS do YT-DLP nativo e não o FFMPEG. Isto serve para usar o Checar segmentos, e mantem o formato do video origianl da plataforma, não o remuxa. (OBS: Se isto for alterado, o script não checará mais os segmentos!)
CHECK_SEGS = True                                # Só funciona com HLS Nativo, True só deixa remuxar se não faltar segmentos.
RESET_SEGS = False                               # Se ativada, quando um segmento falhar irá recomeçar o download do segmento zero.
FORMATO = 'mp4'                                  # Formato original é MP4, se quser criar Metadados, mude para MKV. Só funciona com "HLS_NATIVE = False" (no caso, não irá checar os segmentos)
RETRY_SEGS = 10                                  # Se o segmento falhar, tenta baixar ele novamente por 10x.
RETRY_VIDE = 5                                   # Se o video falhar, ele tenta novamente por 5x.
DELAY = 10                                       # Delay apra proteger o cookie. (OBS: Não diminua se nao quiser ser bloqueado.)
THREADS = 2                                      # Use 2 a 4. Se aumentar mais que '2', aumente o tempo de delay. (OBS: Não aumente mais sem aumentar o DELAY, nao aumente mais que 4 se nao quiser ser bloqueado.)
LOGS = False                                     # Imprime LOGS durante o Download.
####################</pre>
