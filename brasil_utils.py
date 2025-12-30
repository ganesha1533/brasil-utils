#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    BRASIL UTILS - by VanGogh Dev                               ║
║         Biblioteca Python para Validação e Geração de Dados Brasileiros        ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Validação e Geração de:
- CPF / CNPJ
- RG (vários estados)
- CNH
- Título de Eleitor
- PIS/PASEP
- Certidão de Nascimento/Casamento
- CEP
- Telefone
- Placa de Veículo
- Cartão de Crédito (Luhn)
- Email
- Banco/Agência/Conta
"""

import re
import random
import string
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime, date


# ═══════════════════════════════════════════════════════════════════════════════
# CPF
# ═══════════════════════════════════════════════════════════════════════════════

class CPF:
    """Validação e geração de CPF"""
    
    # Estado por dígito (regra antiga, antes de 1972)
    ESTADOS = {
        "0": "RS",
        "1": "DF/GO/MS/MT/TO",
        "2": "AC/AM/AP/PA/RO/RR",
        "3": "CE/MA/PI",
        "4": "AL/PB/PE/RN",
        "5": "BA/SE",
        "6": "MG",
        "7": "ES/RJ",
        "8": "SP",
        "9": "PR/SC"
    }
    
    @staticmethod
    def clean(cpf: str) -> str:
        """Remove formatação"""
        return re.sub(r'\D', '', cpf)
    
    @staticmethod
    def format(cpf: str) -> str:
        """Formata CPF: 000.000.000-00"""
        cpf = CPF.clean(cpf)
        if len(cpf) != 11:
            return cpf
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    
    @staticmethod
    def validate(cpf: str) -> bool:
        """Valida CPF"""
        cpf = CPF.clean(cpf)
        
        if len(cpf) != 11:
            return False
        
        # CPFs com dígitos repetidos são inválidos
        if cpf == cpf[0] * 11:
            return False
        
        # Calcula primeiro dígito verificador
        sum1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
        d1 = (sum1 * 10 % 11) % 10
        
        # Calcula segundo dígito verificador
        sum2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
        d2 = (sum2 * 10 % 11) % 10
        
        return cpf[-2:] == f"{d1}{d2}"
    
    @staticmethod
    def generate(formatted: bool = True) -> str:
        """Gera CPF válido"""
        # Gera 9 dígitos aleatórios
        cpf = [random.randint(0, 9) for _ in range(9)]
        
        # Calcula primeiro dígito verificador
        sum1 = sum(cpf[i] * (10 - i) for i in range(9))
        d1 = (sum1 * 10 % 11) % 10
        cpf.append(d1)
        
        # Calcula segundo dígito verificador
        sum2 = sum(cpf[i] * (11 - i) for i in range(10))
        d2 = (sum2 * 10 % 11) % 10
        cpf.append(d2)
        
        cpf_str = ''.join(map(str, cpf))
        return CPF.format(cpf_str) if formatted else cpf_str
    
    @staticmethod
    def get_info(cpf: str) -> Dict:
        """Retorna informações sobre o CPF"""
        cpf = CPF.clean(cpf)
        
        return {
            "cpf": cpf,
            "formatted": CPF.format(cpf),
            "valid": CPF.validate(cpf),
            "estado_origem": CPF.ESTADOS.get(cpf[8], "Desconhecido") if len(cpf) >= 9 else None
        }


# ═══════════════════════════════════════════════════════════════════════════════
# CNPJ
# ═══════════════════════════════════════════════════════════════════════════════

class CNPJ:
    """Validação e geração de CNPJ"""
    
    @staticmethod
    def clean(cnpj: str) -> str:
        """Remove formatação"""
        return re.sub(r'\D', '', cnpj)
    
    @staticmethod
    def format(cnpj: str) -> str:
        """Formata CNPJ: 00.000.000/0000-00"""
        cnpj = CNPJ.clean(cnpj)
        if len(cnpj) != 14:
            return cnpj
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    
    @staticmethod
    def validate(cnpj: str) -> bool:
        """Valida CNPJ"""
        cnpj = CNPJ.clean(cnpj)
        
        if len(cnpj) != 14:
            return False
        
        if cnpj == cnpj[0] * 14:
            return False
        
        def calc_digit(cnpj: str, weights: List[int]) -> str:
            total = sum(int(cnpj[i]) * weights[i] for i in range(len(weights)))
            remainder = total % 11
            return '0' if remainder < 2 else str(11 - remainder)
        
        w1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        w2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        
        d1 = calc_digit(cnpj, w1)
        d2 = calc_digit(cnpj + d1, w2)
        
        return cnpj[-2:] == d1 + d2
    
    @staticmethod
    def generate(formatted: bool = True, filial: int = 1) -> str:
        """Gera CNPJ válido"""
        # 8 dígitos base + 4 dígitos filial
        base = [random.randint(0, 9) for _ in range(8)]
        filial_digits = list(map(int, str(filial).zfill(4)))
        cnpj = base + filial_digits
        
        # Primeiro dígito verificador
        w1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum1 = sum(cnpj[i] * w1[i] for i in range(12))
        d1 = 0 if sum1 % 11 < 2 else 11 - sum1 % 11
        cnpj.append(d1)
        
        # Segundo dígito verificador
        w2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum2 = sum(cnpj[i] * w2[i] for i in range(13))
        d2 = 0 if sum2 % 11 < 2 else 11 - sum2 % 11
        cnpj.append(d2)
        
        cnpj_str = ''.join(map(str, cnpj))
        return CNPJ.format(cnpj_str) if formatted else cnpj_str
    
    @staticmethod
    def get_info(cnpj: str) -> Dict:
        """Retorna informações sobre o CNPJ"""
        cnpj = CNPJ.clean(cnpj)
        
        filial = int(cnpj[8:12]) if len(cnpj) >= 12 else None
        
        return {
            "cnpj": cnpj,
            "formatted": CNPJ.format(cnpj),
            "valid": CNPJ.validate(cnpj),
            "matriz": filial == 1 if filial else None,
            "filial_numero": filial
        }


# ═══════════════════════════════════════════════════════════════════════════════
# PIS/PASEP
# ═══════════════════════════════════════════════════════════════════════════════

class PIS:
    """Validação e geração de PIS/PASEP"""
    
    @staticmethod
    def clean(pis: str) -> str:
        return re.sub(r'\D', '', pis)
    
    @staticmethod
    def format(pis: str) -> str:
        """Formata PIS: 000.00000.00-0"""
        pis = PIS.clean(pis)
        if len(pis) != 11:
            return pis
        return f"{pis[:3]}.{pis[3:8]}.{pis[8:10]}-{pis[10]}"
    
    @staticmethod
    def validate(pis: str) -> bool:
        """Valida PIS/PASEP"""
        pis = PIS.clean(pis)
        
        if len(pis) != 11:
            return False
        
        weights = [3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        total = sum(int(pis[i]) * weights[i] for i in range(10))
        remainder = total % 11
        digit = 0 if remainder < 2 else 11 - remainder
        
        return int(pis[10]) == digit
    
    @staticmethod
    def generate(formatted: bool = True) -> str:
        """Gera PIS/PASEP válido"""
        pis = [random.randint(0, 9) for _ in range(10)]
        
        weights = [3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        total = sum(pis[i] * weights[i] for i in range(10))
        remainder = total % 11
        digit = 0 if remainder < 2 else 11 - remainder
        pis.append(digit)
        
        pis_str = ''.join(map(str, pis))
        return PIS.format(pis_str) if formatted else pis_str


# ═══════════════════════════════════════════════════════════════════════════════
# TÍTULO DE ELEITOR
# ═══════════════════════════════════════════════════════════════════════════════

class TituloEleitor:
    """Validação e geração de Título de Eleitor"""
    
    ESTADOS = {
        "01": "SP", "02": "MG", "03": "RJ", "04": "BA", "05": "RS",
        "06": "PR", "07": "CE", "08": "PE", "09": "SC", "10": "GO",
        "11": "MA", "12": "PB", "13": "PA", "14": "ES", "15": "PI",
        "16": "RN", "17": "AL", "18": "MT", "19": "MS", "20": "DF",
        "21": "SE", "22": "AM", "23": "RO", "24": "AC", "25": "AP",
        "26": "RR", "27": "TO", "28": "ZZ"  # Exterior
    }
    
    @staticmethod
    def clean(titulo: str) -> str:
        return re.sub(r'\D', '', titulo)
    
    @staticmethod
    def validate(titulo: str) -> bool:
        """Valida Título de Eleitor"""
        titulo = TituloEleitor.clean(titulo)
        
        if len(titulo) != 12:
            return False
        
        estado = titulo[8:10]
        
        # Primeiro dígito
        weights1 = [2, 3, 4, 5, 6, 7, 8, 9]
        sum1 = sum(int(titulo[i]) * weights1[i] for i in range(8))
        d1 = sum1 % 11
        if d1 == 0 and estado in ["01", "02"]:
            d1 = 1
        elif d1 == 0:
            d1 = 0
        elif d1 == 1:
            d1 = 0
        else:
            d1 = 11 - d1
        
        # Segundo dígito
        weights2 = [7, 8, 9]
        nums = [int(titulo[8]), int(titulo[9]), d1]
        sum2 = sum(nums[i] * weights2[i] for i in range(3))
        d2 = sum2 % 11
        if d2 == 0 and estado in ["01", "02"]:
            d2 = 1
        elif d2 == 0:
            d2 = 0
        elif d2 == 1:
            d2 = 0
        else:
            d2 = 11 - d2
        
        return titulo[10:] == f"{d1}{d2}"
    
    @staticmethod
    def get_estado(titulo: str) -> Optional[str]:
        """Retorna estado do título"""
        titulo = TituloEleitor.clean(titulo)
        if len(titulo) >= 10:
            codigo = titulo[8:10]
            return TituloEleitor.ESTADOS.get(codigo)
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# CNH
# ═══════════════════════════════════════════════════════════════════════════════

class CNH:
    """Validação de CNH"""
    
    CATEGORIAS = ["A", "B", "C", "D", "E", "AB", "AC", "AD", "AE"]
    
    @staticmethod
    def clean(cnh: str) -> str:
        return re.sub(r'\D', '', cnh)
    
    @staticmethod
    def validate(cnh: str) -> bool:
        """Valida CNH"""
        cnh = CNH.clean(cnh)
        
        if len(cnh) != 11:
            return False
        
        if cnh == cnh[0] * 11:
            return False
        
        # Primeiro dígito
        dsc = 0
        sum1 = sum(int(cnh[i]) * (9 - i) for i in range(9))
        d1 = sum1 % 11
        if d1 >= 10:
            d1 = 0
            dsc = 2
        
        # Segundo dígito
        sum2 = sum(int(cnh[i]) * (1 + i) for i in range(9))
        d2 = (sum2 % 11) - dsc
        if d2 < 0:
            d2 += 11
        if d2 >= 10:
            d2 = 0
        
        return cnh[9:] == f"{d1}{d2}"


# ═══════════════════════════════════════════════════════════════════════════════
# CEP
# ═══════════════════════════════════════════════════════════════════════════════

class CEP:
    """Validação e formatação de CEP"""
    
    # Faixas de CEP por estado
    FAIXAS = {
        "SP": [(1000000, 19999999)],
        "RJ": [(20000000, 28999999)],
        "ES": [(29000000, 29999999)],
        "MG": [(30000000, 39999999)],
        "BA": [(40000000, 48999999)],
        "SE": [(49000000, 49999999)],
        "PE": [(50000000, 56999999)],
        "AL": [(57000000, 57999999)],
        "PB": [(58000000, 58999999)],
        "RN": [(59000000, 59999999)],
        "CE": [(60000000, 63999999)],
        "PI": [(64000000, 64999999)],
        "MA": [(65000000, 65999999)],
        "PA": [(66000000, 68899999)],
        "AP": [(68900000, 68999999)],
        "AM": [(69000000, 69299999), (69400000, 69899999)],
        "RR": [(69300000, 69399999)],
        "AC": [(69900000, 69999999)],
        "DF": [(70000000, 72799999), (73000000, 73699999)],
        "GO": [(72800000, 72999999), (73700000, 76799999)],
        "TO": [(77000000, 77999999)],
        "MT": [(78000000, 78899999)],
        "RO": [(78900000, 78999999)],
        "MS": [(79000000, 79999999)],
        "PR": [(80000000, 87999999)],
        "SC": [(88000000, 89999999)],
        "RS": [(90000000, 99999999)],
    }
    
    @staticmethod
    def clean(cep: str) -> str:
        return re.sub(r'\D', '', cep)
    
    @staticmethod
    def format(cep: str) -> str:
        """Formata CEP: 00000-000"""
        cep = CEP.clean(cep)
        if len(cep) != 8:
            return cep
        return f"{cep[:5]}-{cep[5:]}"
    
    @staticmethod
    def validate(cep: str) -> bool:
        """Valida formato do CEP"""
        cep = CEP.clean(cep)
        return len(cep) == 8 and cep.isdigit()
    
    @staticmethod
    def get_estado(cep: str) -> Optional[str]:
        """Retorna estado pelo CEP"""
        cep = CEP.clean(cep)
        if not CEP.validate(cep):
            return None
        
        cep_num = int(cep)
        
        for estado, faixas in CEP.FAIXAS.items():
            for inicio, fim in faixas:
                if inicio <= cep_num <= fim:
                    return estado
        
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# TELEFONE
# ═══════════════════════════════════════════════════════════════════════════════

class Telefone:
    """Validação e formatação de telefone brasileiro"""
    
    # DDDs válidos
    DDDS = [
        "11", "12", "13", "14", "15", "16", "17", "18", "19",  # SP
        "21", "22", "24",  # RJ
        "27", "28",  # ES
        "31", "32", "33", "34", "35", "37", "38",  # MG
        "41", "42", "43", "44", "45", "46",  # PR
        "47", "48", "49",  # SC
        "51", "53", "54", "55",  # RS
        "61",  # DF
        "62", "64",  # GO
        "63",  # TO
        "65", "66",  # MT
        "67",  # MS
        "68",  # AC
        "69",  # RO
        "71", "73", "74", "75", "77",  # BA
        "79",  # SE
        "81", "87",  # PE
        "82",  # AL
        "83",  # PB
        "84",  # RN
        "85", "88",  # CE
        "86", "89",  # PI
        "91", "93", "94",  # PA
        "92", "97",  # AM
        "95",  # RR
        "96",  # AP
        "98", "99",  # MA
    ]
    
    @staticmethod
    def clean(phone: str) -> str:
        phone = re.sub(r'\D', '', phone)
        if phone.startswith("55") and len(phone) > 11:
            phone = phone[2:]
        return phone
    
    @staticmethod
    def format(phone: str) -> str:
        """Formata telefone: (00) 00000-0000 ou (00) 0000-0000"""
        phone = Telefone.clean(phone)
        
        if len(phone) == 11:  # Celular
            return f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"
        elif len(phone) == 10:  # Fixo
            return f"({phone[:2]}) {phone[2:6]}-{phone[6:]}"
        return phone
    
    @staticmethod
    def validate(phone: str) -> bool:
        """Valida telefone brasileiro"""
        phone = Telefone.clean(phone)
        
        if len(phone) not in [10, 11]:
            return False
        
        ddd = phone[:2]
        if ddd not in Telefone.DDDS:
            return False
        
        # Celular deve começar com 9
        if len(phone) == 11 and phone[2] != "9":
            return False
        
        return True
    
    @staticmethod
    def is_celular(phone: str) -> bool:
        """Verifica se é celular"""
        phone = Telefone.clean(phone)
        return len(phone) == 11 and phone[2] == "9"
    
    @staticmethod
    def generate(celular: bool = True, ddd: str = None, formatted: bool = True) -> str:
        """Gera telefone válido"""
        if ddd is None:
            ddd = random.choice(Telefone.DDDS)
        
        if celular:
            numero = "9" + ''.join([str(random.randint(0, 9)) for _ in range(8)])
        else:
            primeiro = random.choice(["2", "3", "4", "5"])
            numero = primeiro + ''.join([str(random.randint(0, 9)) for _ in range(7)])
        
        phone = ddd + numero
        return Telefone.format(phone) if formatted else phone


# ═══════════════════════════════════════════════════════════════════════════════
# PLACA DE VEÍCULO
# ═══════════════════════════════════════════════════════════════════════════════

class Placa:
    """Validação e geração de placas de veículo"""
    
    @staticmethod
    def clean(placa: str) -> str:
        return re.sub(r'[^A-Za-z0-9]', '', placa.upper())
    
    @staticmethod
    def validate(placa: str) -> bool:
        """Valida placa (formato antigo ou Mercosul)"""
        placa = Placa.clean(placa)
        
        if len(placa) != 7:
            return False
        
        # Formato antigo: AAA0000
        if re.match(r'^[A-Z]{3}[0-9]{4}$', placa):
            return True
        
        # Formato Mercosul: AAA0A00
        if re.match(r'^[A-Z]{3}[0-9][A-Z][0-9]{2}$', placa):
            return True
        
        return False
    
    @staticmethod
    def is_mercosul(placa: str) -> bool:
        """Verifica se é formato Mercosul"""
        placa = Placa.clean(placa)
        return bool(re.match(r'^[A-Z]{3}[0-9][A-Z][0-9]{2}$', placa))
    
    @staticmethod
    def format(placa: str) -> str:
        """Formata placa: AAA-0000 ou AAA0A00"""
        placa = Placa.clean(placa)
        if len(placa) != 7:
            return placa
        
        if Placa.is_mercosul(placa):
            return placa
        return f"{placa[:3]}-{placa[3:]}"
    
    @staticmethod
    def generate(mercosul: bool = True, formatted: bool = True) -> str:
        """Gera placa válida"""
        letras = string.ascii_uppercase
        
        if mercosul:
            placa = (
                random.choice(letras) +
                random.choice(letras) +
                random.choice(letras) +
                str(random.randint(0, 9)) +
                random.choice(letras) +
                str(random.randint(0, 9)) +
                str(random.randint(0, 9))
            )
        else:
            placa = (
                random.choice(letras) +
                random.choice(letras) +
                random.choice(letras) +
                ''.join([str(random.randint(0, 9)) for _ in range(4)])
            )
        
        return Placa.format(placa) if formatted else placa


# ═══════════════════════════════════════════════════════════════════════════════
# CARTÃO DE CRÉDITO (LUHN)
# ═══════════════════════════════════════════════════════════════════════════════

class CartaoCredito:
    """Validação de cartão de crédito (algoritmo de Luhn)"""
    
    BANDEIRAS = {
        "visa": r'^4[0-9]{12}(?:[0-9]{3})?$',
        "mastercard": r'^5[1-5][0-9]{14}$',
        "amex": r'^3[47][0-9]{13}$',
        "diners": r'^3(?:0[0-5]|[68][0-9])[0-9]{11}$',
        "discover": r'^6(?:011|5[0-9]{2})[0-9]{12}$',
        "jcb": r'^(?:2131|1800|35\d{3})\d{11}$',
        "elo": r'^((((636368)|(438935)|(504175)|(451416)|(636297))\d{0,10})|((5090|5067|5068|5069|6500|6504|6505|6507|6509|6516|6550)\d{0,12}))$',
        "hipercard": r'^(606282\d{10}(\d{3})?)|(3841\d{15})$'
    }
    
    @staticmethod
    def clean(numero: str) -> str:
        return re.sub(r'\D', '', numero)
    
    @staticmethod
    def validate(numero: str) -> bool:
        """Valida cartão usando algoritmo de Luhn"""
        numero = CartaoCredito.clean(numero)
        
        if not numero or len(numero) < 13 or len(numero) > 19:
            return False
        
        # Algoritmo de Luhn
        def luhn_checksum(card_number: str) -> int:
            def digits_of(n):
                return [int(d) for d in str(n)]
            
            digits = digits_of(card_number)
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            
            checksum = sum(odd_digits)
            for d in even_digits:
                checksum += sum(digits_of(d * 2))
            
            return checksum % 10
        
        return luhn_checksum(numero) == 0
    
    @staticmethod
    def get_bandeira(numero: str) -> Optional[str]:
        """Identifica bandeira do cartão"""
        numero = CartaoCredito.clean(numero)
        
        for bandeira, pattern in CartaoCredito.BANDEIRAS.items():
            if re.match(pattern, numero):
                return bandeira
        
        return None
    
    @staticmethod
    def format(numero: str) -> str:
        """Formata cartão: 0000 0000 0000 0000"""
        numero = CartaoCredito.clean(numero)
        return ' '.join([numero[i:i+4] for i in range(0, len(numero), 4)])


# ═══════════════════════════════════════════════════════════════════════════════
# BANCO / AGÊNCIA / CONTA
# ═══════════════════════════════════════════════════════════════════════════════

class Banco:
    """Informações de bancos brasileiros"""
    
    BANCOS = {
        "001": {"nome": "Banco do Brasil", "tipo": "Comercial"},
        "033": {"nome": "Santander", "tipo": "Comercial"},
        "104": {"nome": "Caixa Econômica Federal", "tipo": "Comercial"},
        "237": {"nome": "Bradesco", "tipo": "Comercial"},
        "341": {"nome": "Itaú", "tipo": "Comercial"},
        "356": {"nome": "Banco Real", "tipo": "Comercial"},
        "389": {"nome": "Banco Mercantil do Brasil", "tipo": "Comercial"},
        "399": {"nome": "HSBC", "tipo": "Comercial"},
        "422": {"nome": "Banco Safra", "tipo": "Comercial"},
        "453": {"nome": "Banco Rural", "tipo": "Comercial"},
        "633": {"nome": "Banco Rendimento", "tipo": "Comercial"},
        "652": {"nome": "Itaú Unibanco Holding", "tipo": "Comercial"},
        "745": {"nome": "Citibank", "tipo": "Comercial"},
        "756": {"nome": "Sicoob", "tipo": "Cooperativa"},
        "077": {"nome": "Banco Inter", "tipo": "Digital"},
        "260": {"nome": "Nubank", "tipo": "Digital"},
        "290": {"nome": "PagSeguro", "tipo": "Digital"},
        "323": {"nome": "Mercado Pago", "tipo": "Digital"},
        "380": {"nome": "PicPay", "tipo": "Digital"},
        "403": {"nome": "Cora", "tipo": "Digital"},
        "336": {"nome": "C6 Bank", "tipo": "Digital"},
        "212": {"nome": "Banco Original", "tipo": "Digital"},
        "655": {"nome": "Neon", "tipo": "Digital"},
    }
    
    @staticmethod
    def get_info(codigo: str) -> Optional[Dict]:
        """Retorna informações do banco"""
        codigo = codigo.zfill(3)
        return Banco.BANCOS.get(codigo)
    
    @staticmethod
    def list_all() -> Dict:
        """Lista todos os bancos"""
        return Banco.BANCOS


# ═══════════════════════════════════════════════════════════════════════════════
# CLASSE PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

class BrasilUtils:
    """Classe unificada com todas as utilidades"""
    
    cpf = CPF
    cnpj = CNPJ
    pis = PIS
    titulo_eleitor = TituloEleitor
    cnh = CNH
    cep = CEP
    telefone = Telefone
    placa = Placa
    cartao = CartaoCredito
    banco = Banco
    
    @staticmethod
    def auto_validate(value: str) -> Dict:
        """Detecta e valida automaticamente o tipo de dado"""
        cleaned = re.sub(r'\D', '', value)
        
        # CPF: 11 dígitos
        if len(cleaned) == 11 and not value.startswith("+"):
            if CPF.validate(cleaned):
                return {"type": "cpf", "valid": True, "formatted": CPF.format(cleaned)}
            if CNH.validate(cleaned):
                return {"type": "cnh", "valid": True, "value": cleaned}
            if PIS.validate(cleaned):
                return {"type": "pis", "valid": True, "formatted": PIS.format(cleaned)}
        
        # CNPJ: 14 dígitos
        if len(cleaned) == 14:
            return {"type": "cnpj", "valid": CNPJ.validate(cleaned), "formatted": CNPJ.format(cleaned)}
        
        # Título de Eleitor: 12 dígitos
        if len(cleaned) == 12:
            return {"type": "titulo_eleitor", "valid": TituloEleitor.validate(cleaned)}
        
        # CEP: 8 dígitos
        if len(cleaned) == 8:
            estado = CEP.get_estado(cleaned)
            return {"type": "cep", "valid": True, "formatted": CEP.format(cleaned), "estado": estado}
        
        # Telefone: 10-11 dígitos
        if len(cleaned) in [10, 11]:
            return {
                "type": "telefone",
                "valid": Telefone.validate(cleaned),
                "formatted": Telefone.format(cleaned),
                "celular": Telefone.is_celular(cleaned)
            }
        
        # Cartão de crédito: 13-19 dígitos
        if 13 <= len(cleaned) <= 19:
            return {
                "type": "cartao_credito",
                "valid": CartaoCredito.validate(cleaned),
                "bandeira": CartaoCredito.get_bandeira(cleaned)
            }
        
        # Placa
        placa_clean = re.sub(r'[^A-Za-z0-9]', '', value.upper())
        if len(placa_clean) == 7:
            return {
                "type": "placa",
                "valid": Placa.validate(placa_clean),
                "formatted": Placa.format(placa_clean),
                "mercosul": Placa.is_mercosul(placa_clean)
            }
        
        return {"type": "unknown", "valid": False}


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    import sys
    
    print("""
╔═══════════════════════════════════════════════════════════════╗
║              🇧🇷 BRASIL UTILS - by VanGogh Dev                 ║
║     Validação e Geração de Dados Brasileiros                  ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    if len(sys.argv) > 1:
        value = sys.argv[1]
        result = BrasilUtils.auto_validate(value)
        print(f"Valor: {value}")
        print(f"Tipo: {result['type']}")
        print(f"Válido: {result['valid']}")
        for k, v in result.items():
            if k not in ['type', 'valid']:
                print(f"{k}: {v}")
    else:
        print("Exemplos de uso:")
        print()
        print(f"  CPF válido: {CPF.generate()}")
        print(f"  CNPJ válido: {CNPJ.generate()}")
        print(f"  PIS válido: {PIS.generate()}")
        print(f"  Telefone: {Telefone.generate()}")
        print(f"  Placa Mercosul: {Placa.generate(mercosul=True)}")
        print(f"  Placa Antiga: {Placa.generate(mercosul=False)}")
        print()
        print("Uso: python brasil_utils.py <valor>")
        print("Exemplo: python brasil_utils.py 123.456.789-09")


if __name__ == "__main__":
    main()
