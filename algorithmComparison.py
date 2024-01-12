import os.path
import subprocess
import numpy as np
import math
import matplotlib.pyplot as plt

#Mean calculation from Montecarlo results for GA
seedMontIni=100
numMaxEval=100000
gn=128
numMont=100
# Definition of hyper-parameter ranges for GA
valuesPc = [0.5, 0.6, 0.7, 0.8, 0.9, 1]
valuesPm = [0.01, 0.1, 0.2, 0.3]
valuesPopsize = [50, 200, 400, 600]
arrayToSaveFile = np.zeros((numMaxEval,numMont+1))
num = seedMontIni * numMont
for i in range(0, len(valuesPc)):
    for j in range(0, len(valuesPm)):
        for n in range(0, len(valuesPopsize)):
            paramFileName = "{}_{}_{}_{}_{}_{}".format(gn, valuesPopsize[n], valuesPc[i], valuesPm[j], numMaxEval, num)
            paramFileNameMean = "{}_{}_{}_{}_{}_{}_mean".format(gn, valuesPopsize[n], valuesPc[i], valuesPm[j], numMaxEval, num)
            filename = ''.join(['./ResultsGA/',paramFileName])
            filenameMean = ''.join(['./ResultsGA_mean/', paramFileNameMean])
            data = np.genfromtxt(filename)
            mean = np.zeros((numMaxEval,1))
            evaluations = np.zeros((numMaxEval,1))
            for r in range (0,numMaxEval):
                mean[r] = np.mean(data[r,1:numMont])
                evaluations[r] = data[r,0]
            np.savetxt(filenameMean, mean)

#Mean calculation from Montecarlo results for SA
# Definition of hyper-parameter ranges for SA
valuesTinit = [100, 10000, 100000]
valuesAlpha = [0.8, 0.9, 0.99]
valuesNt = [1, 10, 100]
num = seedMontIni * numMont
for i in range(0, len(valuesTinit)):
    for j in range(0, len(valuesAlpha)):
        for n in range(0, len(valuesNt)):
            paramFileName = "{}_{}_{}_{}_{}_{}".format(gn, valuesTinit[i], valuesAlpha[j], valuesNt[n], numMaxEval, num)
            paramFileNameMean = "{}_{}_{}_{}_{}_{}_mean".format(gn, valuesTinit[i], valuesAlpha[j], valuesNt[n], numMaxEval, num)
            filename = ''.join(['./ResultsSA/', paramFileName])
            filenameMean = ''.join(['./ResultsSA_mean/', paramFileNameMean])
            data = np.genfromtxt(filename)
            mean = np.zeros((numMaxEval, 1))
            evaluations = np.zeros((numMaxEval, 1))
            for r in range(0, numMaxEval):
                mean[r] = np.mean(data[r, 1:numMont])
                evaluations[r] = data[r, 0]
            np.savetxt(filenameMean, mean)

#Plot results for GA
valuesPc = [0.5, 0.6, 0.7, 0.8, 0.9, 1]
valuesPm = [0.01, 0.1, 0.2, 0.3]
valuesPopsize = [50, 200, 400, 600]
num = seedMontIni * numMont
j=0
n=3
i=3
fig, ax = plt.subplots()
for n in range(0, len(valuesPopsize)):
    paramFileNameMean = "{}_{}_{}_{}_{}_{}_mean".format(gn, valuesPopsize[n], valuesPc[i], valuesPm[j], numMaxEval, num)
    filenameMean = ''.join(['./ResultsGA_mean/', paramFileNameMean])
    mean = np.genfromtxt(filenameMean)
    ax.plot(mean, linewidth=2, markersize=10)
    str1 = ""
    for r in range(0, len(valuesPopsize)):
        str1 = ''.join([str1, ' popsize=', str(valuesPopsize[r])])
    ax.legend(str1.split(), fontsize=20)
ylim_low=300499
ylim_high=300501
# ylim_low=280000
# ylim_high=300600
plt.ylim(ylim_low,ylim_high)
plt.title('GA execution under different popsize values', fontsize=20)
plt.xlabel('Number of Evaluations', fontsize=20)
plt.ylabel('Mean Cost Function', fontsize=20)
for tick in ax.xaxis.get_major_ticks():
   tick.label.set_fontsize(20)
for tick in ax.yaxis.get_major_ticks():
   tick.label.set_fontsize(20)
plt.show()


#Plot results for SA
valuesTinit = [100, 10000, 100000]
valuesAlpha = [0.8, 0.9, 0.99]
valuesNt = [1, 10, 100]
num = seedMontIni * numMont
j=2
n=2
fig, ax = plt.subplots()
for i in range(0, len(valuesTinit)):
    paramFileNameMean = "{}_{}_{}_{}_{}_{}_mean".format(gn, valuesTinit[i], valuesAlpha[j], valuesNt[n],
                                                        numMaxEval, num)
    filenameMean = ''.join(['./ResultsSA_mean/', paramFileNameMean])
    mean = np.genfromtxt(filenameMean)
    ax.plot(mean, linewidth=2, markersize=10)
    str1 = ""
    for r in range(0, len(valuesTinit)):
        str1 = ''.join([str1, ' Tinit=', str(valuesTinit[r])])
    ax.legend(str1.split(), fontsize=20)
ylim_low=300480
ylim_high=300501
# ylim_low=280000
# ylim_high=300600
plt.ylim(ylim_low,ylim_high)
plt.title('SA execution under different Tinit values', fontsize=20)
plt.xlabel('Number of Evaluations', fontsize=20)
plt.ylabel('Mean Cost Function', fontsize=20)
for tick in ax.xaxis.get_major_ticks():
   tick.label.set_fontsize(20)
for tick in ax.yaxis.get_major_ticks():
   tick.label.set_fontsize(20)
plt.show()