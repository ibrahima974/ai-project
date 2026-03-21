import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def build_prompt(metrics: list, category: str) -> str:
    data_lines = "\n".join([
        f"- {m['name']}: {m['value']} {m['unit']} (le {m['recorded_at']})"
        for m in metrics
    ])

    return f"""Tu es un analyste business senior spécialisé dans les entreprises B2B SaaS.

Voici les données récentes de la catégorie "{category}" :

{data_lines}

Génère une analyse business structurée avec exactement ce format :

## Tendances clés
Décris en 2-3 phrases les tendances observées dans ces chiffres.

## Points d'alerte
Liste 1-2 points négatifs ou risques à surveiller. Si tout va bien, dis-le clairement.

## Recommandations
Donne 3 actions concrètes et actionnables basées sur ces données.

Sois précis, professionnel et oriente toujours vers l'action. Réponds en français."""


def generate_insight(metrics: list, category: str) -> dict:
    if not metrics:
        raise ValueError(f"Aucune métrique trouvée pour la catégorie '{category}'")

    prompt = build_prompt(metrics, category)

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        content = message.content[0].text

        title = f"Analyse {category} — {metrics[0]['recorded_at'][:7] if metrics else 'N/A'}"

        return {
            "title": title,
            "content": content,
            "category": category
        }

    except anthropic.AuthenticationError:
        raise ValueError("Clé API Anthropic invalide. Vérifie ton .env")

    except anthropic.RateLimitError:
        raise ValueError("Quota API dépassé. Réessaie dans quelques instants.")

    except anthropic.APIConnectionError:
        raise ValueError("Impossible de contacter l'API Claude. Vérifie ta connexion.")

    except Exception as e:
        raise ValueError(f"Erreur inattendue lors de l'appel Claude : {str(e)}")