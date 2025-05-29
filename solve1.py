import csv

# Read data from CSV
games = []

with open("input_game.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip header
    for row in csvreader:
        games.append(row)

#print(games)

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

def compare_strategies(player1_actions, player2_actions, other_player_actions, margin=0.1):
    total_comparisons = len(player1_actions)
    
    if total_comparisons == 0:
        return 0.0  # If there are no comparisons to make, return 0 similarity
    
    similar_strategy_count = 0
    
    for i in range(total_comparisons):
        p1_profit, p2_profit = calculate_profit(player1_actions[i], player2_actions[i])
        for other_actions in other_player_actions:
            other_profit, _ = calculate_profit(player1_actions[i], other_actions[i])
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
pairs = [(p1, p2) for p1 in players for p2 in players if p1 < p2]

# Now let's implement the clustering logic
# We will use Disjoint Set Union (DSU) data structure for clustering

class DSU:
    def __init__(self, n):
        self.parent = [i for i in range(n)]
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        x_root = self.find(x)
        y_root = self.find(y)
        
        if x_root == y_root:
            return
        
        if self.rank[x_root] < self.rank[y_root]:
            self.parent[x_root] = y_root
        elif self.rank[x_root] > self.rank[y_root]:
            self.parent[y_root] = x_root
        else:
            self.parent[y_root] = x_root
            self.rank[x_root] += 1

#Compare strategies and cluster players
margin = 0.1  # Adjust this threshold as needed

dsu = DSU(len(players))

for p1, p2 in pairs:
    print('Comparing player',p1,'and player',p2)
    p1_actions = [action1 for action1, _ in profits if action1 == p1]
    p2_actions = [action2 for _, action2 in profits if action2 == p2]
    other_players_actions = [[action2 for action1, action2 in profits if action1 == other_player] for other_player in players if other_player != p1 and other_player != p2]
    similarity_ratio = compare_strategies(p1_actions, p2_actions, other_players_actions, margin)
    if similarity_ratio >= 1.0:  # If all comparisons are within margin
        dsu.union(players.index(p1), players.index(p2))

# Count clusters
clusters = set()
for i in range(len(players)):
    clusters.add(dsu.find(i))

num_clusters = len(clusters)

print("Number of clusters formed by DSU:", num_clusters)
