"""
	Dominik Suwala <dxs9411@rit.edu>
	2016-07-18
	coorelation_clustering.py
	Generates clusters based on a dissimilarity matrix. MindSumo SIG Challenge
	Dissimilarity is defined as (1-abs(correlation)) between value series of
	selected attributes. The correlation metric used is Pearon's R.
	A lower dissimilarity is therefore indicative of a tighter relationship
"""

import os
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats.stats import pearsonr
from scipy.cluster import hierarchy
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial import distance

"""
	Get column data as a list
"""
def getColData( colNum, fileName ):
	content = open( "./2YearStockData/" + fileName ).read()
	contentRows = content.split( '\r' )
	colData = []
	
	for row in contentRows[ 1: ]:
		colData.append( row.split( ',' )[ colNum ] )
	colData = map( np.double, colData )
	return colData

def main():
	fileList = os.listdir( "./2YearStockData/" )
	readOnce = open( "./2YearStockData/" + fileList[ 0 ] )
	columns = readOnce.read().split( '\r' )
	columns = columns[ 0 ].split( ',' )
	print( columns )
	
	while( True ):
		# Dissimilarity threshold
		threshold = 0.3
		print( '======\nSelect column to cluster by correlation:' )
		i = 0
		for col in columns:
			print( str( i ) + ': ' + col ) 
			i += 1
		col = int( raw_input() )
		
		# The code is data-series agnostic to allow for custom CSVs
		# where the user knows what they are doing, so certain queries
		# (i.e. correlation on date or text) are not defined/supported
		
		dissimilarity = []
		
		i = 0
		tups = {} # Dict of tuples keyed on indeces
		
		for a in range( len( fileList ) ):
			for b in range( len( fileList ) ):
				if( b > a ):
					key = str( a ) + ',' + str( b )
					val = pearsonr( getColData( col, fileList[ a ] ), getColData( col, fileList[ b ] ) )[ 0 ]
					tups[ key ] = val
		
		for a in range( len( fileList ) ):
			dissimilarity.append( [] )
			for b in range( len( fileList ) ):
				if( a == b ):
					dissimilarity[ a ].append( 0 )
				else:
					key = str( min( a, b ) ) + ',' + str( max( a, b ) )
					dissimilarity[ a ].append( np.double( 1 - abs( tups[ key ] ) ) )
		
		plt.figure( figsize=( 20, 10 ) )
		plt.title( 'Dendrogram (Lower Dissimilarity = Higher Correlation)' )
		Z = linkage( dissimilarity, method='complete', metric='correlation' )
		clusters = hierarchy.fcluster( Z, threshold, criterion='distance' )
		
		ind = 0
		totalClusters = max( clusters )
		outputClusters = [ [] for _ in range( totalClusters ) ]
		
		for clusterId in clusters:
			outputClusters[ clusterId - 1 ].append( fileList[ ind ].replace( '.csv', '' ) )
			ind +=1
		
		for thisCluster in range( len( outputClusters ) ):
			print( 'Cluster ' + str( thisCluster + 1 ) + ': ' + ', 	'.join( outputClusters[ thisCluster ] ) )
		
		labelFileList = [ i.replace('.csv','') for i in fileList ]
		hierarchy.dendrogram( Z, leaf_rotation=90, leaf_font_size=8, labels=labelFileList, color_threshold=threshold )
		plt.xlabel( 'Company Name' )
		plt.ylabel( 'Height' )
		plt.show()
		
		# View correlation (pearsonr) between any two symbols, keyed through
		# 0-based index. i.e 0,1 outputs correlation between symbols 0 and 1
		"""
		prompt = raw_input()
		while( prompt != 'next' ):
			print( tups[ prompt ] )
			prompt = raw_input()
		"""

if __name__ == '__main__':
	main()