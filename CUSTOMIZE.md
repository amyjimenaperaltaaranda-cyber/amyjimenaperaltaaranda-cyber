# Cómo personalizar tu perfil ✦

Todo sale de **un solo archivo: `config.json`**. Lo editas, ejecutas el generador y se regeneran el `README.md` y los gráficos de `assets/`. No necesitas instalar nada, solo Python 3.8 o superior.

```bash
python generate.py
```

## Cambiar el estilo

| Quiero... | Cómo |
| :-- | :-- |
| Probar otro tema | `python generate.py --theme retro-sunset` (también `mint-terminal`, `cotton-candy`; `--list-themes` los muestra todos) |
| Dejar un tema fijo | En `config.json`, cambia `"theme"` |
| Otro cielo de estrellas | `python generate.py --seed 21` (cualquier número) o cambia `"seed"` |
| Mis propios colores | En `"palette"` pon solo lo que quieras cambiar, por ejemplo `{ "secondary": "#00ffd0", "warm": "#ffa94d" }` |
| Crear un tema nuevo | En `generate.py`, copia un bloque de `PALETTES`, cámbiale el nombre y los colores |

Colores disponibles: `bg_top`, `bg_bottom` (fondo), `primary`, `secondary`, `warm`, `pink` (acentos), `text`, `muted`, `line`, `card`.

## Cambiar el contenido

- **Textos del banner:** `alias`, `tagline`, `banner_label`, `banner_path`, `banner_line`.
- **Insignias de arriba:** `badges_top` (el color puede ser un nombre de la paleta, como `"primary"`, o un hex sin `#`).
- **Terminal:** `terminal` es una lista de comandos con sus líneas de salida. Agrega, quita o edita las que quieras.
- **Secciones:** en `sections` pon `false` en la que quieras ocultar (`terminal`, `datos_personales`, `travesia`, `reconocimientos`, `experiencia`, `proyectos`, `github`, `habilidades`, `certificaciones`, `contacto`).
- **Reconocimientos:** lista `awards` (puesto, título, organización, fecha). `n` es 1, 2 o 3 y define el color de la medalla.
- **Programas y certificaciones:** listas `experience` y `certifications`. Si pones `url` en una certificación, el título se vuelve enlace.
- **Habilidades:** en `skills`, cada categoría es una lista. El gráfico se acomoda solo.
- **Travesía académica:** cuando cambies de ciclo, sube `academic.cycle_current` y se agrega otro nodo al camino.
- **Proyectos:** copia un bloque de `featured_projects` o `github_repos` y cámbialo. Si pones un `url`, el nombre se vuelve enlace.
- **LinkedIn:** pega tu enlace de perfil en `links.linkedin`. Mientras esté vacío, el botón no aparece.

## Publicarlo en GitHub

1. Crea (o usa) el repositorio público que se llama **igual que tu usuario**.
2. Sube todo el contenido de esta carpeta. Lo que GitHub muestra es `README.md` y la carpeta `assets/`, así que ambos tienen que estar en el repositorio.
3. Cada vez que cambies algo: `python generate.py`, luego commit y push.

## Si cambias tu usuario de GitHub

Actualiza `links.github` y `links.github_label`, y las `url` de `github_repos`, en `config.json`. Después ejecuta `python generate.py` otra vez.

## Notas

- Los gráficos son SVG animados (estrellas que titilan, ciclo actual que pulsa). GitHub los muestra animados en el README.
- Si algo no se ve como esperas, abre los archivos de `assets/` en el navegador para verlos solos.
