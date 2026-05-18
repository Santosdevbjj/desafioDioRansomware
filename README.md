## Bootcamp Santander Cibersegurança #2 · DIO

<img width="892" height="902" alt="Screenshot_20250822-165653" src="https://github.com/user-attachments/assets/9576e30c-d8c6-4a0d-ae5e-84b1626921b4" />

---

> ⚠️ **Aviso Legal:** Este projeto foi desenvolvido exclusivamente para fins educacionais como parte de bootcamp certificado de cibersegurança, sob orientação do instrutor Cassiano Peres. O código demonstra os mecanismos internos de criptografia de arquivo para que profissionais de segurança possam entender, detectar e mitigar esse tipo de ameaça. O uso deste código para criptografar arquivos de terceiros sem autorização expressa configura crime previsto na Lei nº 12.737/2012 e no Art. 154-A do Código Penal Brasileiro. Todos os testes foram realizados sobre o arquivo `teste.txt`, sem envolvimento de arquivos de sistema ou dados de terceiros.

---

# Entendendo um Ransomware na Prática — Criptografia AES-CTR em Python

---

## 1. Problema de Negócio

Ransomware é a categoria de ataque cibernético que mais cresce globalmente e a que mais causa dano financeiro mensurável. O custo médio de um ataque em 2024 superou USD 4,9 milhões por incidente, incluindo tempo de inatividade, recuperação e reputação. Ainda assim, a maioria das equipes de segurança investe em detecção de assinaturas — uma estratégia eficaz apenas contra variantes conhecidas.

O problema técnico central é preciso: equipes que nunca implementaram os dois lados do ciclo — criptografia e descriptografia — não entendem os pontos de intervenção disponíveis. Não sabem onde um SIEM pode disparar um alerta, onde backups se tornam inúteis, ou por que a janela entre infecção e criptografia completa define a diferença entre contenção e perda total.

Este projeto resolve essa lacuna: implementa em Python os dois componentes fundamentais do ciclo — `encrypter.py` e `decrypter.py` — usando AES no modo CTR, documentando cada decisão técnica com seu impacto na detecção e na defesa. O entregável não é o ataque: é o conhecimento operacional que habilita respostas de segurança calibradas para o mecanismo real.

---

## 2. Contexto

O projeto foi desenvolvido como desafio prático do **Bootcamp Santander Cibersegurança #2** na DIO. O objetivo era implementar os dois componentes de criptografia simétrica que definem o ciclo de um ransomware — e documentar cada escolha técnica do ponto de vista de quem precisa detectar e reverter o ataque.

A decisão de implementar **dois scripts independentes** em vez de um único programa com menu não foi organizacional. Ela espelha a arquitetura real: o encrypter é distribuído pelo atacante no momento da infecção; o decrypter só é entregue mediante pagamento, permanecendo sob controle do atacante como alavanca de negociação. Estudar os dois separadamente é a forma mais honesta de entender a assimetria de poder que torna o ransomware tão eficaz como vetor de extorsão.

---

## 3. Premissas

- A biblioteca `pyaes` implementa AES puro em Python, sem dependências de OpenSSL ou binários nativos — escolha deliberada para portabilidade e transparência do código, priorizando didática sobre performance;
- O modo **CTR (Counter Mode)** transforma AES em cifra de fluxo, eliminando a necessidade de padding e permitindo criptografar arquivos de qualquer tamanho sem ajustes no conteúdo;
- A chave `b"chave_segura_16b"` (16 bytes) é hardcoded exclusivamente para fins de demonstração — em um sistema real, a chave seria gerada aleatoriamente por instância, enviada ao servidor C2 e nunca armazenada localmente;
- O comportamento de **remover o arquivo original antes de salvar o criptografado** (`os.remove()` antes de `open("wb")`) é intencional — replica a mecânica destrutiva de ransomwares reais que não mantêm cópia em texto claro após a criptografia;
- Todos os testes foram realizados sobre `teste.txt`, sem envolvimento de arquivos de sistema ou dados reais.

