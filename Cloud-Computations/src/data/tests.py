import logging


def working():
    logger = logging.getLogger(__name__)
    logger.info('Working')
    #print("Working")

from collections import Counter

from math import log2
import pandas as pd
def kl_divergence(dataset1,dataset2):

    distributions1 = pd.DataFrame(Counter(dataset1).items())
    total1 = sum(distributions1[1])
    distributions2 = pd.DataFrame(Counter(dataset2).items())
    total2 = sum(distributions2[1])
    combined = pd.merge(distributions1, distributions2,left_on=0,right_on=0)

    p = [x/total1 for x in combined['1_x']]
    q = [x/total2 for x in combined['1_y']]
    return sum(p[i] * log2(p[i]/q[i]) for i in range(len(p)))

def kl_divergence_all(dataset1,dataset2):
    columns = dataset1.columns
    kls=[]
    for col in columns:
        if col in dataset2.columns:
            print(col)
            kl1 = kl_divergence(dataset1[col], dataset2[col])
            kl2 = kl_divergence(dataset2[col], dataset1[col])
            kls.append([kl1,kl2,col])
    return(kls)
def main():
    working()
    # dataset1= pd.read_csv("../data/processed/Montreal.csv")
    # print(kl_divergence(dataset1['rain'],dataset1['rain']))

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()