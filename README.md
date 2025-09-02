# voter-blotto

settings.py
  BLUE and RED are defined as 0 and 1 respectively.

  Defaults:
  THRESHOLD: a value between 0 and 1; the percentage of neighbors that must be of the opposing color before the node will flip. 
  RATE_OF_INCREASE: a value >=1; the value multiplied by the THRESHOLD between each round. Set to 1 to have no increase.
  RESOURCES: the number of resources an individual player may distribute in each round. 
  NUM_ROUNDS: the number of rounds run_game will play before it terminates. Used mostly for user vs computer play.
  MAX_BOOST: the highest possible boost either player can achieve via the logistic model. 
  STEEPNESS_K: the k value for the logistic model that determines how smooth or steep the curve will be. 

  Network Defaults:
  POLARIZATION: a value between 0.5 and 1; the percentage of the graph held by the more frequent color. 
  NUM_NODES: the number of nodes in each battlefield/graph.
  NUM_BATTELFIELDS: the number of battlefields across which players will distribute resources.
  WATTS_STROGATZ_K: the number of neighbors to connect each node to at the beginning of the Watts-Strogatz algorithm.
  WATTS_STROGATZ_P: the probability of transferring an edge in the Watts-Strogatz algorithm.

run_game.py
  simple_boost: usees a basic fraction to calculate the winning player's boost.
  logistic_boost: uses a logistic function to calculate the winning player's boost.
  get_user_input: helper function that prompts user for input. 
  run_game: This file contains the code necessary to run one round of the game. If you want to run multiple rounds,
  you have to keep calling run_game and giving it the updated battlefields. It modifies the battlefields itself, 
  but only returns the polarization. 

models.py:
  random_model: randomly generates values for one player.
  deterministic_modle: uses features of the graph to deterministically generate values for one player. 
  predictive_model: uses features of the graph to predict and oppose the deterministic model. 
  reactive_model: identical to predictive model, but chooses most difficult graphs rather than low-hanging fruit. 
  run: takes two models and plays them against each other until the graphs converge. 

main.py:
  Allows the user to play against the random model. Useful for getting to know how the game works. 

create_nodes.py:
  create_nodes: generates a graph with deterministic size, watts strogatz k, and watts strogatz p.
  color_nodes: colors the nodes red or blue. 
  
collect_data.py:
  This file can be run by itself and it will create battlefields and run them in autoplay until they converge,
  then output the data into a csv.
