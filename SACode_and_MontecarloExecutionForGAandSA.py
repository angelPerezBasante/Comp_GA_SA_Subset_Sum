import os.path
import subprocess
import numpy as np
import math
from subprocess import STDOUT, PIPE
import matplotlib.pyplot as plt

###SA code and Montecarlo Code to execute GA and SA

#Compilation of ssGA code in Java
def compile_java(java_file):
    subprocess.check_call(['javac', java_file])

#execution of ssGA code in Java
def execute_java(java_file, args):
    java_class, ext = os.path.splitext(java_file)
    cmd = ['java', '-cp', '', java_class] + args
    process = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, universal_newlines=True)
    stdout, stderr = process.communicate()
    print(stdout)
    exitSplit = stdout.split("\n")
    fitnessArray = []
    evalNumArray = []
    for item in exitSplit:
        subl = []
        for num in item.split(' '):
            if num.isnumeric():
                evalNumArray.append(int(num))
            elif isfloat(num):
                fitnessArray.append(float(num))
    return evalNumArray, fitnessArray
    #print(exitArray)

#isfloat function
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

#Simulated Annealing
def SA (seed,Tinit,alpha,Nt,gn,evaluationCounterLimit):
    #seed for random number generator
    #gn number of genes in the chromosome
    #Tinit: initial temperature
    #alpha: Temperature decay coefficient
    #Nt: # of iterations for bit modifications at every T
    #evaluationCounterLimit: evaluation counter limit
    gl=1 #Number of bits per gene
    T=Tinit #Initialize temperature
    #Initialize arrays to store fitness and evaluation counter
    evalCounterArray = []
    fitnessBestArray = []
    #Random generator based on Seed
    np.random.seed(seed)
    #Random generation of initial solution
    solutionBest = gen_init_solSA(gn, gl)
    #Evaluate the initial solution.
    fitnessBest = subset_sum(solutionBest)
    evaluationCounter=1
    #print(evaluationCounter)
    fitnessBestArray.append(fitnessBest[0])
    evalCounterArray.append(evaluationCounter)
    while evaluationCounter < evaluationCounterLimit: #SA iterations
        for i in range(0, Nt):
            if evaluationCounter == evaluationCounterLimit:
                break
            solution = solutionBest
            int1 = np.random.randint(0, gn-1) #generate integer with uniform distribution: ith index
            int2 = np.random.randint(0, gn-1)  # generate integer with uniform distribution: jth index
            while int1==int2:
                int2 = np.random.randint(0, gn-1)
            #swap the ith and jth genes of the chromosome with each other
            interm = solution[int1]
            solution[int1] = solution[int2]
            solution[int2] = interm

            #Negate ith and jth genes with 0.5 probability
            rand1 = np.random.random() #random number [0,1)
            rand2 = np.random.random()  # random number [0,1)
            if rand1>0.5:
                solution[int1] = 1-solution[int1]
            if rand2>0.5:
                solution[int2] = 1-solution[int2]

            fitnessNew = subset_sum(solution)
            if fitnessNew>=fitnessBest: #acceptance of better solutions
                fitnessBest = fitnessNew
                solutionBest = solution
            elif math.exp(-(fitnessBest-fitnessNew)/T)>np.random.random(): #acceptance condition for worse solutions
                fitnessBest = fitnessNew
                solutionBest = solution

            evaluationCounter = evaluationCounter+1
            #print(evaluationCounter)
            #print(fitnessBest[0])
            fitnessBestArray.append(fitnessBest[0])
            evalCounterArray.append(evaluationCounter)
        T=alpha*T#reduction of temperature
    return evalCounterArray, fitnessBestArray


#Generation of initial solution for SA
def gen_init_solSA(gn,gl):
    solution = np.zeros((gn*gl,1))
    for i in range(0, solution.size):
        if np.random.random() > 0.5:
            solution[i] = 1
        else:
            solution[i] = 0
    return solution

