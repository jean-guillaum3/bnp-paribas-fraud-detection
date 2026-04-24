# Comment démasquer les fraudeurs ? BNP Paribas PF

import re

import numpy as np
import pandas as pd


def map_item_group(x: str) -> str: 
    """
    Catégorise un libellé d'article ou de groupe de produits dans une thématique simplifiée.

    Cette fonction analyse une chaîne de caractères et utilise une logique de recherche par 
    mots-clés pour regrouper les articles dans des catégories. Elle est conçue pour être 
    utilisée avec la méthode `apply` d'un DataFrame pandas.

    Parameters
    ----------
    x : str
        Le libellé ou la description de l'article à catégoriser. 
        Peut être une valeur manquante (NaN).

    Returns
    -------
    str
        Le nom de la catégorie simplifiée. Retourne "OTHER" si aucune correspondance 
        n'est trouvée, si la valeur est nulle ou si le libellé est non explicite (ex: SKU).

    Notes
    -----
    La fonction normalise l'entrée en majuscules avant le traitement. L'ordre des 
    conditions `if` définit la priorité de catégorisation en cas de mots-clés multiples.
    """
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
    """
    Normalise une chaîne de caractères pour faciliter les comparaisons textuelles.

    Parameters
    ----------
        x (str): La chaîne de caractères à traiter. Peut être une valeur 
            manquante (NaN) issue d'un objet pandas.

    Returns
    -------
        str: La chaîne nettoyée. Retourne une chaîne vide si l'entrée est nulle (NaN).
    """
    if pd.isna(x):
        return ""
    s = str(x).upper().strip()
    s = s.replace("&", " ")
    s = re.sub(r"\s+", " ", s)
    return s

def extract_family(s: str) -> str:
    """
    Extrait la famille de produits à partir d'une chaîne de caractères normalisée.

    Cette fonction agit comme un classifieur par mots-clés (rule-based classifier).
    Elle scanne le libellé pour identifier des technologies, des marques ou des 
    types d'objets spécifiques afin de les regrouper dans des catégories métier.

    Parameters
    ----------
    s : str
        La chaîne de caractères à analyser (généralement déjà passée par 
        `normalize_text`).

    Returns
    -------
    str
        Le nom de la famille de produits (ex: 'COMPUTER', 'TV_AUDIO_VIDEO').
        Retourne 'OTHER_FAMILY' si aucun mot-clé n'est détecté.

    Notes
    -----
    L'ordre des conditions est hiérarchique. Par exemple, si un libellé contient 
    à la fois "LAPTOP" et "ADAPTER", il sera classé en 'COMPUTER' car cette 
    vérification intervient avant celle des accessoires.
    """
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
    """
    Point d'entrée principal pour la catégorisation des modèles d'articles.

    Cette fonction orchestre le pipeline de prétraitement en deux étapes :
    1. Nettoyage et normalisation de la chaîne via `normalize_text`.
    2. Classification thématique basée sur des règles via `extract_family`.

    Parameters
    ----------
    x : str
        Le libellé brut du modèle (peut contenir des caractères spéciaux, 
        des espaces superflus ou être nul).

    Returns
    -------
    str
        Le libellé de la famille identifiée. Retourne "MISSING" si l'entrée 
        est vide ou non renseignée après normalisation.

    See Also
    --------
    normalize_text : Fonction de nettoyage de la chaîne.
    extract_family : Logique de classification par mots-clés.
    """
    s = normalize_text(x)
    if not s:
        return "MISSING"
    fam = extract_family(s)
    return f"{fam}"

def simplify_make(x: str, top_makes: set) -> str:
    """
    Réduit la cardinalité d'une variable catégorielle (marque) en isolant les valeurs majeures.

    Les marques ne faisant pas partie du groupe de tête (top_makes) sont 
    automatiquement reclassées dans une catégorie générique. Cette approche est 
    essentielle pour la robustesse des modèles d'ingénierie statistique.

    Parameters
    ----------
    x : str
        Le nom de la marque à traiter.
    top_makes : set
        Un ensemble contenant les noms des marques les plus fréquentes 
        que l'on souhaite conserver individuellement.

    Returns
    -------
    str
        Le nom original de la marque si elle est présente dans `top_makes`.
        "MISSING" si la valeur est nulle (NaN).
        "OTHER" pour toutes les autres marques.
    """
    if pd.isna(x):
        return "MISSING"
    # Garder les top_n marques, tout le reste → OTHER
    if x in top_makes:
        return x
    return "OTHER"

def preprocess_wide(df_in: pd.DataFrame, fit_cols=None) -> pd.DataFrame:
    """
    Réalise le prétraitement complet d'un DataFrame en format "wide" pour le Machine Learning.

    Cette fonction prépare les données pour des modèles de type arbres (XGBoost, Random Forest)
    en nettoyant les identifiants inutiles, en gérant les valeurs manquantes numériques 
    et en transformant les variables catégorielles via un One-Hot Encoding (OHE).

    Parameters
    ----------
    df_in : pd.DataFrame
        Le DataFrame d'entrée contenant les variables brutes (numériques et catégorielles).
    fit_cols : list or pd.Index, optional
        La liste exacte des colonnes attendues en sortie. 
        - Si fourni : Aligne `df` sur ces colonnes (ajoute les manquantes avec des 0, 
          supprime les colonnes inconnues). Utile pour le set de Test/Validation.
        - Si None (par défaut) : Génère les colonnes à partir des données présentes. 
          Utile pour le set d'Entraînement.

    Returns
    -------
    pd.DataFrame
        Le DataFrame transformé, entièrement numérique et prêt pour l'entraînement.

    Notes
    -----
    - Les colonnes contenant "goods_code" sont systématiquement supprimées car elles 
      agissent comme des identifiants à trop forte cardinalité.
    - L'imputation des valeurs manquantes numériques par 0 est choisie ici pour 
      permettre aux algorithmes basés sur les arbres de créer des noeuds de décision 
      spécifiques pour les valeurs absentes.
    - `pd.get_dummies` est utilisé avec `dummy_na=True` pour capturer l'aspect 
      informatif de l'absence de données catégorielles.
    """
    df = df_in.copy()
    
    # Suppression des colonnes inutiles (goods_code)
    cols_to_drop = [c for c in df.columns if "goods_code" in c]
    df = df.drop(columns=cols_to_drop)
    
    # Remplissage basique des trous numériques
    # On remplace les NaN par 0 pour que l'arbre les sépare
    num_cols = df.select_dtypes(include=[np.number]).columns
    df[num_cols] = df[num_cols].fillna(0)
    
    # One-Hot Encoding Massif
    # Cela va créer beaucoup de colonnes (item1_A, item1_B...)
    df = pd.get_dummies(df, dummy_na=True)
    
    # Alignement des colonnes (Train vs Test)
    if fit_cols is not None:
        # On ne garde que les colonnes vues dans le Train
        # On ajoute les manquantes (remplies de 0)
        for c in fit_cols:
            if c not in df.columns:
                df[c] = 0
        df = df[fit_cols] # Réordonner et filtrer
    else:
        # Optimisation (Train uniquement) : retirer les colonnes quasi-vides
        # On garde seulement les colonnes qui ont au moins 1% de données non-nulles/non-zéro
        pass
        
    return df