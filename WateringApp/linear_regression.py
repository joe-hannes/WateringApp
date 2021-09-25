from statistics import  mean

def calc_params(temp, activations):
    """based on past temperatures and activations over an interval, calculate parameters to estimate interval

    param :temp: a list of temperature values over interval
    param :activations: a list of activations over an interval

    return: the parameters for linear regression ,
            -1 if no data exists to calculate the parameters

    """

    # TODO: check length of lists
    assert (len(temp) == len(activations)), "Temperature and activation lists do not have equal length"

    enum = 0
    denom = 0

    temp_mean = mean(temp)
    activation_mean = mean(activations)

    for i in range(len(temp)):
        temp_sub = temp[i] - temp_mean
        temp_sub_sq = temp_sub**2
        enum += temp_sub * (activations[i] - activation_mean)
        denom += temp_sub_sq

    # TODO: handle zero devison exception

    beta_one = enum / denom

    beta_zero = activation_mean - (beta_one * temp_mean)

    return beta_zero, beta_one

# print(beta_one)




def regress(temp, params):
    """calculate estimated interval

    param :temp: the avg temperatur of the intervall
    param :beta_one, beta_zero: linear regression parameters
    """

    activations = params[0] + params[1] * temp
    return activations
