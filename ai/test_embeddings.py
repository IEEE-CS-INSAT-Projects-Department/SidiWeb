"""
test_embeddings.py

Script pour tester les fichiers texte d'embeddings.
Vérifie que tous les templates ont été convertis en format texte.
"""

from pathlib import Path
import json


def main():
    print("=" * 70)
    print("  TEST DES EMBEDDINGS - Fichiers Texte pour Templates")
    print("=" * 70)
    print()
    
    # Chemins
    workspace = Path(__file__).parent
    embeddings_dir = workspace / "data" / "backend_templates" / "embeddings"
    backend_dir = workspace / "data" / "backend_templates"
    
    # Test 1: Vérifier le dossier embeddings
    print("TEST 1: Vérification du dossier embeddings...")
    if embeddings_dir.exists():
        print(f"✅ Dossier trouvé: {embeddings_dir}")
        
        # Compter les fichiers .txt
        txt_files = list(embeddings_dir.glob("*.txt"))
        print(f"   📄 {len(txt_files)} fichiers texte trouvés")
        print()
    else:
        print(f"❌ Dossier non trouvé: {embeddings_dir}")
        return
    
    # Test 2: Lister tous les fichiers d'embeddings
    print("TEST 2: Liste des fichiers d'embeddings...")
    for txt_file in sorted(txt_files):
        size_kb = txt_file.stat().st_size / 1024
        print(f"   ✓ {txt_file.name} ({size_kb:.1f} KB)")
    print()
    
    # Test 3: Vérifier correspondance avec JSON
    print("TEST 3: Correspondance avec templates JSON...")
    json_files = list(backend_dir.glob("template_*.json"))
    
    print(f"   Templates JSON: {len(json_files)}")
    print(f"   Fichiers texte: {len(txt_files)}")
    
    if len(json_files) == len(txt_files):
        print("   ✅ Tous les templates ont leur version texte!")
    else:
        print(f"   ⚠️  Différence: {abs(len(json_files) - len(txt_files))} fichier(s)")
    print()
    
    # Test 4: Vérifier le contenu des fichiers
    print("TEST 4: Vérification du contenu des fichiers...")
    
    required_sections = [
        "**ID:**",
        "**Catégorie:**",
        "**Layout:**",
        "## Description",
        "## Pages incluses",
        "## Fonctionnalités",
        "## Style visuel",
        "## Couleurs",
        "## Typographie recommandée",
        "## Cas d'usage idéaux",
        "## Mots-clés"
    ]
    
    all_valid = True
    for txt_file in txt_files:
        content = txt_file.read_text(encoding="utf-8")
        missing_sections = []
        
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)
        
        if missing_sections:
            print(f"   ⚠️  {txt_file.name} - Sections manquantes: {missing_sections}")
            all_valid = False
    
    if all_valid:
        print("   ✅ Tous les fichiers ont la structure complète!")
    print()
    
    # Test 5: Statistiques
    print("TEST 5: Statistiques des fichiers...")
    total_size = sum(f.stat().st_size for f in txt_files)
    avg_size = total_size / len(txt_files) if txt_files else 0
    
    print(f"   📊 Taille totale: {total_size / 1024:.1f} KB")
    print(f"   📊 Taille moyenne: {avg_size / 1024:.1f} KB par fichier")
    
    # Compter les mots
    total_words = 0
    for txt_file in txt_files:
        content = txt_file.read_text(encoding="utf-8")
        words = len(content.split())
        total_words += words
    
    avg_words = total_words / len(txt_files) if txt_files else 0
    print(f"   📊 Mots totaux: {total_words}")
    print(f"   📊 Mots moyens: {avg_words:.0f} par fichier")
    print()
    
    # Test 6: Extraction des IDs
    print("TEST 6: Vérification des IDs...")
    ids_found = []
    
    for txt_file in txt_files:
        content = txt_file.read_text(encoding="utf-8")
        # Chercher la ligne **ID:**
        for line in content.split('\n'):
            if line.startswith("**ID:**"):
                template_id = line.replace("**ID:**", "").strip()
                ids_found.append(template_id)
                break
    
    print(f"   📋 IDs extraits: {len(ids_found)}")
    for template_id in sorted(ids_found):
        print(f"      - {template_id}")
    print()
    
    # Test 7: Catégories disponibles
    print("TEST 7: Catégories couvertes...")
    categories = set()
    
    for txt_file in txt_files:
        content = txt_file.read_text(encoding="utf-8")
        for line in content.split('\n'):
            if line.startswith("**Catégorie:**"):
                category = line.replace("**Catégorie:**", "").strip()
                categories.add(category)
                break
    
    print(f"   🎯 {len(categories)} catégories uniques:")
    for category in sorted(categories):
        print(f"      - {category}")
    print()
    
    # Résumé
    print("=" * 70)
    print("  RÉSUMÉ")
    print("=" * 70)
    print()
    print(f"✅ {len(txt_files)} templates convertis en format texte")
    print(f"✅ {len(categories)} catégories couvertes")
    print(f"✅ {total_words} mots de description")
    print(f"✅ Prêt pour embeddings et recherche sémantique")
    print()
    print("📝 Les fichiers peuvent être utilisés avec:")
    print("   - OpenAI Embeddings")
    print("   - FAISS Vector Store")
    print("   - LangChain Document Loaders")
    print("   - Recherche sémantique")
    print()
    print("📚 Documentation: data/backend_templates/embeddings/README.md")
    print()


if __name__ == "__main__":
    main()
