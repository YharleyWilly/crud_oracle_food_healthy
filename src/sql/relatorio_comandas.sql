-- Exibe cpf, nome e as informações da comanda e itens comanda do cliente. Somando o total de cada produto.
SELECT co.ID_COMANDA,
            i.ID_ITEM_COMANDA as item_comanda,
            c.CPF_CLIENTE,
            c.NOME_CLIENTE as cliente,
            co.DATA_COMANDA,
            co.STATUS_COMANDA,
            i.DESCRICAO_PRODUTO as produto,
            i.QTD_ITEM as quantidade,
            i.VALOR_UNITARIO_ITEM as valor_unitario,
            (i.QTD_ITEM * i.VALOR_UNITARIO_ITEM) as valor_total
            FROM LABDATABASE.CLIENTES c
            INNER JOIN LABDATABASE.COMANDAS co ON c.CPF_CLIENTE = co.CPF_CLIENTE
            LEFT JOIN LABDATABASE.ITENS_COMANDA i ON co.ID_COMANDA = i.ID_COMANDA
            ORDER BY c.NOME_CLIENTE, i.ID_ITEM_COMANDA

