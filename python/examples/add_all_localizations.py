#!/usr/bin/env python3
"""Add all localizations to SleepLoops app based on app's existing localizations."""

import os
from dotenv import load_dotenv
from app_store_connect import Client
from app_store_connect.base import BaseAPI

# Load environment variables
load_dotenv()

# Define all localizations based on what we found in the app
LOCALIZATIONS = {
    "de": {  # German
        "name": "SchlafZyklen",
        "subtitle": "Schlafzyklus-Rechner",
        "description": """SchlafZyklen - Der intelligente Schlafzyklus-Rechner

Müde vom müde Aufwachen? Wir haben die wissenschaftliche Lösung!

SchlafZyklen ist die intelligente Wecker-App, die revolutioniert, wie Sie schlafen und aufwachen. Mit der bewährten Wissenschaft der 90-Minuten-REM-Zyklen berechnen wir den EXAKTEN Zeitpunkt zum Aufwachen - erfrischt statt benommen.

FUNKTIONEN DIE SIE LIEBEN WERDEN:

INTELLIGENTER SCHLAFRECHNER:
Geben Sie ein, wann Sie aufwachen müssen und wir sagen Ihnen die besten Schlafenszeiten. Oder sagen Sie uns, wann Sie schlafen gehen und wir zeigen Ihnen optimale Aufwachzeiten.

MEHRERE INTELLIGENTE ALARME:
Stellen Sie mehrere Alarme mit einem Fingertipp ein. Perfekt für 20-Minuten-Powernaps oder komplette 90-Minuten-Zyklen.

DUNKLE NACHTOBERFLÄCHE:
Speziell entwickelt, um Ihre Augen in der Dunkelheit zu schonen. Sanfte Farben, die Ihre Melatoninproduktion nicht stören.

100% PRIVAT - KEIN TRACKING:
Keine Konten, keine Anmeldung, kein invasives Schlaf-Tracking. Ihre Privatsphäre ist uns heilig. Die App funktioniert komplett offline.

BASIERT AUF ECHTER WISSENSCHAFT:
Entwickelt mit Forschung führender Universitäten über REM-Schlafzyklen und zirkadiane Rhythmen.

WIE DIE MAGIE FUNKTIONIERT:

Ihr Schlaf durchläuft natürlich 90-Minuten-Zyklen, wechselnd zwischen leichtem, tiefem und REM-Schlaf. Aufwachen während des Tiefschlafs = sich schrecklich fühlen. Aufwachen am Ende eines Zyklus = sich großartig fühlen.

SchlafZyklen berechnet diese Zyklen für Sie:
- 1 Zyklus = 1,5 Stunden
- 4 Zyklen = 6 Stunden (empfohlenes Minimum)
- 5 Zyklen = 7,5 Stunden (optimal für Erwachsene)
- 6 Zyklen = 9 Stunden (vollständige Erholung)

PERFEKT FÜR:
- Studenten die Lernzeiten optimieren
- Berufstätige mit unregelmäßigen Zeitplänen
- Eltern die Schlafenszeiten koordinieren
- Schichtarbeiter die Ruhezeiten planen
- Jeden der erfrischt aufwachen möchte

Laden Sie SchlafZyklen heute herunter und wachen Sie morgen erfrischt auf!""",
        "keywords": "schlaf,wecker,zyklus,aufwachen,rem,rechner,erholung,ruhe,alarm,wissenschaft",
        "whats_new": "Erste Veröffentlichung mit intelligenter Schlafzyklus-Berechnung",
        "promotional_text": "Wachen Sie erfrischt auf! Berechnen Sie die PERFEKTE Zeit zum Schlafen und Aufwachen mit 90-Minuten-REM-Zyklen.",
    },
    "fr": {  # French
        "name": "CyclesSommeil",
        "subtitle": "Cycles de Sommeil",
        "description": """CyclesSommeil - Le Calculateur Intelligent de Cycles de Sommeil

Fatigué de vous réveiller fatigué? Nous avons la solution scientifique!

CyclesSommeil est l'application d'alarme intelligente qui révolutionne votre façon de dormir et de vous réveiller. En utilisant la science prouvée des cycles REM de 90 minutes, nous calculons le moment EXACT pour vous réveiller reposé, pas groggy.

CARACTÉRISTIQUES QUE VOUS ADOREREZ:

CALCULATEUR DE SOMMEIL INTELLIGENT:
Entrez quand vous devez vous réveiller et nous vous dirons les meilleurs moments pour vous coucher. Ou dites-nous quand vous vous couchez et nous vous montrerons les moments optimaux pour vous réveiller.

ALARMES MULTIPLES INTELLIGENTES:
Définissez plusieurs alarmes d'un seul toucher. Parfait pour les siestes de 20 minutes ou les cycles complets de 90 minutes.

INTERFACE NOCTURNE SOMBRE:
Conçue spécialement pour ne pas blesser vos yeux dans l'obscurité. Des couleurs douces qui n'interrompent pas votre production de mélatonine.

100% PRIVÉ - SANS SUIVI:
Pas de comptes, pas d'inscription, pas de suivi invasif du sommeil. Votre vie privée est sacrée. L'application fonctionne complètement hors ligne.

BASÉ SUR LA VRAIE SCIENCE:
Développé en utilisant la recherche des universités de premier plan sur les cycles de sommeil REM et les rythmes circadiens.

COMMENT FONCTIONNE LA MAGIE:

Votre sommeil passe naturellement par des cycles de 90 minutes, alternant entre sommeil léger, profond et REM. Se réveiller pendant le sommeil profond = se sentir horrible. Se réveiller à la fin d'un cycle = se sentir incroyable.

CyclesSommeil calcule ces cycles pour vous:
- 1 cycle = 1,5 heures
- 4 cycles = 6 heures (minimum recommandé)
- 5 cycles = 7,5 heures (optimal pour les adultes)
- 6 cycles = 9 heures (récupération complète)

PARFAIT POUR:
- Étudiants optimisant les horaires d'étude
- Professionnels gérant des horaires irréguliers
- Parents coordonnant les routines de sommeil
- Travailleurs postés planifiant les périodes de repos
- Toute personne voulant se réveiller reposée

Téléchargez CyclesSommeil aujourd'hui et réveillez-vous reposé demain!""",
        "keywords": "sommeil,réveil,cycle,alarme,rem,calculateur,repos,dormir,science,santé",
        "whats_new": "Première version avec calcul intelligent des cycles de sommeil",
        "promotional_text": "Réveillez-vous reposé! Calculez le moment PARFAIT pour dormir et vous réveiller avec les cycles REM de 90 minutes.",
    },
    "it": {  # Italian
        "name": "CicliSonno",
        "subtitle": "Calcolatore di Cicli del Sonno",
        "description": """CicliSonno - Il Calcolatore Intelligente dei Cicli del Sonno

Stanco di svegliarti stanco? Abbiamo la soluzione scientifica!

CicliSonno è l'app sveglia intelligente che rivoluziona come dormi e ti svegli. Usando la scienza provata dei cicli REM di 90 minuti, calcoliamo il momento ESATTO per svegliarti riposato, non intontito.

CARATTERISTICHE CHE AMERAI:

CALCOLATORE DEL SONNO INTELLIGENTE:
Inserisci quando devi svegliarti e ti diremo i migliori orari per andare a letto. O dicci quando vai a letto e ti mostreremo i momenti ottimali per svegliarti.

SVEGLIE MULTIPLE INTELLIGENTI:
Imposta più sveglie con un tocco. Perfette per pisolini di 20 minuti o cicli completi di 90 minuti.

INTERFACCIA NOTTURNA SCURA:
Progettata appositamente per non ferire i tuoi occhi al buio. Colori morbidi che non interrompono la tua produzione di melatonina.

100% PRIVATO - NESSUN TRACCIAMENTO:
Nessun account, nessuna registrazione, nessun tracciamento invasivo del sonno. La tua privacy è sacra. L'app funziona completamente offline.

BASATO SU VERA SCIENZA:
Sviluppato utilizzando ricerche di università leader sui cicli del sonno REM e ritmi circadiani.

COME FUNZIONA LA MAGIA:

Il tuo sonno passa naturalmente attraverso cicli di 90 minuti, alternando tra sonno leggero, profondo e REM. Svegliarsi durante il sonno profondo = sentirsi orribili. Svegliarsi alla fine di un ciclo = sentirsi fantastici.

CicliSonno calcola questi cicli per te:
- 1 ciclo = 1,5 ore
- 4 cicli = 6 ore (minimo consigliato)
- 5 cicli = 7,5 ore (ottimale per adulti)
- 6 cicli = 9 ore (recupero completo)

PERFETTO PER:
- Studenti che ottimizzano gli orari di studio
- Professionisti che gestiscono orari irregolari
- Genitori che coordinano le routine del sonno
- Lavoratori a turni che pianificano periodi di riposo
- Chiunque voglia svegliarsi riposato

Scarica CicliSonno oggi e svegliati riposato domani!""",
        "keywords": "sonno,sveglia,ciclo,risveglio,rem,calcolatore,riposo,dormire,scienza,salute",
        "whats_new": "Prima versione con calcolo intelligente dei cicli del sonno",
        "promotional_text": "Svegliati riposato! Calcola il momento PERFETTO per dormire e svegliarti con cicli REM di 90 minuti.",
    },
    "pt-BR": {  # Portuguese (Brazil)
        "name": "CiclosSono",
        "subtitle": "Calculadora de Ciclos de Sono",
        "description": """CiclosSono - A Calculadora Inteligente de Ciclos de Sono

Cansado de acordar cansado? Temos a solução científica!

CiclosSono é o app de alarme inteligente que revoluciona como você dorme e acorda. Usando a ciência comprovada dos ciclos REM de 90 minutos, calculamos o momento EXATO para acordar revigorado, não grogue.

RECURSOS QUE VOCÊ VAI AMAR:

CALCULADORA DE SONO INTELIGENTE:
Digite quando precisa acordar e diremos os melhores horários para dormir. Ou nos diga quando vai dormir e mostraremos os momentos ideais para acordar.

MÚLTIPLOS ALARMES INTELIGENTES:
Configure vários alarmes com um toque. Perfeito para cochilos de 20 minutos ou ciclos completos de 90 minutos.

INTERFACE NOTURNA ESCURA:
Projetada especialmente para não machucar seus olhos no escuro. Cores suaves que não interrompem sua produção de melatonina.

100% PRIVADO - SEM RASTREAMENTO:
Sem contas, sem cadastro, sem rastreamento invasivo de sono. Sua privacidade é sagrada. O app funciona completamente offline.

BASEADO EM CIÊNCIA REAL:
Desenvolvido usando pesquisa de universidades líderes sobre ciclos de sono REM e ritmos circadianos.

COMO FUNCIONA A MÁGICA:

Seu sono naturalmente passa por ciclos de 90 minutos, alternando entre sono leve, profundo e REM. Acordar durante o sono profundo = sentir-se horrível. Acordar no final de um ciclo = sentir-se incrível.

CiclosSono calcula esses ciclos para você:
- 1 ciclo = 1,5 horas
- 4 ciclos = 6 horas (mínimo recomendado)
- 5 ciclos = 7,5 horas (ideal para adultos)
- 6 ciclos = 9 horas (recuperação completa)

PERFEITO PARA:
- Estudantes otimizando horários de estudo
- Profissionais gerenciando horários irregulares
- Pais coordenando rotinas de sono
- Trabalhadores noturnos planejando períodos de descanso
- Qualquer pessoa que queira acordar revigorada

Baixe CiclosSono hoje e acorde revigorado amanhã!""",
        "keywords": "sono,despertar,ciclo,alarme,rem,calculadora,descanso,dormir,ciência,saúde",
        "whats_new": "Primeira versão com cálculo inteligente de ciclos de sono",
        "promotional_text": "Acorde revigorado! Calcule o momento PERFEITO para dormir e acordar com ciclos REM de 90 minutos.",
    },
    "ru": {  # Russian
        "name": "ЦиклыСна",
        "subtitle": "Калькулятор Циклов Сна",
        "description": """ЦиклыСна - Умный Калькулятор Циклов Сна

Устали просыпаться уставшими? У нас есть научное решение!

ЦиклыСна - это умное приложение-будильник, которое революционизирует ваш сон и пробуждение. Используя проверенную науку 90-минутных REM-циклов, мы рассчитываем ТОЧНЫЙ момент для пробуждения бодрым, а не разбитым.

ФУНКЦИИ, КОТОРЫЕ ВАМ ПОНРАВЯТСЯ:

УМНЫЙ КАЛЬКУЛЯТОР СНА:
Введите, когда вам нужно проснуться, и мы скажем лучшее время для сна. Или скажите, когда ложитесь спать, и мы покажем оптимальное время пробуждения.

МНОЖЕСТВЕННЫЕ УМНЫЕ БУДИЛЬНИКИ:
Установите несколько будильников одним касанием. Идеально для 20-минутного сна или полных 90-минутных циклов.

ТЕМНЫЙ НОЧНОЙ ИНТЕРФЕЙС:
Специально разработан, чтобы не напрягать глаза в темноте. Мягкие цвета, которые не нарушают выработку мелатонина.

100% ПРИВАТНОСТЬ - БЕЗ ОТСЛЕЖИВАНИЯ:
Без аккаунтов, без регистрации, без навязчивого отслеживания сна. Ваша приватность священна. Приложение работает полностью офлайн.

ОСНОВАНО НА РЕАЛЬНОЙ НАУКЕ:
Разработано с использованием исследований ведущих университетов о REM-циклах сна и циркадных ритмах.

КАК РАБОТАЕТ МАГИЯ:

Ваш сон естественно проходит через 90-минутные циклы, чередуя легкий, глубокий и REM-сон. Пробуждение во время глубокого сна = чувствовать себя ужасно. Пробуждение в конце цикла = чувствовать себя прекрасно.

ЦиклыСна рассчитывает эти циклы для вас:
- 1 цикл = 1,5 часа
- 4 цикла = 6 часов (рекомендуемый минимум)
- 5 циклов = 7,5 часов (оптимально для взрослых)
- 6 циклов = 9 часов (полное восстановление)

ИДЕАЛЬНО ДЛЯ:
- Студентов, оптимизирующих график учебы
- Профессионалов с нерегулярным графиком
- Родителей, координирующих режим сна
- Работников ночных смен
- Всех, кто хочет просыпаться бодрым

Скачайте ЦиклыСна сегодня и просыпайтесь бодрым завтра!""",
        "keywords": "сон,будильник,цикл,пробуждение,рем,калькулятор,отдых,спать,наука,здоровье",
        "whats_new": "Первая версия с умным расчетом циклов сна",
        "promotional_text": "Просыпайтесь бодрым! Рассчитайте ИДЕАЛЬНОЕ время для сна и пробуждения с 90-минутными REM-циклами.",
    },
    "ja": {  # Japanese
        "name": "睡眠管理",
        "subtitle": "睡眠サイクル計算機",
        "description": """睡眠管理 - インテリジェント睡眠サイクル計算機

疲れて目覚めることにうんざりしていませんか？科学的な解決策があります！

睡眠管理は、睡眠と目覚めの方法を革新するインテリジェントなアラームアプリです。90分のREMサイクルの実証済みの科学を使用して、ぼんやりではなくリフレッシュして目覚める正確な時間を計算します。

あなたが気に入る機能：

インテリジェント睡眠計算機：
起きる必要がある時間を入力すると、最適な就寝時間をお知らせします。または就寝時間を教えていただければ、最適な起床時間を表示します。

複数のインテリジェントアラーム：
ワンタッチで複数のアラームを設定。20分の仮眠や完全な90分サイクルに最適です。

ダークナイトインターフェース：
暗闇で目を傷つけないように特別に設計されています。メラトニンの生成を妨げない柔らかい色。

100％プライベート - トラッキングなし：
アカウントなし、登録なし、侵襲的な睡眠追跡なし。プライバシーは神聖です。アプリは完全にオフラインで動作します。

本物の科学に基づく：
REM睡眠サイクルと概日リズムに関する一流大学の研究を使用して開発されました。

魔法の仕組み：

あなたの睡眠は自然に90分のサイクルを通過し、浅い睡眠、深い睡眠、REM睡眠を交互に繰り返します。深い睡眠中に目覚める＝ひどい気分。サイクルの終わりに目覚める＝素晴らしい気分。

睡眠管理はこれらのサイクルを計算します：
- 1サイクル = 1.5時間
- 4サイクル = 6時間（推奨最小値）
- 5サイクル = 7.5時間（大人に最適）
- 6サイクル = 9時間（完全回復）

最適な人：
- 勉強スケジュールを最適化する学生
- 不規則なスケジュールを管理する専門家
- 睡眠ルーチンを調整する親
- 休憩時間を計画するシフト労働者
- リフレッシュして目覚めたいすべての人

今日睡眠管理をダウンロードして、明日リフレッシュして目覚めましょう！""",
        "keywords": "睡眠,目覚まし,サイクル,起床,レム,計算機,休息,眠る,科学,健康",
        "whats_new": "インテリジェント睡眠サイクル計算による初回リリース",
        "promotional_text": "リフレッシュして目覚める！90分のREMサイクルで睡眠と起床の完璧な時間を計算。",
    },
    "ko": {  # Korean
        "name": "슬립루프",
        "subtitle": "수면 주기 계산기",
        "description": """수면주기 - 스마트 수면 주기 계산기

피곤하게 일어나는 것에 지치셨나요? 과학적인 해결책이 있습니다!

수면주기는 당신의 수면과 기상 방식을 혁신하는 스마트 알람 앱입니다. 90분 REM 주기의 입증된 과학을 사용하여 몽롱하지 않고 상쾌하게 일어날 정확한 시간을 계산합니다.

당신이 좋아할 기능들:

스마트 수면 계산기:
일어나야 할 시간을 입력하면 최적의 취침 시간을 알려드립니다. 또는 취침 시간을 알려주시면 최적의 기상 시간을 보여드립니다.

다중 스마트 알람:
한 번의 터치로 여러 알람 설정. 20분 낮잠이나 완전한 90분 주기에 완벽합니다.

다크 나이트 인터페이스:
어둠 속에서 눈을 아프게 하지 않도록 특별히 설계되었습니다. 멜라토닌 생성을 방해하지 않는 부드러운 색상.

100% 프라이빗 - 추적 없음:
계정 없음, 가입 없음, 침습적인 수면 추적 없음. 프라이버시는 신성합니다. 앱은 완전히 오프라인으로 작동합니다.

실제 과학 기반:
REM 수면 주기와 일주기 리듬에 대한 선도 대학의 연구를 사용하여 개발되었습니다.

마법이 작동하는 방법:

당신의 수면은 자연스럽게 90분 주기를 거치며 가벼운 수면, 깊은 수면, REM 수면을 번갈아 갑니다. 깊은 수면 중 깨어나기 = 끔찍한 기분. 주기 끝에 깨어나기 = 놀라운 기분.

수면주기는 이러한 주기를 계산합니다:
- 1주기 = 1.5시간
- 4주기 = 6시간 (권장 최소)
- 5주기 = 7.5시간 (성인에게 최적)
- 6주기 = 9시간 (완전 회복)

완벽한 대상:
- 학습 일정을 최적화하는 학생
- 불규칙한 일정을 관리하는 전문가
- 수면 루틴을 조정하는 부모
- 휴식 시간을 계획하는 교대 근무자
- 상쾌하게 일어나고 싶은 모든 사람

오늘 수면주기를 다운로드하고 내일 상쾌하게 일어나세요!""",
        "keywords": "수면,알람,주기,기상,렘,계산기,휴식,잠,과학,건강",
        "whats_new": "스마트 수면 주기 계산 기능이 포함된 첫 번째 버전",
        "promotional_text": "상쾌하게 일어나세요! 90분 REM 주기로 수면과 기상의 완벽한 시간을 계산하세요.",
    },
    "ar": {  # Arabic
        "name": "دورات النوم",
        "subtitle": "حاسبة دورات النوم",
        "description": """دورات النوم - حاسبة دورات النوم الذكية

متعب من الاستيقاظ متعباً؟ لدينا الحل العلمي!

دورات النوم هو تطبيق المنبه الذكي الذي يحدث ثورة في كيفية نومك واستيقاظك. باستخدام العلم المثبت لدورات REM التي تستغرق 90 دقيقة، نحسب الوقت الدقيق للاستيقاظ منتعشاً وليس مترنحاً.

الميزات التي ستحبها:

حاسبة النوم الذكية:
أدخل الوقت الذي تحتاج فيه للاستيقاظ وسنخبرك بأفضل أوقات النوم. أو أخبرنا متى تذهب للنوم وسنعرض لك أوقات الاستيقاظ المثلى.

منبهات متعددة ذكية:
اضبط منبهات متعددة بلمسة واحدة. مثالية لقيلولة 20 دقيقة أو دورات كاملة مدتها 90 دقيقة.

واجهة ليلية مظلمة:
مصممة خصيصاً لعدم إيذاء عينيك في الظلام. ألوان ناعمة لا تقاطع إنتاج الميلاتونين.

خصوصية 100% - بدون تتبع:
بدون حسابات، بدون تسجيل، بدون تتبع تطفلي للنوم. خصوصيتك مقدسة. يعمل التطبيق بالكامل دون اتصال.

مبني على علم حقيقي:
تم تطويره باستخدام أبحاث من جامعات رائدة حول دورات نوم REM والإيقاعات اليومية.

كيف يعمل السحر:

ينتقل نومك بشكل طبيعي عبر دورات مدتها 90 دقيقة، بالتناوب بين النوم الخفيف والعميق و REM. الاستيقاظ أثناء النوم العميق = الشعور بالفظاعة. الاستيقاظ في نهاية الدورة = الشعور بالروعة.

دورات النوم تحسب هذه الدورات لك:
- دورة واحدة = 1.5 ساعة
- 4 دورات = 6 ساعات (الحد الأدنى الموصى به)
- 5 دورات = 7.5 ساعة (الأمثل للبالغين)
- 6 دورات = 9 ساعات (التعافي الكامل)

مثالي لـ:
- الطلاب الذين يحسنون جداول الدراسة
- المحترفون الذين يديرون جداول غير منتظمة
- الآباء الذين ينسقون روتين النوم
- عمال المناوبات الذين يخططون لفترات الراحة
- أي شخص يريد الاستيقاظ منتعشاً

قم بتنزيل دورات النوم اليوم واستيقظ منتعشاً غداً!""",
        "keywords": "نوم,منبه,دورة,استيقاظ,ريم,حاسبة,راحة,نعاس,علم,صحة",
        "whats_new": "الإصدار الأول مع حساب دورات النوم الذكي",
        "promotional_text": "استيقظ منتعشاً! احسب الوقت المثالي للنوم والاستيقاظ مع دورات REM لمدة 90 دقيقة.",
    },
    "zh-Hans": {  # Chinese Simplified
        "name": "安眠周期",
        "subtitle": "睡眠周期计算器",
        "description": """安眠周期 - 智能睡眠周期计算器

厌倦了疲惫地醒来？我们有科学的解决方案！

安眠周期是一款智能闹钟应用，彻底改变您的睡眠和醒来方式。使用经过验证的90分钟REM周期科学，我们计算精确的时间让您清爽醒来，而不是昏昏沉沉。

您会喜欢的功能：

智能睡眠计算器：
输入您需要醒来的时间，我们会告诉您最佳入睡时间。或告诉我们您何时入睡，我们会显示最佳醒来时间。

多个智能闹钟：
一键设置多个闹钟。非常适合20分钟小睡或完整的90分钟周期。

深色夜间界面：
专门设计不伤害黑暗中的眼睛。柔和的颜色不会干扰褪黑素的产生。

100%隐私 - 无追踪：
无账户，无注册，无侵入性睡眠追踪。您的隐私是神圣的。应用完全离线工作。

基于真实科学：
使用领先大学关于REM睡眠周期和昼夜节律的研究开发。

魔法如何运作：

您的睡眠自然经历90分钟的周期，在浅睡眠、深睡眠和REM睡眠之间交替。在深睡眠期间醒来=感觉糟糕。在周期结束时醒来=感觉很棒。

安眠周期为您计算这些周期：
- 1个周期 = 1.5小时
- 4个周期 = 6小时（推荐最低）
- 5个周期 = 7.5小时（成人最佳）
- 6个周期 = 9小时（完全恢复）

非常适合：
- 优化学习时间表的学生
- 管理不规律时间表的专业人士
- 协调睡眠习惯的父母
- 计划休息时间的轮班工人
- 任何想要清爽醒来的人

今天下载安眠周期，明天清爽醒来！""",
        "keywords": "睡眠,闹钟,周期,醒来,快速眼动,计算器,休息,睡觉,科学,健康",
        "whats_new": "首个版本，具有智能睡眠周期计算功能",
        "promotional_text": "清爽醒来！用90分钟REM周期计算完美的睡眠和醒来时间。",
    },
    "zh-Hant": {  # Chinese Traditional
        "name": "睡眠週期",
        "subtitle": "睡眠週期計算器",
        "description": """睡眠週期 - 智能睡眠週期計算器

厭倦了疲憊地醒來？我們有科學的解決方案！

睡眠週期是一款智能鬧鐘應用，徹底改變您的睡眠和醒來方式。使用經過驗證的90分鐘REM週期科學，我們計算精確的時間讓您清爽醒來，而不是昏昏沉沉。

您會喜歡的功能：

智能睡眠計算器：
輸入您需要醒來的時間，我們會告訴您最佳入睡時間。或告訴我們您何時入睡，我們會顯示最佳醒來時間。

多個智能鬧鐘：
一鍵設置多個鬧鐘。非常適合20分鐘小睡或完整的90分鐘週期。

深色夜間界面：
專門設計不傷害黑暗中的眼睛。柔和的顏色不會干擾褪黑素的產生。

100%隱私 - 無追蹤：
無賬戶，無註冊，無侵入性睡眠追蹤。您的隱私是神聖的。應用完全離線工作。

基於真實科學：
使用領先大學關於REM睡眠週期和晝夜節律的研究開發。

魔法如何運作：

您的睡眠自然經歷90分鐘的週期，在淺睡眠、深睡眠和REM睡眠之間交替。在深睡眠期間醒來=感覺糟糕。在週期結束時醒來=感覺很棒。

睡眠週期為您計算這些週期：
- 1個週期 = 1.5小時
- 4個週期 = 6小時（推薦最低）
- 5個週期 = 7.5小時（成人最佳）
- 6個週期 = 9小時（完全恢復）

非常適合：
- 優化學習時間表的學生
- 管理不規律時間表的專業人士
- 協調睡眠習慣的父母
- 計劃休息時間的輪班工人
- 任何想要清爽醒來的人

今天下載睡眠週期，明天清爽醒來！""",
        "keywords": "睡眠,鬧鐘,週期,醒來,快速眼動,計算器,休息,睡覺,科學,健康",
        "whats_new": "首個版本，具有智能睡眠週期計算功能",
        "promotional_text": "清爽醒來！用90分鐘REM週期計算完美的睡眠和醒來時間。",
    },
}

