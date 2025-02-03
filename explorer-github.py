import subprocess
import requests

# Autenticar no GitHub CLI
def authenticate_github():
    try:
        # Executa o comando para abrir o login no terminal
        subprocess.run(["gh", "auth", "login"], check=True)
        print("Autenticação concluída com sucesso!")
    except subprocess.CalledProcessError as e:
        raise RuntimeError("Erro ao autenticar no GitHub CLI. Certifique-se de seguir as instruções no terminal.") from e

# Obter o token do GitHub CLI
def get_github_token():
    try:
        result = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("Token não encontrado. Iniciando autenticação...")
        authenticate_github()
        # Tenta obter o token novamente após autenticação
        result = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True)
        return result.stdout.strip()

# Configurações
GITHUB_TOKEN = get_github_token()
GITHUB_API_URL = "https://api.github.com/search/code"
SEARCH_QUERY = "chame"  # Palavra que você deseja buscar
REPO = "usuario/repo"  # Substitua pelo repositório que deseja buscar (exemplo: stack-spot/stackspot-workflows-action)

def search_word_in_repo(word, repo):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    params = {
        "q": f"{word} repo:{repo}"
    }
    response = requests.get(GITHUB_API_URL, headers=headers, params=params)
    if response.status_code == 200:
        results = response.json()
        if results.get("total_count", 0) > 0:
            print(f"Encontrado {results['total_count']} resultado(s) para a palavra '{word}' no repositório '{repo}':")
            for item in results["items"]:
                print(f"- Arquivo: {item['name']}")
                print(f" Caminho: {item['path']}")
                print(f" URL: {item['html_url']}")
        else:
            print(f"Nenhum resultado encontrado para a palavra '{word}' no repositório '{repo}'.")
    else:
        print(f"Erro ao buscar na API do GitHub: {response.status_code}")
        print(response.json())

# Executar a busca
search_word_in_repo(SEARCH_QUERY, REPO)