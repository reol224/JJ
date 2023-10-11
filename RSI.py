period = 0
prev_avg_gain = 0
prev_avg_loss = 0
rsi = []


def compute_moving_average(series):
    if len(rsi) == 0:
        sum_gain = 0
        sum_loss = 0
        for v1, v2 in zip(series[:-1], series[1:]):
            if v2 > v1:
                sum_gain += v2 - v1
            elif v1 > v2:
                sum_loss += v1 - v2
        avg_gain = sum_gain / period
        avg_loss = sum_loss / period
    else:
        if series[-1] >= series[-2]:
            gain = series[-1] - series[-2]
            loss = 0
        elif series[-2] > series[-1]:
            gain = 0
            loss = series[-2] - series[-1]
        avg_gain = (gain + ((period - 1) * prev_avg_gain)) / period
        avg_loss = (loss + ((period - 1) * prev_avg_loss)) / period
    prev_avg_gain = avg_gain
    prev_avg_loss = avg_loss
    return avg_gain, avg_loss


def compute_single_rsi(series):
    avg_gain, avg_loss = compute_moving_average(series)
    if avg_loss == 0:
        rsi = 100
    else:
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
    return rsi


def compute_rsi(series):
    rsi = []
    for i in range(period, len(series)):
        rsi.append(compute_single_rsi(series[i - period:i + 1]))
    return rsi
