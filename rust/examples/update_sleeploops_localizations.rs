use app_store_connect_rust::{Client, AppStoreConnectError, AuthenticationError};
use serde_json::json;
use std::env;

#[tokio::main]
async fn main() -> Result<(), AppStoreConnectError> {
    println!("🌙 SleepLoops App Store Localization Updater");
    println!("============================================\n");
    
    // Load environment variables from parent directory's .env
    let _ = dotenvy::from_path("../.env");
    
    // Get credentials
    let key_id = env::var("ASC_KEY_ID")
        .map_err(|_| AppStoreConnectError::Authentication(AuthenticationError::new("ASC_KEY_ID not set")))?;
    let issuer_id = env::var("ASC_ISSUER_ID")
        .map_err(|_| AppStoreConnectError::Authentication(AuthenticationError::new("ASC_ISSUER_ID not set")))?;
    let mut private_key_path = env::var("ASC_PRIVATE_KEY_PATH")
        .map_err(|_| AppStoreConnectError::Authentication(AuthenticationError::new("ASC_PRIVATE_KEY_PATH not set")))?;
    
    // If path starts with ./, make it relative to parent directory
    if private_key_path.starts_with("./") {
        private_key_path = format!("../{}", private_key_path.trim_start_matches("./"));
    }
    
    // Initialize client
    let client = Client::new(&key_id, &issuer_id, &private_key_path).await?;
    println!("✅ Client initialized successfully\n");
    
    // SleepLoops bundle ID
    let bundle_id = "com.ebowwa.sleeploops";
    
    // Find the app by bundle ID
    println!("🔍 Looking for SleepLoops app...");
    let app = client.get_app_by_bundle_id(bundle_id).await?;
    
    if let Some(app_data) = app {
        let app_id = app_data.get("id")
            .and_then(|id| id.as_str())
            .ok_or_else(|| AppStoreConnectError::Api { 
                message: "App ID not found".to_string() 
            })?;
        
        let app_name = app_data.get("attributes")
            .and_then(|attrs| attrs.get("name"))
            .and_then(|name| name.as_str())
            .unwrap_or("Unknown");
        
        println!("✅ Found app: {} (ID: {})\n", app_name, app_id);
        
        // Define the Spanish (Mexico) localization content
        let spanish_mx_metadata = json!({
            "name": "SleepLoops: Planea Tu Sueño",
            "subtitle": "Calculadora Inteligente de Ciclos de Sueño",
            "description": r#"SleepLoops te ayuda a despertar renovado calculando los horarios óptimos para dormir y despertar basándose en los ciclos naturales de sueño de 90 minutos.

CARACTERÍSTICAS PRINCIPALES:
• Calculadora Inteligente de Sueño - Encuentra la hora perfecta para acostarte según cuando necesitas despertar
• Optimizador de Hora de Despertar - Descubre los mejores momentos para despertar si te acuestas ahora
• Ciencia de los Ciclos de Sueño - Aprende sobre los ciclos REM de 90 minutos y por qué el tiempo importa
• Múltiples Alarmas - Configura alarmas para horarios óptimos con un solo toque
• Hermosa Interfaz Oscura - Fácil para los ojos durante el uso nocturno
• Simple y Rápido - Sin rastreo, sin cuentas, solo cálculos instantáneos

POR QUÉ IMPORTAN LOS CICLOS DE SUEÑO:
Despertar en medio de un ciclo de sueño puede dejarte sintiéndote aturdido y cansado. SleepLoops calcula los momentos óptimos para despertar al final de un ciclo completo, ayudándote a sentirte más renovado y alerta.

LA CIENCIA:
Basado en investigación del sueño que muestra que nuestro descanso sigue ciclos predecibles de 90 minutos. Al sincronizar tu despertar con las etapas más ligeras del sueño, te sentirás naturalmente más descansado.

PERFECTO PARA:
• Estudiantes optimizando horarios de estudio
• Profesionales manejando horarios irregulares
• Padres coordinando rutinas de sueño familiar
• Trabajadores por turnos planeando períodos de descanso
• Cualquiera que quiera despertar sintiéndose mejor

¡Descarga SleepLoops hoy y despierta renovado mañana!"#,
            "keywords": "sueño,ciclos,alarma,despertar,dormir,REM,calculadora,calidad,descanso",
            "whatsNew": "Lanzamiento inicial con características principales de cálculo de ciclos de sueño",
            "promotionalText": "¡Despierta renovado! Calcula tiempos óptimos de sueño basados en ciclos de 90 minutos.",
            "marketingUrl": "",
            "supportUrl": "https://github.com/ebowwa/sleeploops-support",
            "privacyPolicyUrl": ""
        });
        
        // Get app info localizations
        println!("📝 Adding Spanish (Mexico) localization...");
        
        // First, get existing app info
        println!("🔍 Getting app info...");
        let app_infos = client.apps().get_app_infos(app_id).await?;
        println!("  Found {} app info(s)", app_infos.len());
        
        if let Some(app_info) = app_infos.first() {
            let app_info_id = app_info.get("id")
                .and_then(|id| id.as_str())
                .ok_or_else(|| AppStoreConnectError::Api { 
                    message: "App Info ID not found".to_string() 
                })?;
            
            println!("  App Info ID: {}", app_info_id);
            
            // Get existing localizations to see what's already there
            println!("🔍 Checking existing localizations...");
            let existing_localizations = client.localizations().get_all(app_info_id).await?;
            println!("  Found {} existing localization(s)", existing_localizations.len());
            
            for loc in &existing_localizations {
                if let Some(attrs) = loc.get("attributes") {
                    if let Some(locale) = attrs.get("locale").and_then(|l| l.as_str()) {
                        println!("  - {}", locale);
                    }
                }
            }
            
            // Create Spanish (Mexico) localization directly
            println!("\n📝 Creating Spanish (Mexico) localization...");
            
            // Try different locale codes - Apple might use es-ES or es-419 for Latin America
            let locale_code = "es-ES"; // Try Spanish (Spain) first
            println!("  Using locale code: {}", locale_code);
            
            // Extract the values we need
            let name = spanish_mx_metadata.get("name").and_then(|n| n.as_str());
            let subtitle = spanish_mx_metadata.get("subtitle").and_then(|s| s.as_str());
            let privacy_policy_url = spanish_mx_metadata.get("privacyPolicyUrl").and_then(|u| u.as_str());
            
            // Create the localization
            let result = client.localizations().create(
                app_info_id,
                locale_code,
                name,
                subtitle,
                if privacy_policy_url == Some("") { None } else { privacy_policy_url },
                None  // privacy_policy_text
            ).await?;
            
            println!("✅ Successfully added Spanish (Mexico) localization!");
            
            // Print what was created
            if let Some(attrs) = result.get("attributes") {
                println!("\n📋 Created metadata:");
                if let Some(name) = attrs.get("name") {
                    println!("  • Name: {}", name);
                }
                if let Some(subtitle) = attrs.get("subtitle") {
                    println!("  • Subtitle: {}", subtitle);
                }
                if let Some(locale) = attrs.get("locale") {
                    println!("  • Locale: {}", locale);
                }
            }
        } else {
            println!("❌ No app info found for this app");
        }
        
    } else {
        println!("❌ App with bundle ID '{}' not found", bundle_id);
        println!("\n📱 Available apps:");
        
        // List all available apps to help debug
        let all_apps = client.apps().get_all(Some(20)).await?;
        for app in all_apps.iter() {
            if let Some(attrs) = app.get("attributes") {
                let name = attrs.get("name")
                    .and_then(|n| n.as_str())
                    .unwrap_or("Unknown");
                let bundle = attrs.get("bundleId")
                    .and_then(|b| b.as_str())
                    .unwrap_or("Unknown");
                println!("  - {} ({})", name, bundle);
            }
        }
    }
    
    println!("\n✨ Done!");
    Ok(())
}