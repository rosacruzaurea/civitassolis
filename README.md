# Instituto Civitas Solis

Site institucional em HTML, CSS e JavaScript sem framework no navegador.

- Fonte editorial: https://ics.back2basics.com.br/
- Prévia: https://rosacruzaurea.github.io/civitassolis-staging/
- [Estado](ESTADO.md) · [Changelog](CHANGELOG.md) · [Ambientes](docs/AMBIENTES.md)

## Desenvolvimento

```sh
BASE_PATH=/civitassolis SITE_NOINDEX=1 python3 tools/build.py
python3 tools/check.py
```

`content/` contém os textos, traduções e catálogos; `static/` contém CSS, JavaScript e imagens; `site/` é a saída gerada, não versionada. Python 3.12+ gera o site sem dependências adicionais. Node 24+ e `npm ci` são necessários somente para os testes de navegador, com Google Chrome e sandbox ativos.

## Publicação

Mudanças passam por PR. A produção é gerada da `main` e publicada por GitHub Actions, somente a partir de `site/`. O repositório `civitassolis-staging` recebe exclusivamente a prévia gerada e seu workflow. Nenhum domínio personalizado é configurado nesta versão.

## Atualizações de conteúdo

Uma rotina externa semanal pode propor vídeos novos por PR e publicar o candidato no staging. Produção permanece sujeita a revisão e merge. O Instagram utiliza o embed oficial de perfil sob demanda, não uma API autenticada de inventário de posts.
