"""Generate the SVG images used by the profile README.

Usage, from the repo root:
    python scripts/generate_assets.py

The images are written to assets/. To add a project or certification,
edit the `projects` or `certs` lists below, run the script, then commit
the updated SVGs (and reference any new card in README.md).
"""
import sys, html, os

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')
os.makedirs(OUT, exist_ok=True)
FONT = "'Segoe UI', -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
GOLD = "#D4AF37"
GOLDL = "#F0D77B"


def esc(s):
    return html.escape(s, quote=True)


def wrap(text, maxch):
    out, line = [], ''
    for w in text.split():
        if len(line) + len(w) + 1 > maxch and line:
            out.append(line)
            line = w
        else:
            line = (line + ' ' + w).strip()
    out.append(line)
    return out


def defs(gw, gh):
    return f'''<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#17150f"/><stop offset=".55" stop-color="#0d0d0e"/><stop offset="1" stop-color="#111012"/></linearGradient>
  <radialGradient id="glow" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="scale({gw} {gh})"><stop offset="0" stop-color="{GOLD}" stop-opacity=".2"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>
  <linearGradient id="accent" x1="0" x2="1"><stop offset="0" stop-color="{GOLD}"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient>
  <linearGradient id="topline" x1="0" x2="1"><stop offset="0" stop-color="{GOLD}" stop-opacity="0"/><stop offset=".5" stop-color="{GOLD}"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient>
</defs>'''


def write(name, svg):
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
        f.write(svg)


# ---------- banner ----------
W, H = 1200, 330
grid = ''.join(f'<line x1="{x}" y1="24" x2="{x}" y2="{H - 24}"/>' for x in range(800, 1180, 36))
grid += ''.join(f'<line x1="800" y1="{y}" x2="1172" y2="{y}"/>' for y in range(42, H - 20, 36))
code = [
    ('<span>', [('&lt;', GOLDL), ('Interface', '#ffffff')]),
    ('', [('  fast', '#9a9a9b')]),
    ('', [('  dependable', '#9a9a9b')]),
    ('', [('  accessible', '#9a9a9b')]),
    ('', [('/&gt;', GOLDL)]),
]
code_svg = ''
for i, (_, parts) in enumerate(code):
    spans = ''.join(f'<tspan fill="{c}">{t}</tspan>' for t, c in parts)
    code_svg += f'<text x="0" y="{i * 32}" xml:space="preserve">{spans}</text>'

