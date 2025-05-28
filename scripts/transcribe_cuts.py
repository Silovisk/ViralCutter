import os
import subprocess
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def transcribe():
    def generate_whisperx(input_file, output_folder, model='small'):
        output_file = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(input_file))[0]}.srt")
        json_file = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(input_file))[0]}.json")

        # Skip processing if the JSON file already exists
        if os.path.exists(json_file):
            print(f"Arquivo já existe, pulando: {json_file}")
            return

        command = [
            "./venv/bin/whisperx",
            input_file,
            "--model", model,
            "--task", "transcribe",
            "--compute_type", "float32",
            "--batch_size", "4",
            "--output_dir", output_folder,
            "--output_format", "srt",
            "--output_format", "json",
        ]

        print(f"Transcrevendo: {input_file}...")
        print(f"Comando a ser executado: {' '.join(command)}")
        
        try:
            result = subprocess.run(command, text=True, capture_output=True, check=False)
            
            if result.returncode != 0:
                print("Erro durante a transcrição:")
                print(f"Código de saída: {result.returncode}")
                print(f"Stderr: {result.stderr}")
                print(f"Stdout: {result.stdout}")
            else:
                print(f"Transcrição concluída. Arquivo salvo em: {output_file} e {json_file}")
                if result.stdout:
                    print(f"Stdout: {result.stdout}")
        except Exception as e:
            print(f"Erro ao executar comando: {e}")

    # Define o diretório de entrada e o diretório de saída
    input_folder = 'final/'
    output_folder = 'subs/'

    # Cria o diretório de saída se não existir
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Itera sobre todos os arquivos na pasta de entrada
    for filename in os.listdir(input_folder):
        if filename.endswith('.mp4'):  # Filtra apenas arquivos .mp4
            input_file = os.path.join(input_folder, filename)
            generate_whisperx(input_file, output_folder)

if __name__ == "__main__":
    transcribe()

