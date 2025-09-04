
# Guía rápida: subir el proyecto a GitHub (por primera vez)

## Opción A: con la interfaz web (más simple)
1. Crea tu cuenta en https://github.com (si no la tienes).
2. Haz clic en **New** para crear un repositorio:
   - Name: `calola-lab` (por ejemplo)
   - **Private** (recomendado)
   - Añade un README si quieres.
3. En tu computador, **descomprime** `calola_lab_pro_kit_v3.zip` (o el último zip).
4. Dentro del repo en GitHub, pulsa **Add file → Upload files** y **arrastra** el contenido de la carpeta descomprimida (puedes arrastrar carpetas completas).
5. Confirma con **Commit**.
6. Para invitar colaboradores: **Settings → Collaborators → Add people**.

> Nota: Si la carga web te complica por tamaño/estructura, usa la Opción B (línea de comandos).

## Opción B: con Git (línea de comandos)
1. Instala Git: https://git-scm.com/downloads
2. Descomprime el zip y entra a la carpeta:
   ```bash
   unzip calola_lab_pro_kit_v3.zip
   cd calola_lab_pro_kit
   ```
3. Inicializa y sube:
   ```bash
   git init -b main
   git add .
   git commit -m "init: laboratorio CaLola v0.3.0-lab"
   # crea el repo vacío en GitHub (privado) y copia su URL SSH o HTTPS
   git remote add origin <URL_DEL_REPO_EN_GITHUB>
   git push -u origin main
   ```
4. (Opcional) Crea ramas de trabajo y súbelas:
   ```bash
   git checkout -b lab/piloto
   git push -u origin lab/piloto
   git checkout -b exp/ssl
   git push -u origin exp/ssl
   ```

## Etiquetar un "release" (punto 5)
Un *release* es un **hito versionado** del código, con un **tag** (etiqueta) como `v0.3.0-lab`. Sirve para:
- Congelar un estado del proyecto (trazabilidad).
- Facilitar citas (con `CITATION.cff`) y conexión con **Zenodo** (para DOI).
- Entregar a evaluadores un paquete estable.

### Cómo etiquetar (GitHub UI)
1. Ve a **Releases → Draft a new release**.
2. En **Tag version** escribe `v0.3.0-lab` y crea el tag.
3. Título: “CaLola laboratorio v0.3.0-lab”.
4. Notas: copia cambios desde `CHANGELOG.md`.
5. Publica el release.

### Cómo etiquetar (línea de comandos)
```bash
git tag -a v0.3.0-lab -m "Release laboratorio v0.3.0"
git push origin v0.3.0-lab
```
Luego, en GitHub, ve a **Releases** y edita las notas si quieres.

## Generar evidencias y subirlas
Ejecuta localmente:
```bash
python scripts/verify_env.py
python scripts/make_screenshots.py --audio app/assets/sample_02.wav --out reports/
```
Esto crea `reports/env_report.md` y `reports/espectrograma.png`/`vad.png`/`metrics.json`/`report.md`.
Súbelos con:
```bash
git add reports/*
git commit -m "chore: evidencia base de laboratorio"
git push
```

## Conectar con Zenodo (DOI) — opcional
- Crea cuenta en https://zenodo.org y conecta tu GitHub.
- En GitHub, activa Zenodo para tu repo.
- Cuando publiques un release (`v0.3.0-lab`), Zenodo archivará esa versión y te dará un **DOI**.
- Sube **sólo código** (sin datos reales).

Listo. Con esto tendrás el proyecto versionado, reproducible y presentable.
