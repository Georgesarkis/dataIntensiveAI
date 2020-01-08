from sklearn import metrics

"""
    @author @MajedDalain @George Sarkisian
"""
def evaluateModel(y, ypredicted):
    MAE = metrics.mean_absolute_error( y, ypredicted, multioutput='uniform_average')

    R2 = metrics.r2_score(y, ypredicted)*100

    return MAE, R2
