"""
Translation system for Insaka Conference App
Supports multiple languages including Zambian local languages
"""

# Translation dictionary
TRANSLATIONS = {
    "en": {
        # Navigation
        "delegate_dashboard": "Delegate Dashboard",
        "my_information": "My Information",
        "quick_access": "Quick Access",
        "update_details": "Update My Details",
        "daily_checkin": "Daily Check-In",
        "download_materials": "Download Materials",
        
        # Quick Access
        "agenda": "Agenda",
        "speakers": "Speakers",
        "exhibitors": "Exhibitors",
        "venue": "Venue",
        "showcase_news": "Showcase & News",
        "interactive_posts": "Interactive Posts",
        "matchmaking": "Matchmaking",
        "view_schedule": "View Schedule",
        "meet_speakers": "Meet Speakers",
        "explore_booths": "Explore Booths",
        "venue_info": "Venue Info",
        "latest_updates": "Latest Updates",
        "engage_posts": "Engage Posts",
        "network_now": "Network Now",
        
        # Sections
        "latest_announcements": "Latest Announcements",
        "latest_news": "Latest News",
        "trending_posts": "Trending Posts",
        "networking": "Networking",
        "conference_info": "Conference Information",
        
        # Common
        "welcome": "Welcome",
        "hello": "Hello",
        "logout": "Logout",
        "language": "Language",
        "english": "English",
        "nyanja": "Chichewa/Nyanja",
        "bemba": "Bemba",
        "tonga": "Tonga",
        "lozi": "Lozi",
        
        # Conference specific
        "conference_dates": "Conference Dates",
        "location": "Location",
        "theme": "Theme",
        "collaborate_innovate_thrive": "Collaborate • Innovate • Thrive",
        "opening_keynote": "Opening & Keynote",
        "important_notes": "Important Notes",
        "key_sessions": "Key Sessions",
        "connections": "Connections",
        "checkins": "Check-ins",
        "posts_liked": "Posts Liked",
        "comments_made": "Comments Made",
        "no_announcements": "No announcements available",
        "no_news": "No news available",
        "no_trending_posts": "No trending posts available",
        "ensure_details_updated": "Please ensure your details are up to date",
        "check_agenda_regularly": "Check the agenda regularly for updates",
        "download_materials_section": "Download conference materials from the Materials section",
        
        # Matchmaking
        "connect_with_delegates": "Connect with fellow delegates and expand your network",
        "pending_requests": "Pending Requests",
        "my_conversations": "My Conversations",
        "find_delegates": "Find Delegates",
        "recommended": "Recommended",
        "send_message": "Send Message",
        "accept_connection": "Accept Connection",
        "decline": "Decline",
        "connection_request": "Connection Request",
        "chat_message": "Chat Message",
        
        # Authentication
        "authenticated_as": "Authenticated as",
        "authentication_required": "Authentication Required",
        "please_authenticate": "Please authenticate first by visiting the Delegate Self-Service page",
        "quick_login": "Quick Login",
        "enter_delegate_id": "Enter your delegate ID",
        "use_id_shown": "Use the ID shown after your first search"
    },
    
    "ny": {  # Chichewa/Nyanja
        "delegate_dashboard": "Dashboard ya Olamulira",
        "my_information": "Zidziwitso Zanga",
        "quick_access": "Kufikira Mwachangu",
        "update_details": "Sinthani Zidziwitso Zanga",
        "daily_checkin": "Kuwonjezera Tsiku Lonse",
        "download_materials": "Tsitsani Zinthu",
        
        "agenda": "Ndondomeko",
        "speakers": "Amafunsa",
        "exhibitors": "Owonetsa",
        "venue": "Malobwe",
        "showcase_news": "Chiwonetsero ndi Nkhani",
        "interactive_posts": "Mapepa Ophatikizana",
        "matchmaking": "Kukambirana",
        "view_schedule": "Onani Ndondomeko",
        "meet_speakers": "Kukumana ndi Amafunsa",
        "explore_booths": "Yendani M'malo Owonetsa",
        "venue_info": "Zidziwitso za Malobwe",
        "latest_updates": "Zosintha Zaposachedwa",
        "engage_posts": "Kuchita Ntchito ndi Mapepa",
        "network_now": "Kambiranani Tsopano",
        
        "latest_announcements": "Zidziwitso Zaposachedwa",
        "latest_news": "Nkhani Zaposachedwa",
        "trending_posts": "Mapepa Okondweretsa",
        "networking": "Kukambirana",
        "conference_info": "Zidziwitso za Msonkhano",
        
        "welcome": "Takulandirani",
        "hello": "Moni",
        "logout": "Tulukani",
        "language": "Chiyankhulo",
        "english": "Chingerezi",
        "nyanja": "Chichewa",
        "bemba": "Chibemba",
        "tonga": "Chitonga",
        "lozi": "Chilozi",
        
        "conference_dates": "Tsiku la Msonkhano",
        "location": "Malobwe",
        "theme": "Mutu",
        "collaborate_innovate_thrive": "Kugwirizana • Kupanga Zatsopano • Kukula",
        "opening_keynote": "Kutsegula ndi Mawu Othamanga",
        "important_notes": "Zolemba Zofunika",
        "key_sessions": "Misonkhano Yofunika",
        "connections": "Maganizo",
        "checkins": "Kuwonjezera",
        "posts_liked": "Mapepa Omwe Mumakonda",
        "comments_made": "Ndemanga Zomwe Munachita",
        "no_announcements": "Palibe zidziwitso zilipo",
        "no_news": "Palibe nkhani zilipo",
        "no_trending_posts": "Palibe mapepa okondweretsa",
        "ensure_details_updated": "Chonde onetsetsani kuti zidziwitso zanu ndi zaposachedwa",
        "check_agenda_regularly": "Yang'anani ndondomeko nthawi zonse kuti muwone zosintha",
        "download_materials_section": "Tsitsani zinthu za msonkhano kuchokera ku gawo la Zinthu",
        
        "connect_with_delegates": "Kambiranani ndi olamulira ena ndikuwongolera mfundo zanu",
        "pending_requests": "Zopempha Zikudikira",
        "my_conversations": "Nkhani Zanga",
        "find_delegates": "Pezani Olamulira",
        "recommended": "Zolimbikitsidwa",
        "send_message": "Tumizani Uthenga",
        "accept_connection": "Landirani Maganizo",
        "decline": "Kanani",
        "connection_request": "Chopempha Maganizo",
        "chat_message": "Uthenga wa Nkhani",
        
        "authenticated_as": "Loledwa ngati",
        "authentication_required": "Kuloledwa Kwafunika",
        "please_authenticate": "Chonde loledwani kaye pokapita ku tsamba la Olamulira Olimbikitsa Ntchito",
        "quick_login": "Kulowa Mwachangu",
        "enter_delegate_id": "Lowezani ID yanu ya Olamulira",
        "use_id_shown": "Gwiritsani ID yomwe ikuwonetsedwa pambuyo pa kuyamba kuyang'ana"
    },
    
    "be": {  # Bemba
        "delegate_dashboard": "Dashboard ya Abalimbi",
        "my_information": "Ifyabwino Fyandi",
        "quick_access": "Ukupona Ukwema",
        "update_details": "Sinteni Ifyabwino Fyandi",
        "daily_checkin": "Ukwingilisha Bushiku Bonse",
        "download_materials": "Kulanda Ifipanga",
        
        "agenda": "Iciyelo",
        "speakers": "Abalimbi",
        "exhibitors": "Abalondeshya",
        "venue": "Icipililila",
        "showcase_news": "Ukulondeshya na Amakani",
        "interactive_posts": "Amapila Ya Ukupitana",
        "matchmaking": "Ukupitana",
        "view_schedule": "Mweneni Iciyelo",
        "meet_speakers": "Ukukumanana na Abalimbi",
        "explore_booths": "Kulonda mu Fipanga",
        "venue_info": "Ifyabwino fy'icpililila",
        "latest_updates": "Ifyabwino Fyaposha",
        "engage_posts": "Ukucita na Amapila",
        "network_now": "Pitanani Nomba",
        
        "latest_announcements": "Ifyabwino Fyaposha",
        "latest_news": "Amakani Aposha",
        "trending_posts": "Amapila Ya Ukukondwa",
        "networking": "Ukupitana",
        "conference_info": "Ifyabwino fy'icilanda",
        
        "welcome": "Mwakulilileni",
        "hello": "Shani",
        "logout": "Fumeni",
        "language": "Ululimi",
        "english": "Icilungu",
        "nyanja": "Icinjanja",
        "bemba": "Icibemba",
        "tonga": "Icitonga",
        "lozi": "Icilozi",
        
        "conference_dates": "Imiti ya Icilanda",
        "location": "Icipililila",
        "theme": "Inshita",
        "collaborate_innovate_thrive": "Ukupitana • Ukupanga Ifipya • Ukukula",
        "opening_keynote": "Ukufungulwa na Amakani Apalililwa",
        "important_notes": "Amakani Apalililwa",
        "key_sessions": "Imiti Ipalililwa",
        "connections": "Ukupitana",
        "checkins": "Ukwingilisha",
        "posts_liked": "Amapila Yamukonda",
        "comments_made": "Amakani Yamucitile",
        "no_announcements": "Tapali fyabwino fyaba",
        "no_news": "Tapali amakani aba",
        "no_trending_posts": "Tapali amapila ya ukukondwa",
        "ensure_details_updated": "Napapata ukuti fyabwino fyenu fyaposha",
        "check_agenda_regularly": "Mweneni iciyelo cilyonse kuti mwene ifyabwino fyaposha",
        "download_materials_section": "Landeni ifipanga fya icilanda ku cipanga ca Ifipanga",
        
        "connect_with_delegates": "Pitanani na balimbi bampe na ukupita mfundo yenu",
        "pending_requests": "Ilyolomba Likupapata",
        "my_conversations": "Amakani Yandi",
        "find_delegates": "Sekani Abalimbi",
        "recommended": "Ifyabwino Fyapalililwa",
        "send_message": "Tumyeni Utenge",
        "accept_connection": "Landeni Ukupitana",
        "decline": "Kanani",
        "connection_request": "Ilyolomba Ukupitana",
        "chat_message": "Utenge wa Amakani",
        
        "authenticated_as": "Ilyalililwa nga",
        "authentication_required": "Ukulililwa Kwafwile",
        "please_authenticate": "Napapata ukulililwa cila cikamba ku cipanga ca Abalimbi Abacitila",
        "quick_login": "Ukwingila Ukwema",
        "enter_delegate_id": "Ingileni ID yenu ya Abalimbi",
        "use_id_shown": "Shileni ID yali ikalondeshya pambili pa kucila kwamba ukuseka"
    },
    
    "fr": {  # French
        "delegate_dashboard": "Tableau de Bord des Délégués",
        "my_information": "Mes Informations",
        "quick_access": "Accès Rapide",
        "update_details": "Mettre à Jour Mes Détails",
        "daily_checkin": "Enregistrement Quotidien",
        "download_materials": "Télécharger les Matériaux",
        
        "agenda": "Ordre du Jour",
        "speakers": "Intervenants",
        "exhibitors": "Exposants",
        "venue": "Lieu",
        "showcase_news": "Vitrine & Actualités",
        "interactive_posts": "Publications Interactives",
        "matchmaking": "Mise en Relation",
        "view_schedule": "Voir le Programme",
        "meet_speakers": "Rencontrer les Intervenants",
        "explore_booths": "Explorer les Stands",
        "venue_info": "Info Lieu",
        "latest_updates": "Dernières Mises à Jour",
        "engage_posts": "Participer aux Publications",
        "network_now": "Réseauter Maintenant",
        
        "latest_announcements": "Dernières Annonces",
        "latest_news": "Dernières Actualités",
        "trending_posts": "Publications Tendance",
        "networking": "Réseautage",
        "conference_info": "Informations de la Conférence",
        
        "welcome": "Bienvenue",
        "hello": "Bonjour",
        "logout": "Déconnexion",
        "language": "Langue",
        "english": "Anglais",
        "french": "Français",
        "portuguese": "Portugais",
        "arabic": "Arabe",
        "nyanja": "Chichewa",
        "bemba": "Bemba",
        
        "conference_dates": "Dates de la Conférence",
        "location": "Lieu",
        "theme": "Thème",
        "collaborate_innovate_thrive": "Collaborer • Innover • Prospérer",
        "opening_keynote": "Ouverture & Conférence Principale",
        "important_notes": "Notes Importantes",
        "key_sessions": "Sessions Clés",
        "connections": "Connexions",
        "checkins": "Enregistrements",
        "posts_liked": "Publications Aimées",
        "comments_made": "Commentaires Faits",
        "no_announcements": "Aucune annonce disponible",
        "no_news": "Aucune actualité disponible",
        "no_trending_posts": "Aucune publication tendance disponible",
        "ensure_details_updated": "Veuillez vous assurer que vos détails sont à jour",
        "check_agenda_regularly": "Consultez l'ordre du jour régulièrement pour les mises à jour",
        "download_materials_section": "Téléchargez les matériaux de la conférence depuis la section Matériaux",
        
        "connect_with_delegates": "Connectez-vous avec d'autres délégués et développez votre réseau",
        "pending_requests": "Demandes en Attente",
        "my_conversations": "Mes Conversations",
        "find_delegates": "Trouver des Délégués",
        "recommended": "Recommandé",
        "send_message": "Envoyer un Message",
        "accept_connection": "Accepter la Connexion",
        "decline": "Refuser",
        "connection_request": "Demande de Connexion",
        "chat_message": "Message de Chat",
        
        "authenticated_as": "Authentifié en tant que",
        "authentication_required": "Authentification Requise",
        "please_authenticate": "Veuillez d'abord vous authentifier en visitant la page d'auto-service des délégués",
        "quick_login": "Connexion Rapide",
        "enter_delegate_id": "Entrez votre ID de délégué",
        "use_id_shown": "Utilisez l'ID affiché après votre première recherche"
    },
    
    "pt": {  # Portuguese
        "delegate_dashboard": "Painel do Delegado",
        "my_information": "Minhas Informações",
        "quick_access": "Acesso Rápido",
        "update_details": "Atualizar Meus Detalhes",
        "daily_checkin": "Check-in Diário",
        "download_materials": "Baixar Materiais",
        
        "agenda": "Agenda",
        "speakers": "Palestrantes",
        "exhibitors": "Expositores",
        "venue": "Local",
        "showcase_news": "Vitrine & Notícias",
        "interactive_posts": "Postagens Interativas",
        "matchmaking": "Conectividade",
        "view_schedule": "Ver Cronograma",
        "meet_speakers": "Conhecer Palestrantes",
        "explore_booths": "Explorar Estandes",
        "venue_info": "Info do Local",
        "latest_updates": "Últimas Atualizações",
        "engage_posts": "Interagir com Postagens",
        "network_now": "Conectar Agora",
        
        "latest_announcements": "Últimos Anúncios",
        "latest_news": "Últimas Notícias",
        "trending_posts": "Postagens em Alta",
        "networking": "Networking",
        "conference_info": "Informações da Conferência",
        
        "welcome": "Bem-vindo",
        "hello": "Olá",
        "logout": "Sair",
        "language": "Idioma",
        "english": "Inglês",
        "french": "Francês",
        "portuguese": "Português",
        "arabic": "Árabe",
        "nyanja": "Chichewa",
        "bemba": "Bemba",
        
        "conference_dates": "Datas da Conferência",
        "location": "Local",
        "theme": "Tema",
        "collaborate_innovate_thrive": "Colaborar • Inovar • Prosperar",
        "opening_keynote": "Abertura & Palestra Principal",
        "important_notes": "Notas Importantes",
        "key_sessions": "Sessões Principais",
        "connections": "Conexões",
        "checkins": "Check-ins",
        "posts_liked": "Postagens Curtidas",
        "comments_made": "Comentários Feitos",
        "no_announcements": "Nenhum anúncio disponível",
        "no_news": "Nenhuma notícia disponível",
        "no_trending_posts": "Nenhuma postagem em alta disponível",
        "ensure_details_updated": "Por favor, certifique-se de que seus detalhes estão atualizados",
        "check_agenda_regularly": "Verifique a agenda regularmente para atualizações",
        "download_materials_section": "Baixe os materiais da conferência da seção de Materiais",
        
        "connect_with_delegates": "Conecte-se com outros delegados e expanda sua rede",
        "pending_requests": "Solicitações Pendentes",
        "my_conversations": "Minhas Conversas",
        "find_delegates": "Encontrar Delegados",
        "recommended": "Recomendado",
        "send_message": "Enviar Mensagem",
        "accept_connection": "Aceitar Conexão",
        "decline": "Recusar",
        "connection_request": "Solicitação de Conexão",
        "chat_message": "Mensagem de Chat",
        
        "authenticated_as": "Autenticado como",
        "authentication_required": "Autenticação Necessária",
        "please_authenticate": "Por favor, autentique-se primeiro visitando a página de Autoatendimento do Delegado",
        "quick_login": "Login Rápido",
        "enter_delegate_id": "Digite seu ID de Delegado",
        "use_id_shown": "Use o ID mostrado após sua primeira busca"
    },
    
    "ar": {  # Arabic
        "delegate_dashboard": "لوحة تحكم المندوب",
        "my_information": "معلوماتي",
        "quick_access": "الوصول السريع",
        "update_details": "تحديث تفاصيلي",
        "daily_checkin": "تسجيل الحضور اليومي",
        "download_materials": "تحميل المواد",
        
        "agenda": "الأجندة",
        "speakers": "المتحدثون",
        "exhibitors": "المعارضون",
        "venue": "المكان",
        "showcase_news": "العرض والأخبار",
        "interactive_posts": "المنشورات التفاعلية",
        "matchmaking": "التطابق",
        "view_schedule": "عرض الجدول",
        "meet_speakers": "مقابلة المتحدثين",
        "explore_booths": "استكشاف الأجنحة",
        "venue_info": "معلومات المكان",
        "latest_updates": "أحدث التحديثات",
        "engage_posts": "التفاعل مع المنشورات",
        "network_now": "التواصل الآن",
        
        "latest_announcements": "أحدث الإعلانات",
        "latest_news": "أحدث الأخبار",
        "trending_posts": "المنشورات الرائجة",
        "networking": "التواصل",
        "conference_info": "معلومات المؤتمر",
        
        "welcome": "مرحباً",
        "hello": "مرحبا",
        "logout": "تسجيل الخروج",
        "language": "اللغة",
        "english": "الإنجليزية",
        "french": "الفرنسية",
        "portuguese": "البرتغالية",
        "arabic": "العربية",
        "nyanja": "تشيتشيوا",
        "bemba": "بيمبا",
        
        "conference_dates": "تواريخ المؤتمر",
        "location": "الموقع",
        "theme": "الموضوع",
        "collaborate_innovate_thrive": "التعاون • الابتكار • الازدهار",
        "opening_keynote": "الافتتاح والخطاب الرئيسي",
        "important_notes": "ملاحظات مهمة",
        "key_sessions": "الجلسات الرئيسية",
        "connections": "الاتصالات",
        "checkins": "تسجيلات الحضور",
        "posts_liked": "المنشورات المحبوبة",
        "comments_made": "التعليقات المضافة",
        "no_announcements": "لا توجد إعلانات متاحة",
        "no_news": "لا توجد أخبار متاحة",
        "no_trending_posts": "لا توجد منشورات رائجة متاحة",
        "ensure_details_updated": "يرجى التأكد من تحديث تفاصيلك",
        "check_agenda_regularly": "تحقق من الأجندة بانتظام للحصول على التحديثات",
        "download_materials_section": "قم بتحميل مواد المؤتمر من قسم المواد",
        
        "connect_with_delegates": "تواصل مع المندوبين الآخرين ووسع شبكتك",
        "pending_requests": "الطلبات المعلقة",
        "my_conversations": "محادثاتي",
        "find_delegates": "البحث عن المندوبين",
        "recommended": "موصى به",
        "send_message": "إرسال رسالة",
        "accept_connection": "قبول الاتصال",
        "decline": "رفض",
        "connection_request": "طلب الاتصال",
        "chat_message": "رسالة دردشة",
        
        "authenticated_as": "مصادق عليه كـ",
        "authentication_required": "المصادقة مطلوبة",
        "please_authenticate": "يرجى المصادقة أولاً بزيارة صفحة الخدمة الذاتية للمندوب",
        "quick_login": "تسجيل الدخول السريع",
        "enter_delegate_id": "أدخل معرف المندوب الخاص بك",
        "use_id_shown": "استخدم المعرف المعروض بعد بحثك الأول"
    }
}