---

## 4. Estratégia da Solução

A implementação foi estruturada em torno de duas funções simétricas e inversas:

```
teste.txt (legível)
      ↓ encrypter.py
os.remove(teste.txt) → teste.txt.encrypted (ilegível sem a chave)
      ↓ decrypter.py (mesma chave)
os.remove(teste.txt.encrypted) → teste.txt (restaurado)
```

**`encrypt_file(file_name, key)` — o lado do atacante:**

1. Leitura do arquivo em modo binário (`"rb"`) com bloco `with`, garantindo fechamento do file handle mesmo em caso de exceção;
2. `os.remove(file_name)` — o arquivo original deixa de existir antes que o criptografado seja gravado. Esta é a decisão mais destrutiva do código: qualquer falha entre o `remove` e o `open("wb")` resulta em perda permanente;
3. Instanciação de `pyaes.AESModeOfOperationCTR(key)` e aplicação de `.encrypt()` sobre os bytes lidos;
4. Gravação do resultado em `{nome_original}.encrypted` — a extensão funciona como marcador para o script de recuperação localizar arquivos afetados.

**`decrypt_file(encrypted_file, key)` — o lado da recuperação:**

1. Leitura do arquivo `.encrypted` em modo binário;
2. Instanciação do mesmo objeto AES-CTR com a mesma chave — a simetria do CTR garante que `.decrypt()` com a mesma chave produz os dados originais;
3. `os.remove(encrypted_file)` e restauração com o nome sem a extensão `.encrypted`.

**Validação defensiva em ambos os scripts:** `if len(key) != 16` encerra a execução com erro antes de tocar em qualquer arquivo. `FileNotFoundError` e `Exception` genérica garantem que falhas não deixem o sistema em estado inconsistente.

```python
# encrypter.py — núcleo da operação
aes = pyaes.AESModeOfOperationCTR(key)
crypto_data = aes.encrypt(file_data)

# decrypter.py — operação inversa com a mesma chave
aes = pyaes.AESModeOfOperationCTR(key)
decrypted_data = aes.decrypt(file_data)
```

---

## 5. Decisões Técnicas e Trade-offs

**Por que AES-CTR e não AES-CBC?**
O modo CBC processa blocos fixos de 16 bytes e exige padding — qualquer arquivo cujo tamanho não seja múltiplo de 16 bytes precisa de tratamento especial. O CTR usa um contador incremental que gera um keystream XOR-ado com os dados, tornando `encrypt` e `decrypt` matematicamente a mesma operação e eliminando a necessidade de padding. O custo é a restrição crítica de segurança: reutilizar IV+chave com CTR quebra toda a confidencialidade do esquema — uma única linha de mudança no inicializador expõe todos os dados criptografados. Para um laboratório didático que prioriza transparência de código, CTR é a escolha correta. Para produção, AES-GCM com autenticação seria o padrão.

**Por que `pyaes` e não `cryptography` (PyCryptodome)?**
A biblioteca `cryptography` é o padrão de produção — usa bindings para OpenSSL, é auditada, e tem performance ordens de magnitude superior. A `pyaes` é implementação pura de Python: cada linha do algoritmo AES é legível, sem binários opacos. Para um laboratório onde o objetivo é entender o mecanismo, não performar, `pyaes` expõe o comportamento de forma transparente. O trade-off aceito é explícito: didática sobre performance e segurança operacional.

**Por que `os.remove()` antes de gravar o arquivo criptografado?**
Em ransomwares reais, manter o arquivo original em disco seria um erro fatal: ferramentas forenses poderiam recuperá-lo diretamente. A sequência `lê → remove original → grava criptografado` garante que não exista janela de tempo onde ambas as versões coexistam. Do ponto de vista defensivo, essa decisão identifica o ponto exato onde shadow copies e snapshots de filesystem se tornam a única alternativa de recuperação — pois capturas feitas após o `remove` já não contêm o arquivo em texto claro.

