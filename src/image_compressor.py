"""
Script pour compresser des images en réduisant le nombre de couleurs avec K-means
Le clustering K-means regroupe les couleurs similaires pour réduire la taille
"""

import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import os


def load_image(image_path):
    """
    Charge une image et la convertit en array numpy
    """
    print(f"Chargement de l'image: {image_path}")
    
    try:
        img = Image.open(image_path)
        img_array = np.array(img)
        
        print(f"✓ Image chargée: {img_array.shape}")
        print(f"  - Dimensions: {img_array.shape[1]}x{img_array.shape[0]} pixels")
        print(f"  - Canaux: {img_array.shape[2] if len(img_array.shape) == 3 else 1}")
        
        return img_array
    
    except Exception as e:
        print(f"✗ Erreur lors du chargement: {e}")
        return None


def compress_image_kmeans(img_array, n_colors=16):
    """
    Compresse une image en réduisant le nombre de couleurs avec K-means
    
    Principe:
    - Au lieu d'avoir des millions de couleurs possibles
    - On regroupe les couleurs similaires en clusters
    - Chaque pixel prend la couleur du centre de son cluster
    """
    print(f"\nCompression avec K-means ({n_colors} couleurs)...")
    
    # Sauvegarder les dimensions originales
    original_shape = img_array.shape
    
    # Aplatir l'image en une liste de pixels (chaque pixel = un point RGB)
    # De (hauteur, largeur, 3) vers (hauteur*largeur, 3)
    pixels = img_array.reshape(-1, 3)
    
    print(f"  - Nombre de pixels: {len(pixels):,}")
    print(f"  - Couleurs uniques originales: {len(np.unique(pixels, axis=0)):,}")
    
    # Appliquer K-means pour trouver les n_colors couleurs représentatives
    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
    kmeans.fit(pixels)
    
    # Remplacer chaque pixel par la couleur du centre de son cluster
    compressed_pixels = kmeans.cluster_centers_[kmeans.labels_]
    
    # Remettre au format image
    compressed_img = compressed_pixels.reshape(original_shape).astype(np.uint8)
    
    print(f"✓ Compression terminée")
    print(f"  - Couleurs après compression: {n_colors}")
    print(f"  - Réduction: {len(np.unique(pixels, axis=0)):,} → {n_colors} couleurs")
    
    return compressed_img


def calculate_compression_ratio(original_img, compressed_img):
    """
    Calcule le taux de compression approximatif
    En réalité, il faudrait sauvegarder les fichiers pour avoir le ratio exact
    """
    # Nombre de couleurs uniques
    orig_colors = len(np.unique(original_img.reshape(-1, 3), axis=0))
    comp_colors = len(np.unique(compressed_img.reshape(-1, 3), axis=0))
    
    # Ratio basé sur le nombre de couleurs
    ratio = orig_colors / comp_colors if comp_colors > 0 else 1
    
    return ratio


def save_image(img_array, output_path):
    """
    Sauvegarde l'image compressée
    """
    print(f"\nSauvegarde de l'image: {output_path}")
    
    # Créer le dossier si nécessaire
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Convertir en image et sauvegarder
    img = Image.fromarray(img_array)
    img.save(output_path)
    
    # Obtenir la taille du fichier
    file_size = os.path.getsize(output_path)
    print(f"✓ Image sauvegardée ({file_size / 1024:.1f} KB)")
    
    return file_size


def compress_image_file(input_path, output_path, n_colors=16):
    """
    Pipeline complet de compression d'une image
    """
    print("=" * 70)
    print(f"COMPRESSION D'IMAGE - {n_colors} couleurs")
    print("=" * 70)
    
    # Charger l'image
    img_array = load_image(input_path)
    
    if img_array is None:
        return None
    
    # Compresser
    compressed_img = compress_image_kmeans(img_array, n_colors)
    
    # Calculer le ratio
    ratio = calculate_compression_ratio(img_array, compressed_img)
    print(f"\n✓ Ratio de compression (couleurs): {ratio:.2f}x")
    
    # Sauvegarder
    file_size = save_image(compressed_img, output_path)
    
    print("\n" + "=" * 70)
    print("✓ COMPRESSION TERMINÉE")
    print("=" * 70)
    
    return compressed_img


def compress_with_multiple_levels(input_path, output_dir, levels=[2, 4, 8, 16, 32, 64]):
    """
    Compresse une image avec différents nombres de couleurs
    Utile pour comparer la qualité vs la compression
    """
    print("=" * 70)
    print("COMPRESSION MULTI-NIVEAUX")
    print("=" * 70)
    
    # Charger l'image originale
    img_array = load_image(input_path)
    
    if img_array is None:
        return None
    
    results = []
    
    for n_colors in levels:
        print(f"\n--- Niveau {n_colors} couleurs ---")
        
        # Compresser
        compressed_img = compress_image_kmeans(img_array, n_colors)
        
        # Sauvegarder
        filename = f"compressed_{n_colors}_colors.png"
        output_path = os.path.join(output_dir, filename)
        file_size = save_image(compressed_img, output_path)
        
        # Ratio
        ratio = calculate_compression_ratio(img_array, compressed_img)
        
        results.append({
            'n_colors': n_colors,
            'path': output_path,
            'image': compressed_img,
            'ratio': ratio,
            'file_size': file_size
        })
    
    print("\n" + "=" * 70)
    print("✓ TOUTES LES COMPRESSIONS TERMINÉES")
    print("=" * 70)
    
    return results


# Test du script si exécuté directement
if __name__ == "__main__":
    print("Script de compression d'images par K-means")
    print("Utilisation:")
    print("  from image_compressor import compress_image_file")
    print("  compress_image_file('input.jpg', 'output.jpg', n_colors=16)")
