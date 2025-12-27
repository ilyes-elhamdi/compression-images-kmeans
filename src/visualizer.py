"""
Script pour visualiser et comparer les images avant/après compression
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os


def compare_images(original_img, compressed_img, n_colors, save_path=None):
    """
    Affiche côte à côte l'image originale et compressée
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Image originale
    ax1.imshow(original_img)
    ax1.set_title('Image Originale', fontsize=14, fontweight='bold')
    ax1.axis('off')
    
    # Nombre de couleurs originales
    orig_colors = len(np.unique(original_img.reshape(-1, 3), axis=0))
    ax1.text(0.5, -0.1, f'{orig_colors:,} couleurs uniques', 
             ha='center', transform=ax1.transAxes, fontsize=10)
    
    # Image compressée
    ax2.imshow(compressed_img)
    ax2.set_title(f'Compressée ({n_colors} couleurs)', fontsize=14, fontweight='bold')
    ax2.axis('off')
    
    # Ratio de compression
    ratio = orig_colors / n_colors
    ax2.text(0.5, -0.1, f'Ratio: {ratio:.1f}x', 
             ha='center', transform=ax2.transAxes, fontsize=10)
    
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"✓ Comparaison sauvegardée: {save_path}")
    
    plt.close()
    
    return fig


def show_color_palette(img_array, n_colors_to_show=20, save_path=None):
    """
    Affiche les couleurs dominantes de l'image
    """
    # Obtenir toutes les couleurs uniques et leur fréquence
    pixels = img_array.reshape(-1, 3)
    unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)
    
    # Trier par fréquence (les plus communes en premier)
    sorted_indices = np.argsort(-counts)
    top_colors = unique_colors[sorted_indices[:n_colors_to_show]]
    top_counts = counts[sorted_indices[:n_colors_to_show]]
    
    # Créer la palette visuelle
    fig, ax = plt.subplots(figsize=(12, 3))
    
    # Dessiner chaque couleur comme un carré
    for i, (color, count) in enumerate(zip(top_colors, top_counts)):
        percentage = (count / len(pixels)) * 100
        rect = plt.Rectangle((i, 0), 1, 1, facecolor=color/255.0)
        ax.add_patch(rect)
        
        # Ajouter le pourcentage en dessous
        ax.text(i + 0.5, -0.2, f'{percentage:.1f}%', 
                ha='center', va='top', fontsize=8)
    
    ax.set_xlim(0, n_colors_to_show)
    ax.set_ylim(-0.3, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(f'Top {n_colors_to_show} couleurs dominantes', 
                 fontsize=12, fontweight='bold', pad=20)
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"✓ Palette sauvegardée: {save_path}")
    
    plt.close()
    
    return fig


def compare_multiple_compressions(original_img, compression_results, save_path=None):
    """
    Compare l'image originale avec plusieurs niveaux de compression
    """
    n_results = len(compression_results)
    cols = min(4, n_results + 1)
    rows = (n_results + 1 + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(4*cols, 4*rows))
    axes = axes.flatten() if n_results > 1 else [axes]
    
    # Image originale
    axes[0].imshow(original_img)
    orig_colors = len(np.unique(original_img.reshape(-1, 3), axis=0))
    axes[0].set_title(f'Originale\n{orig_colors:,} couleurs', fontweight='bold')
    axes[0].axis('off')
    
    # Images compressées
    for i, result in enumerate(compression_results):
        axes[i+1].imshow(result['image'])
        axes[i+1].set_title(f"{result['n_colors']} couleurs\nRatio: {result['ratio']:.1f}x")
        axes[i+1].axis('off')
    
    # Cacher les axes inutilisés
    for i in range(n_results + 1, len(axes)):
        axes[i].axis('off')
    
    plt.suptitle('Comparaison des niveaux de compression', 
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"✓ Comparaison multiple sauvegardée: {save_path}")
    
    plt.close()
    
    return fig


def plot_compression_stats(compression_results, save_path=None):
    """
    Graphique montrant la relation entre nombre de couleurs et taille de fichier
    """
    n_colors = [r['n_colors'] for r in compression_results]
    file_sizes = [r['file_size'] / 1024 for r in compression_results]  # En KB
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Créer le graphique
    ax.plot(n_colors, file_sizes, marker='o', linewidth=2, markersize=8, color='#2E86AB')
    ax.fill_between(n_colors, file_sizes, alpha=0.3, color='#2E86AB')
    
    # Annotations
    for n, size in zip(n_colors, file_sizes):
        ax.annotate(f'{size:.1f} KB', 
                   xy=(n, size), 
                   xytext=(0, 10), 
                   textcoords='offset points',
                   ha='center',
                   fontsize=9)
    
    ax.set_xlabel('Nombre de couleurs', fontsize=12, fontweight='bold')
    ax.set_ylabel('Taille du fichier (KB)', fontsize=12, fontweight='bold')
    ax.set_title('Impact du nombre de couleurs sur la taille du fichier', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log', base=2)
    
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"✓ Statistiques sauvegardées: {save_path}")
    
    plt.close()
    
    return fig


def generate_full_report(input_path, compression_results, output_dir):
    """
    Génère un rapport complet avec toutes les visualisations
    """
    print("\n" + "=" * 70)
    print("GÉNÉRATION DU RAPPORT VISUEL")
    print("=" * 70)
    
    # Charger l'image originale
    original_img = np.array(Image.open(input_path))
    
    # 1. Comparaison simple avec le meilleur niveau
    best_result = compression_results[len(compression_results)//2]  # Niveau moyen
    compare_images(
        original_img, 
        best_result['image'], 
        best_result['n_colors'],
        save_path=os.path.join(output_dir, 'comparison_simple.png')
    )
    
    # 2. Palette de couleurs originale
    show_color_palette(
        original_img,
        save_path=os.path.join(output_dir, 'color_palette_original.png')
    )
    
    # 3. Comparaison multiple
    compare_multiple_compressions(
        original_img,
        compression_results,
        save_path=os.path.join(output_dir, 'comparison_multiple.png')
    )
    
    # 4. Graphique des stats
    plot_compression_stats(
        compression_results,
        save_path=os.path.join(output_dir, 'compression_stats.png')
    )
    
    print("\n" + "=" * 70)
    print("✓ RAPPORT VISUEL GÉNÉRÉ")
    print("=" * 70)


# Test du module
if __name__ == "__main__":
    print("Module de visualisation pour la compression d'images")
