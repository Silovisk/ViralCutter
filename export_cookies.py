#!/usr/bin/env python3
"""
Script para exportar cookies do YouTube usando yt-dlp.
Execute este script para criar um arquivo cookies.txt que pode ser usado pelo ViralCutter.
"""

import yt_dlp
import os
import sys

def export_cookies():
    print("🍪 Exportador de Cookies do YouTube para ViralCutter (WSL + Firefox)")
    print("=" * 60)
    
    # Verifica se o Firefox está instalado no WSL
    try:
        os.system("which firefox > /dev/null 2>&1")
        print("✅ Firefox encontrado no WSL")
    except:
        print("❌ Firefox não encontrado. Instale com: sudo apt update && sudo apt install firefox")
        return False
    
    # Configuração específica para Firefox no WSL
    browser_configs = [
        ('firefox', None),  # Firefox local do WSL
    ]
    
    for browser, profile_path in browser_configs:
        try:
            print(f"\nTentando exportar cookies do {browser}...")
            
            ydl_opts = {
                'simulate': True,  # Não baixa, apenas exporta cookies
                'writeinfojson': False,
                'quiet': True,
            }
            
            # Adiciona configuração de cookies baseada no navegador
            if profile_path:
                ydl_opts['cookiesfrombrowser'] = (browser, profile_path)
            else:
                ydl_opts['cookiesfrombrowser'] = (browser,)
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Usa uma URL simples do YouTube que sempre existe
                test_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'  # Never Gonna Give You Up
                info = ydl.extract_info(test_url, download=False)
                
                # Se chegou aqui, os cookies funcionaram
                # Agora exporta os cookies para arquivo
                cookie_ydl_opts = {
                    'cookiesfrombrowser': ydl_opts['cookiesfrombrowser'],
                    'cookies': 'cookies.txt',
                    'simulate': True,
                }
                
                with yt_dlp.YoutubeDL(cookie_ydl_opts) as cookie_ydl:
                    cookie_ydl.extract_info(test_url, download=False)
            
            if os.path.exists('cookies.txt'):
                print(f"✅ Cookies exportados com sucesso do {browser}!")
                print(f"📁 Arquivo salvo como: cookies.txt")
                print("\nAgora você pode executar o ViralCutter normalmente.")
                return True
                
        except Exception as e:
            error_msg = str(e)
            if "could not find" in error_msg and "cookies database" in error_msg:
                print(f"❌ Base de dados de cookies do {browser} não encontrada")
            elif "Extracted 0 cookies" in error_msg:
                print(f"❌ Nenhum cookie encontrado no {browser} (faça login no YouTube primeiro)")
            else:
                print(f"❌ Erro ao exportar do {browser}: {error_msg[:100]}...")
            continue
    
    print("\n⚠️  Não foi possível exportar cookies automaticamente.")
    print("\n🔧 SOLUÇÃO PARA WSL + FIREFOX:")
    print("1. Abra o Firefox no WSL executando:")
    print("   firefox &")
    print("2. No Firefox, vá para https://www.youtube.com")
    print("3. Faça LOGIN com sua conta do Google/YouTube")
    print("4. Feche o Firefox")
    print("5. Execute este script novamente")
    
    print("\n📝 MÉTODO ALTERNATIVO - Exportar manualmente:")
    print("Execute este comando no terminal (ambiente virtual ativado):")
    print("yt-dlp --cookies-from-browser firefox --cookies cookies.txt --simulate 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'")
    
    return False

def login_firefox_guide():
    print("\n" + "="*60)
    print("🦊 GUIA DE LOGIN NO FIREFOX DO WSL")
    print("="*60)
    print("\n1️⃣ ABRIR FIREFOX NO WSL:")
    print("   firefox &")
    print("   (O & executa em background, você pode continuar usando o terminal)")
    
    print("\n2️⃣ FAZER LOGIN NO YOUTUBE:")
    print("   - Vá para: https://www.youtube.com")
    print("   - Clique em 'Sign in' (Fazer login)")
    print("   - Digite seu email e senha do Google")
    print("   - Complete qualquer verificação em duas etapas se necessário")
    
    print("\n3️⃣ VERIFICAR SE ESTÁ LOGADO:")
    print("   - Você deve ver sua foto de perfil no canto superior direito")
    print("   - Teste assistir um vídeo para confirmar")
    
    print("\n4️⃣ FECHAR FIREFOX E TENTAR NOVAMENTE:")
    print("   - Feche o Firefox")
    print("   - Execute: python export_cookies.py")
    
    print("\n⚠️  IMPORTANTE:")
    print("   - Mantenha o Firefox fechado após o login")
    print("   - Os cookies são salvos automaticamente no perfil do Firefox")
    print("   - Se ainda não funcionar, use o método manual com yt-dlp")

def manual_export_guide():
    print("\n" + "="*60)
    print("📋 GUIA COMPLETO PARA EXPORTAR COOKIES MANUALMENTE")
    print("="*60)
    print("\n1️⃣ MÉTODO 1: Usar extensão do navegador")
    print("   Firefox: Instale 'cookies.txt' extension")
    print("   Chrome: Instale 'Get cookies.txt LOCALLY' extension")
    print("   - Faça login no YouTube")
    print("   - Use a extensão para exportar cookies do youtube.com")
    print("   - Salve como 'cookies.txt' nesta pasta")
    
    print("\n2️⃣ MÉTODO 2: Exportar via linha de comando")
    print("   Execute no terminal (ambiente virtual ativado):")
    print("   yt-dlp --cookies-from-browser firefox --cookies cookies.txt --simulate 'https://www.youtube.com/'")
    
    print("\n3️⃣ MÉTODO 3: Método da aba privada (mais confiável)")
    print("   - Abra uma aba privada/incógnito no Firefox")
    print("   - Faça login no YouTube")
    print("   - Navegue para https://www.youtube.com/")
    print("   - Instale extensão cookies.txt")
    print("   - Exporte cookies do youtube.com")
    print("   - Feche a aba privada imediatamente")
    
    print("\n4️⃣ VERIFICAR SE FUNCIONOU:")
    print("   - Deve aparecer um arquivo 'cookies.txt' nesta pasta")
    print("   - Execute o ViralCutter normalmente")

if __name__ == "__main__":
    success = export_cookies()
    if not success:
        login_firefox_guide()
