import os
import yt_dlp

def download(url):
    output_path = 'tmp/input_video.mp4'
    
    # Configurações base do yt-dlp
    base_opts = {
        'format': 'bestvideo+bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat':'mp4'
        }],
        'outtmpl': output_path,
        'postprocessor_args': [
            '-movflags', 'faststart'
        ],
        'merge_output_format':'mp4',
        'noplaylist': True,  # Baixa apenas o vídeo, não a playlist
    }
      # Lista de configurações de cookies para tentar (em ordem de preferência)
    cookie_configs = [
        # Tenta Firefox do Windows (WSL)
        {'cookiesfrombrowser': ('firefox',)},
        # Tenta Chrome do Windows (WSL)
        {'cookiesfrombrowser': ('chrome',)},
        # Tenta Edge do Windows (WSL)
        {'cookiesfrombrowser': ('edge',)},
        # Tenta arquivo cookies.txt se existir
        {'cookies': 'cookies.txt'} if os.path.exists('cookies.txt') else {},
        # Sem cookies (último recurso)
        {}
    ]
    for i, cookie_config in enumerate(cookie_configs):
        # Combina configurações base com configuração de cookies
        ydl_opts = {**base_opts, **cookie_config}
        
        browser_name = cookie_config.get('cookiesfrombrowser', ['sem cookies'])[0] if 'cookiesfrombrowser' in cookie_config else 'sem cookies'
        print(f"Tentando usar cookies do {browser_name}...")
        
        while True:
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                print(f"✅ Download realizado com sucesso usando {browser_name}!")
                return output_path
                
            except yt_dlp.utils.DownloadError as e:
                error_msg = str(e)
                
                if "is not a valid URL" in error_msg:
                    print("Erro: o link inserido não é válido.")
                    url = input("\nPor favor, insira um link válido: ")
                    continue
                    
                elif "Sign in to confirm you're not a bot" in error_msg or "cookies" in error_msg.lower():
                    print(f"❌ Falha ao usar cookies do {browser_name}")
                    break  # Tenta próxima configuração
                    
                elif "could not find" in error_msg and "cookies database" in error_msg:
                    print(f"❌ Cookies do {browser_name} não encontrados")
                    break  # Tenta próxima configuração
                    
                else:
                    print(f"Erro inesperado: {error_msg}")
                    break  # Tenta próxima configuração
                    
            except Exception as e:
                print(f"❌ Erro com {browser_name}: {str(e)}")
                break  # Tenta próxima configuração
    
    # Se chegou aqui, nenhuma configuração funcionou
    print("\n⚠️  Nenhuma configuração de cookies funcionou!")
    print("Soluções manuais:")
    print("1. Abra uma aba privada/incógnito no Firefox")
    print("2. Faça login no YouTube")
    print("3. Navegue para https://www.youtube.com/robots.txt")
    print("4. Use uma extensão como 'cookies.txt' para exportar os cookies")
    print("5. Salve o arquivo como 'cookies.txt' na pasta do ViralCutter")
    print("6. Execute novamente o programa")
    
    raise Exception("Não foi possível baixar o vídeo. Autenticação necessária.")