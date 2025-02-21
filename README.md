# The Ultimate Maze
**Un projet pour apprendre les graphes en Python**  

---

## Fonctionnalités

- **Génération du labyrinthe** :  
  - Algorithme **DFS** (*Depth-First Search*)  
  - Algorithme **Prim's Algorithm**  

- **Visualisation de la génération DFS** *(optionnelle)*  

- **Système de labyrinthe extensible** :  
  - Prise en charge des **très grands labyrinthes**  
  - **Visibilité limitée** du labyrinthe pour le joueur  

- **Téléporteurs** :  
  - Permettent de se déplacer instantanément  
  - Peuvent être **un avantage** ou un **piège**  

- **Trois modes de difficulté**  

- **Une sorte de Pacman** *(peut rester bloqué dans les téléporteurs !)*  

- **Déplacements et assistance** :  
  - **Flèches directionnelles** → Déplacement  
  - **Q** → Afficher le **chemin optimal** *(Dijkstra)*  
  - **TAB** → **Mode auto** (*déplacement automatique vers la sortie*)  

---

## Idées non implémentées (pour l’instant !)

- **Un mode multi-dimensionnel (>2D)**  
- **Algorithme A\*** (plus rapide et plus efficace que Dijkstra)  
- **Rendre Pacman plus intelligent** et ajouter des **malus**  
- **Changer la couleur du joueur** en fonction de la distance à la sortie  
- **Un vrai menu interactif** (*au lieu d'une CLI*)  
- **Un mode "ONLINE"** avec un **classement des meilleurs temps**  
- **Implémenter le labyrinthe en RUST** (*pour améliorer les performances, et utiliser Pygame pour la GUI*)  
- **Générer un binaire réutilisable pour le labyrinthe**  
- **Réimplémenter Dijkstra sans `heapq`** (*en utilisant `LSC`*)  
- **Créer une IA qui explore le labyrinthe en même temps que l'utilisateur pour voir qui gagne avec la même visibilité**  
