MENU_PRINCIPAL = """Menu Principal

[1] - Relatórios
[2] - Inserir Registros
[3] - Atualizar Registros
[4] - Remover Registros
[5] - Sair
"""

MENU_RELATORIOS = """Relatórios

[1] - Relatório clientes
[2] - Relatório comandas
[3] - Relatório itens de comandas
[4] - Relatório comanda cliente específico
[0] - Sair
"""

MENU_ENTIDADES = """Entidades

[1] - CLIENTES
[2] - Comandas
[3] - Itens de Comandas
"""

MENU_ENTIDADES_ATUALIZAR = """Entidades

[1] - CLIENTES
[2] - Status comanda
[3] - Itens de Comandas

"""

STATUS_COMANDA = """Status comanda

[1] - Em andamento
[2] - Pronto
[3] - Cancelado

"""

MENU_CARDAPIO = """
\n
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
│                Cardápio de Lanches Saudáveis                  │
├───────────────────────────────────────────────────────────────┤
│ [1] - Sanduíche Natural                      - R$ 9,90        │
│ [2] - Salada de Frutas                       - R$ 6,50        │
│ [3] - Smoothie de Frutas                     - R$ 7,90        │
│ [4] - Wrap de Vegetais                       - R$ 8,50        │
│ [5] - Iogurte com Granola                    - R$ 5,50        │
├───────────────────────────────────────────────────────────────┤
│          Opções de Bebidas:                                   │
│ [A] - Água Mineral                           - R$ 3,00        │
│ [B] - Suco Natural                           - R$ 5,00        │
│ [C] - Chá Verde                              - R$ 4,00        │
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
\n
"""


# Consulta de contagem de registros por tabela
QUERY_COUNT = 'select count(1) as total_{tabela} from {tabela}'

def clear_console(wait_time:int=3):
    '''
       Esse método limpa a tela após alguns segundos
       wait_time: argumento de entrada que indica o tempo de espera
    '''
    import os
    from time import sleep
    sleep(wait_time)
    os.system("clear")