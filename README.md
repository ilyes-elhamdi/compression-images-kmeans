# 🖼️ Compression d'Images par K-means

Projet de compression d'images utilisant le clustering K-means pour réduire le nombre de couleurs et optimiser la taille des fichiers.

## 📋 Description

Ce projet implémente un algorithme de **compression d'images par quantification de couleurs** utilisant l'algorithme **K-means clustering**. Le principe est simple : au lieu d'utiliser des millions de couleurs, on regroupe les couleurs similaires en un nombre limité de clusters, ce qui réduit considérablement la taille du fichier tout en préservant la qualité visuelle.

### 🎯 Principe de fonctionnement :
1. Chaque pixel est considéré comme un point dans l'espace RGB (Rouge, Vert, Bleu)
2. L'algorithme K-means regroupe ces points en K clusters (K = nombre de couleurs voulues)
3. Chaque pixel est remplacé par la couleur du centre de son cluster
4. L'image finale n'utilise que K couleurs au lieu de millions

## 🛠️ Technologies utilisées

- **NumPy** : Manipulation des données d'images
- **Scikit-learn** : Algorithme K-means clustering
- **Matplotlib** : Visualisations et comparaisons
- **Pillow (PIL)** : Chargement et sauvegarde d'images
- **OpenCV** : Traitement d'images avancé

## 📁 Structure du projet

```
compression-images-kmeans/
│
├── src/
│   ├── image_compressor.py   # Algorithme de compression K-means
│   ├── visualizer.py          # Comparaisons visuelles et graphiques
│   └── main.py                # Script principal
│
├── images/
│   ├── input/                 # Images originales
│   ├── output/                # Images compressées
│   └── comparisons/           # Visualisations comparatives
│
├── examples/                  # Exemples de résultats
├── requirements.txt
└── README.md
```

## 🚀 Installation

1. Cloner le repository :
```bash
git clone https://github.com/ilyes-elhamdi/compression-images-kmeans.git
cd compression-images-kmeans
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## 💻 Utilisation

### Mode simple (compression rapide)

```bash
cd src
python main.py ../images/input/image.jpg
```

Ou avec un nombre de couleurs spécifique :
```bash
python main.py image.jpg -c 32
```

### Mode analyse complète

Génère plusieurs versions compressées avec différents niveaux + visualisations :
```bash
python main.py image.jpg -a
```

### Utilisation dans le code Python

```python
from image_compressor import compress_image_file

# Compression simple
compress_image_file('input.jpg', 'output.jpg', n_colors=16)

# Compression avec plusieurs niveaux
from image_compressor import compress_with_multiple_levels
results = compress_with_multiple_levels('input.jpg', 'output/', levels=[4, 8, 16, 32])

# Visualisation
from visualizer import compare_images
compare_images(original_img, compressed_img, n_colors=16, save_path='comparison.png')
```

## 📊 Exemples de résultats

### Nombre de couleurs vs Qualité

| Couleurs | Qualité | Taille | Cas d'usage |
|----------|---------|--------|-------------|
| 4        | Faible  | Très petit | Icônes, logos simples |
| 8        | Moyenne-faible | Petit | Graphiques, diagrammes |
| 16       | Moyenne | Moyen | Images web, prévisualisations |
| 32       | Bonne   | Moyen-grand | Photos web optimisées |
| 64       | Très bonne | Grand | Photos standard |
| 128      | Excellente | Très grand | Photos haute qualité |

### Réduction typique

- **16 couleurs** : Réduction de 50-70% de la taille
- **32 couleurs** : Réduction de 30-50% de la taille
- **64 couleurs** : Réduction de 20-40% de la taille

## 🔧 Fonctionnalités

- ✅ Compression avec nombre de couleurs personnalisable
- ✅ Comparaison visuelle avant/après
- ✅ Analyse multi-niveaux (4, 8, 16, 32, 64, 128 couleurs)
- ✅ Palette de couleurs dominantes
- ✅ Graphiques de statistiques (taille vs qualité)
- ✅ Rapport complet avec toutes les visualisations
- ✅ Support de tous les formats d'images (JPG, PNG, BMP, etc.)

## 📝 Options de ligne de commande

```
usage: main.py [-h] [-c COLORS] [-a] [-o OUTPUT] input

Arguments:
  input                 Chemin vers l'image à compresser

Options:
  -h, --help           Afficher l'aide
  -c, --colors COLORS  Nombre de couleurs (défaut: 16)
  -a, --analysis       Générer une analyse complète
  -o, --output OUTPUT  Dossier de sortie (défaut: ../images/output)
```

## 🎓 Concepts utilisés

- **K-means Clustering** : Algorithme de machine learning non supervisé
- **Quantification de couleurs** : Réduction de la palette de couleurs
- **Espace RGB** : Représentation des couleurs en 3 dimensions
- **Compression avec perte** : Trade-off entre qualité et taille

## 📈 Améliorations possibles

- [ ] Support de la compression par zones (préserver détails importants)
- [ ] Algorithmes alternatifs (K-medoids, Mean Shift)
- [ ] Compression adaptative basée sur le contenu
- [ ] Interface graphique (GUI)
- [ ] Batch processing pour dossiers entiers
- [ ] Comparaison avec autres méthodes (JPEG, WebP, etc.)

## 🔬 Comment ça marche ?

### Algorithme K-means pour l'image

1. **Initialisation** : Choisir K couleurs aléatoires comme centres de clusters
2. **Attribution** : Assigner chaque pixel au cluster le plus proche
3. **Mise à jour** : Recalculer les centres des clusters (moyenne des couleurs)
4. **Répétition** : Répéter étapes 2-3 jusqu'à convergence
5. **Compression** : Remplacer chaque pixel par la couleur de son centre

### Exemple visuel

```
Image originale : 1 million de couleurs uniques
     ↓ (K-means avec K=16)
Image compressée : 16 couleurs seulement
     ↓
Réduction : ~95% des couleurs, mais l'image reste visuellement similaire
```

## 👤 Auteur

**Ilyes Elhamdi**
- LinkedIn: [ilyes-elhamdi](https://www.linkedin.com/in/ilyes-elhamdi-320202248)
- Email: ilyeshamdi48@gmail.com

## 📄 Licence

Projet personnel - libre d'utilisation à des fins éducatives

## 🙏 Remerciements

- Scikit-learn pour l'implémentation K-means
- Communauté Python pour les bibliothèques de traitement d'images
