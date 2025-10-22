import subprocess
import re
import json
import requests
from flask import Flask, render_template, jsonify
from flask_cors import CORS
import socket

app = Flask(__name__)
CORS(app)

def get_netstat_connections():
    """Obtiene las conexiones activas usando netstat"""
    try:
        # Ejecutar netstat en Windows
        result = subprocess.run(['netstat', '-n'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
        output = result.stdout
        
        connections = []
        lines = output.split('\n')
        
        for line in lines:
            # Buscar líneas con conexiones TCP
            if 'TCP' in line or 'UDP' in line:
                parts = line.split()
                if len(parts) >= 4:
                    try:
                        protocol = parts[0]
                        local_address = parts[1]
                        foreign_address = parts[2]
                        state = parts[3] if len(parts) > 3 else 'N/A'
                        
                        # Extraer IP y puerto
                        if ':' in foreign_address:
                            foreign_ip = foreign_address.rsplit(':', 1)[0]
                            foreign_port = foreign_address.rsplit(':', 1)[1]
                            
                            # Filtrar IPs locales, privadas y multicast
                            if not (foreign_ip.startswith('127.') or 
                                   foreign_ip.startswith('192.168.') or 
                                   foreign_ip.startswith('10.') or
                                   foreign_ip.startswith('172.') or
                                   foreign_ip.startswith('169.254.') or
                                   foreign_ip.startswith('224.') or
                                   foreign_ip == '0.0.0.0' or
                                   foreign_ip == '*' or
                                   foreign_ip.startswith('[::')):
                                
                                connections.append({
                                    'protocol': protocol,
                                    'local_address': local_address,
                                    'foreign_ip': foreign_ip,
                                    'foreign_port': foreign_port,
                                    'foreign_address': foreign_address,
                                    'state': state
                                })
                    except Exception as e:
                        continue
        
        return connections
    except Exception as e:
        print(f"Error ejecutando netstat: {e}")
        return []

def get_ip_location(ip):
    """Obtiene la geolocalización de una IP usando ip-api.com (gratuito)"""
    try:
        # API gratuita sin necesidad de key
        response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                return {
                    'ip': ip,
                    'country': data.get('country', 'Unknown'),
                    'countryCode': data.get('countryCode', ''),
                    'region': data.get('regionName', ''),
                    'city': data.get('city', 'Unknown'),
                    'lat': data.get('lat', 0),
                    'lon': data.get('lon', 0),
                    'isp': data.get('isp', 'Unknown'),
                    'org': data.get('org', 'Unknown')
                }
    except Exception as e:
        print(f"Error obteniendo ubicación para {ip}: {e}")
    
    return None

def get_my_location():
    """Obtiene la ubicación actual del equipo"""
    try:
        response = requests.get('http://ip-api.com/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                return {
                    'ip': data.get('query', 'Unknown'),
                    'country': data.get('country', 'Unknown'),
                    'city': data.get('city', 'Unknown'),
                    'lat': data.get('lat', 0),
                    'lon': data.get('lon', 0),
                    'isp': data.get('isp', 'Unknown')
                }
    except Exception as e:
        print(f"Error obteniendo mi ubicación: {e}")
    
    # Ubicación por defecto si falla
    return {
        'ip': 'Unknown',
        'country': 'Unknown',
        'city': 'Unknown',
        'lat': 0,
        'lon': 0,
        'isp': 'Unknown'
    }

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/api/connections')
def get_connections():
    """API que devuelve las conexiones con geolocalización"""
    print("Obteniendo conexiones...")
    
    # Obtener conexiones de netstat
    connections = get_netstat_connections()
    print(f"Encontradas {len(connections)} conexiones")
    
    # Obtener mi ubicación
    my_location = get_my_location()
    print(f"Mi ubicación: {my_location['city']}, {my_location['country']}")
    
    # Obtener ubicación de cada IP (limitamos para evitar rate limit)
    connections_with_location = []
    processed_ips = {}  # Cache para no consultar la misma IP múltiples veces
    
    for conn in connections[:50]:  # Limitamos a 50 conexiones para no saturar la API
        foreign_ip = conn['foreign_ip']
        
        # Usar cache si ya procesamos esta IP
        if foreign_ip in processed_ips:
            location = processed_ips[foreign_ip]
        else:
            location = get_ip_location(foreign_ip)
            processed_ips[foreign_ip] = location
        
        if location:
            connections_with_location.append({
                'connection': conn,
                'location': location
            })
    
    print(f"Conexiones con ubicación: {len(connections_with_location)}")
    
    return jsonify({
        'my_location': my_location,
        'connections': connections_with_location,
        'total_connections': len(connections)
    })

if __name__ == '__main__':
    print("=" * 60)
    print("🌍 VISUALIZADOR DE CONEXIONES DE RED")
    print("=" * 60)
    print("\n📡 Iniciando servidor...")
    print("🌐 Abre tu navegador en: http://localhost:5000")
    print("\n⚠️  Presiona Ctrl+C para detener el servidor\n")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
