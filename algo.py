def calc_sma2(data, i, period):
    if i > period:
        data = data[i - period : i]
    i = 0
    for j in data:
        i += float(j)
    mean = i / len(data)
    return float("{:.2f}".format(mean))


def calc_sma(prices, period):
    sma = []

    for i in range(len(prices)):
        data = prices[: i + 1]
        sma.append(calc_sma2(data, i, period))

    return sma
