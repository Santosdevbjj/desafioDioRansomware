## Bootcamp Santander Cibersegurança #2 · DIO

<img width="892" height="902" alt="Screenshot_20250822-165653" src="https://github.com/user-attachments/assets/9576e30c-d8c6-4a0d-ae5e-84b1626921b4" />

---

> ⚠️ **Aviso Legal:** Este projeto foi desenvolvido exclusivamente para fins educacionais como parte de bootcamp certificado de cibersegurança. O código demonstra os mecanismos internos de um ransomware para que profissionais de segurança possam entender, detectar e mitigar esse tipo de ameaça. O uso deste código para criptografar arquivos de terceiros sem autorização expressa configura crime previsto na Lei nº 12.737/2012 e no Art. 154-A do Código Penal Brasileiro.

---

# 🔒 Entendendo um Ransomware na Prática — Criptografia AES-CTR em Python

## 1. Problema de Negócio

Ransomware é a categoria de ataque cibernético que mais cresce globalmente — e a que mais causa dano financeiro mensurável. A razão pela qual equipes de segurança têm dificuldade em combatê-lo é precisa: **a maioria dos profissionais nunca implementou um**, e portanto não entende o mecanismo técnico que precisa ser detectado, bloqueado ou revertido.

O desafio técnico central é duplo: implementar criptografia simétrica funcional em Python que torne um arquivo ilegível sem a chave correta, e implementar o processo inverso de descriptografia — o mesmo par de operações que define o ciclo completo de um ransomware real. Entender os dois lados do ciclo é o que habilita a construção de defesas efetivas.

---

## 2. Contexto

O projeto foi desenvolvido como desafio prático do **Bootcamp Santander Cibersegurança #2** na DIO, sob orientação do instrutor Cassiano Peres. O objetivo era implementar em Python os dois componentes fundamentais de um ransomware — `encrypter.py` e `decrypter.py` — usando criptografia AES no modo CTR via biblioteca `pyaes`.

A escolha de implementar **dois scripts separados** em vez de um único programa com opções de menu não foi apenas organizacional. Ela espelha a arquitetura real de ransomwares em produção: o componente de criptografia é lançado pelo atacante, e o componente de descriptografia só é entregue à vítima mediante pagamento. Estudar os dois separadamente reforça a compreensão de cada etapa do ataque como uma operação independente.

---

## 3. Premissas

- A biblioteca `pyaes` implementa AES puro em Python, sem dependências de OpenSSL ou binários nativos — escolha deliberada para portabilidade e transparência do código, priorizando didática sobre performance.
- O modo **CTR (Counter Mode)** foi adotado: transforma AES em cifra de fluxo, eliminando a necessidade de padding e permitindo criptografar arquivos de qualquer tamanho sem ajustes no conteúdo.
- A chave `b"chave_segura_16b"` (16 bytes) é hardcoded nos scripts exclusivamente para fins de demonstração. Em um sistema real, a chave seria gerada aleatoriamente, enviada ao servidor do atacante e nunca armazenada localmente.
- O comportamento de **remover o arquivo original antes de salvar o criptografado** (`os.remove()` antes de `open(..., "wb")`) é intencional — replica a mecânica destrutiva de ransomwares reais que não mantêm cópia em texto claro após a criptografia.
- Todos os testes foram realizados sobre o arquivo `teste.txt`, sem envolvimento de arquivos de sistema ou dados de terceiros.

---

## 4. Estratégia da Solução

A implementação foi estruturada em torno de duas funções simétricas e inversas entre si:

**`encrypt_file(file_name, key)` — o lado do atacante:**

1. Leitura do arquivo em modo binário (`"rb"`) com bloco `with`, garantindo fechamento do file handle mesmo em caso de exceção.
2. Remoção do arquivo original via `os.remove()` — o arquivo em texto claro deixa de existir no sistema antes que o criptografado seja gravado.
3. Instanciação do objeto `pyaes.AESModeOfOperationCTR(key)` e aplicação de `.encrypt()` sobre os bytes lidos.
4. Gravação do resultado em `{nome_original}.encrypted` — a extensão padronizada funciona como marcador para o script de descriptografia localizar os arquivos afetados.

**`decrypt_file(encrypted_file, key)` — o lado da recuperação:**

1. Leitura do arquivo `.encrypted` em modo binário.
2. Instanciação do mesmo objeto AES-CTR com a mesma chave — a simetria do CTR garante que `.decrypt()` aplicado sobre dados criptografados com a mesma chave e IV produz os dados originais.
3. Remoção do arquivo `.encrypted` e restauração do arquivo original com o nome sem a extensão.

**Validação defensiva em ambos os scripts:** antes de executar qualquer operação, o bloco `if __name__ == "__main__"` valida `len(key) != 16` — se a chave tiver tamanho inválido, o script encerra com mensagem de erro antes de tocar em qualquer arquivo. Tratamento de `FileNotFoundError` e `Exception` genérica garantem que falhas não deixem o sistema em estado inconsistente.

