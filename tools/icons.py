"""Local inline icons: no font, script or remote request required."""
import html


def social_icon(network):
    paths = {
        'instagram': '<rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.5" cy="6.5" r="1.2"/>',
        'youtube': '<path d="M22 8a4 4 0 0 0-3-3c-3-.4-11-.4-14 0a4 4 0 0 0-3 3 27 27 0 0 0 0 8 4 4 0 0 0 3 3c3 .4 11 .4 14 0a4 4 0 0 0 3-3 27 27 0 0 0 0-8Z m-12 0 6 4-6 4Z" fill-rule="evenodd"/>',
        'facebook': '<path d="M14 22v-9h3l.5-4H14V7c0-1 .3-2 2-2h2V1.5C17 1.2 16 1 15 1c-3 0-5 2-5 5v3H7v4h3v9Z"/>',
    }
    return '<svg class="social-icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false">'+paths[network]+'</svg>'


def social_link(url, network, label, css=''):
    esc = lambda value: html.escape(str(value), quote=True)
    return f'<a class="social-icon-link {esc(css)}" href="{esc(url)}" aria-label="{esc(label)}" title="{esc(label)}" data-social="{network}">'+social_icon(network)+'</a>'


def language_flag(language):
    # Preserve the locale representations already used by the selector.
    flags = {
        'pt': '<path fill="#009739" d="M0 0h30v20H0z"/><path fill="#ffdf00" d="m15 2 12 8-12 8-12-8Z"/><circle fill="#002776" cx="15" cy="10" r="5"/><path d="M10.5 8.5q5-1 9 3" fill="none" stroke="#fff" stroke-width="1"/>',
        'en': '<path fill="#fff" d="M0 0h30v20H0z"/>'+''.join(f'<path fill="#b22234" d="M0 {i*40/13:g}h30v{20/13:g}H0z"/>' for i in range(7))+'<path fill="#3c3b6e" d="M0 0h13v11H0z"/>'+''.join(f'<circle fill="#fff" cx="{x}" cy="{y}" r=".6"/>' for y in [2,4.3,6.6,9] for x in [2,5,8,11]),
        'es': '<path fill="#aa151b" d="M0 0h30v20H0z"/><path fill="#f1bf00" d="M0 5h30v10H0z"/>',
        'fr': '<path fill="#fff" d="M0 0h30v20H0z"/><path fill="#002395" d="M0 0h10v20H0z"/><path fill="#ed2939" d="M20 0h10v20H20z"/>',
        'de': '<path fill="#000" d="M0 0h30v20H0z"/><path fill="#d00" d="M0 6.667h30v6.667H0z"/><path fill="#ffce00" d="M0 13.333h30V20H0z"/>',
        'it': '<path fill="#fff" d="M0 0h30v20H0z"/><path fill="#009246" d="M0 0h10v20H0z"/><path fill="#ce2b37" d="M20 0h10v20H20z"/>',
    }
    return '<svg class="language-flag" viewBox="0 0 30 20" aria-hidden="true" focusable="false">'+flags[language]+'</svg>'
