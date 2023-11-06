from flask import Flask, render_template, request
from initdb import MusicInfo, MusicFeature
from dbsetting import session, Engine
import numpy as np
import cvxpy as cp
from scipy.spatial import distance
from deap import base, creator, tools, algorithms
import random

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_index():
  return render_template('index.html')

@app.route('/', methods=['POST'])
def post_index():
  hour = int(request.form['hour'])
  minute = int(request.form['minute'])
  sec = int(request.form['seconds'])
  time = hour * 3600 + minute * 60 + sec

  songs = session.query(MusicInfo.id, MusicInfo.music_name, MusicInfo.length, MusicInfo.url).all()
  selected_songs, total_time = select_songs(time, songs)
  print(selected_songs)
  names = [song[1] for song in selected_songs]
  ordered_index = order_songs(names)
  ordered_songs = [songs[i] for i in ordered_index]
  return render_template('index.html', ordered_songs=ordered_songs, total_time=total_time)

def select_songs(target_duration, songs):
  song_vars = cp.Variable(len(songs), boolean=True)
  song_durations = [song[2] for song in songs]

  cons = [cp.sum(cp.multiply(song_durations, song_vars)) <= target_duration]
  obj = cp.Maximize(cp.sum(song_vars))

  problem = cp.Problem(obj, cons)
  problem.solve()

  selected_songs = [songs[i] for i in range(len(songs)) if song_vars.value[i] == 1]
  total_duration = sum([song[2] for song in selected_songs])
  hours = total_duration // 3600
  minutes = (total_duration % 3600) // 60
  seconds = total_duration % 60
  total_time = f'{hours}時間{minutes}分{seconds}秒'
  return  selected_songs, total_time

def order_songs(selected_songs):
  order_songs = session.query(MusicInfo.music_name, MusicFeature.rock, MusicFeature.pop, MusicFeature.painful, MusicFeature.magnificent, MusicFeature.sad, MusicFeature.kyomu).join(MusicFeature, MusicInfo.id==MusicFeature.id).filter(MusicInfo.music_name.in_(selected_songs)).all()
  features = np.array([feature[1:] for feature in order_songs])
  num_songs = features.shape[0]
  dist_matrix = np.zeros((num_songs, num_songs))
  for i in range(num_songs):
      for j in range(num_songs):
          dist_matrix[i, j] = distance.euclidean(features[i], features[j])
  
  # TSP
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
  ordered_songs = solve_tsp(features)
  return ordered_songs

if __name__ == '__main__':
  app.run(debug=True)
