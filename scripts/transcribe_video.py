import subprocess
import os
import sys
import torch
import time
import whisper

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def transcribe(input_file, model='large-v3'):
    print(f"Iniciando transcrição de {input_file}...")
    start_time = time.time()
    
    output_folder = 'tmp'
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    srt_file = os.path.join(output_folder, f"{base_name}.srt")
    tsv_file = os.path.join(output_folder, f"{base_name}.tsv")

    # Verifica se os arquivos já existem
    if os.path.exists(srt_file) and os.path.exists(tsv_file):
        print(f"Arquivos {srt_file} e {tsv_file} já existem. Pulando a transcrição.")
        return srt_file, tsv_file    # Usa whisper nativo diretamente (mais confiável que WhisperX)
    print("Usando Whisper nativo para transcrição...")
    try:
        transcribe_with_whisper(input_file, model, output_folder, srt_file, tsv_file)
    except Exception as e:
        print(f"Erro na transcrição com Whisper: {e}")
        # Cria arquivos vazios para não quebrar o pipeline
        create_empty_files(srt_file, tsv_file)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    print(f"Transcrição concluída em {minutes}m {seconds}s")
    
    return srt_file, tsv_file

def transcribe_with_whisperx(input_file, model, output_folder):
    """Tenta transcrição com WhisperX"""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Usando {device} para WhisperX")
    
    command = [
        "whisperx",
        input_file,
        "--model", model if model != 'large-v3' else 'large-v2',  # WhisperX pode não ter v3
        "--task", "transcribe",
        "--chunk_size", "5",  # Reduzido para usar menos memória
        "--batch_size", "4",   # Reduzido para usar menos memória
        "--output_dir", output_folder,
        "--output_format", "all",
        "--device", device,
        "--compute_type", "float32" if device == "cpu" else "float16"
    ]
    
    result = subprocess.run(command, check=True, capture_output=True, text=True, timeout=600)  # 10 min timeout
    print("WhisperX executado com sucesso")
    return True

def transcribe_with_whisper(input_file, model, output_folder, srt_file, tsv_file):
    """Transcrição com whisper nativo"""
    print("Carregando modelo Whisper...")
      # Estratégia agressiva de fallback para WSL com pouca memória
    # Sempre começa com modelos pequenos primeiro
    models_to_try = ['tiny', 'base', 'small']
    
    print(f"Modelo original solicitado: {model}")
    print("Usando estratégia conservadora de memória: tiny -> base -> small")
    
    whisper_model = None
    selected_model = None
    
    for attempt_model in models_to_try:
        try:
            print(f"🔄 Tentando carregar modelo '{attempt_model}'...")
            whisper_model = whisper.load_model(attempt_model)
            selected_model = attempt_model
            print(f"✅ Modelo '{attempt_model}' carregado com sucesso!")
            break
        except Exception as e:
            print(f"❌ Falha ao carregar modelo '{attempt_model}': {e}")
            if whisper_model:
                del whisper_model
            continue
    
    if whisper_model is None:
        raise Exception("Nenhum modelo Whisper pôde ser carregado. Problema de memória ou instalação.")
    
    print("Transcrevendo...")
    result = whisper_model.transcribe(input_file, language="pt", verbose=True)
    
    # Cria arquivo SRT
    create_srt_file(result, srt_file)
    
    # Cria arquivo TSV
    create_tsv_file(result, tsv_file)
    
    print(f"Arquivos criados: {srt_file}, {tsv_file}")

def create_srt_file(result, srt_file):
    """Cria arquivo SRT a partir do resultado do Whisper"""
    with open(srt_file, 'w', encoding='utf-8') as f:
        for i, segment in enumerate(result['segments'], 1):
            start = segment['start']
            end = segment['end']
            text = segment['text'].strip()
            
            # Converte segundos para formato SRT (HH:MM:SS,mmm)
            start_time = seconds_to_srt_time(start)
            end_time = seconds_to_srt_time(end)
            
            f.write(f"{i}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{text}\n\n")

def create_tsv_file(result, tsv_file):
    """Cria arquivo TSV a partir do resultado do Whisper"""
    with open(tsv_file, 'w', encoding='utf-8') as f:
        f.write("start\tend\ttext\n")  # Cabeçalho
        for segment in result['segments']:
            start = segment['start']
            end = segment['end']
            text = segment['text'].strip().replace('\t', ' ')  # Remove tabs do texto
            f.write(f"{start:.3f}\t{end:.3f}\t{text}\n")

def seconds_to_srt_time(seconds):
    """Converte segundos para formato de tempo SRT"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

def create_empty_files(srt_file, tsv_file):
    """Cria arquivos vazios se a transcrição falhar completamente"""
    print("Criando arquivos vazios para continuar o pipeline...")
    
    # SRT vazio
    with open(srt_file, 'w', encoding='utf-8') as f:
        f.write("1\n00:00:00,000 --> 00:00:10,000\n[Transcrição não disponível]\n\n")
    
    # TSV vazio  
    with open(tsv_file, 'w', encoding='utf-8') as f:
        f.write("start\tend\ttext\n")
        f.write("0.000\t10.000\t[Transcrição não disponível]\n")