---

## 5. Insights Técnicos

A implementação revelou aspectos do design de ransomware que não ficam visíveis apenas na teoria:

- **`os.remove()` antes de gravar é a decisão mais destrutiva do código:** a sequência lê → remove original → grava criptografado significa que qualquer falha entre o `remove` e o `open("wb")` resulta em perda permanente do arquivo — sem backup, sem recuperação. Em um ransomware real, essa janela de falha é o principal vetor para ferramentas de recuperação baseadas em shadow copies ou snapshots de filesystem.

- **AES-CTR transforma criptografia de bloco em cifra de fluxo:** diferente do modo CBC, que processa blocos fixos de 16 bytes e exige padding, o CTR usa um contador incremental que gera um keystream XOR-ado com os dados. Isso significa que `encrypt` e `decrypt` são a mesma operação matematicamente — o que simplifica a implementação mas também significa que reutilizar IV+chave quebra toda a segurança do esquema.

- **A chave hardcoded é o ponto fraco intencional:** em ransomwares reais, a chave é gerada aleatoriamente por instância, enviada para um servidor C2 (Command & Control) antes da criptografia começar, e nunca persiste localmente. A hardcode neste projeto é didática — mas também demonstra por que análise forense de ransomware muitas vezes começa por buscar a chave em memória ou em tráfego de rede antes da exfiltração.

- **A extensão `.encrypted` é um indicador de comprometimento (IoC):** em ambientes corporativos, a proliferação súbita de arquivos com extensão desconhecida é um dos alertas mais confiáveis de ransomware ativo. Um SIEM configurado para monitorar criação massiva de arquivos com nova extensão detectaria este script em execução em segundos.

- **Separar encrypter e decrypter é uma decisão de arquitetura, não de organização:** ter os dois scripts como binários independentes permite que o atacante distribua apenas o encrypter — o decrypter permanece sob controle do atacante como alavanca de negociação. Estudar os dois separadamente é a forma mais honesta de entender essa assimetria de poder.

---

## 6. Resultados

O projeto entrega:

- Implementação funcional de criptografia e descriptografia AES-CTR em Python com tratamento de erros, validação de chave e gerenciamento seguro de file handles
- Demonstração completa do ciclo de um ransomware: arquivo legível → remoção do original → arquivo `.encrypted` → restauração pelo decrypter com a mesma chave
- Documentação técnica do mecanismo que fundamenta a maioria dos ataques de ransomware modernos — base para argumentar a necessidade de controles como backup imutável, monitoramento de criação de arquivos via SIEM e restrição de permissões de escrita por política de menor privilégio

O entendimento operacional deste ciclo é o que habilita respostas como: por que backups offline são a única defesa confiável, por que detecção comportamental supera detecção por assinatura, e por que a janela entre infecção e criptografia completa define o tempo de resposta disponível para contenção.

---

## 7. Próximos Passos

- **Implementar geração de chave aleatória com `os.urandom(16)`** em vez de chave hardcoded, simulando o comportamento real de ransomwares que geram chaves únicas por instância — e documentar por que isso torna a recuperação sem pagamento matematicamente inviável.
- **Adicionar varredura de diretório:** evoluir o script para usar `os.walk()` e criptografar todos os arquivos de uma pasta, simulando o comportamento de propagação lateral — e medir o tempo de execução como base para entender janelas de detecção.
- **Construir o script de detecção:** implementar um monitor que use `watchdog` para detectar criação massiva de arquivos `.encrypted` em tempo real e encerrar processos suspeitos — fechando o ciclo ataque → defesa.
- **Integrar com análise forense:** documentar quais artefatos o script deixa em disco (arquivo `.encrypted`, logs do sistema, entradas no registro) e como ferramentas como Autopsy ou Volatility os identificam em uma análise post-mortem.

---

## 🛠️ Tecnologias e Bibliotecas

| Componente | Papel no Projeto |
|------------|-----------------|
| **Python 3.x** | Linguagem principal — manipulação de arquivos, lógica de criptografia e tratamento de erros |
| **pyaes** | Implementação pura de AES em Python — modo CTR para criptografia de fluxo sem padding |
| **os (stdlib)** | Remoção de arquivos e operações de filesystem |
| **Git / GitHub** | Controle de versão e documentação |

---

## ▶️ Como Executar (Somente em Ambiente Controlado)

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

**Contato:**

[![Portfólio Sérgio Santos](https://img.shields.io/badge/Portfólio-Sérgio_Santos-111827?style=for-the-badge&logo=githubpages&logoColor=00eaff)](https://portfoliosantossergio.vercel.app)

[![LinkedIn Sérgio Santos](https://img.shields.io/badge/LinkedIn-Sérgio_Santos-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/santossergioluiz)


---
