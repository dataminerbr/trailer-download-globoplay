# trailer-download-globoplay
Projeto para baixar trailers do site globoplay.
<hr>

Para o uso é necessario ter o aplicativo 'yt-dlp' na pasta do projeto ou no 'system32'.
<pre>https://github.com/yt-dlp/yt-dlp</pre>
<hr>
Também é nescessário logar com sua conta globoplay no navegador firefox e obter o seu profile, que é o nome de uma das pastas dentro de:
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
├── yt-dlp.exe (opcional / pode usar do system32)
└── requirements.txt</pre>

<hr>
Configuração:

<pre>#######CONFIG#######
FORMATO = 'mp4'                               # Formato original é MP4, se quser criar Metadados, mude para MKV.
FOLDER = ''                                   # Vazio cria uma pasta downloads.
F_PROFILE = 'PROFILE.default-release'         # Aqui vai o nome da pasta do profile firefox.
INVERTER_EPS = False                          # Isto corrige a ordem invertida se necessário.
DELAY = 10                                    # Delay apra proteger o cookie
THREADS = 2                                   # Use 2 a 4. Se aumentar mais que '2', aumente o tempo de delay.
####################</pre>
