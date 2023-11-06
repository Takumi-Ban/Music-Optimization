import cvxpy as cp

songs = [
  ['aaa', 300],
  ['bbb', 210],
  ['ccc', 200],
  ['ddd', 320],
  ['eee', 150],
  ['fff', 180],
  ['ggg', 236],
  ['hhh', 271]
]
target_duration = 900
song_vars = cp.Variable(len(songs), boolean=True)
song_durations = [song[1] for song in songs]

cons = [cp.sum(cp.multiply(song_durations, song_vars)) <= target_duration]
obj = cp.Maximize(cp.sum(song_vars))

problem = cp.Problem(obj, cons)
problem.solve()

selected_songs = [songs[i] for i in range(len(songs)) if song_vars.value[i] == 1]
print(selected_songs)

import numpy as np
from scipy.spatial import distance
from deap import base, creator, tools, algorithms
import random

# 選ばれた楽曲の特徴ベクトル
features = np.array([
    [1, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 0, 0],
    [1, 1, 1, 0, 0, 1]
])

# 距離行列を計算
num_songs = features.shape[0]
dist_matrix = np.zeros((num_songs, num_songs))
for i in range(num_songs):
    for j in range(num_songs):
        dist_matrix[i, j] = distance.euclidean(features[i], features[j])

# TSPを解くための遺伝的アルゴリズム設定
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("indices", random.sample, range(num_songs), num_songs)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalTSP(individual):
    return sum(dist_matrix[individual[i-1], individual[i]] for i in range(num_songs)),

toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evalTSP)

def solve_tsp(features):
    pop = toolbox.population(n=100)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("Avg", np.mean)
    stats.register("Std", np.std)
    stats.register("Min", np.min)
    stats.register("Max", np.max)

    algorithms.eaSimple(pop, toolbox, cxpb=0.7, mutpb=0.2, ngen=100, stats=stats, halloffame=hof, verbose=True)

    return hof[0]

playlist_order = solve_tsp(features)
print(playlist_order)