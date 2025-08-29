#!/usr/bin/env python3
"""
Example script to update App Store Connect localizations with keywords, descriptions, and metadata

This script demonstrates how to update all localizations for a specific app version.
It includes proper character limits and localized content for each market.

Usage:
    1. Set environment variables:
       - ASC_KEY_ID
       - ASC_ISSUER_ID  
       - ASC_PRIVATE_KEY_PATH
       - ASC_APP_ID
    2. Update VERSION_ID below or pass as environment variable
    3. Run: python update_localizations.py
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from app_store_connect import Client
from app_store_connect.api.localizations import AppStoreVersionLocalizationsAPI


# Localization data for each language
# NOTE: Excluding en-US as requested - don't edit the main English market
# IMPORTANT: App Store Connect limits:
#   - Description: 4000 characters max
#   - Keywords: 100 characters max (comma-separated)
#   - Promotional text: 170 characters max
#   - Subtitle: 30 characters max
#   - What's new: 4000 characters max
LOCALIZATIONS = {
    'de-DE': {
        'description': """SicherFoto schützt Ihre Privatsphäre durch Entfernen von GPS-Standorten und EXIF-Metadaten aus Fotos.

• GPS-Daten entfernen
• Kameradetails löschen  
• Zeitstempel bereinigen
• Stapelverarbeitung
• Originalqualität erhalten
• Ein-Tap-Reinigung

Perfekt für soziale Medien, Online-Verkäufe und datenschutzbewusste Nutzer.""",
        'keywords': 'exif,metadaten,privatsphäre,gps,standort,entfernen,foto,sicher',
        'subtitle': 'Privatsphäre-Schutz',
        'promotional_text': 'GPS und EXIF-Metadaten aus Fotos entfernen. Schützen Sie Ihre Privatsphäre!',
        'whats_new': 'Fehlerbehebungen und Leistungsverbesserungen'
    },
    'es-ES': {
        'description': """FotoPrivada protege tu privacidad eliminando GPS y metadatos EXIF de las fotos.

• Eliminar ubicación GPS
• Borrar datos de cámara
• Limpiar timestamps
• Procesamiento por lotes
• Calidad original
• Un toque para limpiar

Ideal para redes sociales, ventas online y usuarios conscientes de privacidad.""",
        'keywords': 'exif,metadatos,privacidad,gps,ubicación,eliminar,foto,limpiar',
        'subtitle': 'Protección de Privacidad',
        'promotional_text': 'Elimina GPS y EXIF de fotos. ¡Protege tu privacidad con un toque!',
        'whats_new': 'Corrección de errores y mejoras de rendimiento'
    },
    'fr-FR': {
        'description': """PhotoPure protège votre vie privée en supprimant GPS et métadonnées EXIF des photos.

• Supprimer localisation GPS
• Effacer données appareil photo
• Nettoyer horodatages
• Traitement par lots
• Qualité originale
• Nettoyage en un tap

Parfait pour réseaux sociaux, ventes en ligne et utilisateurs soucieux de confidentialité.""",
        'keywords': 'exif,métadonnées,confidentialité,gps,localisation,supprimer,photo',
        'subtitle': 'Protection Vie Privée',
        'promotional_text': 'Supprimez GPS et EXIF des photos. Protégez votre vie privée!',
        'whats_new': 'Corrections de bugs et améliorations de performances'
    },
    'ja': {
        'description': """クリーンショットは写真のGPSとEXIFメタデータを削除してプライバシーを保護します。

• GPS位置データ削除
• カメラ情報消去
• タイムスタンプクリア
• 一括処理
• 画質保持
• ワンタップ

SNS共有や販売に最適。""",
        'keywords': 'exif,メタデータ,プライバシー,gps,位置情報,削除,写真',
        'subtitle': 'プライバシー保護',
        'promotional_text': 'GPSとEXIFを削除。ワンタップでプライバシー保護！',
        'whats_new': 'バグ修正とパフォーマンスの改善'
    },
    'ko': {
        'description': """클린샷은 사진에서 GPS와 EXIF 메타데이터를 제거하여 개인정보를 보호합니다.