def get_translation(key: str, language: str = "en") -> str:
    """Get translation for a key in specified language"""
    # Handle English variants (en-us, en-gb both map to en)
    if language.startswith("en-"):
        language = "en"
    
    if language not in TRANSLATIONS:
        language = "en"  # Fallback to English
    
    if key not in TRANSLATIONS[language]:
        # Fallback to English if key not found
        return TRANSLATIONS.get("en", {}).get(key, key)
    
    return TRANSLATIONS[language][key]

def get_available_languages():
    """Get list of available languages"""
    return [
        {"code": "en-us", "name": "English (US)", "flag": "🇺🇸"},
        {"code": "en-gb", "name": "English (UK)", "flag": "🇬🇧"},
        {"code": "fr", "name": "Français", "flag": "🇫🇷"},
        {"code": "pt", "name": "Português", "flag": "🇵🇹"},
        {"code": "ar", "name": "العربية", "flag": "🇸🇦"},
        {"code": "ny", "name": "Chichewa", "flag": "🇲🇼"},
        {"code": "be", "name": "Bemba", "flag": "🇿🇲"}
    ]

def is_rtl_language(language_code):
    """Check if language is right-to-left"""
    rtl_languages = ['ar', 'he', 'fa', 'ur']
    return language_code in rtl_languages

