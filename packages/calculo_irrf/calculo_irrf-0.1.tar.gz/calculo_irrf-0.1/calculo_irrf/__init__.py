from decimal import Decimal

__all__ = ['calculo_irrf',]
"""
Tabelas de incidência mensal
A partir do mês de abril do ano-calendário de 2015:
----------------------------------------------------------------------------
| Base de cálculo (R$)     | Alíquota (%) | Parcela a deduzir do IRPF (R$) |
| Até 1.903,98             | -            | -                              |
| De 1.903,99 até 2.826,65 | 7,5          | 142,80                         |
| De 2.826,66 até 3.751,05 | 15           | 354,80                         |
| De 3.751,06 até 4.664,68 | 22,5         | 636,13                         |
| Acima de 4.664,68        | 27,5         | 869,36                         |
----------------------------------------------------------------------------

>>> tabela_teste =  {
>>>     1903.99 : 0.075,
>>>     2826.66 : 0.15,
>>>     3751.06 : 0.225,
>>>     4664.68 : 0.275,
>>> }
>>> print(calculo_irrf(valor=2000, tabela=tabela_teste))
Decimal('7.20')
"""

def calculo_irrf(valor, tabela):
    if valor <= 0:
        return Decimal('0')
    valor = Decimal('%.2f' % valor)
    faixas = [i for i in tabela.keys()]
    faixas.sort(reverse=True)
    valores = []
    for i in faixas:
        if valor >= i:
            valor_inicidente = valor-Decimal('%.2f' % i)+Decimal('0.01')
            valores.append(
                arredondar(valor_inicidente * Decimal('%.4f' % tabela[i]))
                )
            valor -= valor_inicidente
    if not valores:
        return Decimal('0')
    return sum(valores)

def arredondar(decimal):
    "Conforme ABNT NBR 5891:2014 - Regras de arredondamento"
    p_ar = decimal % Decimal('0.01')
    arr = (
        p_ar > 0.005 or
        (p_ar == Decimal('0.005') and (decimal-p_ar) % Decimal('0.02') > 0)
        )
    return decimal - p_ar + (Decimal('0.01') if arr else Decimal('0'))
