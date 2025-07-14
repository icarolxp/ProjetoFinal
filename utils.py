from functools import reduce

def filtrar_dias_quentes(df, limite=30):
    return list(filter(lambda linha: linha['temperatura'] > limite, df.to_dict('records')))

def somar_precipitacao(df):
    return reduce(lambda acc, val: acc + val, df['precipitacao'])
