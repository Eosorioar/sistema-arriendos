import requests
import json
from datetime import datetime, timedelta

class UFApiClient:
    def __init__(self):
        self.base_url = "https://mindicador.cl/api"
        self.ultimos_valores_uf = {}  # Cache local: {fecha: valor}
        self.cargar_ultimo_mes_uf()
    
    def cargar_ultimo_mes_uf(self):
        """Carga una vez todos los valores UF del último mes"""
        try:
            print("📥 Cargando valores UF del último mes desde API...")
            url = f"{self.base_url}/uf"
            response = requests.get(url)
            
            if response.status_code == 200:
                datos = response.json()
                
                for registro in datos['serie']:
                    fecha_iso = registro['fecha']
                    fecha_simple = fecha_iso.split('T')[0]
                    valor = registro['valor']
                    self.ultimos_valores_uf[fecha_simple] = valor
                
                print(f"✅ Cargados {len(self.ultimos_valores_uf)} valores UF")
                fechas = sorted(self.ultimos_valores_uf.keys())
                if fechas:
                    print(f"📅 Rango: {fechas[0]} a {fechas[-1]}")
                    
        except Exception as e:
            print(f"❌ Error cargando UF: {e}")
    
    def obtener_uf_fecha(self, fecha):
        """Obtiene UF desde cache local"""
        try:
            if isinstance(fecha, datetime):
                fecha_str = fecha.strftime("%Y-%m-%d")
            else:
                fecha_str = fecha
            
            return self.ultimos_valores_uf.get(fecha_str)
            
        except Exception as e:
            print(f"❌ Error obteniendo UF: {e}")
            return None
    
    def obtener_ultima_uf_disponible(self):
        """Retorna el último valor UF disponible (más reciente)"""
        if not self.ultimos_valores_uf:
            return None
        
        fechas_ordenadas = sorted(self.ultimos_valores_uf.keys(), reverse=True)
        fecha_reciente = fechas_ordenadas[0]
        return self.ultimos_valores_uf[fecha_reciente]

    def obtener_ultima_fecha_disponible(self):
        """Retorna la última fecha con datos UF disponibles"""
        if not self.ultimos_valores_uf:
            return None
        
        fechas_ordenadas = sorted(self.ultimos_valores_uf.keys(), reverse=True)
        return fechas_ordenadas[0]

    def obtener_primera_fecha_disponible(self):
        """Retorna la primera fecha con datos UF disponibles"""
        if not self.ultimos_valores_uf:
            return None
        
        fechas_ordenadas = sorted(self.ultimos_valores_uf.keys())
        return fechas_ordenadas[0]
    
    def formatear_fecha_para_api(self, fecha):
        """
        Convierte fecha de YYYY-MM-DD a DD-MM-YYYY para la API
        """
        if isinstance(fecha, datetime):
            return fecha.strftime("%d-%m-%Y")
        else:
            # Asume que viene como string YYYY-MM-DD
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
            return fecha_obj.strftime("%d-%m-%Y")
    
    def obtener_uf_mas_cercana(self, fecha):
        """
        Busca UF para fecha específica
        CORREGIDO: Usa formato correcto DD-MM-YYYY para consultas API
        """
        try:
            if isinstance(fecha, datetime):
                fecha_str = fecha.strftime("%Y-%m-%d")
            else:
                fecha_str = fecha
        
            # 1. Primero intentar con cache
            uf_exacta = self.obtener_uf_fecha(fecha_str)
            if uf_exacta:
                return uf_exacta
            
            # 2. ✅ CORREGIDO: Usar formato DD-MM-YYYY para la API
            fecha_formateada = self.formatear_fecha_para_api(fecha_str)
            print(f"🔍 Consultando UF específica para {fecha_str} (URL: {fecha_formateada})...")
            
            url = f"{self.base_url}/uf/{fecha_formateada}"
            response = requests.get(url)
            
            if response.status_code == 200:
                datos = response.json()
                if datos['serie'] and len(datos['serie']) > 0:
                    valor_uf = datos['serie'][0]['valor']
                    # Guardar en cache para futuras consultas
                    self.ultimos_valores_uf[fecha_str] = valor_uf
                    print(f"✅ UF específica encontrada: ${valor_uf:,.0f}")
                    return valor_uf
                else:
                    print(f"⚠️ No hay datos en la serie para {fecha_str}")
            else:
                print(f"❌ Error API específica para {fecha_str} (HTTP {response.status_code})")
            
            # 3. Solo si falla la API específica, buscar en cache
            print("🔍 Buscando fecha UF más cercana en cache...")
            fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d")
            
            # Buscar hacia atrás (días anteriores)
            for dias in range(1, 30):
                fecha_anterior = fecha_obj - timedelta(days=dias)
                fecha_anterior_str = fecha_anterior.strftime("%Y-%m-%d")
                
                uf_anterior = self.obtener_uf_fecha(fecha_anterior_str)
                if uf_anterior:
                    print(f"⚠️ Usando UF de {fecha_anterior_str} para {fecha_str}")
                    return uf_anterior
            
            # 4. Último recurso
            ultima_uf = self.obtener_ultima_uf_disponible()
            if ultima_uf:
                print(f"⚠️ Usando última UF disponible para {fecha_str}")
                return ultima_uf
            
            return None
            
        except Exception as e:
            print(f"❌ Error buscando UF: {e}")
            return None

    # Método opcional para ver datos cargados (debug)
    def mostrar_datos_cargados(self):
        """Muestra todos los valores UF cargados (para debug)"""
        print("\n📊 DATOS UF CARGADOS EN MEMORIA:")
        print("Fecha".ljust(12) + "|" + "Valor UF".ljust(15))
        print("-" * 30)
        
        for fecha, valor in sorted(self.ultimos_valores_uf.items()):
            print(f"{fecha} | ${valor:,.0f}")
        
        print(f"\nTotal: {len(self.ultimos_valores_uf)} registros")