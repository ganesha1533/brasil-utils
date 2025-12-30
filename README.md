# 🇧🇷 Brasil Utils

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-brightgreen.svg)

**Biblioteca Python completa para validação e geração de dados brasileiros**

[Instalação](#-instalação) •
[Documentação](#-documentação) •
[Exemplos](#-exemplos) •
[Contribuir](#-contribuir)

</div>

---

## 🎯 O que é?

Brasil Utils é uma biblioteca Python **sem dependências externas** para validação e geração de documentos e dados brasileiros. Ideal para testes, desenvolvimento e validação de formulários.

## ⚡ Features

| Documento | Validar | Gerar | Formatar |
|-----------|:-------:|:-----:|:--------:|
| **CPF** | ✅ | ✅ | ✅ |
| **CNPJ** | ✅ | ✅ | ✅ |
| **PIS/PASEP** | ✅ | ✅ | ✅ |
| **Título de Eleitor** | ✅ | ❌ | ❌ |
| **CNH** | ✅ | ❌ | ❌ |
| **CEP** | ✅ | ❌ | ✅ |
| **Telefone** | ✅ | ✅ | ✅ |
| **Placa de Veículo** | ✅ | ✅ | ✅ |
| **Cartão de Crédito** | ✅ | ❌ | ✅ |
| **Bancos** | ✅ | ❌ | ❌ |

## 🚀 Instalação

```bash
git clone https://github.com/ganesha1533/brasil-utils.git
cd brasil-utils

# Ou simplesmente copie o arquivo brasil_utils.py para seu projeto
```

**Zero dependências!** Apenas Python 3.8+.

## 📖 Documentação

### CPF

```python
from brasil_utils import CPF

# Validar
CPF.validate("123.456.789-09")  # True ou False

# Gerar
cpf = CPF.generate()  # "123.456.789-09"
cpf = CPF.generate(formatted=False)  # "12345678909"

# Formatar
CPF.format("12345678909")  # "123.456.789-09"

# Informações
info = CPF.get_info("12345678909")
# {'cpf': '12345678909', 'formatted': '123.456.789-09', 'valid': True, 'estado_origem': 'SP'}
```

### CNPJ

```python
from brasil_utils import CNPJ

# Validar
CNPJ.validate("11.222.333/0001-81")  # True ou False

# Gerar
cnpj = CNPJ.generate()  # "11.222.333/0001-81"
cnpj = CNPJ.generate(filial=2)  # Gera filial específica

# Informações
info = CNPJ.get_info("11222333000181")
# {'cnpj': '11222333000181', 'formatted': '11.222.333/0001-81', 'valid': True, 'matriz': True, 'filial_numero': 1}
```

### Telefone

```python
from brasil_utils import Telefone

# Validar
Telefone.validate("11999998888")  # True

# Verificar tipo
Telefone.is_celular("11999998888")  # True

# Gerar
tel = Telefone.generate(celular=True, ddd="11")  # "(11) 99999-8888"

# Formatar
Telefone.format("11999998888")  # "(11) 99999-8888"
```

### Placa de Veículo

```python
from brasil_utils import Placa

# Validar
Placa.validate("ABC1234")  # True (formato antigo)
Placa.validate("ABC1D23")  # True (formato Mercosul)

# Verificar formato
Placa.is_mercosul("ABC1D23")  # True

# Gerar
placa = Placa.generate(mercosul=True)  # "ABC1D23"
placa = Placa.generate(mercosul=False)  # "ABC-1234"
```

### CEP

```python
from brasil_utils import CEP

# Validar formato
CEP.validate("01310100")  # True

# Formatar
CEP.format("01310100")  # "01310-100"

# Identificar estado
CEP.get_estado("01310100")  # "SP"
CEP.get_estado("20040020")  # "RJ"
```

### Cartão de Crédito

```python
from brasil_utils import CartaoCredito

# Validar (algoritmo de Luhn)
CartaoCredito.validate("4111111111111111")  # True

# Identificar bandeira
CartaoCredito.get_bandeira("4111111111111111")  # "visa"
CartaoCredito.get_bandeira("5500000000000004")  # "mastercard"

# Formatar
CartaoCredito.format("4111111111111111")  # "4111 1111 1111 1111"
```

### Detecção Automática

```python
from brasil_utils import BrasilUtils

# Detecta automaticamente o tipo de dado
result = BrasilUtils.auto_validate("123.456.789-09")
# {'type': 'cpf', 'valid': True, 'formatted': '123.456.789-09'}

result = BrasilUtils.auto_validate("11999998888")
# {'type': 'telefone', 'valid': True, 'formatted': '(11) 99999-8888', 'celular': True}

result = BrasilUtils.auto_validate("ABC1D23")
# {'type': 'placa', 'valid': True, 'formatted': 'ABC1D23', 'mercosul': True}
```

## 🔧 CLI

```bash
# Validar qualquer dado
python brasil_utils.py 123.456.789-09
python brasil_utils.py 11.222.333/0001-81
python brasil_utils.py 11999998888
python brasil_utils.py ABC1D23
```

## 📊 Tabela de DDDs

O módulo `Telefone` inclui todos os DDDs válidos do Brasil e identifica automaticamente a região.

## 🏦 Bancos Suportados

```python
from brasil_utils import Banco

# Informações de banco pelo código
Banco.get_info("341")  # {'nome': 'Itaú', 'tipo': 'Comercial'}
Banco.get_info("260")  # {'nome': 'Nubank', 'tipo': 'Digital'}

# Listar todos
todos = Banco.list_all()
```

## ⚠️ Aviso Legal

Esta biblioteca é para fins **educacionais e de desenvolvimento**:

- Dados gerados são **fictícios** e matematicamente válidos
- **Não** devem ser usados para fraude ou atividades ilegais
- Ideal para testes, validação de formulários e desenvolvimento

## 🤝 Contribuir

1. Fork o projeto
2. Crie sua branch (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Add: nova feature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

---

<div align="center">

### 🎨 Desenvolvido por **VanGogh Dev**

[![GitHub](https://img.shields.io/badge/GitHub-ganesha1533-black?style=flat&logo=github)](https://github.com/ganesha1533)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-+595%20987%20352983-25D366?style=flat&logo=whatsapp)](https://wa.me/595987352983)

**☕ Me apoie:**

[![Crypto](https://img.shields.io/badge/Donate-Crypto-orange?style=flat&logo=bitcoin)](https://plisio.net/donate/phlGd6L5)
[![Donate](https://img.shields.io/badge/Donate-PIX%2FOther-green?style=flat)](https://vendas.snoopintelligence.space/#donate)

</div>


