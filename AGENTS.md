# Manutenção

Leia [ESTADO.md](ESTADO.md), [README.md](README.md) e [docs/AMBIENTES.md](docs/AMBIENTES.md).

- Edite conteúdo em `content/` e apresentação em `static/`/`tools/build.py`; não edite a saída gerada.
- Preserve as oito rotas, os seis idiomas, a ordem editorial dos vídeos e as fontes do catálogo. Não invente títulos, endereços, avaliações ou links.
- Não reintroduza React, analytics, carregamento automático de terceiros ou formulário com envio simulado.
- Gere e valide para o subcaminho real e para a raiz. Execute os testes de navegador para mudanças funcionais.
- PR antes de alterações em `main`. Merge e produção exigem aprovação do candidato. Staging é artefato, não segunda fonte de código.
- Documentação pública deve ser curta, impessoal e técnica. Evidências operacionais e conversas ficam fora do repositório.
- Conclua o build antes de iniciar os testes de navegador; não regenere `site/` durante a leitura pela fixture. Use artefato estável por rodada.
- Em sincronização da referência, compare o catálogo completo (adições, retiradas e idiomas), não apenas a contagem anunciada de novos itens.

- Preserve caminhos existentes. A cada mudança, confira a consistência do sitemap com as páginas publicáveis e registre explicitamente URLs novas, alteradas ou removidas na entrega; se não houver delta, declare isso.

- Em ajustes visuais, capturar e inspecionar cada região alterada (incluindo rodapé e menu aberto), não apenas o topo. Para grupos de ícones, conferir alinhamento, dimensões de toque e foco em desktop/mobile.

- YouTube e Instagram no menu são páginas internas: manter os nomes por extenso. Ícones sociais representam links externos, não substituem esses rótulos de navegação.
