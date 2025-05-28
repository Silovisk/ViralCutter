import os
import subprocess
import json
import whisper

def transcribe_with_native_whisper(video_path, output_dir):
    """Usa Whisper nativo ao invés de WhisperX para segmentos"""
    
    print(f"🔄 Transcrevendo {video_path} com Whisper nativo...")
    
    try:
        # Carregar modelo Whisper nativo (mais estável)
        model = whisper.load_model("base")
        
        # Transcrever
        result = model.transcribe(video_path)
        
        # Criar arquivo SRT
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        srt_path = os.path.join(output_dir, f"{video_name}.srt")
        json_path = os.path.join(output_dir, f"{video_name}.json")
        
        # Gerar SRT
        with open(srt_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(result['segments']):
                start = segment['start']
                end = segment['end']
                text = segment['text'].strip()
                
                # Converter para formato SRT
                start_time = format_time(start)
                end_time = format_time(end)
                
                f.write(f"{i+1}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")
        
        # Gerar JSON
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Transcrição salva: {srt_path}")
        return True
        
    except Exception as e:
        print(f"❌ Erro na transcrição: {e}")
        return False

def format_time(seconds):
    """Converte segundos para formato SRT (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def fix_transcriptions():
    """Corrige as transcrições que falharam"""
    
    final_dir = "final"
    subs_dir = "subs"
    
    # Criar pasta de legendas se não existir
    os.makedirs(subs_dir, exist_ok=True)
    
    # Listar vídeos finais
    if not os.path.exists(final_dir):
        print(f"❌ Pasta {final_dir} não encontrada!")
        return False
    
    video_files = [f for f in os.listdir(final_dir) if f.endswith('.mp4')]
    
    if not video_files:
        print("❌ Nenhum vídeo encontrado!")
        return False
    
    print(f"📹 Encontrados {len(video_files)} vídeos para transcrever")
    
    success_count = 0
    
    for video_file in video_files:
        video_path = os.path.join(final_dir, video_file)
        print(f"\n🔄 Processando: {video_file}")
        
        if transcribe_with_native_whisper(video_path, subs_dir):
            success_count += 1
        else:
            print(f"❌ Falha na transcrição de {video_file}")
    
    print(f"\n✅ Transcrições concluídas: {success_count}/{len(video_files)}")
    return success_count > 0

if __name__ == "__main__":
    fix_transcriptions()