import math

def beta_one(temp, activations):
    """based on past temperatures and activations over an interval, calculate parameters to estimate interval

    param :temp: a list of temperature values over interval
    param :activations: a list of activations over an interval
    """

    enum = 0
    denom = 0
    temp_mean = math.mean(temp)
    activation_mean = math.mean(activation)
    for i in range(len(temp_mean)-1):
        temp_sub = temp_mean[i] - temp_mean
        temp_sub_sq = temp_sub**2
        enum += temp_sub * (activations[i] - activation_mean)
        denom += temp_sub_sq

    beta_one = enum / denom

    beta_zero = activation_mean - (beta_one * temp_mean)

    return beta_one, beta_zero

# print(beta_one)




def regress(temp, beta_zero, beta_one):
    """calculate estimated interval

    param :temp: the avg temperatur of the intervall
    param :beta_one, beta_zero: linear regression parameters
    """

    interval = beta_zero + beta_one * temp
    return interval
