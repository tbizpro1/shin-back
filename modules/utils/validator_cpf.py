import re

def validar_cpf(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', cpf)
    
    if len(cpf) != 11:
        return False
    
    if cpf == cpf[0] * 11:
        return False
    
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    primeiro_digito = (soma * 10) % 11
    if primeiro_digito == 10:
        primeiro_digito = 0
    if primeiro_digito != int(cpf[9]):
        return False
    
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    segundo_digito = (soma * 10) % 11
    if segundo_digito == 10:
        segundo_digito = 0
    if segundo_digito != int(cpf[10]):
        return False
    
    return True
