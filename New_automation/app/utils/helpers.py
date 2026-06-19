"""
Funções auxiliares de formatação e validação.
"""
import re
from config.constants import MESES_PT


def clean_numbers(text: str) -> str:
    """Remove todos os caracteres não numéricos de uma string."""
    return "".join(filter(str.isdigit, str(text)))


def format_cnpj(cnpj: str) -> str:
    """Formata uma string de 14 dígitos no padrão XX.XXX.XXX/XXXX-XX."""
    cnpj = clean_numbers(cnpj)
    if len(cnpj) == 14:
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    return cnpj


def format_cpf(cpf: str) -> str:
    """Formata uma string de 11 dígitos no padrão XXX.XXX.XXX-XX."""
    cpf = clean_numbers(cpf)
    if len(cpf) == 11:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return cpf


def build_periodo_em_data(data_inicio, data_fim) -> str:
    """
    Gera string curta de período contábil.
    Ex: '01/24 a 12/24' ou '01/23 a 12/24' (quando anos diferentes).
    """
    mi = str(data_inicio.month).zfill(2)
    ai = str(data_inicio.year)[-2:]
    mf = str(data_fim.month).zfill(2)
    af = str(data_fim.year)[-2:]

    if data_inicio.year != data_fim.year:
        return f"{mi}/{ai} a {mf}/{af}"
    return f"{mi} a {mf}/{af}"


def build_periodo_anual(data_inicio, data_fim) -> str:
    """
    Gera descrição longa do período contábil.
    Ex: 'Janeiro a Dezembro de 2024'
    """
    mi = MESES_PT[data_inicio.month]
    mf = MESES_PT[data_fim.month]

    if data_inicio.year == data_fim.year:
        return f"{mi} a {mf} de {data_inicio.year}"
    return f"{mi} de {data_inicio.year} a {mf} de {data_fim.year}"


def validate_cnpj(cnpj: str) -> bool:
    """Valida CNPJ usando algoritmo oficial."""
    cnpj = clean_numbers(cnpj)
    if len(cnpj) != 14 or len(set(cnpj)) == 1:
        return False

    def calc_digit(cnpj_digits, weights):
        total = sum(int(d) * w for d, w in zip(cnpj_digits, weights))
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder

    weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    d1 = calc_digit(cnpj[:12], weights1)
    d2 = calc_digit(cnpj[:13], weights2)
    return int(cnpj[12]) == d1 and int(cnpj[13]) == d2


def validate_cpf(cpf: str) -> bool:
    """Valida CPF usando algoritmo oficial."""
    cpf = clean_numbers(cpf)
    if len(cpf) != 11 or len(set(cpf)) == 1:
        return False

    def calc_digit(cpf_digits, factor):
        total = sum(int(d) * f for d, f in zip(cpf_digits, range(factor, 1, -1)))
        remainder = (total * 10) % 11
        return remainder if remainder < 10 else 0

    d1 = calc_digit(cpf[:9], 10)
    d2 = calc_digit(cpf[:10], 11)
    return int(cpf[9]) == d1 and int(cpf[10]) == d2