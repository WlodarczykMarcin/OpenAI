import openai
from pathlib import Path

def loadArticle(filepath):
    "Funkcja wczytująca zawartość pliku tekstowego"
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Błąd: Plik {filepath} nie istnieje.")
        return None

def generate_html_with_ai(articleContent, prompt, apiOpenAiKey):
    "Funkcja wysyłająca zapytanie do API OpenAI w celu wygenerowania HTML"
    openai.api_key = apiOpenAiKey
    
    full_prompt = (
        f"{prompt}\n\n"
        f"---\n\n"
        f"Artykuł:\n{articleContent}\n\n"
        "Instrukcje:\n"
        "Przekształć tekst artykułu na HTML, używając odpowiednich nagłówków (h1, h2, itp.) oraz paragrafów.\n"
        "W miejscach, gdzie przydałyby się obrazy, umieść tag <img src='' alt=''>.\n"
        "Dopisz krótki podpis pod każdym obrazkiem używając <figcaption>.\n"
        "Zwróć tylko treść do wstawienia pomiędzy <body> i </body>."
    )

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=full_prompt,
            max_tokens=2048,
            temperature=0.5,
        )
        htmlContent = response['choices'][0]['text'].strip()
        return htmlContent
    except openai.error.OpenAIError as e:
        print(f"Wystąpił błąd z API OpenAI: {e}")
        return None

def saveHTMLfile(content, output_filepath):
    "Funkcja zapisująca wygenerowany kod HTML do pliku"
    try:
        with open(output_filepath, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Plik HTML został zapisany w {output_filepath}")
    except Exception as e:
        print(f"Błąd przy zapisywaniu pliku: {e}")

def main():
    apiOpenAiKey = "proszę tu wpisać kod podany mi przez maila ponieważ z podanym kodem nie mógłbym państwu udostępnić tego pliku"
    articleFilePath = Path(r".\ZadaniedlaJuniorAIDeveloperaTresc.txt")
    output_filepath = Path(r".\OpenAi\artykul.html")
    prompt = "Zamień poniższy artykuł na odpowiednio sformatowany kod HTML z sugestiami miejsc na grafiki."
    if not articleFilePath.is_file():
        print(f"Błąd: Plik {articleFilePath} nie istnieje.")
        return
    article_content = loadArticle(articleFilePath)
    if article_content is None:
        return
    html_content = generate_html_with_ai(article_content, prompt, apiOpenAiKey)
    if html_content is None:
        print("Błąd: Nie udało się wygenerować HTML.")
        return
    saveHTMLfile(html_content, output_filepath)

if __name__ == "__main__":
    main()