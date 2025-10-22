# 🌍 Visualizador de Conexiones de Red

Herramienta que muestra en un mapa interactivo todas las conexiones activas de tu equipo usando `netstat`.

## 📋 Características

- ✅ Captura todas las conexiones activas con `netstat`
- 🌍 Geolocaliza cada IP remota
- 🗺️ Muestra las conexiones en un mapa interactivo
- 📊 Estadísticas en tiempo real
- 🔄 Actualización manual de conexiones
- 📍 Líneas conectando tu ubicación con cada servidor remoto

## 🚀 Instalación

### 1. Instalar Python (si no lo tienes)
Descarga Python desde: https://www.python.org/downloads/

### 2. Instalar dependencias

Abre PowerShell en esta carpeta y ejecuta:

```powershell
pip install -r requirements.txt
```

## ▶️ Cómo Usar

### 1. Ejecutar el programa

En PowerShell, ejecuta:

```powershell
python network_mapper.py
```

### 2. Abrir en el navegador

Abre tu navegador y ve a:
```
http://localhost:5000
```

### 3. ¡Listo! 🎉

Verás un mapa con:
- 🟢 **Punto verde**: Tu ubicación actual
- 🔴 **Puntos rojos**: Servidores remotos conectados
- 🟡 **Líneas amarillas**: Conexiones activas

## 🎮 Controles

- **🔄 Actualizar Conexiones**: Captura nuevas conexiones
- **Click en marcadores**: Ver detalles de cada conexión
- **Zoom**: Usar scroll o botones +/- del mapa
- **Arrastrar**: Mover el mapa

## 📊 Información que muestra

Para cada conexión verás:
- IP y puerto remoto
- Ciudad y país del servidor
- ISP (Proveedor de servicios)
- Estado de la conexión (ESTABLISHED, TIME_WAIT, etc.)
- Protocolo (TCP/UDP)
- Organización propietaria de la IP

## ⚠️ Notas Importantes

1. **Requiere conexión a Internet** para geolocalizar las IPs
2. **No muestra IPs locales** (192.168.x.x, 127.0.0.1, etc.)
3. **Límite de 50 conexiones** mostradas simultáneamente (para no saturar la API)
4. **API gratuita**: ip-api.com (límite: 45 peticiones/minuto)

## 🛠️ Tecnologías Usadas

- **Backend**: Python + Flask
- **Frontend**: HTML + JavaScript + Leaflet.js
- **Geolocalización**: ip-api.com (API gratuita)
- **Comando**: netstat (Windows)

## 🐛 Solución de Problemas

### Error: "No se encuentra Python"
Instala Python desde python.org y marca "Add to PATH"

### Error: "pip no se reconoce"
Reinstala Python marcando la opción "Add Python to PATH"

### No aparecen conexiones
- Verifica que tengas conexiones activas (navega en internet)
- Ejecuta como Administrador si es necesario

### El mapa no carga
- Verifica tu conexión a Internet
- Revisa la consola del navegador (F12) para ver errores

## 📝 Autor

Proyecto creado para visualizar conexiones de red con netstat.
**BY JHOEL TITIRICO CHARCA**

## 📄 Licencia

Libre para uso educativo.
