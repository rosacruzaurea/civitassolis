"""Verify multilingual metadata against editorial data and the built URL base."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
config = json.loads((ROOT / 'content/seo.json').read_text())
manifest = json.loads((SITE / 'build-manifest.json').read_text())
site_url = manifest['origin'] + manifest['base_path'] + '/'


class Head(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta = {}; self.links = []; self.structured = ''; self.ld = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta':
            key = a.get('name', a.get('property'))
            assert key not in self.meta, ('duplicate metadata', key)
            self.meta[key] = a.get('content')
        if tag == 'link': self.links.append(a)
        if tag == 'script': self.ld = a.get('type') == 'application/ld+json'

    def handle_endtag(self, tag):
        if tag == 'script': self.ld = False

    def handle_data(self, data):
        if self.ld: self.structured += data


seen = set(); total = 0
for lang, descriptions in config['descriptions'].items():
    assert len(descriptions) == 8
    for route, desc in descriptions.items():
        assert desc.strip() == desc and 70 <= len(desc) <= 190
        assert desc not in seen
        seen.add(desc)
        path = ('/' + lang if lang != 'pt' else '') + ('/' + route if route else '') + '/'
        rel = path.lstrip('/') + 'index.html'
        canonical = manifest['origin'] + manifest['base_path'] + path
        raw = (SITE / rel).read_text(); head = Head(); head.feed(raw)
        assert head.meta['description'] == head.meta['og:description'] == desc
        assert head.meta['og:url'] == canonical
        assert next(x['href'] for x in head.links if x['rel'] == 'canonical') == canonical
        alternatives = {x['hreflang']: x['href'] for x in head.links if x['rel'] == 'alternate'}
        assert set(alternatives) == set(config['descriptions'])
        for other, href in alternatives.items():
            expected = site_url + (other + '/' if other != 'pt' else '') + (route + '/' if route else '')
            assert href == expected
        assert head.meta['og:image'] == site_url + config['sharing_image']
        assert (SITE / config['sharing_image']).is_file()
        assert ('noindex' in head.meta['robots']) == manifest['noindex']
        data = json.loads(head.structured)
        org, website, page = data['@graph']
        assert [g['@type'] for g in data['@graph']] == ['Organization', 'WebSite', 'WebPage']
        assert org['url'] == website['url'] == site_url
        assert org['logo'] == site_url + 'assets/logo.png'
        assert website['publisher']['@id'] == org['@id']
        assert page['isPartOf']['@id'] == website['@id']
        assert page['url'] == canonical and page['description'] == desc
        assert page['inLanguage'] == ('pt-BR' if lang == 'pt' else lang)
        assert page['name'] == head.meta['og:title']
        for value in [page['url'], org['url'], org['logo'], head.meta['og:image']]:
            assert urlsplit(value).netloc == urlsplit(site_url).netloc
        if lang in ['de', 'it'] and route == '':
            for residual in ['Art, Spirituality and Science for a New Consciousness', 'Founded to promote', 'We promote spiritual development']:
                assert residual not in raw
        total += 1
assert total == 48
print(json.dumps({'metadata_pages': total, 'unique_descriptions': len(seen), 'base': manifest['base_path'], 'origin': manifest['origin'], 'ok': True}))
