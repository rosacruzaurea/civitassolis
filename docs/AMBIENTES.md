# Ambientes

## Fonte e produção

`rosacruzaurea/civitassolis`, branch principal `main`. Pages configurado para GitHub Actions. O workflow `pages.yml` gera o site com o caminho-base informado pelo Pages, valida e publica somente `site/`. Primeiro deploy após revisão e merge do candidato. Não apontar Pages para a raiz do repositório.

## Staging

`rosacruzaurea/civitassolis-staging`, branch de publicação `main`. Somente artefato em `site/`, manifesto com SHA de origem e workflow do Pages. Build: `BASE_PATH=/civitassolis-staging SITE_NOINDEX=1`. Sem CNAME. Noindex não é autenticação; a prévia contém apenas material público.

Publicação pontual por candidato, como no fluxo inicial do Pentagrama. Não existe sincronização automática de cada push do PR. Não são criados previews nativos por branch.

Para atualizar: resolver o SHA do PR; construir em worktree isolado; validar; copiar apenas `site/` ao repositório de staging; registrar SHA e opções no commit; enviar e acompanhar o workflow. Conferir o manifesto e a navegação na URL pública. Preservar `main` da fonte e PRs alheios.

## Retorno

Staging: reconstruir e publicar um SHA anterior validado, sem force push. Produção: PR de reversão do commit e deploy pelo mesmo workflow; preservar configuração de domínio. Não há banco ou migração de dados.
