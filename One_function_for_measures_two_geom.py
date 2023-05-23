import itertools
import numpy


def measures(N, a, b):
    ra = [x for x in range(0, N)]
    numbers = [(a / b) ** x for x in ra]
    alloptions = [seq for i in range(N, 0, -1)
                  for seq in itertools.combinations(numbers, i)]
    sumi = [sum(i) for i in alloptions]
    leni = [len(i) for i in alloptions]

    #print(numbers)
    #print(alloptions)

    overallsumsabs = []
    overallsumseu = []
    overallsumskl = []
    overallsumskl2 = []
    worlds = []



    for i, z, j in zip(range(len(alloptions)), sumi, leni):
        #print(j)
        evidence = [x for x in ra if (a / b) ** x in alloptions[i] and len(alloptions[i])>1]
        evidenceclean = [i for i in evidence if i != []]
        worlds.append(evidenceclean)

        listabs = [abs(((1 / j) - (((a / b) ** k) / z))) for k in evidence if k !=[]] # sum of absolute values
        if listabs != []:
            overallsumsabs.append(sum(listabs))

        listeu = [((1 / j) - (((a / b) ** k) / z)) ** 2 for k in evidence if k !=[]] # squared Euclidean distance
        #print(listeu)
        if listeu != []:
            overallsumseu.append(sum(listeu))

        listkl = [(1 / j) * numpy.log((1 / j) / (((a / b) ** k) / z)) # kl-divergence
                    for k in evidence if k !=[]]
        if listkl != []:
            overallsumskl.append(sum(listkl))

        listkl2 = [(((a / b) ** k) / z) * numpy.log( (((a / b) ** k) / z)/(1 / j))  # kl-divergence
                  for k in evidence if k != []]
        if listkl2 != []:
            overallsumskl2.append(sum(listkl2))


    overalldiffioverviewabs = list(zip(overallsumsabs, worlds))
    minimalabs = [min(overalldiffioverviewabs)]

    overalldiffiovervieweu = list(zip(overallsumseu, worlds))
    minimaleu = [min(overalldiffiovervieweu)]

    overalldiffioverviewkl = list(zip(overallsumskl, worlds))
    minimalkl = [min(overalldiffioverviewkl)]

    overalldiffioverviewkl2 = list(zip(overallsumskl2, worlds))
    minimalkl2 = [min(overalldiffioverviewkl2)]


    print(minimalabs)
    print(minimaleu)
    print(minimalkl)
    print(minimalkl2)


measures(12, 125, 187)