def main():
    """Add all localizations to SleepLoops."""
    print("🌙 SleepLoops Multi-Language Localization")
    print("==========================================\n")
    
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
    
    # Get app info and version
    app_infos = client.apps.get_app_infos(app_id)
    if not app_infos:
        print("❌ No app info found")
        return
        
    app_info = app_infos[-1]
    app_info_id = app_info["id"]
    
    # Get editable version
    versions = client.versions.get_all(app_id)
    editable_version = None
    
    for version in versions:
        state = version.get("attributes", {}).get("appStoreState")
        if state in ["PREPARE_FOR_SUBMISSION", "DEVELOPER_REJECTED", "REJECTED", "WAITING_FOR_REVIEW"]:
            editable_version = version
            break
    
    if not editable_version:
        print("❌ No editable version found")
        return
        
    version_id = editable_version["id"]
    version_string = editable_version.get("attributes", {}).get("versionString", "Unknown")
    print(f"📝 Using version: {version_string} (ID: {version_id})\n")
    
    # Process each localization
    for locale_code, content in LOCALIZATIONS.items():
        # Map locale codes to App Store Connect format
        asc_locale = {
            "de": "de-DE",
            "fr": "fr-FR",
            "it": "it",
            "pt-BR": "pt-BR",
            "ru": "ru",
            "ja": "ja",
            "ko": "ko",
            "ar": "ar-SA",
            "zh-Hans": "zh-Hans",
            "zh-Hant": "zh-Hant",
        }.get(locale_code, locale_code)
        
        print(f"🌍 Processing {asc_locale} ({content['name']})...")
        
        try:
            # Update App Info localization (name and subtitle)
            existing_locs = client.localizations.get_all(app_info_id)
            locale_exists = any(loc.get("attributes", {}).get("locale") == asc_locale for loc in existing_locs)
            
            if not locale_exists:
                client.localizations.create(
                    app_info_id=app_info_id,
                    locale=asc_locale,
                    name=content["name"],
                    subtitle=content["subtitle"],
                    privacy_policy_url=None,
                    privacy_policy_text=None
                )
                print(f"   ✅ Created app info localization")
            
            # Update App Store Version localization
            version_locs_response = BaseAPI.get(client.versions, f"appStoreVersions/{version_id}/appStoreVersionLocalizations")
            version_locs = version_locs_response.get("data", [])
            
            version_loc = None
            for loc in version_locs:
                if loc.get("attributes", {}).get("locale") == asc_locale:
                    version_loc = loc
                    break
            
            update_attrs = {
                "description": content["description"],
                "keywords": content["keywords"],
                "whatsNew": content["whats_new"],
                "promotionalText": content["promotional_text"],
                "supportUrl": "https://github.com/ebowwa/sleeploops-support",
            }
            
            if version_loc:
                # Update existing
                loc_id = version_loc["id"]
                update_data = {
                    "data": {
                        "type": "appStoreVersionLocalizations",
                        "id": loc_id,
                        "attributes": update_attrs
                    }
                }
                BaseAPI.patch(client.versions, f"appStoreVersionLocalizations/{loc_id}", update_data)
                print(f"   ✅ Updated version localization")
            else:
                # Create new
                create_attrs = {"locale": asc_locale, **update_attrs}
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
                BaseAPI.post(client.versions, "appStoreVersionLocalizations", create_data)
                print(f"   ✅ Created version localization")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n✨ All localizations added successfully!")

if __name__ == "__main__":
    main()