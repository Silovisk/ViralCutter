#!/usr/bin/env python3
"""
Script para limpar todos os arquivos gerados e resetar o projeto para um novo teste
"""
import os
import shutil
import glob

def clean_project():
    """Remove todos os arquivos gerados durante o processamento"""
    
    # Diretórios para limpar completamente
    dirs_to_clean = [
        'tmp',
        'final', 
        'subs',
        'subs_ass',
        'burned_sub'
    ]
    
    print("🧹 Iniciando limpeza do projeto...")
    
    # Limpar diretórios
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"  📁 Limpando diretório: {dir_name}/")
            
            # Remover todos os arquivos do diretório
            for filename in os.listdir(dir_name):
                file_path = os.path.join(dir_name, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"    ❌ Removido: {file_path}")
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        print(f"    📂 Removido diretório: {file_path}")
                except Exception as e:
                    print(f"    ⚠️  Erro ao remover {file_path}: {e}")
        else:
            print(f"  ✅ Diretório {dir_name}/ não existe")
    
    
    # Recriar diretórios vazios necessários
    print("  📁 Recriando diretórios necessários...")
    for dir_name in dirs_to_clean:
        os.makedirs(dir_name, exist_ok=True)
        print(f"    ✅ Criado: {dir_name}/")
    
    print("\n🎉 Limpeza concluída! O projeto está pronto para um novo teste.")
    print("\n📋 Próximos passos:")
    print("1. Execute o main.py ou o notebook")
    print("2. Forneça uma nova URL do YouTube")
    print("3. Configure as opções desejadas")

if __name__ == "__main__":
    clean_project()
