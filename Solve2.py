import csv
import numpy as np
import random

# Read data from CSV
games = []

with open("input_game.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip header
    for row in csvreader:
        games.append(row)

# Define functions for calculating profits and comparing strategies
def calculate_profit(action1, action2):
    if action1 == 'TRUST' and action2 == 'TRUST':
        return 3, 3
    elif action1 == 'CHEAT' and action2 == 'CHEAT':
        return 1, 1
    elif action1 == 'TRUST' and action2 == 'CHEAT':
        return 0, 5
    elif action1 == 'CHEAT' and action2 == 'TRUST':
        return 5, 0

def compare_strategies(player_actions, other_player_actions, margin=0.1):
    total_comparisons = len(player_actions)
    
    if total_comparisons == 0:
        return 0.0  # If there are no comparisons to make, return 0 similarity
    
    similar_strategy_count = 0
    
    for i in range(total_comparisons):
        p1_profit = calculate_profit(player_actions[i], player_actions[i])[0]  # Get only the first element of the tuple
        for other_actions in other_player_actions:
            other_profit = calculate_profit(player_actions[i], other_actions[i])[0]  # Get only the first element of the tuple
            if abs(p1_profit - other_profit) <= margin:
                similar_strategy_count += 1
                break
    similarity_ratio = similar_strategy_count / total_comparisons
    return similarity_ratio

# Organize data
players = set()
rounds = []
profits = []

for game in games:
    _, p1_id, p2_id, p1_action, p2_action, _ = game
    players.add(p1_id)
    players.add(p2_id)
    rounds.append((p1_id, p2_id))
    profits.append((p1_action, p2_action))

players = sorted(list(players))

# Collect player actions for K-means clustering
player_actions = np.zeros((len(profits), 2))
for idx, (p1_action, p2_action) in enumerate(profits):
    if p1_action == 'TRUST':
        player_actions[idx][0] = 1
    if p2_action == 'TRUST':
        player_actions[idx][1] = 1

# Implement K-means clustering
class KMeans:
    def __init__(self, n_clusters, max_iter=300):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
    
    def fit(self, X):
        centroids = self._initialize_centroids(X)
        for _ in range(self.max_iter):
            clusters = self._assign_clusters(X, centroids)
            new_centroids = self._calculate_centroids(X, clusters)
            if self._is_converged(centroids, new_centroids):
                break
            centroids = new_centroids
        self.centroids = centroids
        self.labels = self._assign_clusters(X, centroids)
    
    def _initialize_centroids(self, X):
        return random.sample(list(X), self.n_clusters)
    
    def _assign_clusters(self, X, centroids):
        clusters = {i: [] for i in range(self.n_clusters)}
        for point in X:
            distances = [self._distance(point, centroid) for centroid in centroids]
            closest_centroid_idx = distances.index(min(distances))
            clusters[closest_centroid_idx].append(point)
        return clusters
    
    def _calculate_centroids(self, X, clusters):
        centroids = []
        for cluster_points in clusters.values():
            centroid = [sum(coord) / len(cluster_points) for coord in zip(*cluster_points)]
            centroids.append(centroid)
        return centroids
    
    def _distance(self, p1, p2):
        return sum((x - y) ** 2 for x, y in zip(p1, p2)) ** 0.5
    
    def _is_converged(self, centroids, new_centroids):
        return centroids == new_centroids

num_clusters = 100  # Adjust this number as needed
kmeans = KMeans(n_clusters=num_clusters)
kmeans.fit(player_actions)
labels = kmeans.labels

# Compare player strategies and cluster similar players
margin = 0.1  # Adjust this threshold as needed

similar_players = set()

for i in range(len(players)):
    for j in range(i + 1, len(players)):
        p1_actions = [action1 for action1, _ in profits if action1 == players[i]]
        p2_actions = [action2 for _, action2 in profits if action2 == players[j]]
        other_players_actions = [[action2 for action1, action2 in profits if action1 == other_player] for other_player in players if other_player != players[i] and other_player != players[j]]
        similarity_ratio1 = compare_strategies(p1_actions, other_players_actions, margin)
        similarity_ratio2 = compare_strategies(p2_actions, other_players_actions, margin)
        if (similarity_ratio1 >= 1.0).all() and (similarity_ratio2 >= 1.0).all():  # Corrected condition
            similar_players.add(players[i])
            similar_players.add(players[j])

# Count clusters
num_clusters = len(similar_players)

print("Number of clusters:", num_clusters)