#subset_sum evaluation function
def subset_sum(solution):
    w = [2902, 5235, 357, 6058, 4846, 8280, 1295, 181, 3264,
          7285, 8806, 2344, 9203, 6806, 1511, 2172, 843, 4697,
           3348, 1866, 5800, 4094, 2751, 64, 7181, 9167, 5579,
           9461, 3393, 4602, 1796, 8174, 1691, 8854, 5902, 4864,
           5488, 1129, 1111, 7597, 5406, 2134, 7280, 6465, 4084,
           8564, 2593, 9954, 4731, 1347, 8984, 5057, 3429, 7635,
           1323, 1146, 5192, 6547, 343, 7584, 3765, 8660, 9318,
           5098, 5185, 9253, 4495, 892, 5080, 5297, 9275, 7515,
           9729, 6200, 2138, 5480, 860, 8295, 8327, 9629, 4212,
           3087, 5276, 9250, 1835, 9241, 1790, 1947, 8146, 8328,
           973, 1255, 9733, 4314, 6912, 8007, 8911, 6802, 5102,
           5451, 1026, 8029, 6628, 8121, 5509, 3603, 6094, 4447,
           683, 6996, 3304, 3130, 2314, 7788, 8689, 3253, 5920,
           3660, 2489, 8153, 2822, 6132, 7684, 3032, 9949, 59,
           6669, 6334]
    C = 300500

    fitness = 0.0
    if solution.size!=len(w):
        print("Length mismatch error in Subset sum function.")
    for i in range(0, solution.size):
        fitness = fitness + solution[i]*w[i]

    if fitness>C:
      fitness = C-(fitness*0.1)
      if fitness<0.0:
        fitness=0.0

    return fitness

#Execute a Montecarlo Method to adjust the hyper-parameters and compare both GA and SA algorithms
seedMontIni=100
numMaxEval=100000
gn=128
numMont=100
#Definition of hyper-parameter ranges for GA
valuesPc = [0.5, 0.6, 0.7, 0.8, 0.9, 1]
valuesPm = [0.01, 0.1, 0.2, 0.3]
valuesPopsize = [50, 200, 400, 600]
arrayToSaveFile = np.zeros((numMaxEval,numMont+1))
for i in range(0, len(valuesPc)):
    for j in range(0, len(valuesPm)):
        for n in range(0, len(valuesPopsize)):
            numMaxEval = max(valuesPopsize[n],numMaxEval)
            for l in range(0, numMont):
                seedMont = seedMontIni*(l+1)#Different seed for every execution in Montecarlo Method
                param = "{} {} {} {} {} {}".format(gn, valuesPopsize[n], valuesPc[i], valuesPm[j], numMaxEval, seedMont)
                paramFileName = "{}_{}_{}_{}_{}_{}".format(gn, valuesPopsize[n], valuesPc[i], valuesPm[j], numMaxEval, seedMont)
                # GA execution
                compile_java(os.path.join('ga', 'ssGA', 'Exe.java'))
                [evalCounter, fitnessValue] = execute_java('ga/ssGA/Exe.class', param.split())
                arrayToSaveFile[:, 0] = evalCounter
                arrayToSaveFile[:, l + 1] = fitnessValue
                printString = "{} {} {} {}".format(i, j, n, l)
                print(printString)

            filename = ''.join(['./ResultsGA/',paramFileName])
            np.savetxt(filename, arrayToSaveFile)
            data = np.genfromtxt(filename)

#Definition of hyper-parameter ranges for SA
valuesTinit = [100, 10000, 100000]
valuesAlpha = [0.8, 0.9, 0.99]
valuesNt = [1, 10, 100]
arrayToSaveFile = np.zeros((numMaxEval,numMont+1))
for i in range(0, len(valuesTinit)):
    for j in range(0, len(valuesAlpha)):
        for n in range(0, len(valuesNt)):
            paramFileName = "{}_{}_{}_{}_{}_{}".format(gn, valuesTinit[i], valuesAlpha[j], valuesNt[n], numMaxEval,
                                                       seedMontIni * numMont)
            # if (not os.path.isfile(''.join(['./ResultsSA/', paramFileName]))):
            for l in range(0, numMont):
                seedMont = seedMontIni * (l+1)  # Different seed for every execution in Montecarlo Method
                [evalCounter, fitnessValue] = SA(seedMont, valuesTinit[i], valuesAlpha[j], valuesNt[n], gn, numMaxEval)
                # paramFileName = "{}_{}_{}_{}_{}".format(gn, valuesTinit[i], valuesAlpha[j], numMaxEval, seedMont)
                # [evalCounter, fitnessValue] = SA(seedMont, valuesTinit[i], valuesAlpha[j], gn, numMaxEval)
                arrayToSaveFile[:, 0] = evalCounter
                arrayToSaveFile[:, l + 1] = fitnessValue
                printString = "{} {} {} {}".format(i, j, n, l)
                # printString = "{} {} {}".format(i, j, l)
                print(printString)
            filename = ''.join(['./ResultsSA/',paramFileName])
            np.savetxt(filename, arrayToSaveFile)
            data = np.genfromtxt(filename)