"""
Script de test pour identifier le problème d'écriture CSV
"""
import os
import csv

# Test 1 : Écrire un fichier simple
print("Test 1: Ecriture fichier texte simple...")
try:
    with open('test_simple.txt', 'w') as f:
        f.write("Test\n")
    print("  OK - Fichier texte simple")
    os.remove('test_simple.txt')
except Exception as e:
    print(f"  ECHEC: {e}")

# Test 2 : Écrire un CSV simple sans pygame
print("\nTest 2: Ecriture CSV simple (sans pygame)...")
try:
    with open('test_csv.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Nom', 'Prenom'])
        writer.writerow(['Test', 'User'])
    print("  OK - CSV simple")
    os.remove('test_csv.csv')
except Exception as e:
    print(f"  ECHEC: {e}")

# Test 3 : Vérifier si joueurs.csv est accessible
print("\nTest 3: Verification acces joueurs.csv...")
try:
    # Essayer de lire
    if os.path.exists('joueurs.csv'):
        with open('joueurs.csv', 'r') as f:
            content = f.read()
        print(f"  OK - Lecture possible ({len(content)} bytes)")
        
        # Essayer d'écrire
        with open('joueurs.csv', 'a') as f:
            pass  # Juste ouvrir en mode append
        print("  OK - Ecriture possible")
    else:
        print("  Le fichier joueurs.csv n'existe pas")
except Exception as e:
    print(f"  ECHEC: {e}")
    print("  --> Le fichier est peut-etre ouvert dans Excel ou un autre programme!")

# Test 4 : Importer pygame et retenter
print("\nTest 4: Test apres import pygame...")
try:
    import pygame
    pygame.init()
    
    with open('test_pygame.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Test', 'Pygame'])
    
    print("  OK - Ecriture CSV avec pygame charge")
    os.remove('test_pygame.csv')
except Exception as e:
    print(f"  ECHEC: {e}")
    print("  --> C'est pygame qui cause le probleme!")

print("\n" + "="*50)
print("CONCLUSION:")
print("Si Test 1-3 sont OK mais Test 4 echoue --> probleme pygame")
print("Si Test 3 echoue --> joueurs.csv est ouvert ailleurs")
print("="*50)
