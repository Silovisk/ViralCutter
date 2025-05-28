import os
import subprocess

def convert_srt_to_ass():
    """Converte arquivos SRT para ASS"""
    
    subs_dir = "subs"
    subs_ass_dir = "subs_ass"
    
    os.makedirs(subs_ass_dir, exist_ok=True)
    
    # Listar arquivos SRT
    srt_files = [f for f in os.listdir(subs_dir) if f.endswith('.srt')]
    
    if not srt_files:
        print("❌ Nenhum arquivo SRT encontrado!")
        return False
    
    print(f"🔄 Convertendo {len(srt_files)} arquivos SRT para ASS...")
    
    for srt_file in srt_files:
        srt_path = os.path.join(subs_dir, srt_file)
        ass_file = srt_file.replace('.srt', '.ass')
        ass_path = os.path.join(subs_ass_dir, ass_file)
        
        # Converter usando ffmpeg
        cmd = [
            'ffmpeg', '-y',
            '-i', srt_path,
            ass_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Convertido: {ass_file}")
            else:
                print(f"❌ Erro ao converter {srt_file}: {result.stderr}")
        except Exception as e:
            print(f"❌ Erro ao converter {srt_file}: {e}")
    
    return True

def burn_subtitles():
    """Queima legendas nos vídeos"""
    
    final_dir = "final"
    subs_ass_dir = "subs_ass"
    burned_dir = "burned_sub"
    
    os.makedirs(burned_dir, exist_ok=True)
    
    # Listar vídeos
    video_files = [f for f in os.listdir(final_dir) if f.endswith('.mp4')]
    
    for video_file in video_files:
        video_path = os.path.join(final_dir, video_file)
        
        # Procurar legenda correspondente
        video_name = os.path.splitext(video_file)[0]
        ass_file = f"{video_name}.ass"
        ass_path = os.path.join(subs_ass_dir, ass_file)
        
        if not os.path.exists(ass_path):
            print(f"❌ Legenda não encontrada para: {video_name}")
            continue
        
        # Arquivo de saída
        output_file = f"burned_{video_file}"
        output_path = os.path.join(burned_dir, output_file)
        
        print(f"🔥 Queimando legenda em: {video_file}")
        
        # Comando para queimar legenda
        cmd = [
            'ffmpeg', '-y',
            '-i', video_path,
            '-vf', f"ass={ass_path}",
            '-c:a', 'copy',
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            output_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Legenda queimada: {output_file}")
            else:
                print(f"❌ Erro ao queimar legenda: {result.stderr}")
        except Exception as e:
            print(f"❌ Erro ao queimar legenda: {e}")

def main():
    print("🔄 Iniciando processo completo de legendas...")
    
    # 1. Converter SRT para ASS
    if convert_srt_to_ass():
        print("\n✅ Conversão SRT->ASS concluída!")
        
        # 2. Queimar legendas
        print("\n🔥 Iniciando queima de legendas...")
        burn_subtitles()
        
        print("\n🎉 Processo completo de legendas finalizado!")
        print("Verifique a pasta 'burned_sub/' para os vídeos com legendas!")
    else:
        print("❌ Falha na conversão para ASS")

if __name__ == "__main__":
    main()