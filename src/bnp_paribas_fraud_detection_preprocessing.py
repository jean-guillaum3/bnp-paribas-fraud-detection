# Comment démasquer les fraudeurs ? BNP Paribas PF

import re

import pandas as pd


def map_item_group(x: str) -> str: 
    if pd.isna(x):
        return "OTHER"
    s = x.upper()

    # TECH / INFORMATIQUE / ÉLECTRO
    if ("COMPUTER" in s or "IMAGING EQUIPMENT" in s
        or "PRINTER" in s or "SCANNER" in s
        or "NETWORKING" in s or "GAMING" in s
        or "TOSHIBA PORTABLE HARD DRIVE" in s
        or "HP ELITEBOOK" in s
        or "LOGITECH PEBBLE" in s
        or "MICROSOFT OFFICE" in s
        or "VIDEOS DVD DIGITAL EQUIPMENT" in s):
        return "TECH & COMPUTING"

    # TV / AUDIO / HIFI
    if ("TELEVISION" in s or "HOME CINEMA" in s
        or "HI-FI" in s or "AUDIO ACCESSORIES" in s
        or "STANDS BRACKETS" in s or "STANDS & BRACKETS" in s):
        return "TV AUDIO VIDEO"

    # MEUBLES / MAISON
    if ("FURNITURE" in s or "CARPETS" in s or "RUGS" in s
        or "BED LINEN" in s or "BATH LINEN" in s
        or "NURSERY FURNITURE" in s
        or "FITTED KITCHENS" in s
        or "KITCHEN ACCESSORIES" in s
        or "KITCHEN STORAGE" in s
        or "BATHROOM" in s
        or "LIGHTING" in s
        or "DECORATIVE ACCESSORIES" in s
        or "WINDOW DRESSING" in s
        or "SOFT FURNISHINGS" in s
        or "STORAGE" in s):
        return "HOME & FURNITURE"

    # VÊTEMENTS / CHAUSSURES
    if ("CLOTHES" in s or "MENS CLOTHES" in s or "WOMEN S CLOTHES" in s
        or "BOYSWEAR" in s or "GIRLSWEAR" in s
        or "NIGHTWEAR" in s or "UNDERWEAR" in s
        or "SCHOOLWEAR" in s
        or "FOOTWEAR" in s or "LINGERIE" in s):
        return "CLOTHING"

    # SACS / ACCESSOIRES MODE
    if ("BAGS" in s or "LUGGAGE" in s
        or "SUNGLASSES" in s
        or "JEWELLERY" in s
        or "ACCESSORIES" in s and "HEALTH BEAUTY" not in s):
        return "FASHION ACCESSORIES"

    # BÉBÉ / ENFANT
    if ("BABY" in s or "NURSERY" in s
        or "CHILDREN S" in s
        or "NURSERY TOYS" in s
        or "BABYWEAR" in s):
        return "BABY & CHILD"

    # SANTÉ / BEAUTÉ
    if ("HEALTH" in s or "BEAUTY" in s
        or "MAKEUP" in s or "FRAGRANCE" in s
        or "FACIAL SKINCARE" in s
        or "BATH & BODYCARE" in s or "BATH BODYCARE" in s
        or "HAIRCARE" in s or "SUNCARE" in s):
        return "HEALTH & BEAUTY"

    # CUISINE / FOOD
    if ("COOKWARE" in s or "COOKING APPLIANCES" in s
        or "FOOD PREPARATION" in s
        or "FOOD STORAGE" in s
        or "PRESERVING" in s
        or "KITCHEN UTENSILS" in s or "KITCHEN SCALES" in s
        or "HOT DRINK PREPARATION" in s
        or "TABLEWARE" in s or "TABLE LINEN" in s
        or "PICNICWARE" in s
        or "GIFT FOOD DRINK" in s):
        return "KITCHEN & FOOD"

    # LOISIRS / JEUX / SPORT
    if ("TOYS" in s or "GAMES" in s
        or "SPORTS EQUIPMENT" in s or "GYM EQUIPMENT" in s
        or "CRAFT" in s
        or "BOOKS" in s):
        return "TOYS GAMES SPORTS"

    # JARDIN / EXTÉRIEUR
    if ("OUTDOOR" in s or "GARDENING EQUIPMENT" in s
        or "BARBECUES" in s):
        return "OUTDOOR & GARDEN"

    # PAPETERIE / BUREAU
    if ("STATIONERY" in s or "PAPER & NOTEBOOKS" in s
        or "FILING" in s or "DESK ACCESSORIES" in s
        or "HOME OFFICE" in s
        or "GREETING CARDS" in s):
        return "STATIONERY & OFFICE"

    # SERVICES / FRAIS
    if ("SERVICE" in s or "WARRANTY" in s or "FULFILMENT" in s):
        return "SERVICES & FEES"

    # Cas inconnus, codes ou items bizarres
    if ("UNKNOWN" in s or "APPLE PRODUCTDESCRIPTION" in s
        or s.strip().isdigit() or "SKU" in s):
        return "OTHER"

    return "OTHER"

def normalize_text(x: str) -> str:
    if pd.isna(x):
        return ""
    s = str(x).upper().strip()
    s = s.replace("&", " ")
    s = re.sub(r"\s+", " ", s)
    return s

def extract_family(s: str) -> str:
    # TV / audio-video
    if any(k in s for k in ["OLED", "QLED", "ULTRA HD", "4K", "SMART TV", "BRAVIA", "THE FRAME", "HOME CINEMA"]):
        return "TV_AUDIO_VIDEO"
    # Ordinateurs
    if any(k in s for k in ["MACBOOK", "ELITEBOOK", "LAPTOP", "NOTEBOOK", "CHROMEBOOK", "PC"]):
        return "COMPUTER"
    # Tablettes
    if any(k in s for k in ["IPAD", "TABLET"]):
        return "TABLET"
    # Montres / wearables
    if any(k in s for k in ["WATCH", "FITBIT", "GARMIN"]):
        return "WEARABLE"
    # Téléphonie (si présent chez toi)
    if any(k in s for k in ["IPHONE", "GALAXY", "SMARTPHONE", "MOBILE"]):
        return "PHONE"
    # Accessoires / périphériques
    if any(k in s for k in ["MOUSE", "KEYBOARD", "CASE", "COVER", "ADAPTER", "CABLE", "HARD DRIVE", "SSD"]):
        return "ACCESSORY"
    # Électroménager / maison
    if any(k in s for k in ["DYSON", "NESPRESSO", "COFFEE", "VACUUM", "AIRFRYER", "APPLIANCE"]):
        return "HOME_APPLIANCE"
    # Services / libellés retail
    if any(k in s for k in ["WARRANTY", "SERVICE", "CHARGE", "FULFILMENT"]):
        return "SERVICE_FEE"
    return "OTHER_FAMILY"

def map_model_group(x: str) -> str:
    s = normalize_text(x)
    if not s:
        return "MISSING"
    fam = extract_family(s)
    return f"{fam}"

def simplify_make(x: str, top_makes: set) -> str:
    if pd.isna(x):
        return "MISSING"
    # Garder les top_n marques, tout le reste → OTHER
    if x in top_makes:
        return x
    return "OTHER"

