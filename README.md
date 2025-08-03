# Analisador de Ponto por Chat (Chat Attendance Parser)

Este projeto é um script em Python que analisa um arquivo de texto de log de chat (como o exportado pelo WhatsApp) para extrair registros de ponto (entrada e saída) e os organiza em uma planilha Excel.
![img](./chat.png)

## Funcionalidades

- Analisa logs de chat no formato `DD/MM/AAAA HH:MM - Nome do Remetente: Mensagem`.
- Extrai o horário de ponto informado dentro da própria mensagem (ex: "ponto 18:00").
- Agrupa os registros por remetente e por data.
- Exporta os dados para um arquivo Excel (`.xlsx`), com uma aba dedicada para cada remetente.

## Pré-requisitos

- Python 3.x

## Instalação

1.  Clone este repositório:

    ```bash
    git clone https://github.com/rhault/chat-attendance-parser.git
    cd ChatAttendanceParser
    ```

2.  (Opcional, mas recomendado) Crie e ative um ambiente virtual:

    ```bash
    python -m venv venv
    ```

3.  Instale as dependências necessárias:
    ```bash
    pip install -r requirements.txt
    ```

## Como Usar

1.  **Crie a estrutura de pastas:**
    Certifique-se de que as pastas `input` e `output` existem na raiz do projeto.

    ```
    .
    ├── input/
    ├── output/
    └── main.py
    ```

2.  **Adicione o arquivo de entrada:**
    Coloque o seu arquivo de log de chat na pasta `input`. O script está configurado para ler o arquivo `Controle de Jornada.txt` por padrão.

    **Formato do arquivo de entrada:**
    O script espera que cada linha relevante do chat siga este padrão:
    `DD/MM/AAAA HH:MM - Nome do Remetente: Sua mensagem aqui com o horário HH:MM`

3.  **Execute o script:**
    Abra o terminal na pasta do projeto e execute:

    ```bash
    python main.py
    ```

4.  **Verifique a saída:**
    Após a execução, um arquivo chamado `chat_attendance.xlsx` será gerado na pasta `output`. Este arquivo conterá os dados de ponto organizados.
