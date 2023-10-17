select c.cpf_cliente
   , c.nome_cliente
   , c.telefone_cliente
   , c.email_cliente
   from clientes c
   order by c.cpf_cliente