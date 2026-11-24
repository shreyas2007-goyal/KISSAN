"""
Grounded AI Krishi Assistant Query Engine.
Pulls verified data from database models to eliminate hallucination.
"""
from apps.markets.models import MandiPrice
from apps.crops.models import Crop
from apps.schemes.models import Scheme
from apps.buyers.models import BuyerRequirement
from apps.calculator.models import SellingOption

def process_krishi_query(query, lang='hi'):
    q = query.lower()
    
    # 1. Price queries
    if any(k in q for k in ['price', 'mandi', 'bhav', 'rate', 'bhaav', 'kimat', 'daam', 'भाव', 'रेट', 'दाम', 'ਭਾਅ']):
        # Find if a specific crop is mentioned
        for crop in Crop.objects.all():
            if crop.name.lower() in q or (crop.name_hi and crop.name_hi in q):
                latest_p = MandiPrice.objects.filter(crop=crop).first()
                if latest_p:
                    if lang == 'hi':
                        return f"वर्तमान में {crop.name_hi or crop.name} का {latest_p.mandi.name} में मॉडल भाव ₹{latest_p.modal_price}/क्विंटल है (न्यूनतम: ₹{latest_p.min_price}, उच्चतम: ₹{latest_p.max_price})। यह डेटा {latest_p.price_date} का सत्यापित सरकारी स्रोत ({latest_p.get_source_display()}) से है।"
                    elif lang == 'pa':
                        return f"ਇਸ ਸਮੇਂ {crop.name} ਦਾ {latest_p.mandi.name} ਵਿੱਚ ਮਾਡਲ ਭਾਅ ₹{latest_p.modal_price}/ਕੁਇੰਟਲ ਹੈ। ਸਰਕਾਰੀ ਸਰੋਤ: {latest_p.get_source_display()} ({latest_p.price_date})।"
                    elif lang == 'hr':
                        return f"भाई, {crop.name_hi or crop.name} का चालू भाव {latest_p.mandi.name} मंदी म्ह ₹{latest_p.modal_price}/क्विंटल चाल रह्या सै। तारीख: {latest_p.price_date}।"
                    else:
                        return f"The current modal price for {crop.name} in {latest_p.mandi.name} is ₹{latest_p.modal_price}/quintal (Min: ₹{latest_p.min_price}, Max: ₹{latest_p.max_price}) recorded on {latest_p.price_date} from {latest_p.get_source_display()}."
        # Generic price summary
        top_prices = MandiPrice.objects.all()[:3]
        summary = ", ".join([f"{p.crop.name}: ₹{p.modal_price}/qtl ({p.mandi.name})" for p in top_prices])
        if lang == 'hi':
            return f"आज के प्रमुख मंडी भाव: {summary}। किसी विशेष फसल (जैसे गेहूं, धान, सरसों) का भाव जानने के लिए फसल का नाम लिखकर पूछें।"
        return f"Today's active market prices: {summary}. Please specify a crop name for exact market trends."

    # 2. Government Schemes query
    if any(k in q for k in ['scheme', 'yojana', 'subsidy', 'sarkar', 'योजना', 'सब्सिडी', 'ਕਿਸਾਨ']):
        schemes = Scheme.objects.filter(is_active=True)[:3]
        names = " | ".join([f"{s.name} ({s.benefits[:60]}...)" for s in schemes])
        if lang == 'hi':
            return f"सत्यापित सरकारी योजनाएं: {names}। अधिक जानकारी या पात्रता जांचने के लिए 'सरकारी योजनाएं' मेनू में जाएं।"
        return f"Verified Active Govt Schemes: {names}. Visit the Schemes section to check eligibility criteria."

    # 3. Net realization / selling calculation
    if any(k in q for k in ['calculator', 'net', 'nuksan', 'nafa', 'realisation', 'मुनाफा', 'खर्च', 'कैलकुलेटर', 'ਨਫ਼ਾ']):
        if lang == 'hi':
            return "किसानसाथी नेट रियलाइज़ेशन कैलकुलेटर का उपयोग करके आप ढुलाई, पल्लेदारी, और मंडी टैक्स घटाकर अपनी जेब में बचने वाले शुद्ध मुनाफे की तुलना कर सकते हैं। ऊपर 'शुद्ध मुनाफा कैलकुलेटर' पर क्लिक करें।"
        return "Using the Net Realisation Calculator, you can factor in transport costs, labor, APMC cess, and bag charges to determine true in-hand profits. Click on 'Net Selling Calculator'."

    # 4. Disease / Crop Wellness
    if any(k in q for k in ['disease', 'pest', 'leaf', 'bimar', 'rog', 'kida', 'बीमारी', 'रोग', 'कीड़ा', 'ਸੁੰਡੀ']):
        if lang == 'hi':
            return "फसल में बीमारी या पत्ती पर धब्बे होने पर 'फसल स्वास्थ्य (AI)' विकल्प पर जाएं और पौधे की पत्ती की साफ फोटो अपलोड करें। हमारा PyTorch AI मॉडल तुरंत बीमारी की पहचान और उपचार का सुझाव देगा।"
        return "For plant disease screening, visit the 'Crop Wellness AI' section and upload a clear leaf photo. Our PyTorch vision pipeline provides disease classification and verified treatment steps."

    # Default friendly grounded response
    if lang == 'hi':
        return f"नमस्ते! मैं आपका डिजिटल कृषि अधिकारी हूं। आप मुझसे आज के मंडी भाव, शुद्ध बिक्री मुनाफा, फसल बीमारी के उपचार, या सरकारी योजनाओं के बारे में पूछ सकते हैं।"
    elif lang == 'pa':
        return f"ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ ਜੀ! ਮੈਂ ਤੁਹਾਡਾ ਡਿਜੀਟਲ ਕ੍ਰਿਸ਼ੀ ਅਧਿਕਾਰੀ ਹਾਂ। ਤੁਸੀਂ ਮੰਡੀ ਭਾਅ, ਖ਼ਰਚੇ ਤੇ ਮੁਨਾਫ਼ਾ, ਫ਼ਸਲ ਰੋਗ ਜਾਂ ਸਰਕਾਰੀ ਸਕੀਮਾਂ ਬਾਰੇ ਸਵਾਲ ਪੁੱਛ ਸਕਦੇ ਹੋ।"
    elif lang == 'hr':
        return f"राम राम जी! म्हे थारा डिजिटल कृषि साथी सैं। मंडी के ताजा भाव, फसल की बीमारी, या सरकारी योजना का सवाल पूछ सको सो।"
    return "Hello! I am your KisanSAATHI Digital Krishi Officer. Ask me about real-time mandi prices, net realization calculations, crop disease identification, or verified government schemes."
