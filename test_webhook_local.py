"""
Script para testar webhook localmente com mensagens simuladas.
Simula mensagens do WhatsApp para testar o fluxo completo.
"""
import requests
import json

WEBHOOK_URL = "http://localhost:5001/webhook/whatsapp"
PHONE = "554191851256"  # Estevao Antunes

def send_test_message(text: str):
    """Simula mensagem do Evolution API."""
    payload = {
        "event": "messages.upsert",
        "data": {
            "key": {
                "remoteJid": f"{PHONE}@s.whatsapp.net",
                "fromMe": False,
                "id": "test123"
            },
            "message": {
                "conversation": text
            }
        }
    }

    print(f"\n📱 Enviando: '{text}'")
    print("─" * 50)

    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=30)
        print(f"✅ Status: {response.status_code}")
        print(f"📦 Resposta: {response.json()}")
    except Exception as e:
        print(f"❌ Erro: {e}")


def test_regex_commands():
    """Testa comandos que o regex deve capturar (rápido)."""
    print("\n" + "="*50)
    print("🧪 TESTANDO COMANDOS REGEX (rápido)")
    print("="*50)

    send_test_message("minhas tarefas")
    send_test_message("feito 2")
    send_test_message("andamento 1")
    send_test_message("progresso")
    send_test_message("ajuda")


def test_llm_fallback():
    """Testa comandos que precisam do LLM (linguagem natural)."""
    print("\n" + "="*50)
    print("🤖 TESTANDO LLM FALLBACK (linguagem natural)")
    print("="*50)

    send_test_message("o que tenho pra hoje?")
    send_test_message("terminei a primeira")
    send_test_message("tô fazendo a 3")
    send_test_message("como tá meu dia?")
    send_test_message("quais são meus comandos?")


def test_unknown_commands():
    """Testa comandos que nem regex nem LLM devem reconhecer."""
    print("\n" + "="*50)
    print("❓ TESTANDO COMANDOS NÃO RECONHECIDOS")
    print("="*50)

    send_test_message("eae blz?")
    send_test_message("qual é o sentido da vida?")
    send_test_message("fala sobre o clima")


if __name__ == "__main__":
    print("🚀 Iniciando testes do webhook local")
    print(f"📍 Webhook: {WEBHOOK_URL}")
    print(f"📱 Telefone: {PHONE} (Estevao Antunes)")

    # Menu interativo
    print("\n" + "="*50)
    print("MENU DE TESTES")
    print("="*50)
    print("1. Testar comandos REGEX (rápido)")
    print("2. Testar LLM FALLBACK (linguagem natural)")
    print("3. Testar comandos NÃO RECONHECIDOS")
    print("4. Testar TUDO")
    print("5. Mensagem CUSTOMIZADA")
    print("="*50)

    choice = input("\nEscolha uma opção (1-5): ").strip()

    if choice == "1":
        test_regex_commands()
    elif choice == "2":
        test_llm_fallback()
    elif choice == "3":
        test_unknown_commands()
    elif choice == "4":
        test_regex_commands()
        test_llm_fallback()
        test_unknown_commands()
    elif choice == "5":
        custom_text = input("\n💬 Digite sua mensagem: ").strip()
        if custom_text:
            send_test_message(custom_text)
    else:
        print("❌ Opção inválida!")

    print("\n" + "="*50)
    print("✅ Testes concluídos!")
    print("="*50)
