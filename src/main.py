"""
Script principal pour compresser des images
Permet de compresser une image ou un dossier entier
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from image_compressor import compress_image_file, compress_with_multiple_levels, load_image
from visualizer import generate_full_report
import argparse


def compress_single_image(input_path, n_colors=16, output_dir='../images/output'):
    """
    Compresse une seule image avec un nombre de couleurs spécifique
    """
    # Créer le nom du fichier de sortie
    filename = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_dir, f'{filename}_compressed_{n_colors}.png')
    
    # Compresser
    compressed_img = compress_image_file(input_path, output_path, n_colors)
    
    return compressed_img


def compress_with_analysis(input_path, output_dir='../images/output', 
                           comparison_dir='../images/comparisons'):
    """
    Compresse avec plusieurs niveaux et génère un rapport complet
    """
    print("\n" + "=" * 70)
    print("COMPRESSION AVEC ANALYSE COMPLÈTE")
    print("=" * 70)
    
    # Niveaux de compression à tester
    levels = [4, 8, 16, 32, 64, 128]
    
    # Créer les dossiers
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(comparison_dir, exist_ok=True)
    
    # Compresser avec tous les niveaux
    results = compress_with_multiple_levels(input_path, output_dir, levels)
    
    if results:
        # Générer le rapport visuel
        generate_full_report(input_path, results, comparison_dir)
        
        print("\n📊 Résumé des résultats:")
        print("-" * 70)
        print(f"{'Couleurs':<12} {'Taille fichier':<15} {'Ratio':<10} {'Chemin'}")
        print("-" * 70)
        
        for r in results:
            print(f"{r['n_colors']:<12} {r['file_size']/1024:>10.1f} KB   {r['ratio']:>6.2f}x    {os.path.basename(r['path'])}")
        
        print("-" * 70)


def main():
    """
    Point d'entrée principal avec arguments en ligne de commande
    """
    parser = argparse.ArgumentParser(
        description='Compression d\'images par clustering K-means'
    )
    
    parser.add_argument('input', help='Chemin vers l\'image à compresser')
    parser.add_argument('-c', '--colors', type=int, default=16,
                       help='Nombre de couleurs (défaut: 16)')
    parser.add_argument('-a', '--analysis', action='store_true',
                       help='Générer une analyse complète avec plusieurs niveaux')
    parser.add_argument('-o', '--output', default='../images/output',
                       help='Dossier de sortie')
    
    args = parser.parse_args()
    
    # Vérifier que le fichier existe
    if not os.path.exists(args.input):
        print(f"✗ Erreur: Le fichier '{args.input}' n'existe pas")
        sys.exit(1)
    
    # Mode analyse ou compression simple
    if args.analysis:
        compress_with_analysis(args.input, args.output)
    else:
        compress_single_image(args.input, args.colors, args.output)


if __name__ == "__main__":
    # Si appelé sans arguments, afficher l'aide
    if len(sys.argv) == 1:
        print("=" * 70)
        print("COMPRESSION D'IMAGES PAR K-MEANS")
        print("=" * 70)
        print("\nUtilisation:")
        print("  python main.py image.jpg                    # Compression simple (16 couleurs)")
        print("  python main.py image.jpg -c 32              # 32 couleurs")
        print("  python main.py image.jpg -a                 # Analyse complète")
        print("  python main.py image.jpg -c 8 -o ./output   # Spécifier dossier sortie")
        print("\n" + "=" * 70)
    else:
        main()
