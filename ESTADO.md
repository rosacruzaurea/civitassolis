# Estado

Versão 0.1.1 em revisão, branch `feat/static-site`.

## Conteúdo

Oito rotas em português, inglês, espanhol, francês, alemão e italiano, mais página 404. Publicações contém seis títulos; a galeria contém os 87 vídeos identificados na fonte, não um inventário completo do canal. 115 imagens locais.

Textos e traduções extraídos da referência pública. O formulário simulado foi substituído por contato nos canais oficiais. A rota legada `/livro/` usa a ficha de A Renascença Oculta do catálogo, sem os depoimentos e especificações conflitantes do protótipo. Vídeos e embed oficial do Instagram só conectam a terceiros após interação.

## Ambientes e verificação

Builds de raiz e staging, verificação estrutural e 107 verificações locais de navegador aprovados para a atualização. Cobertura inclui desktop, mobile, idiomas, catálogo, links de compra, foco nos painéis e conteúdo sem JavaScript. O PR registra SHA, CI e publicação do candidato vigente. Execuções e evidências atuais ficam no PR e no GitHub Actions. Staging separado, sem CNAME e com noindex. Produção e domínio original não migrados.

Próxima etapa: revisão humana do staging, conteúdo e integrações externas; aprovar o PR antes de produção. A checagem semanal de vídeos prepara PR e staging, nunca merge automático.

## Candidato SEO

Descrições em `content/seo.json`, geração em `tools/seo.py`, revisão editorial em [REVISAO-SEO](docs/REVISAO-SEO.md). Produção atual usa https://civitassolis.org.br/ e base raiz; staging permanece separado. Validar os dois destinos com `python3 tools/check_seo.py` após o build. Novos textos e imagem aguardam revisão humana; a descrição anterior do domínio não migrado é histórica.
