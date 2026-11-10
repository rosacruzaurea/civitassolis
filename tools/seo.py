"""Metadata from the same editorial source and URL configuration as each page."""
import html
import json
from pathlib import Path

CONTENT = json.loads((Path(__file__).resolve().parents[1] / 'content/seo.json').read_text())
LOCALES = {'pt': 'pt_BR', 'en': 'en_US', 'es': 'es_ES', 'fr': 'fr_FR', 'de': 'de_DE', 'it': 'it_IT'}
IMAGE_ALT = {
    'pt': 'Paisagem de montanhas e rio, imagem da página inicial do Civitas Solis.',
    'en': 'Mountain and river landscape from the Civitas Solis home page.',
    'es': 'Paisaje de montañas y río de la página de inicio de Civitas Solis.',
    'fr': "Paysage de montagnes et de rivière de la page d'accueil de Civitas Solis.",
    'de': 'Berg- und Flusslandschaft von der Startseite des Civitas Solis Instituts.',
    'it': 'Paesaggio di montagne e fiume dalla pagina iniziale di Civitas Solis.'
}


def description(language, route):
    # Missing editorial copy must fail the build, not silently fall back to English.
    return CONTENT['descriptions'][language][route]


def metadata(language, title, desc, canonical, site_url, asset_url):
    image = asset_url(CONTENT['sharing_image'])
    tags = {
        'og:site_name': 'Instituto Civitas Solis', 'og:type': 'website',
        'og:locale': LOCALES[language], 'og:title': title,
        'og:description': desc, 'og:url': canonical, 'og:image': image,
        'og:image:type': 'image/jpeg',
        'og:image:width': CONTENT['sharing_image_width'],
        'og:image:height': CONTENT['sharing_image_height'],
        'og:image:alt': IMAGE_ALT[language],
    }
    head = ''.join(f'<meta property="{key}" content="{html.escape(str(value), quote=True)}">' for key, value in tags.items())
    org = site_url + '#organization'
    website = site_url + '#website'
    graph = [
        {'@type': 'Organization', '@id': org, 'name': 'Instituto Civitas Solis',
         'url': site_url, 'logo': asset_url('assets/logo.png')},
        {'@type': 'WebSite', '@id': website, 'name': 'Instituto Civitas Solis',
         'url': site_url, 'inLanguage': ['pt-BR', 'en', 'es', 'fr', 'de', 'it'],
         'publisher': {'@id': org}},
        {'@type': 'WebPage', '@id': canonical + '#page', 'url': canonical,
         'name': title, 'description': desc, 'inLanguage': 'pt-BR' if language == 'pt' else language,
         'isPartOf': {'@id': website}},
    ]
    data = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, separators=(',', ':'))
    data = data.replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    return head + '<script type="application/ld+json">' + data + '</script>'