def get_text_direction(language_code):
    """Get text direction for language"""
    return "rtl" if is_rtl_language(language_code) else "ltr"

def create_language_switcher():
    """Create simple language switcher for Streamlit"""
    return """
    <div style="position: fixed; top: 10px; right: 10px; z-index: 1000; background: white; padding: 5px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.2);">
        <div style="display: flex; gap: 5px; align-items: center;">
            <span style="font-size: 12px; color: #666;">🌍</span>
            <button onclick="setLanguage('en')" style="border: 1px solid #ddd; background: white; padding: 2px 6px; border-radius: 5px; cursor: pointer; font-size: 10px;" title="English">EN</button>
            <button onclick="setLanguage('ny')" style="border: 1px solid #ddd; background: white; padding: 2px 6px; border-radius: 5px; cursor: pointer; font-size: 10px;" title="Chichewa">NY</button>
            <button onclick="setLanguage('be')" style="border: 1px solid #ddd; background: white; padding: 2px 6px; border-radius: 5px; cursor: pointer; font-size: 10px;" title="Bemba">BE</button>
        </div>
    </div>
    
    <script>
    function setLanguage(lang) {
        localStorage.setItem('insaka_language', lang);
        window.location.reload();
    }
    
    // Highlight current language
    window.addEventListener('load', function() {
        const savedLang = localStorage.getItem('insaka_language') || 'en';
        const buttons = document.querySelectorAll('button[onclick^="setLanguage"]');
        buttons.forEach(btn => {
            if (btn.onclick.toString().includes("'" + savedLang + "'")) {
                btn.style.background = '#198A00';
                btn.style.color = 'white';
            }
        });
    });
    </script>
    """
