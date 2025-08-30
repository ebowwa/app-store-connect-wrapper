#!/usr/bin/env python3
"""Add complete Spanish localization to SleepLoops app - all fields."""

import os
from dotenv import load_dotenv
from app_store_connect import Client

# Load environment variables
load_dotenv()

def main():
    """Add complete Spanish localization to SleepLoops."""
    print("🌙 SleepLoops Complete Spanish Localization")
    print("===========================================\n")
    
    # Initialize client
    client = Client(
        key_id=os.getenv("ASC_KEY_ID"),
        issuer_id=os.getenv("ASC_ISSUER_ID"),
        private_key_path=os.getenv("ASC_PRIVATE_KEY_PATH")
    )
    print("✅ Client initialized\n")
    
    # Find SleepLoops
    app = client.apps.get_by_bundle_id("com.ebowwa.sleeploops")
    if not app:
        print("❌ SleepLoops app not found")
        return
    
    app_id = app["id"]
    print(f"✅ Found SleepLoops (ID: {app_id})\n")
    
    # Complete Spanish (Mexico) content
    spanish_content = {
        # App Info fields (name and subtitle)
        "app_info": {
            "name": "SleepLoops: Planea Tu Sueño",
            "subtitle": "Calculadora de Ciclos de Sueño",
        },
        
        # App Store Version fields (description, keywords, etc.)
        "version": {
            # Description: Max 4000 chars - optimize for ASO with keywords!
            "description": """SleepLoops - La Calculadora Inteligente de Ciclos de Sueño

CANSADO DE DESPERTAR CANSADO? Tenemos la solucion cientifica!

SleepLoops es la aplicacion de alarma inteligente que revoluciona como duermes y despiertas. Usando la ciencia probada de los ciclos REM de 90 minutos, calculamos el momento EXACTO para despertar sintiendote renovado, no aturdido.

CARACTERISTICAS QUE AMARAS:

CALCULADORA DE SUEÑO INTELIGENTE:
Ingresa cuando necesitas despertar y te diremos las mejores horas para acostarte. O dinos cuando te acuestas y te mostraremos los momentos optimos para despertar. Asi de simple!

MULTIPLES ALARMAS INTELIGENTES:
Configura varias alarmas con un toque. Perfectas para siestas cortas de 20 minutos o ciclos completos de 90 minutos.

INTERFAZ NOCTURNA OSCURA:
Diseñada especificamente para no lastimar tus ojos en la oscuridad. Colores suaves que no interrumpen tu produccion de melatonina.

100% PRIVADO - SIN RASTREO:
Sin cuentas, sin registro, sin rastreo de sueño invasivo. Tu privacidad es sagrada. La app funciona completamente offline.

BASADO EN CIENCIA REAL:
Desarrollado usando investigacion de universidades lideres sobre ciclos de sueño REM y ritmos circadianos.

COMO FUNCIONA LA MAGIA:

Tu sueño naturalmente pasa por ciclos de 90 minutos, moviendose entre sueño ligero, profundo y REM. Despertar durante el sueño profundo = sentirte horrible. Despertar al final de un ciclo = sentirte increible.

SleepLoops calcula estos ciclos por ti:
- 1 ciclo = 1.5 horas
- 4 ciclos = 6 horas (minimo recomendado)
- 5 ciclos = 7.5 horas (optimo para adultos)
- 6 ciclos = 9 horas (recuperacion completa)

PERFECTO PARA:

ESTUDIANTES UNIVERSITARIOS
Optimiza tu sueño durante examenes. Estudia mejor con menos horas pero mejor calidad de descanso.

PROFESIONALES OCUPADOS
Reuniones tempranas, vuelos, presentaciones - despierta listo para conquistar el dia.

PADRES NUEVOS
Maximiza esas pocas horas de sueño. Cada minuto cuenta cuando el bebe finalmente duerme.

TRABAJADORES NOCTURNOS
Turnos nocturnos, guardias medicas, programadores - sincroniza tu sueño irregular perfectamente.

ATLETAS Y FITNESS
Recuperacion muscular optima sucede durante el sueño profundo. Maximiza tus ganancias.

VIAJEROS FRECUENTES
Combate el jet lag calculando los mejores momentos para dormir en nuevas zonas horarias.

BENEFICIOS BASADOS EN LA CIENCIA DEL SUEÑO:

Los ciclos de sueño de 90 minutos estan cientificamente documentados. Al despertar al final de un ciclo completo en lugar de en medio de uno:

- Te sientes mas alerta y menos aturdido
- Reduces la inercia del sueño (esa sensacion de zombie)
- Mejoras tu estado de animo matutino
- Necesitas menos tiempo para despertar completamente
- Tu cerebro procesa mejor la informacion del dia anterior

GRATIS Y SIN TRUCOS
Sin compras ocultas. Sin suscripciones. Sin anuncios molestos. Creemos que todos merecen dormir mejor.

DESCARGA AHORA Y ESTA NOCHE DORMIRAS MEJOR

Tu mejor sueño esta a solo un toque de distancia. Basado en ciencia real, sin promesas falsas - solo matematicas simples de ciclos de sueño que funcionan.""",
            
            # Keywords: Max 100 chars, comma-separated, prioritize high-search terms
            "keywords": "sueño,dormir,alarma,despertar,ciclos,rem,calculadora,insomnio,descanso,siesta,reloj,smart",
            
            # What's New: Max 4000 chars - use all of it for ASO!
            "whats_new": """NUEVA VERSION 2.0!

MEJORAS PRINCIPALES:
- Calculo mejorado de ciclos de sueño de 90 minutos
- Interfaz oscura rediseñada para uso nocturno
- Multiples alarmas con un solo toque
- Tiempos de siesta optimizados agregados

CORRECCIONES:
- Solucionado problema con calculos despues de medianoche
- Mejorado rendimiento en dispositivos antiguos
- Interfaz mas fluida y rapida

POR QUE SLEEPLOOPS?
Basado en ciencia del sueño comprobada. Despierta en el momento optimo de tu ciclo REM para sentirte renovado, no aturdido.

Gracias por usar SleepLoops! Tu feedback nos ayuda a mejorar.""",
            
            # Promotional text: Max 170 chars - make it compelling!
            "promotional_text": "Despierta renovado, no cansado! Calcula el momento PERFECTO para dormir y despertar usando ciclos REM de 90min. Sin rastreo, sin cuentas. Simple y efectivo!",
            
            "marketing_url": "",
            "support_url": "https://github.com/ebowwa/sleeploops-support",
        }
    }
    
    # Step 1: Update App Info localizations (name and subtitle)
    print("📝 Step 1: Updating App Info localizations...")
    app_infos = client.apps.get_app_infos(app_id)
    if app_infos:
        # Use the most recent app info
        app_info = app_infos[-1]
        app_info_id = app_info["id"]
        print(f"   Using App Info ID: {app_info_id}")
        
        # Check if Spanish localization already exists
        existing_locs = client.localizations.get_all(app_info_id)
        spanish_exists = any(loc.get("attributes", {}).get("locale") == "es-ES" for loc in existing_locs)
        
        if spanish_exists:
            print("   Spanish (es-ES) localization already exists for app info")
            # Could update it here if needed
        else:
            try:
                result = client.localizations.create(
                    app_info_id=app_info_id,
                    locale="es-ES",
                    name=spanish_content["app_info"]["name"],
                    subtitle=spanish_content["app_info"]["subtitle"],
                    privacy_policy_url=None,
                    privacy_policy_text=None
                )
                print("   ✅ Created Spanish app info localization")
            except Exception as e:
                print(f"   ❌ Error: {e}")
    
    # Step 2: Update App Store Version localizations (description, keywords, etc.)
    print("\n📝 Step 2: Updating App Store Version localizations...")
    
    # Get the editable version (PREPARE_FOR_SUBMISSION state)
    versions = client.versions.get_all(app_id)
    editable_version = None
    
    for version in versions:
        state = version.get("attributes", {}).get("appStoreState")
        if state in ["PREPARE_FOR_SUBMISSION", "DEVELOPER_REJECTED", "REJECTED", "WAITING_FOR_REVIEW"]:
            editable_version = version
            break
    
    if editable_version:
        version_id = editable_version["id"]
        version_string = editable_version.get("attributes", {}).get("versionString", "Unknown")
        print(f"   Found editable version: {version_string} (ID: {version_id})")
        
        # Get version localizations
        try:
            # Import the base request method
            from app_store_connect.base import BaseAPI
            
            # First, check existing localizations - need to access the base get method
            # The versions object inherits from BaseAPI
            version_locs_response = BaseAPI.get(client.versions, f"appStoreVersions/{version_id}/appStoreVersionLocalizations")
            version_locs = version_locs_response.get("data", [])
            
            # Check if Spanish already exists
            spanish_version_loc = None
            for loc in version_locs:
                if loc.get("attributes", {}).get("locale") == "es-ES":
                    spanish_version_loc = loc
                    break
            
            if spanish_version_loc:
                # Update existing Spanish localization
                loc_id = spanish_version_loc["id"]
                print(f"   Updating existing Spanish version localization (ID: {loc_id})")
                
                # Remove empty URLs - they might cause type errors
                update_attrs = {
                    "description": spanish_content["version"]["description"],
                    "keywords": spanish_content["version"]["keywords"],
                    "whatsNew": spanish_content["version"]["whats_new"],
                    "promotionalText": spanish_content["version"]["promotional_text"],
                    "supportUrl": spanish_content["version"]["support_url"],
                }
                
                # Only add marketing URL if it's not empty
                if spanish_content["version"]["marketing_url"]:
                    update_attrs["marketingUrl"] = spanish_content["version"]["marketing_url"]
                
                update_data = {
                    "data": {
                        "type": "appStoreVersionLocalizations",
                        "id": loc_id,
                        "attributes": update_attrs
                    }
                }
                
                result = BaseAPI.patch(client.versions, f"appStoreVersionLocalizations/{loc_id}", update_data)
                print("   ✅ Updated Spanish version localization with all fields!")
                
            else:
                # Create new Spanish localization
                print("   Creating new Spanish version localization...")
                
                # Prepare attributes without empty URLs
                create_attrs = {
                    "locale": "es-ES",
                    "description": spanish_content["version"]["description"],
                    "keywords": spanish_content["version"]["keywords"],
                    "whatsNew": spanish_content["version"]["whats_new"],
                    "promotionalText": spanish_content["version"]["promotional_text"],
                    "supportUrl": spanish_content["version"]["support_url"],
                }
                
                # Only add marketing URL if it's not empty
                if spanish_content["version"]["marketing_url"]:
                    create_attrs["marketingUrl"] = spanish_content["version"]["marketing_url"]
                
                create_data = {
                    "data": {
                        "type": "appStoreVersionLocalizations",
                        "attributes": create_attrs,
                        "relationships": {
                            "appStoreVersion": {
                                "data": {
                                    "type": "appStoreVersions",
                                    "id": version_id
                                }
                            }
                        }
                    }
                }
                
                result = BaseAPI.post(client.versions, "appStoreVersionLocalizations", create_data)
                print("   ✅ Created Spanish version localization with all fields!")
            
            print("\n📋 Spanish localization details:")
            print(f"   • Name: {spanish_content['app_info']['name']}")
            print(f"   • Subtitle: {spanish_content['app_info']['subtitle']}")
            print(f"   • Keywords: {spanish_content['version']['keywords'][:50]}...")
            print(f"   • Promotional Text: {spanish_content['version']['promotional_text']}")
            print(f"   • Description: {len(spanish_content['version']['description'])} characters")
            
        except Exception as e:
            print(f"   ❌ Error updating version localization: {e}")
    else:
        print("   ⚠️  No editable version found. You need a version in PREPARE_FOR_SUBMISSION state")
        print("      Available versions:")
        for v in versions:
            print(f"      - {v.get('attributes', {}).get('versionString')} ({v.get('attributes', {}).get('appStoreState')})")
    
    print("\n✨ Done!")

if __name__ == "__main__":
    main()