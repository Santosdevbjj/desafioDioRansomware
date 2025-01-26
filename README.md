# Ransomware Simples em Python - Bootcamp Santander Cibersegurança, parceria com DIO 

## 📘 Descrição do Projeto

Este projeto foi desenvolvido como parte do Bootcamp de Cibersegurança do Santander em parceria com a Digital Innovation One (DIO), com o objetivo de demonstrar os princípios fundamentais de um ransomware de forma educacional e ética.

## 🎯 Objetivo

Compreender os mecanismos internos de um ransomware, desenvolvendo uma aplicação em Python capaz de:
- Criptografar arquivos de forma segura
- Implementar um processo de descriptografia controlado
- Explorar conceitos de segurança cibernética na prática

## 🔒 Funcionalidades

- Criptografia de arquivos utilizando técnicas de segurança
- Descriptografia controlada de arquivos previamente criptografados
- Demonstração didática de técnicas de segurança da informação

## 📁 Estrutura do Projeto

- `readme.md`: Documentação do projeto
- `encrypter.py`: Script responsável pela criptografia de arquivos
- `decrypter.py`: Script para descriptografia dos arquivos
- `teste.txt`: Arquivo de exemplo para demonstração

## 🚀 Melhorias Implementadas

### Aprimoramentos Técnicos

1. **Tratamento de Erros**
   - Implementação de tratamento de exceções para prevenir falhas críticas
   - Garantia de execução robusta e resiliente

2. **Documentação do Código**
   - Adição de comentários detalhados
   - Melhoria da compreensão do código

3. **Modularização**
   - Separação de funções para maior reutilização
   - Código mais organizado e manutenível

4. **Segurança**
   - Validação de chave criptográfica
   - Checagem rigorosa do tamanho da chave (16 bytes)

5. **Experiência do Usuário**
   - Interface de terminal simples
   - Feedback claro durante operações

### Detalhes Técnicos das Melhorias

1. **Tratamento de Exceções**
   - Garante tratamento apropriado de erros
   - Previne interrupções inesperadas

2. **Gerenciamento de Arquivos**
   - Uso de `with` para abertura segura
   - Prevenção de vazamentos de recursos

3. **Validação Criptográfica**
   - Verificação precisa do tamanho da chave
   - Compatibilidade com padrão AES

4. **Padronização**
   - Extensão `.encrypted` para arquivos criptografados
   - Consistência no processo de criptografia

## 🔧 Execução do Projeto

### Pré-requisitos
- Python 3.x
- Biblioteca de criptografia instalada

### Passos para Uso

1. **Criptografia**
   ```
   python encrypter.py
   ```

2. **Descriptografia**
   ```
   python decrypter.py
   ```

### Arquivo de Teste

Conteúdo de `teste.txt`:
```
Este é um arquivo de teste para o ransomware.
```

## ⚠️ Aviso Importante

**Atenção**: Este código é estritamente para fins educacionais e de pesquisa em cibersegurança. 

**Diretrizes Éticas**:
- Nunca utilize este código para fins maliciosos
- Sempre obtenha permissão explícita antes de realizar qualquer teste
- Respeite os princípios éticos da segurança da informação

## 🙏 Agradecimentos

Agradecimento especial à Digital Innovation One (DIO) e ao Banco Santander por proporcionar esta oportunidade única de aprendizado em cibersegurança.

## 📜 Licença

**Licença de Uso Livre - Código:Livre007**

O projeto foi elaborado unicamente para fins didáticos e educacionais. 

Condições de Uso:
- Livre distribuição
- Uso educacional irrestrito
- Proibido uso comercial ou malicioso
- Manutenção dos créditos originais

## 🔗 Contato

[Perfil no LinkedIn](https://www.linkedin.com/in/sergio-luiz-dos-santos-3b081a326)

Fique à vontade para entrar em contato para discussões sobre cibersegurança, programação ou projetos educacionais.
