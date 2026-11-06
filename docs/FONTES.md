# Fontes e limites

Referência pública coletada em 06/11/2026: https://ics.back2basics.com.br/. Rotas identificadas também no roteador entregue pelo site: `/`, `/missao-visao-valores`, `/publicacoes`, `/youtube`, `/instagram`, `/contato`, `/trabalho-global`, `/livro`. O endpoint sitemap.xml entregava o shell da aplicação; não era um sitemap editorial.

Textos e traduções foram extraídos dos dados públicos; as sete descrições de valores que não tinham tradução na origem receberam traduções complementares para revisão humana, sem executar o bundle de origem no build. `content/media.json` relaciona imagens, URLs de origem e SHA-256. Capas, marca e material editorial permanecem vinculados a seus respectivos titulares; este repositório não atribui uma nova licença ao acervo.

A galeria preserva 87 entradas configuradas e sua ordem. A presença do link não comprova reprodução integral nem disponibilidade permanente. Os seis links de compra são externos; preços, estoques, avaliações e transações não foram auditados. Não há PDFs ou EPUBs locais vinculados na referência de Publicações.

A rota legada de livro tinha ficha técnica divergente e depoimentos sem referência; a réplica usa o registro correspondente do catálogo atual. O formulário original simulava sucesso sem envio. Nesta versão, o contato utiliza os perfis oficiais, sem coletar dados.

Instagram utiliza o embed oficial de perfil (`instagram.com/embed.js`), carregado apenas após escolha, sem token no navegador. O endpoint oEmbed da Meta respondeu para este perfil. A apresentação e disponibilidade dependem do Instagram e das permissões de incorporação da conta; o link direto permanece disponível. O embed não constitui uma API de inventário completo nem uma sincronização de posts. Referência: https://github.com/facebook/meta-embeds-for-wordpress. YouTube também carrega somente após interação; testes com player controlado não certificam reprodução externa.

O conteúdo é um retrato editorial, não uma sincronização automática. Revisão humana de identidade, textos, direitos e integrações antes da produção.

## Atualização do catálogo e visual

Referência pública `index-approved-state-9e4b2c7`, de 06/11/2026: incluídos **Um Coração Para o Rei** e **O Cavalinho Pérola** com capas AVIF e links Amazon; **Cartas de Amor** saiu da listagem conforme a fonte (mídia anterior preservada). Os quatro registros mantidos conservam as traduções existentes. A fonte atual fornece os dois novos registros somente em português; eles permanecem assim nas seis rotas de idioma, com marcação `lang`, enquanto a interface é traduzida. Sem tradução editorial inferida.

Painéis de Trabalho Global reproduzem sobreposição e destaque por foco/hover, com empilhamento em telas menores. Catálogo usa molduras, cartões alternados e botões de compra da referência; seletor de idiomas usa códigos de país.