• GPS 위치 제거
• 카메라 정보 삭제
• 타임스탬프 정리
• 일괄 처리
• 원본 품질 유지
• 원탭 정리

SNS 공유와 온라인 판매에 최적.""",
        'keywords': 'exif,메타데이터,개인정보,gps,위치,제거,사진',
        'subtitle': '개인정보 보호',
        'promotional_text': 'GPS와 EXIF 제거. 원탭으로 개인정보 보호!',
        'whats_new': '버그 수정 및 성능 개선'
    },
    'pt-BR': {
        'description': """FotoLimpa protege sua privacidade removendo GPS e metadados EXIF das fotos.

• Remover localização GPS
• Apagar dados da câmera
• Limpar timestamps
• Processamento em lote
• Qualidade original
• Limpeza com um toque

Perfeito para redes sociais, vendas online e usuários conscientes sobre privacidade.""",
        'keywords': 'exif,metadados,privacidade,gps,localização,remover,foto,limpar',
        'subtitle': 'Proteção de Privacidade',
        'promotional_text': 'Remove GPS e EXIF de fotos. Proteja sua privacidade!',
        'whats_new': 'Correções de bugs e melhorias de desempenho'
    },
    'ru': {
        'description': """ЧистыйСнимок защищает конфиденциальность, удаляя GPS и EXIF метаданные из фото.

• Удаление GPS-локации
• Стирание данных камеры
• Очистка временных меток
• Пакетная обработка
• Исходное качество
• Очистка одним касанием

Идеально для соцсетей, онлайн-продаж и пользователей, заботящихся о конфиденциальности.""",
        'keywords': 'exif,метаданные,конфиденциальность,gps,локация,удалить,фото',
        'subtitle': 'Защита Конфиденциальности',
        'promotional_text': 'Удаляйте GPS и EXIF из фото. Защитите конфиденциальность!',
        'whats_new': 'Исправления ошибок и улучшения производительности'
    },
    'zh-Hans': {
        'description': """净图通过删除GPS和EXIF元数据保护您的隐私。

• 删除GPS位置
• 清除相机信息
• 清理时间戳
• 批量处理
• 保持原始质量
• 一键清理

适合社交媒体分享和在线销售。""",
        'keywords': 'exif,元数据,隐私,gps,位置,删除,照片,清理',
        'subtitle': '隐私保护',
        'promotional_text': '删除GPS和EXIF元数据。一键保护隐私！',
        'whats_new': '错误修复和性能改进'
    },
    'zh-Hant': {
        'description': """淨圖通過刪除GPS和EXIF元數據保護您的隱私。

• 刪除GPS位置
• 清除相機資訊
• 清理時間戳
• 批量處理
• 保持原始質量
• 一鍵清理

適合社交媒體分享和線上銷售。""",
        'keywords': 'exif,元數據,隱私,gps,位置,刪除,照片,清理',
        'subtitle': '隱私保護',
        'promotional_text': '刪除GPS和EXIF元數據。一鍵保護隱私！',
        'whats_new': '錯誤修復和性能改進'
    },
    'ar-SA': {
        'description': """صورة نظيفة تحمي خصوصيتك بإزالة GPS وبيانات EXIF من الصور.

• إزالة موقع GPS
• مسح بيانات الكاميرا
• تنظيف الطوابع الزمنية
• معالجة دفعية
• جودة أصلية
• تنظيف بلمسة واحدة

مثالي لوسائل التواصل الاجتماعي والبيع عبر الإنترنت.""",
        'keywords': 'exif,بيانات وصفية,خصوصية,gps,موقع,إزالة,صورة,تنظيف',
        'subtitle': 'حماية الخصوصية',
        'promotional_text': 'إزالة GPS وEXIF من الصور. احم خصوصيتك بلمسة!',
        'whats_new': 'إصلاحات الأخطاء وتحسينات الأداء'
    },
    'hi': {
        'description': """साफ़ छवि GPS और EXIF मेटाडेटा हटाकर आपकी गोपनीयता की रक्षा करती है।

• GPS स्थान हटाएं
• कैमरा डेटा मिटाएं
• टाइमस्टैम्प साफ़ करें
• बैच प्रोसेसिंग
• मूल गुणवत्ता
• एक टैप सफाई

