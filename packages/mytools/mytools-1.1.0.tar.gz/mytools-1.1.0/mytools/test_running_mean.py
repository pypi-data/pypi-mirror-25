import numpy as np
from My_Utils import running_mean, running_median, running_mean_pandas, running_median_pandas
from binning import binning1D


np.random.seed(1)
data = np.random.random(20) * np.random.randint(1,20,20)
x = 5.

mean,_ = binning1D(data, x, setting='mean', normalize=False) 
median,_ = binning1D(data, x, setting='median', normalize=False) 
runmean = running_mean(data, x)
runmedian = running_median(data, x)
runmean_pandas = running_mean_pandas(data, x)
runmedian_pandas = running_median_pandas(data, x)




print data
print '---'
print 'mean', mean, '>>>', np.std(mean)
print 'runmean', runmean, '>>>', np.std(runmean)
print 'runmean_pandas', runmean_pandas, '>>>', np.std(runmean_pandas)
print '---'
print 'median', median, '>>>', np.std(median)
print 'runmedian', runmedian, '>>>', np.std(runmean)
print 'runmedian_pandas', runmedian_pandas, '>>>', np.std(runmedian_pandas)

# RUNMEDIAN DOES NOT AGREE WITH THE PANDAS IMPLEMENTATION


##::: COMPARISON 1 & 2:
##::: (copy code into ipython console)
#x = np.random.random(100000)
#N = 1000
#%timeit np.convolve(x, np.ones((N,))/N, mode='valid')
##10 loops, best of 3: 172 ms per loop
#
#%timeit running_mean(x, N)
##100 loops, best of 3: 6.72 ms per loop
#
#%timeit pd.rolling_mean(x, N)[N-1:]
##100 loops, best of 3: 4.74 ms per loop
#
#np.allclose(pd.rolling_mean(x, N)[N-1:], running_mean(x, N))
##True
