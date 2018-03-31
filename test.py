from numpy import mat, ones, zeros, random, append, argmax, round, multiply
from predict import predict
from random import randint
from network import Network, RandomNetwork

featuresInput = mat([[0.8811651, 0.23581383, 0.17974721, 0.67861582]])

weigthsLayer1 = mat([[0.99432703, 0.24572309, 0.68608379, 0.40004707, 0.66598601],
                     [0.70197419, 0.35910313, 0.2677427, 0.94146031, 0.94605904],
                     [0.80076253, 0.31943012, 0.30837179, 0.74619264, 0.63441821],
                     [0.94715879, 0.75585274, 0.19069712, 0.64035945, 0.35072943],
                     [0.35471748, 0.18253035, 0.28165175, 0.83779806, 0.31040002],
                     [0.92432488, 0.1955757, 0.98399418, 0.69450245, 0.94505385]])

weigthsLayer2 = mat([[0.94012599, 0.81365859, 0.96482615, 0.28366462, 0.16048148,
                      0.82270952, 0.22885948],
                     [0.74267231, 0.29537496, 0.39415236, 0.67715737, 0.41649228,
                      0.9974577, 0.04451441],
                     [0.54504325, 0.68236789, 0.70653258, 0.55575627, 0.13546398,
                      0.56770818, 0.66565225]])

net = Network([weigthsLayer1, weigthsLayer2], inputCount=4, outputCount=4, activationCount=6)

rnet1 = RandomNetwork()
rnet2 = RandomNetwork()

print("net1", rnet1.predict(featuresInput))
print("net2", rnet2.predict(featuresInput))

child = Network.children(rnet1, rnet2)

print("child", child.predict(featuresInput))
