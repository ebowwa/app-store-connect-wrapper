#!/usr/bin/env python3
"""Complete missing version descriptions for de-DE, fr-FR, and ko."""

import os
from dotenv import load_dotenv
from app_store_connect import Client
from app_store_connect.base import BaseAPI

# Load environment variables
load_dotenv()

def main():
    """Complete missing descriptions."""
    print("🌙 Completing Missing Descriptions")
    print("===================================\n")
    
    # Initialize client
    client = Client(
        key_id=os.getenv("ASC_KEY_ID"),
        issuer_id=os.getenv("ASC_ISSUER_ID"),
        private_key_path=os.getenv("ASC_PRIVATE_KEY_PATH")
    )
    print("✅ Client initialized\n")
    
    # Find SleepLoops
    app = client.apps.get_by_bundle_id("com.ebowwa.sleeploops")
    app_id = app["id"]
    
    # Get version
    versions = client.versions.get_all(app_id)
    version = None
    for v in versions:
        if v.get("attributes", {}).get("appStoreState") in ["PREPARE_FOR_SUBMISSION"]:
            version = v
            break
    
    if not version:
        print("❌ No editable version found")
        return
    
    version_id = version["id"]
    
    # Get existing localizations
    version_locs_response = BaseAPI.get(client.versions, f"appStoreVersions/{version_id}/appStoreVersionLocalizations")
    version_locs = version_locs_response.get("data", [])
    
    updates = {
        "de-DE": {
            "description": """SchlafZyklen hilft Ihnen erfrischt aufzuwachen, indem es die optimalen Schlaf- und Aufwachzeiten basierend auf natürlichen 90-Minuten-Schlafzyklen berechnet.

HAUPTFUNKTIONEN:
- Intelligenter Schlafrechner - Finden Sie die perfekte Schlafenszeit basierend auf Ihrer Aufwachzeit
- Weckzeit-Optimierer - Entdecken Sie die besten Aufwachzeiten wenn Sie jetzt schlafen gehen
- Schlafzyklus-Wissenschaft - Lernen Sie über 90-Minuten-REM-Zyklen
- Mehrere Alarme - Stellen Sie Alarme für optimale Zeiten mit einem Fingertipp ein
- Schöne dunkle Oberfläche - Augenschonend für die Nacht
- Einfach und schnell - Kein Tracking, keine Konten, nur sofortige Berechnungen

WARUM SCHLAFZYKLEN WICHTIG SIND:
Aufwachen mitten in einem Schlafzyklus kann Sie benommen und müde fühlen lassen. SchlafZyklen berechnet optimale Aufwachzeiten am Ende vollständiger Zyklen.

DIE WISSENSCHAFT:
Basierend auf Schlafforschung die zeigt, dass unser Schlaf vorhersehbaren 90-Minuten-Zyklen folgt. Indem Sie Ihr Aufwachen mit leichteren Schlafphasen synchronisieren, fühlen Sie sich natürlich ausgeruhter.

PERFEKT FÜR:
Studenten, Berufstätige, Eltern, Schichtarbeiter und jeden der erfrischt aufwachen möchte.

Laden Sie SchlafZyklen heute herunter und wachen Sie morgen erfrischt auf!""",
            "keywords": "schlaf,wecker,zyklus,aufwachen,rem,rechner,erholung,ruhe,alarm,wissenschaft",
            "whats_new": "Version 2.0 mit verbesserter Schlafzyklus-Berechnung",
            "promotional_text": "Erfrischt aufwachen! PERFEKTE Schlaf- und Aufwachzeiten mit 90-Min-REM-Zyklen berechnen."
        },
        "fr-FR": {
            "description": """CyclesSommeil vous aide à vous réveiller reposé en calculant les heures optimales de sommeil et de réveil basées sur les cycles naturels de sommeil de 90 minutes.

CARACTÉRISTIQUES PRINCIPALES:
- Calculateur de Sommeil Intelligent - Trouvez l'heure parfaite pour vous coucher selon votre heure de réveil
- Optimiseur d'Heure de Réveil - Découvrez les meilleurs moments pour vous réveiller si vous dormez maintenant
- Science des Cycles de Sommeil - Apprenez sur les cycles REM de 90 minutes
- Alarmes Multiples - Réglez des alarmes pour des heures optimales d'un seul toucher
- Belle Interface Sombre - Facile pour les yeux la nuit
- Simple et Rapide - Pas de suivi, pas de comptes, juste des calculs instantanés

POURQUOI LES CYCLES DE SOMMEIL SONT IMPORTANTS:
Se réveiller au milieu d'un cycle de sommeil peut vous laisser groggy et fatigué. CyclesSommeil calcule les moments optimaux pour se réveiller à la fin de cycles complets.

LA SCIENCE:
Basé sur la recherche du sommeil montrant que notre repos suit des cycles prévisibles de 90 minutes. En synchronisant votre réveil avec les phases de sommeil plus légères, vous vous sentirez naturellement plus reposé.

PARFAIT POUR:
Étudiants, professionnels, parents, travailleurs postés et toute personne voulant se réveiller reposée.

Téléchargez CyclesSommeil aujourd'hui et réveillez-vous reposé demain!""",
            "keywords": "sommeil,réveil,cycle,alarme,rem,calculateur,repos,dormir,science,santé",
            "whats_new": "Version 2.0 avec calcul amélioré des cycles de sommeil",
            "promotional_text": "Réveillez-vous reposé! Calculez les moments PARFAITS pour dormir et vous réveiller avec cycles REM 90min."
        },
        "ko": {
            "description": """슬립루프는 자연스러운 90분 수면 주기를 기반으로 최적의 수면 및 기상 시간을 계산하여 상쾌하게 일어나도록 도와줍니다.

주요 기능:
- 스마트 수면 계산기 - 기상 시간에 따른 완벽한 취침 시간 찾기
- 기상 시간 최적화 - 지금 잠들면 가장 좋은 기상 시간 발견
- 수면 주기 과학 - 90분 REM 주기에 대해 알아보기
- 다중 알람 - 한 번의 터치로 최적 시간에 알람 설정
- 아름다운 다크 인터페이스 - 밤에 눈이 편안함
- 간단하고 빠름 - 추적 없음, 계정 없음, 즉시 계산

수면 주기가 중요한 이유:
수면 주기 중간에 깨어나면 몽롱하고 피곤할 수 있습니다. 슬립루프는 완전한 주기가 끝날 때 깨어나는 최적의 시간을 계산합니다.

과학:
우리의 수면이 예측 가능한 90분 주기를 따른다는 수면 연구에 기반합니다. 가벼운 수면 단계와 기상을 동기화하면 자연스럽게 더 상쾌함을 느낄 수 있습니다.

완벽한 대상:
학생, 전문가, 부모, 교대 근무자 및 상쾌하게 일어나고 싶은 모든 사람.

오늘 슬립루프를 다운로드하고 내일 상쾌하게 일어나세요!""",
            "keywords": "수면,알람,주기,기상,렘,계산기,휴식,잠,과학,건강",
            "whats_new": "버전 2.0 - 개선된 수면 주기 계산",
            "promotional_text": "상쾌하게 일어나세요! 90분 REM 주기로 완벽한 수면과 기상 시간을 계산하세요."
        }
    }
    
    for locale, content in updates.items():
        print(f"📝 Updating {locale}...")
        
        # Find the localization
        loc_id = None
        for loc in version_locs:
            if loc.get("attributes", {}).get("locale") == locale:
                loc_id = loc["id"]
                break
        
        if loc_id:
            update_data = {
                "data": {
                    "type": "appStoreVersionLocalizations",
                    "id": loc_id,
                    "attributes": {
                        "description": content["description"],
                        "keywords": content["keywords"],
                        "whatsNew": content["whats_new"],
                        "promotionalText": content["promotional_text"],
                    }
                }
            }
            
            try:
                BaseAPI.patch(client.versions, f"appStoreVersionLocalizations/{loc_id}", update_data)
                print(f"   ✅ Updated {locale} successfully")
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"   ⚠️  {locale} localization not found")
    
    print("\n✨ Done!")

if __name__ == "__main__":
    main()