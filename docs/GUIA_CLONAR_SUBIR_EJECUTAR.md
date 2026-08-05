# Guía para clonar, aplicar, ejecutar y subir el prototipo

El ZIP entregado contiene el proyecto completo modificado. El repositorio parece corresponder a
`CZalbert67/ImpactX-machine-learning`; si la URL cambió, copia la dirección correcta desde el botón
**Code** de GitHub.

## 1. Instalar herramientas en Arch Linux

```bash
sudo pacman -S --needed git python python-pip rsync unzip github-cli
```

## 2. Autenticarse en GitHub

```bash
gh auth login
```

Selecciona GitHub.com, HTTPS y autenticación desde el navegador.

## 3. Clonar el repositorio

```bash
cd ~/Documentos
git clone https://github.com/CZalbert67/ImpactX-machine-learning.git
cd ImpactX-machine-learning
git switch -c feat/modelo-predictivo-v1
```

Para SSH se puede usar:

```bash
git clone git@github.com:CZalbert67/ImpactX-machine-learning.git
```

## 4. Copiar la versión entregada sobre el clon

Suponiendo que el ZIP está en `~/Descargas`:

```bash
mkdir -p /tmp/impactx-ml-entregado
unzip -o ~/Descargas/ImpactX-machine-learning-prototipo-v1.zip \
  -d /tmp/impactx-ml-entregado

rsync -av --delete --exclude='.git/' \
  /tmp/impactx-ml-entregado/ImpactX-machine-learning-main/ \
  ~/Documentos/ImpactX-machine-learning/
```

El comando conserva la carpeta `.git` del clon y actualiza el resto del proyecto.

## 5. Preparar y ejecutar

```bash
cd ~/Documentos/ImpactX-machine-learning
chmod +x scripts/*.sh
./scripts/bootstrap.sh
source .venv/bin/activate
python app.py
```

Abre:

- Aplicación: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- Salud: `http://127.0.0.1:8000/health`

Detén el servidor con `Ctrl+C`.

## 6. Ejecutar pruebas

```bash
source .venv/bin/activate
pytest --cov=impactx_ml
```

## 7. Guardar y subir la rama

```bash
git status
git add .
git commit -m "feat: add collision severity ML prototype"
git push -u origin feat/modelo-predictivo-v1
```

Después abre el Pull Request:

```bash
gh pr create \
  --base main \
  --head feat/modelo-predictivo-v1 \
  --title "feat: modelo predictivo de gravedad de choque" \
  --body "Agrega modelo Random Forest, frontend local, API, política de alertas, pruebas y documentación."
```
