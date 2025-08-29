use app_store_connect_rust::{Client, Result};
use serde_json::json;
use std::collections::HashMap;
use std::env;

#[tokio::main]
async fn main() -> Result<()> {
    dotenvy::dotenv().ok();

    let args: Vec<String> = env::args().collect();
    let dry_run = args.contains(&"--dry-run".to_string());

    let app_id =
        env::var("ASC_APP_ID").map_err(|_| app_store_connect_rust::AppStoreConnectError::Api {
            message: "ASC_APP_ID environment variable not set".to_string(),
        })?;

    println!(
        "{}Syncing localizations for app {}...",
        if dry_run { "[DRY RUN] " } else { "" },
        app_id
    );

    let localizations = get_localizations();

    if dry_run {
        println!("\nWould update the following localizations:");
        for (locale, data) in &localizations {
            println!("  {}:", locale);
            if let Some(name) = data.get("name") {
                println!("    Name: {}", name);
            }
            if let Some(subtitle) = data.get("subtitle") {
                println!("    Subtitle: {}", subtitle);
            }
        }
        return Ok(());
    }

    let client = Client::from_env().await?;

    println!("\nFetching app info...");
    let app_infos = client.apps().get_app_infos(&app_id).await?;

    if app_infos.is_empty() {
        println!("ERROR: No app info found!");
        return Ok(());
    }

    let mut app_info_id = None;
    for app_info in &app_infos {
        if let Some(state) = app_info
            .get("attributes")
            .and_then(|a| a.get("appStoreState"))
            .and_then(|s| s.as_str())
        {
            let id = app_info
                .get("id")
                .and_then(|i| i.as_str())
                .unwrap_or("unknown");
            println!("  App info {}: state={}", id, state);

            if matches!(
                state,
                "DEVELOPER_REJECTED" | "PREPARE_FOR_SUBMISSION" | "METADATA_REJECTED"
            ) {
                app_info_id = Some(id.to_string());
                println!("  -> Using editable app info: {}", id);
                break;
            }
        }
    }

    let app_info_id = app_info_id.unwrap_or_else(|| {
        let id = app_infos[0]
            .get("id")
            .and_then(|i| i.as_str())
            .unwrap_or("unknown");
        println!(
            "WARNING: No editable app info found. Using first available: {}",
            id
        );
        id.to_string()
    });

    println!("\nUpdating localizations for app info {}...", app_info_id);
    let results = client
        .localizations()
        .bulk_update(&app_info_id, localizations)
        .await?;

    let mut success_count = 0;
    let mut failure_count = 0;

    for (locale, result) in &results {
        if let Some(success) = result.get("success").and_then(|s| s.as_bool()) {
            if success {
                success_count += 1;
                let action = result
                    .get("action")
                    .and_then(|a| a.as_str())
                    .unwrap_or("updated");
                println!("  ✓ {}: {}", locale, action);
            } else {
                failure_count += 1;
                let error = result
                    .get("error")
                    .and_then(|e| e.as_str())
                    .unwrap_or("Unknown error");
                println!("  ✗ {}: {}", locale, error);
            }
        }
    }

    println!("\nSummary:");
    println!("  Success: {}", success_count);
    println!("  Failed: {}", failure_count);

    Ok(())
}

fn get_localizations() -> HashMap<String, serde_json::Value> {
    let mut localizations = HashMap::new();

    let app_names = [
        ("de-DE", "SauberBild"),
        ("en-US", "CleanShot"),
        ("es-ES", "FotoLimpia"),
        ("es-MX", "FotoLimpia México"),
        ("fr-FR", "PhotoPure"),
        ("ja", "クリーンショット"),
        ("ko", "클린샷"),
        ("pt-BR", "FotoLimpa Brasil"),
        ("ru", "ЧистыйСнимок"),
        ("zh-Hans", "净图"),
        ("zh-Hant", "淨圖"),
        ("ar-SA", "صورة نظيفة"),
        ("hi", "साफ़ छवि"),
        ("it", "Scatto Pulito"),
    ];

    let app_subtitles = [
        ("de-DE", "Entfernen Sie Metadaten sicher"),
        ("en-US", "Remove metadata safely"),
        ("es-ES", "Elimina metadatos de forma segura"),
        ("es-MX", "Elimina metadatos de forma segura"),
        ("fr-FR", "Supprimez les métadonnées en toute sécurité"),
        ("ja", "メタデータを安全に削除"),
        ("ko", "메타데이터를 안전하게 제거"),
        ("pt-BR", "Remova metadados com segurança"),
        ("ru", "Безопасно удаляйте метаданные"),
        ("zh-Hans", "安全地删除元数据"),
        ("zh-Hant", "安全地刪除元數據"),
        ("ar-SA", "إزالة البيانات الوصفية بأمان"),
        ("hi", "मेटाडेटा को सुरक्षित रूप से हटाएं"),
        ("it", "Rimuovi i metadati in sicurezza"),
    ];

    for (locale, name) in &app_names {
        let subtitle = app_subtitles
            .iter()
            .find(|(l, _)| l == locale)
            .map(|(_, s)| *s)
            .unwrap_or("");

        localizations.insert(
            locale.to_string(),
            json!({
                "name": name,
                "subtitle": subtitle
            }),
        );
    }

    localizations
}
