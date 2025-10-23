"""
Script de testes para o LLM Agent.
Testa interpretação de linguagem natural.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.llm.agent import llm_agent
from config.settings import settings

# Casos de teste
TEST_CASES = [
    # List tasks
    {"text": "minhas tarefas", "expected": "list_tasks"},
    {"text": "o que tenho pra hoje?", "expected": "list_tasks"},
    {"text": "mostra minhas tasks", "expected": "list_tasks"},

    # Mark done
    {"text": "terminei a primeira", "expected": "mark_done"},
    {"text": "feito 3", "expected": "mark_done"},
    {"text": "concluí a 2", "expected": "mark_done"},
    {"text": "finalizei a tarefa 5", "expected": "mark_done"},

    # Mark progress
    {"text": "tô fazendo a 2", "expected": "mark_progress"},
    {"text": "comecei a 4", "expected": "mark_progress"},
    {"text": "andamento 1", "expected": "mark_progress"},

    # Show progress
    {"text": "como tá meu dia?", "expected": "show_progress"},
    {"text": "progresso", "expected": "show_progress"},
    {"text": "quanto falta?", "expected": "show_progress"},

    # Help
    {"text": "ajuda", "expected": "help"},
    {"text": "o que posso fazer?", "expected": "help"},
]

def test_llm():
    """Testa LLM com casos de uso reais."""
    print("🧪 Testando LLM Agent\n")
    print(f"Modelo: {settings.GPT_MODEL}")
    print(f"Threshold: {settings.LLM_CONFIDENCE_THRESHOLD}\n")

    # Contexto simulado
    context = {
        "user_name": "Estevao",
        "tasks": [
            {"id": "1", "title": "Revisar código", "status": "To Do"},
            {"id": "2", "title": "Atualizar docs", "status": "To Do"},
            {"id": "3", "title": "Fazer deploy", "status": "In Progress"}
        ],
        "task_count": 3
    }

    passed = 0
    failed = 0

    for i, test in enumerate(TEST_CASES, 1):
        text = test["text"]
        expected = test["expected"]

        print(f"Teste {i}/{len(TEST_CASES)}: \"{text}\"")

        try:
            result = llm_agent.parse_natural_language(text, context)

            command = result["command"]
            confidence = result["confidence"]
            reasoning = result["reasoning"]

            # Verificar se passou no threshold
            if confidence < settings.LLM_CONFIDENCE_THRESHOLD:
                print(f"  ⚠️  Confidence baixa: {confidence:.2f}")
                print(f"  Expected: {expected}, Got: {command}")
                print(f"  Reasoning: {reasoning}\n")
                failed += 1
                continue

            # Verificar comando correto
            if command == expected:
                print(f"  ✅ Passou! ({confidence:.2f})")
                print(f"  Reasoning: {reasoning}\n")
                passed += 1
            else:
                print(f"  ❌ Falhou!")
                print(f"  Expected: {expected}, Got: {command} ({confidence:.2f})")
                print(f"  Reasoning: {reasoning}\n")
                failed += 1

        except Exception as e:
            print(f"  💥 Erro: {e}\n")
            failed += 1

    # Resultados finais
    print("=" * 50)
    print(f"📊 Resultados: {passed}/{len(TEST_CASES)} passaram")
    print(f"✅ Passou: {passed}")
    print(f"❌ Falhou: {failed}")
    print(f"Taxa de sucesso: {passed/len(TEST_CASES)*100:.1f}%")

    if passed == len(TEST_CASES):
        print("\n🎉 Todos os testes passaram!")
    elif passed >= len(TEST_CASES) * 0.8:
        print("\n✅ Maioria dos testes passou (>80%)")
    else:
        print("\n⚠️  Muitos testes falharam, revisar prompts ou threshold")


if __name__ == "__main__":
    print("Iniciando testes do LLM...\n")

    # Verificar API key
    if not settings.OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY não configurada!")
        sys.exit(1)

    test_llm()
