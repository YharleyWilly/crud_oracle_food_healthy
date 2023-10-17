--Select as comandas com seus respectivos itens de comanda
select i.id_comanda
     , i.id_item_comanda
     , i.descricao_produto
     , i.qtd_item
     , i.valor_unitario_item
     , (i.qtd_item * i.valor_unitario_item) as valor_total
  from itens_comanda i
  order by i.id_comanda, prd.descricao_produto