सोशल मीडिया शेयरिंग और ऑनलाइन बिक्री के लिए आदर्श।""",
        'keywords': 'exif,मेटाडेटा,गोपनीयता,gps,स्थान,हटाना,फोटो',
        'subtitle': 'गोपनीयता सुरक्षा',
        'promotional_text': 'GPS और EXIF हटाएं। एक टैप से गोपनीयता सुरक्षित करें!',
        'whats_new': 'बग फिक्स और प्रदर्शन सुधार'
    },
    'it': {
        'description': """Scatto Pulito protegge la privacy rimuovendo GPS e metadati EXIF dalle foto.

• Rimuovi posizione GPS
• Cancella dati fotocamera
• Pulisci timestamp
• Elaborazione batch
• Qualità originale
• Pulizia con un tocco

Perfetto per social media, vendite online e utenti attenti alla privacy.""",
        'keywords': 'exif,metadati,privacy,gps,posizione,rimuovere,foto,pulire',
        'subtitle': 'Protezione Privacy',
        'promotional_text': 'Rimuovi GPS e EXIF dalle foto. Proteggi la privacy!',
        'whats_new': 'Correzioni di bug e miglioramenti delle prestazioni'
    },
    'es-MX': {
        'description': """FotoLimpia México protege tu privacidad eliminando GPS y metadatos EXIF de las fotos.

• Eliminar ubicación GPS
• Borrar datos de cámara
• Limpiar timestamps
• Procesamiento por lotes
• Calidad original
• Un toque para limpiar

