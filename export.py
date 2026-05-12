import os
import re
import markdown
from weasyprint import HTML

# --- CONFIGURACIÓN DE RUTAS ---
PORTADA_MD = os.path.join('front-matter', 'portada.md')

ARCHIVOS_MD = [
    '10-startup-profile.md',
    '11-solution-profile.md',
    '12-lean-ux-process.md',
    '13-target-segments.md',
    '20-competitors.md',
    '21-interviews.md',
    '22-needfinding.md',
    '23-big-picture-event-storming.md',
    '24-ubiquitous-language.md',
    '30-user-stories.md',
    '31-impact-mapping.md',
    '32-product-backlog.md',
    '40-style-guidelines.md',
    '41-information-architecture.md',
    '42-landing-page-ui-design.md',
    '43-web-application-design.md',
    '44-web-applications-prototyping.md',
    '45-design-level-event-storming.md',
    '46-model-c4.md',
    '47-class-diagrams.md',
    '48-database-diagram.md',
    '50-software-configuration-management.md',
    '51-sprint-01.md',
    '52-validation-interviews.md',
    '53-heuristics.md',
    '54-video-about-the-team.md',
    '97-conclusions.md',
]

OUTPUT_PDF = 'Informe_Final_TB1.pdf'

# Archivos que son SOLO un encabezado de capítulo (h1) sin contenido real.
# NO ponemos page-break después de ellos para evitar la hoja en blanco.
SOLO_HEADER = {
    '40-style-guidelines.md',
}

def leer(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def tiene_solo_header(contenido):
    """True si el archivo tiene únicamente líneas de heading h1 y espacios."""
    lineas = [l.strip() for l in contenido.splitlines() if l.strip()]
    return all(l.startswith('#') for l in lineas)

def export_to_pdf():
    print("Recolectando archivos...")
    full_md_content = ""

    # 1. Portada
    if os.path.exists(PORTADA_MD):
        full_md_content += leer(PORTADA_MD) + "\n\n"
    else:
        print(f"Advertencia: No se encontró la portada en {PORTADA_MD}")

    # 2. Resto de archivos
    for md_file in ARCHIVOS_MD:
        if not os.path.exists(md_file):
            print(f"Advertencia: Omitiendo {md_file} (No encontrado)")
            continue

        contenido = leer(md_file)

        # Si el archivo es solo un header de capítulo, NO agregamos page-break
        # después para que el siguiente archivo (con el contenido real) continúe
        # en la misma hoja en lugar de dejarla en blanco.
        if tiene_solo_header(contenido):
            full_md_content += contenido + "\n\n"
        else:
            full_md_content += contenido + "\n\n<div class='page-break'></div>\n\n"

    # 3. Markdown → HTML
    print("Generando HTML e Índice...")
    html_body = markdown.markdown(
        full_md_content,
        extensions=['extra', 'fenced_code', 'toc']
    )

    # 4. Plantilla HTML + CSS
    html_template = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{
                size: A4;
                margin: 2.5cm;
                @bottom-right {{
                    content: counter(page);
                    font-size: 10pt;
                }}
            }}

            body {{
                font-family: 'Helvetica', 'Arial', sans-serif;
                font-size: 10.5pt;
                line-height: 1.5;
                color: #333;
                text-align: justify;
                counter-reset: h1;
            }}

            /* ── Headings ── */
            h1 {{
                counter-reset: h2;
                color: #003366;
                border-bottom: 2px solid #003366;
                padding-bottom: 5px;
                margin-top: 1cm;
                page-break-after: avoid;
            }}
            h2 {{
                counter-reset: h3;
                color: #004080;
                margin-top: 1.5em;
                page-break-after: avoid;
            }}
            h3 {{
                color: #005099;
                margin-top: 1em;
                page-break-after: avoid;
            }}
            h4, h5 {{
                color: #333;
                margin-top: 0.8em;
                page-break-after: avoid;
            }}

            /* Numeración automática — excluye los no-number de la portada */
            h1:not(.no-number)::before {{
                counter-increment: h1;
                content: counter(h1) ". ";
            }}
            h2:not(.no-number)::before {{
                counter-increment: h2;
                content: counter(h1) "." counter(h2) ". ";
            }}
            h3:not(.no-number)::before {{
                counter-increment: h3;
                content: counter(h1) "." counter(h2) "." counter(h3) ". ";
            }}

            /* ── Saltos de página ── */
            .page-break {{ page-break-after: always; }}

            /* h1 que NO es no-number arranca en nueva página */
            h1:not(.no-number) {{
                page-break-before: always;
            }}

            /* ── Imágenes ── */
            img {{
                max-width: 100%;
                height: auto;
                display: block;
                margin: 0.8cm auto;
            }}

            /* ── Tablas: no se salen de la página ── */
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 1em 0;
                table-layout: fixed;       /* columnas proporcionales */
                word-wrap: break-word;     /* corta palabras largas   */
                overflow-wrap: break-word;
                font-size: 9pt;            /* un poco más pequeño para caber */
            }}
            th, td {{
                border: 1px solid #ccc;
                padding: 6px 8px;
                text-align: left;
                vertical-align: top;
                word-break: break-word;
            }}
            th {{
                background-color: #f2f2f2;
                font-weight: bold;
            }}

            /* ── Código ── */
            code {{
                background: #eee;
                padding: 2px 4px;
                border-radius: 4px;
                font-family: monospace;
                font-size: 9pt;
                word-break: break-all;
            }}
            pre {{
                background: #f8f8f8;
                padding: 12px;
                border-left: 5px solid #003366;
                overflow-x: auto;
                page-break-inside: avoid;
                font-size: 9pt;
            }}

            /* ── TOC / Índice ── */
            .toc {{
                background: #f9f9f9;
                padding: 20px;
                border: 1px solid #ddd;
            }}
            .toc ul {{
                list-style-type: none;
                padding-left: 20px;
            }}
            .toc > ul {{ padding-left: 0; }}
            .toc a {{
                text-decoration: none;
                color: #003366;
            }}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """

    # 5. Generar PDF
    print("Creando PDF...")
    HTML(string=html_template, base_url='.').write_pdf(OUTPUT_PDF)
    print(f"\n¡Listo! PDF generado como: {OUTPUT_PDF}")

if __name__ == "__main__":
    export_to_pdf()
