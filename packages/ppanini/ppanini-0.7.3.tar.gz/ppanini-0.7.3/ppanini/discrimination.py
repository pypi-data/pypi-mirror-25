#!/usr/bin/env python

#print(__doc__)
#from ppanini import utilities
import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

def ncolors( n, colormap="jet" ):
        """utility for defining N evenly spaced colors across a color map"""
        cmap = plt.get_cmap( colormap )
        cmap_max = cmap.N
        return [cmap( int( k * cmap_max / (n - 1) ) ) for k in range( n )] 
def do_lda(X,y, target_names):
    

    #pca = PCA(n_components=2)
    #X_r = pca.fit(X).transform(X)
    
    lda = LinearDiscriminantAnalysis(n_components=len(set(y))-1)
    X_r2 = lda.fit(X, y).transform(X)
    #print(X_r2),
    #print(y)
    # Percentage of variance explained for each components
    #print('explained variance ratio (first two components): %s'
    #      % str(lda.explained_variance_ratio_))
    
    plt.figure()
    colors = ['navy', 'turquoise', 'darkorange'] #ncolors(n= len(set(y)))#
    lw = 2
    
    '''for color, i, target_name in zip(colors, [0, 1, 2], target_names):
        plt.scatter(X_r[y == i, 0], X_r[y == i, 1], color=color, alpha=.8, lw=lw,
                    label=target_name)
    plt.legend(loc='best', shadow=False, scatterpoints=1)
    plt.title('PCA of IRIS dataset')
    '''
    #plt.figure()
    plt.scatter(X_r2[:,0], X_r2[:,1], color =colors)
    for color, i, target_name in zip(colors, [0, 1, 2], target_names):
        plt.scatter(X_r2[y == i, 0], X_r2[y == i, 1], alpha=.8, color=color, label=target_name)
    plt.legend(loc='best', shadow=False, scatterpoints=1)
    plt.title('LDA of gene families (HMP2)')
    plt.savefig('/Users/rah/Documents/HMP2/figures/hmp2_lda.pdf', dpi=300)
    plt.savefig('/Users/rah/Documents/HMP2/figures/hmp2_lda.png', dpi=300)
    plt.show()
    
def main():
    iris = datasets.load_iris()
    import pandas as pd
    import csv, numpy
    import sys
    #df_in = pd.read_csv(str(sys.argv[0]), sep='\t', header=0, index_col =0)
    with open(sys.argv[1]) as f:
        reader = csv.reader(f, delimiter="\t")
        d = list(reader)
    d = numpy.asarray(d)
    labels = d[7, 1:]#iris.target
    target_names = list(set(labels))
    #print target_names
      #print (d[7][1:10])
    
    data = d[12:, 1:]#iris.data
    #print len(labels), len(labels[0]), labels
    data = [map(float, x) for x in  data]
    data = numpy.asarray(data).T
    #labels = numpy.asarray(labels)#.T#.tolist()
    #print labels
    labels = numpy.asarray([0 if value == 'nonIBD' else 1 if value =='UC' else 2 for value in labels ])
    #y= sorted(labels)
    #print y
    #print len(labels), len(data), len(data[0])
    # ['Normal', 'CD', 'UC'] #iris.target_names
    #print iris.data
    '''data = iris.data
    labels = iris.target
    target_names = iris.target_names'''
    #print data, labels, target_names
    do_lda(X = data, y = labels, target_names = target_names)
    return
if __name__ == '__main__':
    main()