Ideal para redes sociales, ventas online y usuarios conscientes de privacidad.""",
        'keywords': 'exif,metadatos,privacidad,gps,ubicación,eliminar,foto,limpiar',
        'subtitle': 'Protección de Privacidad',
        'promotional_text': 'Elimina GPS y EXIF de fotos. ¡Protege tu privacidad con un toque!',
        'whats_new': 'Corrección de errores y mejoras de rendimiento'
    }
}


def update_app_store_version_localizations(client: Client, app_id: str, dry_run: bool = False) -> Dict[str, Any]:
    """
    Update App Store version localizations with keywords, descriptions, and metadata
    
    IMPORTANT: App Store Connect only allows updating localizations for versions in certain states:
    - DEVELOPER_REJECTED: Developer rejected the app after review
    - PREPARE_FOR_SUBMISSION: New version being prepared
    - METADATA_REJECTED: Metadata was rejected during review
    - REJECTED: App was rejected by Apple
    
    Versions in these states CANNOT be edited:
    - READY_FOR_SALE: Already live on the App Store
    - WAITING_FOR_REVIEW: Submitted and waiting for Apple review
    - IN_REVIEW: Currently being reviewed by Apple
    - PENDING_DEVELOPER_RELEASE: Approved but waiting for developer to release
    """
    results = {}
    
    # Get current version - prioritize editable versions
    print("\nFetching app versions...")
    try:
        versions = client.versions.get_all(app_id)
        print(f"Found {len(versions)} version(s)")
        
        # Find the rejected/editable version (1.1.01)
        current_version = None
        for version in versions:
            ver_str = version['attributes']['versionString']
            state = version['attributes'].get('appStoreState')
            print(f"  - Version {ver_str}: {state}")
            
            # Look for version 1.1.01 or any editable state
            if ver_str == '1.1.01' or state in ['DEVELOPER_REJECTED', 'PREPARE_FOR_SUBMISSION', 'METADATA_REJECTED', 'REJECTED']:
                current_version = version
                break
        
        if not current_version:
            print("✗ No editable version found. Version must be in DEVELOPER_REJECTED, PREPARE_FOR_SUBMISSION, or METADATA_REJECTED state.")
            return results
            
        version_id = current_version['id']
        version_string = current_version['attributes']['versionString']
        state = current_version['attributes'].get('appStoreState', 'Unknown')
        print(f"\n✓ Using version {version_string} (ID: {version_id}, State: {state})")
        
    except Exception as e:
        print(f"✗ Failed to get app version: {e}")
        return results
    
    # Get existing version localizations
    print("\nFetching existing version localizations...")
    try:
        # Create the API instance using client's auth
        version_localizations_api = AppStoreVersionLocalizationsAPI(auth=client._auth)
        version_localizations = version_localizations_api.get_all(version_id)
        print(f"✓ Found {len(version_localizations)} version localization(s)")
        
        # Create locale to ID mapping
        locale_map = {}
        for loc in version_localizations:
            locale = loc['attributes']['locale']
            locale_map[locale] = loc['id']
            
    except Exception as e:
        print(f"✗ Failed to get version localizations: {e}")
        return results
    
    # Update each localization
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Updating version localizations...")
    
    for locale, content in LOCALIZATIONS.items():
        print(f"\n  Processing {locale}...")
        
        if dry_run:
            print(f"    [DRY RUN] Would update with:")
            print(f"      - Description: {len(content.get('description', ''))} chars")
            print(f"      - Keywords: {content.get('keywords', '')[:50]}...")
            print(f"      - Promotional text: {content.get('promotional_text', '')[:50]}...")
            results[locale] = {'success': True, 'action': 'dry_run'}
            continue
        
        try:
            if locale in locale_map:
                # Update existing localization
                loc_id = locale_map[locale]
                print(f"    Updating existing localization (ID: {loc_id})...")
                
                result = version_localizations_api.update(
                    loc_id,
                    description=content.get('description'),
                    keywords=content.get('keywords'),
                    promotional_text=content.get('promotional_text'),
                    whats_new=content.get('whats_new')
                )
                
                print(f"    ✓ Updated successfully")
                results[locale] = {'success': True, 'action': 'updated', 'data': result}
                
            else:
                # Create new localization
                print(f"    Creating new localization...")
                
                result = version_localizations_api.create(
                    version_id,
                    locale,
                    description=content.get('description'),
                    keywords=content.get('keywords'),
                    promotional_text=content.get('promotional_text'),
                    whats_new=content.get('whats_new')
                )
                
                print(f"    ✓ Created successfully")
                results[locale] = {'success': True, 'action': 'created', 'data': result}
                
        except Exception as e:
            print(f"    ✗ Failed: {e}")
            results[locale] = {'success': False, 'error': str(e)}
    
    return results


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Update App Store Connect localizations')
    parser.add_argument('--app-id', help='App ID (defaults to env var ASC_APP_ID)')
    parser.add_argument('--dry-run', action='store_true', help='Simulate updates without making changes')
    
    args = parser.parse_args()
    
    # Load environment
    env_path = Path(__file__).parent.parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    
    # Set auth key path if not already set
    if not os.environ.get('ASC_PRIVATE_KEY_PATH'):
        # Look for .p8 file in parent directories
        key_path = Path(__file__).parent.parent.parent / 'AuthKey_*.p8'
        key_files = list(Path(__file__).parent.parent.parent.glob('AuthKey_*.p8'))
        if key_files:
            os.environ['ASC_PRIVATE_KEY_PATH'] = str(key_files[0])
    
    # Create client
    try:
        client = Client.from_env()
        print("✓ Connected to App Store Connect")
    except Exception as e:
        print(f"✗ Failed to connect: {e}")
        return 1
    
    # Get app ID
    app_id = args.app_id or os.getenv('ASC_APP_ID')
    if not app_id:
        print("✗ No app ID provided. Set ASC_APP_ID environment variable or use --app-id")
        return 1
    print(f"\nApp ID: {app_id}")
    
    # Update localizations
    results = update_app_store_version_localizations(client, app_id, args.dry_run)
    
    # Summary
    print("\n" + "="*50)
    print("Summary:")
    success_count = sum(1 for r in results.values() if r.get('success'))
    failed_count = len(results) - success_count
    
    print(f"  Success: {success_count}")
    print(f"  Failed: {failed_count}")
    
    if failed_count > 0:
        print("\nFailed locales:")
        for locale, result in results.items():
            if not result.get('success'):
                print(f"  - {locale}: {result.get('error')}")
    
    return 0 if failed_count == 0 else 1


if __name__ == '__main__':
    sys.exit(main())