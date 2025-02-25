import numpy as np


def kurtosis(x):
    return np.mean(((x - x.min())/x.std())**4) - 3

def skewness(x):
    return np.mean(((x - x.min())/x.std())**3)

def RMS(x):
    return np.sqrt(np.mean(x**2))

def percentile_5th(x):
    return np.percentile(x, 5)

def percentile_10th(x):
    return np.percentile(x, 10)

def percentile_25th(x):
    return np.percentile(x, 25)

def percentile_50th(x):
    return np.percentile(x, 50)

def percentile_75th(x):
    return np.percentile(x, 75)

def percentile_90th(x):
    return np.percentile(x, 90)

def percentile_95th(x):
    return np.percentile(x, 95)

def mean(x):
    return np.mean(x)

def standard_deviation(x):
    return np.std(x)


func_map = {
    "Kurtosis": kurtosis,
    "Skewness": skewness,
    "Mean": mean,
    "Median": percentile_50th,
    "10th-Percentile": percentile_10th,
    "25th-Percentile": percentile_25th,
    "75th-Percentile": percentile_75th,
    "90th-Percentile": percentile_90th,
    "Standard Deviation": standard_deviation,
    "RMS": RMS,
    
}

STAT_LABELS = ['Mean', 'Median', '10th-Percentile', '25th-Percentile', '75th-Percentile', '90th-Percentile', 'RMS', 'Standard Deviation', 'Skewness', 'Kurtosis']

def get_statistics_with_line_formatting(df, statistics_label):
    line = f"{statistics_label:<20}"
    vals = df.apply(func_map.get(statistics_label), axis=0).values.tolist()
    for val in vals:
        rval = np.round(val, 2)
        line += f"{rval:<20}"
    return line