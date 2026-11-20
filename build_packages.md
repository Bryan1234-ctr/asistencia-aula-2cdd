# 📦 Cómo generar instaladores (EXE, Linux, Mac, APK)

## Resumen rápido

| Plataforma | Formato | Cómo obtenerlo |
|-----------|---------|----------------|
| **Windows** | `.exe` | PyInstaller (ver abajo) |
| **Linux** | binario / AppImage | PyInstaller o AppImage |
| **macOS** | `.app` / `.dmg` | PyInstaller en Mac |
| **Android** | PWA instalable + APK | PWA ya incluida + Capacitor (opcional) |

---

## 1. Escritorio (Windows / Linux / Mac) con PyInstaller

### Requisitos
```bash
pip install pyinstaller
```

### Generar el ejecutable

Desde la raíz del proyecto:

```bash
# Windows (genera .exe)
pyinstaller --noconfirm --onefile --windowed \
  --name "Asistencia_2CDD_A" \
  --add-data "templates;templates" \
  --add-data "static;static" \
  --add-data "app;app" \
  run_desktop.py

# Linux / Mac (genera binario)
pyinstaller --noconfirm --onefile \
  --name "Asistencia_2CDD_A" \
  --add-data "templates:templates" \
  --add-data "static:static" \
  --add-data "app:app" \
  run_desktop.py
```

El ejecutable queda en la carpeta `dist/`.

> **Nota Windows:** El separador de `--add-data` es `;`  
> **Nota Linux/Mac:** El separador es `:`

### Uso del ejecutable
1. Doble clic en `Asistencia_2CDD_A.exe` (Windows) o `./Asistencia_2CDD_A` (Linux/Mac)
2. Se abre el navegador automáticamente con la app
3. Funciona offline (usa SQLite local)

---

## 2. Android – Opción A: PWA (ya incluida, sin APK)

La app ya es una **Progressive Web App**:

1. Abre la app en **Chrome** del celular (http://IP-de-tu-PC:8000 o el servidor)
2. Menú → **“Agregar a la pantalla de inicio”** / **“Instalar aplicación”**
3. Queda un ícono como cualquier app

Ventajas: no necesitas Play Store ni APK firmado.

---

## 3. Android – Opción B: APK real con Capacitor

```bash
npm install -g @capacitor/cli
npm init -y
npm install @capacitor/core @capacitor/cli @capacitor/android
npx cap init "Asistencia 2CDD A" "com.fonseca.asistencia2cdd" --web-dir=www
npx cap add android
npx cap sync
npx cap open android   # Android Studio → Build → Generate Signed APK/Bundle
```

---

## 4. Comandos rápidos

```bash
# Solo ejecutar
python run_desktop.py

# EXE en Windows
pip install pyinstaller
pyinstaller --onefile --windowed --name Asistencia_2CDD_A --add-data "templates;templates" --add-data "static;static" --add-data "app;app" run_desktop.py

# Binario Linux/Mac
pyinstaller --onefile --name Asistencia_2CDD_A --add-data "templates:templates" --add-data "static:static" --add-data "app:app" run_desktop.py
```

## Notas

- El ejecutable incluye el servidor + SQLite. Se crea `asistencia.db` junto al ejecutable.
- La **PWA** es la forma más rápida de tener la app en el celular sin Play Store.
- Un APK para Play Store requiere cuenta de desarrollador Google.