**Por que dois scripts independentes e não um único com parâmetro `--mode encrypt/decrypt`?**
A separação força a compreensão de cada operação como autônoma. Um script unificado mascara a assimetria fundamental: em ransomwares reais, apenas o encrypter chega ao sistema da vítima. O decrypter é o ativo de negociação do atacante. Estudar os dois como binários independentes — como são em produção — é o que torna o aprendizado operacionalmente honesto.

---

## 6. Resultados

O projeto entrega:

- **Ciclo completo implementado e validado:** `teste.txt` legível → `os.remove()` → `teste.txt.encrypted` (ilegível sem a chave) → restauração pelo decrypter com a mesma chave de 16 bytes
- **Validação de chave e tratamento de erros** em ambos os scripts — nenhuma operação de filesystem é executada sem validação prévia do tamanho da chave e tratamento de `FileNotFoundError`
- **Documentação técnica operacional** do mecanismo que fundamenta a maioria dos ataques de ransomware modernos — base para argumentar controles concretos:
  - Backups imutáveis offline são a única defesa confiável porque eliminam a alavanca de negociação do atacante
  - Monitoramento de criação massiva de arquivos com nova extensão via SIEM detecta o script em execução em segundos
  - Restrição de permissões de escrita por política de menor privilégio limita o raio de impacto de uma infecção
  - Detecção comportamental supera detecção por assinatura porque o mecanismo (criptografia em massa) é invariante entre variantes

---

## 7. Próximos Passos

- **Implementar geração de chave aleatória com `os.urandom(16)`** em vez de chave hardcoded, simulando o comportamento real de ransomwares que geram chaves únicas por instância — e documentar por que isso torna a recuperação sem a chave matematicamente inviável;
- **Adicionar varredura de diretório com `os.walk()`** para criptografar todos os arquivos de uma pasta em laboratório isolado, medindo o tempo de execução como base para definir janelas de detecção disponíveis para contenção;
- **Construir o script de detecção com `watchdog`:** monitor que detecta criação massiva de arquivos `.encrypted` em tempo real e encerra processos suspeitos — fechando o ciclo ataque → defesa neste mesmo repositório;
- **Documentar artefatos forenses:** mapear o que o script deixa em disco (arquivo `.encrypted`, logs do sistema) e como ferramentas como Autopsy ou Volatility os identificam em análise post-mortem.

---

## Tecnologias Utilizadas

| Componente | Papel no Projeto |
|---|---|
| **Python 3.x** | Linguagem principal — manipulação de arquivos, lógica de criptografia e tratamento de erros |
| **pyaes** | Implementação pura de AES em Python — modo CTR para criptografia de fluxo sem padding |
| **os (stdlib)** | Remoção de arquivos e operações de filesystem |
| **Git / GitHub** | Controle de versão e documentação |

---

## Como Executar (Somente em Ambiente Controlado)

```bash
# Instalar dependência
pip install pyaes

# 1. Criptografar o arquivo de teste
python encrypter.py
# Saída: teste.txt removido → teste.txt.encrypted criado

# 2. Descriptografar e restaurar
python decrypter.py
# Saída: teste.txt.encrypted removido → teste.txt restaurado
```

> ⚠️ Execute apenas sobre arquivos próprios em ambiente de laboratório. O script remove o arquivo original antes de salvar o criptografado — não há desfazer sem o decrypter e a chave correta.


---

[![Portfólio Sérgio Santos](https://img.shields.io/badge/Portfólio-Sérgio_Santos-111827?style=for-the-badge&logo=githubpages&logoColor=00eaff)](https://portfoliosantossergio.vercel.app)
[![LinkedIn Sérgio Santos](https://img.shields.io/badge/LinkedIn-Sérgio_Santos-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/santossergioluiz)