banner = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Forever Oluwayomi, Senior Frontend Engineer">
<title>Forever Oluwayomi · Senior Frontend Engineer</title>
{defs(560, 340)}
<style>
  @keyframes draw {{ from {{ stroke-dashoffset: 260; }} to {{ stroke-dashoffset: 0; }} }}
  @keyframes blink {{ 0%, 49% {{ opacity: 1; }} 50%, 100% {{ opacity: 0; }} }}
  @keyframes rise {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
  .line {{ stroke-dasharray: 260; animation: draw 1.4s ease-out both; }}
  .caret {{ animation: blink 1.1s steps(1) infinite; }}
  .a1 {{ animation: rise .8s ease-out both; }}
  .a2 {{ animation: rise .8s .2s ease-out both; }}
  .a3 {{ animation: rise .8s .4s ease-out both; }}
  @media (prefers-reduced-motion: reduce) {{ .line, .caret, .a1, .a2, .a3 {{ animation: none; }} }}
</style>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="url(#bg)" stroke="#2a2723"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="url(#glow)"/>
<rect x="200" y="1" width="800" height="2" fill="url(#topline)"/>
<g opacity=".05" stroke="#ffffff">{grid}</g>
<g class="a1" font-family="{FONT}">
  <text x="70" y="98" font-size="17" letter-spacing="4" font-weight="600" fill="{GOLD}">HI THERE, I'M</text>
  <text x="67" y="162" font-size="58" font-weight="700" fill="#ffffff">Forever Oluwayomi</text>
</g>
<path class="line" d="M70 190 H330" stroke="url(#accent)" stroke-width="3" fill="none" stroke-linecap="round"/>
<g class="a2" font-family="{FONT}">
  <text x="70" y="234" font-size="28" font-weight="600" fill="{GOLDL}">Senior Frontend Engineer</text>
  <text x="70" y="274" font-size="20" fill="#9a9a9b">React · Next.js · TypeScript · Google Cloud certified</text>
</g>
<g transform="translate(860 112)"><g class="a3" font-family="{MONO}" font-size="22">
  {code_svg}
  <rect class="caret" x="42" y="111" width="12" height="24" fill="{GOLD}"/>
</g></g>
</svg>'''
write('banner.svg', banner)

# ---------- project cards ----------
CW, CH = 600, 300
projects = [
    ('conviso', 'Conviso', 'B2B Platform',
     'Behavioural messaging for growing teams: automated journeys across email, WhatsApp, and push in one platform.',
     'Next.js · React Query · TypeScript · Tailwind'),
    ('cdp-editor', 'CDP Editor', 'NPM Package',
     'Rich text editor for crafting HTML emails, with dynamic attributes injected at the cursor and DOMPurify sanitisation.',
     'React · TypeScript · Webpack · Tailwind'),
    ('havara', 'Havara', 'Booking Platform',
     'Luxury residences and a private beach house in Lagos, with stays, concierge, and enquiries.',
     'Next.js · React Query · TypeScript · Tailwind'),
    ('roe-weddings', 'ROE Weddings', 'Business Website',
     'Luxury wedding planning across Barbados, the UK, and beyond: event portfolio, client stories, and enquiries.',
     'Next.js · Tailwind · Google Cloud Storage'),
]
for slug, title, cat, desc, stack in projects:
    pw = len(cat) * 9.8 + 36
    lines = wrap(desc, 44)
    dl = ''.join(f'<text x="40" y="{156 + i * 31}">{esc(l)}</text>' for i, l in enumerate(lines))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{CW}" height="{CH}" viewBox="0 0 {CW} {CH}" role="img" aria-label="{esc(title)}, {esc(cat)}">
<title>{esc(title)} · {esc(cat)}</title>
{defs(380, 260)}
<rect x="1" y="1" width="{CW - 2}" height="{CH - 2}" rx="16" fill="#141416" stroke="#2a2723"/>
<rect x="1" y="1" width="{CW - 2}" height="{CH - 2}" rx="16" fill="url(#glow)" opacity=".7"/>
<rect x="100" y="1" width="400" height="2" fill="url(#topline)"/>
<g font-family="{FONT}">
  <rect x="{CW - 40 - pw:.0f}" y="32" width="{pw:.0f}" height="34" rx="17" fill="{GOLD}" fill-opacity=".1" stroke="{GOLD}" stroke-opacity=".35"/>
  <text x="{CW - 40 - pw / 2:.0f}" y="55" text-anchor="middle" font-size="16" font-weight="600" fill="{GOLDL}">{esc(cat)}</text>
  <text x="40" y="108" font-size="36" font-weight="700" fill="#ffffff">{esc(title)}</text>
  <g font-size="21" fill="#a9a9ab">{dl}</g>
  <line x1="40" y1="{CH - 66}" x2="{CW - 40}" y2="{CH - 66}" stroke="#2a2a2d"/>
  <text x="40" y="{CH - 34}" font-size="17" fill="#85858a">{esc(stack)}</text>
  <text x="{CW - 40}" y="{CH - 34}" text-anchor="end" font-size="17" font-weight="600" fill="{GOLD}">View ↗</text>
</g>
</svg>'''
    write(f'project-{slug}.svg', svg)

# ---------- certifications ----------
certs = [('Generative AI Leader', 'Nov 2026'), ('Professional Cloud Developer', 'Mar 2026'),
         ('Professional Cloud Architect', 'Sep 2024'), ('Associate Cloud Engineer', 'May 2024')]
CWd, CHd = 1200, 190
colw = (CWd - 80) / 4
items = ''
for i, (n, d) in enumerate(certs):
    x = 40 + i * colw
    if i:
        items += f'<line x1="{x:.0f}" y1="36" x2="{x:.0f}" y2="{CHd - 36}" stroke="#2a2a2d"/>'
    ln = wrap(n, 17)
    nt = ''.join(f'<text x="{x + 26:.0f}" y="{96 + j * 28}" font-size="23" font-weight="600" fill="#ffffff">{esc(l)}</text>' for j, l in enumerate(ln))
    items += (f'<circle cx="{x + 30:.0f}" cy="55" r="4" fill="{GOLD}"/>'
              f'<text x="{x + 42:.0f}" y="60" font-size="15" letter-spacing="2" font-weight="600" fill="{GOLD}">GOOGLE CLOUD</text>'
              f'{nt}<text x="{x + 26:.0f}" y="{96 + len(ln) * 28 + 6}" font-size="17" fill="#85858a">{d}</text>')
cert = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{CWd}" height="{CHd}" viewBox="0 0 {CWd} {CHd}" role="img" aria-label="Four Google Cloud certifications">
<title>Google Cloud certifications</title>
{defs(560, 200)}
<rect x="1" y="1" width="{CWd - 2}" height="{CHd - 2}" rx="16" fill="#141416" stroke="#2a2723"/>
<rect x="1" y="1" width="{CWd - 2}" height="{CHd - 2}" rx="16" fill="url(#glow)" opacity=".6"/>
<rect x="200" y="1" width="800" height="2" fill="url(#topline)"/>
<g font-family="{FONT}">{items}</g>
</svg>'''
write('certifications.svg', cert)
print('ok')

# ---------- link buttons ----------
for slug, label in [('portfolio', 'Portfolio'), ('linkedin', 'LinkedIn'), ('email', 'Email')]:
    bw = int(len(label) * 11.5 + 78)
    btn = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{bw}" height="48" viewBox="0 0 {bw} 48" role="img" aria-label="{label}">
<title>{label}</title>
<rect x="1" y="1" width="{bw - 2}" height="46" rx="23" fill="#141416" stroke="{GOLD}" stroke-opacity=".55"/>
<g font-family="{FONT}"><text x="{(bw - 22) / 2:.0f}" y="30.5" text-anchor="middle" font-size="18" font-weight="600" fill="{GOLDL}">{label}</text>
<text x="{bw - 30}" y="30.5" text-anchor="middle" font-size="17" font-weight="600" fill="{GOLD}">↗</text></g>
</svg>'''
    write(f'button-{slug}.svg', btn)
print('buttons ok')
