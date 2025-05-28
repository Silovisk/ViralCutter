import os
import subprocess
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def check_nvenc_support():
    try:
        # First check if nvenc encoder is available
        result = subprocess.run(["ffmpeg", "-encoders"], capture_output=True, text=True)
        if "h264_nvenc" not in result.stdout:
            return False
        
        # Test if nvenc actually works by trying to use it
        test_result = subprocess.run([
            "ffmpeg", "-f", "lavfi", "-i", "testsrc=duration=1:size=320x240:rate=1", 
            "-c:v", "h264_nvenc", "-preset", "p1", "-f", "null", "-"
        ], capture_output=True, text=True, timeout=10)
        
        return test_result.returncode == 0
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return False

def burn():
    # Check NVENC support first
    if check_nvenc_support():
        print("NVENC suportado. Usando h264_nvenc para acelerar o processamento.")
        video_codec = "h264_nvenc"
        preset = "p1"
        encoding_params = ["-b:v", "5M"]
    else:
        print("NVENC não suportado ou não disponível. Usando libx264 como fallback.")
        video_codec = "libx264"
        preset = "ultrafast"
        encoding_params = ["-crf", "23"]

    # Caminhos das pastas
    subs_folder = 'subs_ass'
    videos_folder = 'final'
    output_folder = 'burned_sub'  # Pasta para salvar os vídeos com legendas

    # Cria a pasta de saída se não existir
    os.makedirs(output_folder, exist_ok=True)

    # Itera sobre os arquivos de vídeo na pasta final
    for video_file in os.listdir(videos_folder):
        if video_file.endswith(('.mp4', '.mkv', '.avi')):  # Formatos suportados
            # Extrai o nome base do vídeo (sem extensão)
            video_name = os.path.splitext(video_file)[0]

            # Define o caminho para a legenda correspondente
            subtitle_file = os.path.join(subs_folder, f"{video_name}.ass")
            print(f"Caminho da legenda: {subtitle_file}")

            # Verifica se a legenda existe
            if os.path.exists(subtitle_file):
                # Define o caminho de saída para o vídeo com legendas
                output_file = os.path.join(output_folder, f"{video_name}_subtitled.mp4")                # Ajuste no caminho da legenda para FFmpeg
                subtitle_file_ffmpeg = subtitle_file.replace('\\', '/')

                # Comando FFmpeg para adicionar as legendas
                command = [
                    'ffmpeg',
                    '-i', os.path.join(videos_folder, video_file),  # Vídeo de entrada
                    '-vf', f"subtitles='{subtitle_file_ffmpeg}'",  # Filtro de legendas com caminho corrigido
                    '-c:v', video_codec,  # Codificador (h264_nvenc ou libx264)
                    '-preset', preset,  # Preset (p1 para NVENC ou ultrafast para x264)
                ]
                
                # Adiciona parâmetros específicos do encoder
                command.extend(encoding_params)
                
                # Adiciona parâmetros de áudio e arquivo de saída
                command.extend([
                    '-c:a', 'copy',  # Copia o áudio
                    output_file
                ])

                # Log dos caminhos e do comando
                print(f"Processando vídeo: {video_file}")
                print(f"Caminho da legenda: {subtitle_file}")
                print(f"Caminho de saída: {output_file}")
                print(f"Comando: {' '.join(command)}")

                # Executa o comando
                try:
                    subprocess.run(command, check=True)
                    print(f"Processado: {output_file}")
                except subprocess.CalledProcessError as e:
                    print(f"Erro ao processar {video_name}: {e}")
            else:
                print(f"Legenda não encontrada para: {video_name}")

