import statistics

def beta_one(temp, activations):
    """based on past temperatures and activations over an interval, calculate parameters to estimate interval

    param :temp: a list of temperature values over interval
    param :activations: a list of activations over an interval

    for i in range(len(x)-1):
  x_sub = x[i] - x_mean
  x_sub_sq = x_sub**2
  enum += x_sub * (medv[i] - medv_mean)
  denom += x_sub_sq
    """

    # TODO: check length of lists

    enum = 0
    denom = 0
    temp_mean = statistics.mean(temp)
    activation_mean = statistics.mean(activations)
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
