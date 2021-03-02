import re
import colorama
import ipaddress
import argparse
from os import path
from sys import argv

# regular expressions
re_domain = re.compile(r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z0-9][A-Za-z0-9-]{0,61}[A-Za-z]\b")
re_ipv4 = re.compile(r"\b(?:(?:[1-9][0-9]?|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}(?:1[0-9][0-9]|2[0-4][0-9]|25[0-5]|[1-9][0-9]?)\b")
re_url = re.compile(r"""
    (?:https?|ftps?)://         # Define protocol
    [\w-]+(?:\.[\w-]+)*\.\w+    # Define domain
    (?::\d+)?                   # Define port - optional
    (?:/\w+)*                   # Define path - optional
    (?:\.\w+)?                  # Define file extention - optional
    """, re.VERBOSE)
re_email = re.compile(r"""
    [\w\.-]+                    # inner mailbox
    @                           # at
    [\w-]+(?:\.[\w-]+)*\.\w+\b  # domain
    """, re.VERBOSE)

# results lists
list_domains = []
list_ipv4s = []
list_urls = []
list_emails = []

# tlds_lists
tlds_all = ['AAA', 'AARP', 'ABARTH', 'ABB', 'ABBOTT', 'ABBVIE', 'ABC', 'ABLE', 'ABOGADO', 'ABUDHABI', 'AC', 'ACADEMY',
            'ACCENTURE', 'ACCOUNTANT', 'ACCOUNTANTS', 'ACO', 'ACTOR', 'AD', 'ADAC', 'ADS', 'ADULT', 'AE', 'AEG', 'AERO',
            'AETNA', 'AF', 'AFAMILYCOMPANY', 'AFL', 'AFRICA', 'AG', 'AGAKHAN', 'AGENCY', 'AI', 'AIG', 'AIRBUS',
            'AIRFORCE', 'AIRTEL', 'AKDN', 'AL', 'ALFAROMEO', 'ALIBABA', 'ALIPAY', 'ALLFINANZ', 'ALLSTATE', 'ALLY',
            'ALSACE', 'ALSTOM', 'AM', 'AMAZON', 'AMERICANEXPRESS', 'AMERICANFAMILY', 'AMEX', 'AMFAM', 'AMICA',
            'AMSTERDAM', 'ANALYTICS', 'ANDROID', 'ANQUAN', 'ANZ', 'AO', 'AOL', 'APARTMENTS', 'APP', 'APPLE', 'AQ',
            'AQUARELLE', 'AR', 'ARAB', 'ARAMCO', 'ARCHI', 'ARMY', 'ARPA', 'ART', 'ARTE', 'AS', 'ASDA', 'ASIA',
            'ASSOCIATES', 'AT', 'ATHLETA', 'ATTORNEY', 'AU', 'AUCTION', 'AUDI', 'AUDIBLE', 'AUDIO', 'AUSPOST', 'AUTHOR',
            'AUTO', 'AUTOS', 'AVIANCA', 'AW', 'AWS', 'AX', 'AXA', 'AZ', 'AZURE', 'BA', 'BABY', 'BAIDU', 'BANAMEX',
            'BANANAREPUBLIC', 'BAND', 'BANK', 'BAR', 'BARCELONA', 'BARCLAYCARD', 'BARCLAYS', 'BAREFOOT', 'BARGAINS',
            'BASEBALL', 'BASKETBALL', 'BAUHAUS', 'BAYERN', 'BB', 'BBC', 'BBT', 'BBVA', 'BCG', 'BCN', 'BD', 'BE',
            'BEATS', 'BEAUTY', 'BEER', 'BENTLEY', 'BERLIN', 'BEST', 'BESTBUY', 'BET', 'BF', 'BG', 'BH', 'BHARTI', 'BI',
            'BIBLE', 'BID', 'BIKE', 'BING', 'BINGO', 'BIO', 'BIZ', 'BJ', 'BLACK', 'BLACKFRIDAY', 'BLOCKBUSTER', 'BLOG',
            'BLOOMBERG', 'BLUE', 'BM', 'BMS', 'BMW', 'BN', 'BNPPARIBAS', 'BO', 'BOATS', 'BOEHRINGER', 'BOFA', 'BOM',
            'BOND', 'BOO', 'BOOK', 'BOOKING', 'BOSCH', 'BOSTIK', 'BOSTON', 'BOT', 'BOUTIQUE', 'BOX', 'BR', 'BRADESCO',
            'BRIDGESTONE', 'BROADWAY', 'BROKER', 'BROTHER', 'BRUSSELS', 'BS', 'BT', 'BUDAPEST', 'BUGATTI', 'BUILD',
            'BUILDERS', 'BUSINESS', 'BUY', 'BUZZ', 'BV', 'BW', 'BY', 'BZ', 'BZH', 'CA', 'CAB', 'CAFE', 'CAL', 'CALL',
            'CALVINKLEIN', 'CAM', 'CAMERA', 'CAMP', 'CANCERRESEARCH', 'CANON', 'CAPETOWN', 'CAPITAL', 'CAPITALONE',
            'CAR', 'CARAVAN', 'CARDS', 'CARE', 'CAREER', 'CAREERS', 'CARS', 'CASA', 'CASE', 'CASEIH', 'CASH', 'CASINO',
            'CAT', 'CATERING', 'CATHOLIC', 'CBA', 'CBN', 'CBRE', 'CBS', 'CC', 'CD', 'CENTER', 'CEO', 'CERN', 'CF',
            'CFA', 'CFD', 'CG', 'CH', 'CHANEL', 'CHANNEL', 'CHARITY', 'CHASE', 'CHAT', 'CHEAP', 'CHINTAI', 'CHRISTMAS',
            'CHROME', 'CHURCH', 'CI', 'CIPRIANI', 'CIRCLE', 'CISCO', 'CITADEL', 'CITI', 'CITIC', 'CITY', 'CITYEATS',
            'CK', 'CL', 'CLAIMS', 'CLEANING', 'CLICK', 'CLINIC', 'CLINIQUE', 'CLOTHING', 'CLOUD', 'CLUB', 'CLUBMED',
            'CM', 'CN', 'CO', 'COACH', 'CODES', 'COFFEE', 'COLLEGE', 'COLOGNE', 'COM', 'COMCAST', 'COMMBANK',
            'COMMUNITY', 'COMPANY', 'COMPARE', 'COMPUTER', 'COMSEC', 'CONDOS', 'CONSTRUCTION', 'CONSULTING', 'CONTACT',
            'CONTRACTORS', 'COOKING', 'COOKINGCHANNEL', 'COOL', 'COOP', 'CORSICA', 'COUNTRY', 'COUPON', 'COUPONS',
            'COURSES', 'CPA', 'CR', 'CREDIT', 'CREDITCARD', 'CREDITUNION', 'CRICKET', 'CROWN', 'CRS', 'CRUISE',
            'CRUISES', 'CSC', 'CU', 'CUISINELLA', 'CV', 'CW', 'CX', 'CY', 'CYMRU', 'CYOU', 'CZ', 'DABUR', 'DAD',
            'DANCE', 'DATA', 'DATE', 'DATING', 'DATSUN', 'DAY', 'DCLK', 'DDS', 'DE', 'DEAL', 'DEALER', 'DEALS',
            'DEGREE', 'DELIVERY', 'DELL', 'DELOITTE', 'DELTA', 'DEMOCRAT', 'DENTAL', 'DENTIST', 'DESI', 'DESIGN', 'DEV',
            'DHL', 'DIAMONDS', 'DIET', 'DIGITAL', 'DIRECT', 'DIRECTORY', 'DISCOUNT', 'DISCOVER', 'DISH', 'DIY', 'DJ',
            'DK', 'DM', 'DNP', 'DO', 'DOCS', 'DOCTOR', 'DOG', 'DOMAINS', 'DOT', 'DOWNLOAD', 'DRIVE', 'DTV', 'DUBAI',
            'DUCK', 'DUNLOP', 'DUPONT', 'DURBAN', 'DVAG', 'DVR', 'DZ', 'EARTH', 'EAT', 'EC', 'ECO', 'EDEKA', 'EDU',
            'EDUCATION', 'EE', 'EG', 'EMAIL', 'EMERCK', 'ENERGY', 'ENGINEER', 'ENGINEERING', 'ENTERPRISES', 'EPSON',
            'EQUIPMENT', 'ER', 'ERICSSON', 'ERNI', 'ES', 'ESQ', 'ESTATE', 'ET', 'ETISALAT', 'EU', 'EUROVISION', 'EUS',
            'EVENTS', 'EXCHANGE', 'EXPERT', 'EXPOSED', 'EXPRESS', 'EXTRASPACE', 'FAGE', 'FAIL', 'FAIRWINDS', 'FAITH',
            'FAMILY', 'FAN', 'FANS', 'FARM', 'FARMERS', 'FASHION', 'FAST', 'FEDEX', 'FEEDBACK', 'FERRARI', 'FERRERO',
            'FI', 'FIAT', 'FIDELITY', 'FIDO', 'FILM', 'FINAL', 'FINANCE', 'FINANCIAL', 'FIRE', 'FIRESTONE', 'FIRMDALE',
            'FISH', 'FISHING', 'FIT', 'FITNESS', 'FJ', 'FK', 'FLICKR', 'FLIGHTS', 'FLIR', 'FLORIST', 'FLOWERS', 'FLY',
            'FM', 'FO', 'FOO', 'FOOD', 'FOODNETWORK', 'FOOTBALL', 'FORD', 'FOREX', 'FORSALE', 'FORUM', 'FOUNDATION',
            'FOX', 'FR', 'FREE', 'FRESENIUS', 'FRL', 'FROGANS', 'FRONTDOOR', 'FRONTIER', 'FTR', 'FUJITSU', 'FUJIXEROX',
            'FUN', 'FUND', 'FURNITURE', 'FUTBOL', 'FYI', 'GA', 'GAL', 'GALLERY', 'GALLO', 'GALLUP', 'GAME', 'GAMES',
            'GAP', 'GARDEN', 'GAY', 'GB', 'GBIZ', 'GD', 'GDN', 'GE', 'GEA', 'GENT', 'GENTING', 'GEORGE', 'GF', 'GG',
            'GGEE', 'GH', 'GI', 'GIFT', 'GIFTS', 'GIVES', 'GIVING', 'GL', 'GLADE', 'GLASS', 'GLE', 'GLOBAL', 'GLOBO',
            'GM', 'GMAIL', 'GMBH', 'GMO', 'GMX', 'GN', 'GODADDY', 'GOLD', 'GOLDPOINT', 'GOLF', 'GOO', 'GOODYEAR',
            'GOOG', 'GOOGLE', 'GOP', 'GOT', 'GOV', 'GP', 'GQ', 'GR', 'GRAINGER', 'GRAPHICS', 'GRATIS', 'GREEN', 'GRIPE',
            'GROCERY', 'GROUP', 'GS', 'GT', 'GU', 'GUARDIAN', 'GUCCI', 'GUGE', 'GUIDE', 'GUITARS', 'GURU', 'GW', 'GY',
            'HAIR', 'HAMBURG', 'HANGOUT', 'HAUS', 'HBO', 'HDFC', 'HDFCBANK', 'HEALTH', 'HEALTHCARE', 'HELP', 'HELSINKI',
            'HERE', 'HERMES', 'HGTV', 'HIPHOP', 'HISAMITSU', 'HITACHI', 'HIV', 'HK', 'HKT', 'HM', 'HN', 'HOCKEY',
            'HOLDINGS', 'HOLIDAY', 'HOMEDEPOT', 'HOMEGOODS', 'HOMES', 'HOMESENSE', 'HONDA', 'HORSE', 'HOSPITAL', 'HOST',
            'HOSTING', 'HOT', 'HOTELES', 'HOTELS', 'HOTMAIL', 'HOUSE', 'HOW', 'HR', 'HSBC', 'HT', 'HU', 'HUGHES',
            'HYATT', 'HYUNDAI', 'IBM', 'ICBC', 'ICE', 'ICU', 'ID', 'IE', 'IEEE', 'IFM', 'IKANO', 'IL', 'IM', 'IMAMAT',
            'IMDB', 'IMMO', 'IMMOBILIEN', 'IN', 'INC', 'INDUSTRIES', 'INFINITI', 'INFO', 'ING', 'INK', 'INSTITUTE',
            'INSURANCE', 'INSURE', 'INT', 'INTERNATIONAL', 'INTUIT', 'INVESTMENTS', 'IO', 'IPIRANGA', 'IQ', 'IR',
            'IRISH', 'IS', 'ISMAILI', 'IST', 'ISTANBUL', 'IT', 'ITAU', 'ITV', 'IVECO', 'JAGUAR', 'JAVA', 'JCB', 'JE',
            'JEEP', 'JETZT', 'JEWELRY', 'JIO', 'JLL', 'JM', 'JMP', 'JNJ', 'JO', 'JOBS', 'JOBURG', 'JOT', 'JOY', 'JP',
            'JPMORGAN', 'JPRS', 'JUEGOS', 'JUNIPER', 'KAUFEN', 'KDDI', 'KE', 'KERRYHOTELS', 'KERRYLOGISTICS',
            'KERRYPROPERTIES', 'KFH', 'KG', 'KH', 'KI', 'KIA', 'KIM', 'KINDER', 'KINDLE', 'KITCHEN', 'KIWI', 'KM', 'KN',
            'KOELN', 'KOMATSU', 'KOSHER', 'KP', 'KPMG', 'KPN', 'KR', 'KRD', 'KRED', 'KUOKGROUP', 'KW', 'KY', 'KYOTO',
            'KZ', 'LA', 'LACAIXA', 'LAMBORGHINI', 'LAMER', 'LANCASTER', 'LANCIA', 'LAND', 'LANDROVER', 'LANXESS',
            'LASALLE', 'LAT', 'LATINO', 'LATROBE', 'LAW', 'LAWYER', 'LB', 'LC', 'LDS', 'LEASE', 'LECLERC', 'LEFRAK',
            'LEGAL', 'LEGO', 'LEXUS', 'LGBT', 'LI', 'LIDL', 'LIFE', 'LIFEINSURANCE', 'LIFESTYLE', 'LIGHTING', 'LIKE',
            'LILLY', 'LIMITED', 'LIMO', 'LINCOLN', 'LINDE', 'LINK', 'LIPSY', 'LIVE', 'LIVING', 'LIXIL', 'LK', 'LLC',
            'LLP', 'LOAN', 'LOANS', 'LOCKER', 'LOCUS', 'LOFT', 'LOL', 'LONDON', 'LOTTE', 'LOTTO', 'LOVE', 'LPL',
            'LPLFINANCIAL', 'LR', 'LS', 'LT', 'LTD', 'LTDA', 'LU', 'LUNDBECK', 'LUXE', 'LUXURY', 'LV', 'LY', 'MA',
            'MACYS', 'MADRID', 'MAIF', 'MAISON', 'MAKEUP', 'MAN', 'MANAGEMENT', 'MANGO', 'MAP', 'MARKET', 'MARKETING',
            'MARKETS', 'MARRIOTT', 'MARSHALLS', 'MASERATI', 'MATTEL', 'MBA', 'MC', 'MCKINSEY', 'MD', 'ME', 'MED',
            'MEDIA', 'MEET', 'MELBOURNE', 'MEME', 'MEMORIAL', 'MEN', 'MENU', 'MERCKMSD', 'MG', 'MH', 'MIAMI',
            'MICROSOFT', 'MIL', 'MINI', 'MINT', 'MIT', 'MITSUBISHI', 'MK', 'ML', 'MLB', 'MLS', 'MM', 'MMA', 'MN', 'MO',
            'MOBI', 'MOBILE', 'MODA', 'MOE', 'MOI', 'MOM', 'MONASH', 'MONEY', 'MONSTER', 'MORMON', 'MORTGAGE', 'MOSCOW',
            'MOTO', 'MOTORCYCLES', 'MOV', 'MOVIE', 'MP', 'MQ', 'MR', 'MS', 'MSD', 'MT', 'MTN', 'MTR', 'MU', 'MUSEUM',
            'MUTUAL', 'MV', 'MW', 'MX', 'MY', 'MZ', 'NA', 'NAB', 'NAGOYA', 'NAME', 'NATIONWIDE', 'NATURA', 'NAVY',
            'NBA', 'NC', 'NE', 'NEC', 'NET', 'NETBANK', 'NETFLIX', 'NETWORK', 'NEUSTAR', 'NEW', 'NEWHOLLAND', 'NEWS',
            'NEXT', 'NEXTDIRECT', 'NEXUS', 'NF', 'NFL', 'NG', 'NGO', 'NHK', 'NI', 'NICO', 'NIKE', 'NIKON', 'NINJA',
            'NISSAN', 'NISSAY', 'NL', 'NO', 'NOKIA', 'NORTHWESTERNMUTUAL', 'NORTON', 'NOW', 'NOWRUZ', 'NOWTV', 'NP',
            'NR', 'NRA', 'NRW', 'NTT', 'NU', 'NYC', 'NZ', 'OBI', 'OBSERVER', 'OFF', 'OFFICE', 'OKINAWA', 'OLAYAN',
            'OLAYANGROUP', 'OLDNAVY', 'OLLO', 'OM', 'OMEGA', 'ONE', 'ONG', 'ONL', 'ONLINE', 'ONYOURSIDE', 'OOO', 'OPEN',
            'ORACLE', 'ORANGE', 'ORG', 'ORGANIC', 'ORIGINS', 'OSAKA', 'OTSUKA', 'OTT', 'OVH', 'PA', 'PAGE', 'PANASONIC',
            'PARIS', 'PARS', 'PARTNERS', 'PARTS', 'PARTY', 'PASSAGENS', 'PAY', 'PCCW', 'PE', 'PET', 'PF', 'PFIZER',
            'PG', 'PH', 'PHARMACY', 'PHD', 'PHILIPS', 'PHONE', 'PHOTO', 'PHOTOGRAPHY', 'PHOTOS', 'PHYSIO', 'PICS',
            'PICTET', 'PICTURES', 'PID', 'PIN', 'PING', 'PINK', 'PIONEER', 'PIZZA', 'PK', 'PL', 'PLACE', 'PLAY',
            'PLAYSTATION', 'PLUMBING', 'PLUS', 'PM', 'PN', 'PNC', 'POHL', 'POKER', 'POLITIE', 'PORN', 'POST', 'PR',
            'PRAMERICA', 'PRAXI', 'PRESS', 'PRIME', 'PRO', 'PROD', 'PRODUCTIONS', 'PROF', 'PROGRESSIVE', 'PROMO',
            'PROPERTIES', 'PROPERTY', 'PROTECTION', 'PRU', 'PRUDENTIAL', 'PS', 'PT', 'PUB', 'PW', 'PWC', 'PY', 'QA',
            'QPON', 'QUEBEC', 'QUEST', 'QVC', 'RACING', 'RADIO', 'RAID', 'RE', 'READ', 'REALESTATE', 'REALTOR',
            'REALTY', 'RECIPES', 'RED', 'REDSTONE', 'REDUMBRELLA', 'REHAB', 'REISE', 'REISEN', 'REIT', 'RELIANCE',
            'REN', 'RENT', 'RENTALS', 'REPAIR', 'REPORT', 'REPUBLICAN', 'REST', 'RESTAURANT', 'REVIEW', 'REVIEWS',
            'REXROTH', 'RICH', 'RICHARDLI', 'RICOH', 'RIL', 'RIO', 'RIP', 'RMIT', 'RO', 'ROCHER', 'ROCKS', 'RODEO',
            'ROGERS', 'ROOM', 'RS', 'RSVP', 'RU', 'RUGBY', 'RUHR', 'RUN', 'RW', 'RWE', 'RYUKYU', 'SA', 'SAARLAND',
            'SAFE', 'SAFETY', 'SAKURA', 'SALE', 'SALON', 'SAMSCLUB', 'SAMSUNG', 'SANDVIK', 'SANDVIKCOROMANT', 'SANOFI',
            'SAP', 'SARL', 'SAS', 'SAVE', 'SAXO', 'SB', 'SBI', 'SBS', 'SC', 'SCA', 'SCB', 'SCHAEFFLER', 'SCHMIDT',
            'SCHOLARSHIPS', 'SCHOOL', 'SCHULE', 'SCHWARZ', 'SCIENCE', 'SCJOHNSON', 'SCOT', 'SD', 'SE', 'SEARCH', 'SEAT',
            'SECURE', 'SECURITY', 'SEEK', 'SELECT', 'SENER', 'SERVICES', 'SES', 'SEVEN', 'SEW', 'SEX', 'SEXY', 'SFR',
            'SG', 'SH', 'SHANGRILA', 'SHARP', 'SHAW', 'SHELL', 'SHIA', 'SHIKSHA', 'SHOES', 'SHOP', 'SHOPPING', 'SHOUJI',
            'SHOW', 'SHOWTIME', 'SI', 'SILK', 'SINA', 'SINGLES', 'SITE', 'SJ', 'SK', 'SKI', 'SKIN', 'SKY', 'SKYPE',
            'SL', 'SLING', 'SM', 'SMART', 'SMILE', 'SN', 'SNCF', 'SO', 'SOCCER', 'SOCIAL', 'SOFTBANK', 'SOFTWARE',
            'SOHU', 'SOLAR', 'SOLUTIONS', 'SONG', 'SONY', 'SOY', 'SPA', 'SPACE', 'SPORT', 'SPOT', 'SPREADBETTING', 'SR',
            'SRL', 'SS', 'ST', 'STADA', 'STAPLES', 'STAR', 'STATEBANK', 'STATEFARM', 'STC', 'STCGROUP', 'STOCKHOLM',
            'STORAGE', 'STORE', 'STREAM', 'STUDIO', 'STUDY', 'STYLE', 'SU', 'SUCKS', 'SUPPLIES', 'SUPPLY', 'SUPPORT',
            'SURF', 'SURGERY', 'SUZUKI', 'SV', 'SWATCH', 'SWIFTCOVER', 'SWISS', 'SX', 'SY', 'SYDNEY', 'SYSTEMS', 'SZ',
            'TAB', 'TAIPEI', 'TALK', 'TAOBAO', 'TARGET', 'TATAMOTORS', 'TATAR', 'TATTOO', 'TAX', 'TAXI', 'TC', 'TCI',
            'TD', 'TDK', 'TEAM', 'TECH', 'TECHNOLOGY', 'TEL', 'TEMASEK', 'TENNIS', 'TEVA', 'TF', 'TG', 'TH', 'THD',
            'THEATER', 'THEATRE', 'TIAA', 'TICKETS', 'TIENDA', 'TIFFANY', 'TIPS', 'TIRES', 'TIROL', 'TJ', 'TJMAXX',
            'TJX', 'TK', 'TKMAXX', 'TL', 'TM', 'TMALL', 'TN', 'TO', 'TODAY', 'TOKYO', 'TOOLS', 'TOP', 'TORAY',
            'TOSHIBA', 'TOTAL', 'TOURS', 'TOWN', 'TOYOTA', 'TOYS', 'TR', 'TRADE', 'TRADING', 'TRAINING', 'TRAVEL',
            'TRAVELCHANNEL', 'TRAVELERS', 'TRAVELERSINSURANCE', 'TRUST', 'TRV', 'TT', 'TUBE', 'TUI', 'TUNES', 'TUSHU',
            'TV', 'TVS', 'TW', 'TZ', 'UA', 'UBANK', 'UBS', 'UG', 'UK', 'UNICOM', 'UNIVERSITY', 'UNO', 'UOL', 'UPS',
            'US', 'UY', 'UZ', 'VA', 'VACATIONS', 'VANA', 'VANGUARD', 'VC', 'VE', 'VEGAS', 'VENTURES', 'VERISIGN',
            'VERSICHERUNG', 'VET', 'VG', 'VI', 'VIAJES', 'VIDEO', 'VIG', 'VIKING', 'VILLAS', 'VIN', 'VIP', 'VIRGIN',
            'VISA', 'VISION', 'VIVA', 'VIVO', 'VLAANDEREN', 'VN', 'VODKA', 'VOLKSWAGEN', 'VOLVO', 'VOTE', 'VOTING',
            'VOTO', 'VOYAGE', 'VU', 'VUELOS', 'WALES', 'WALMART', 'WALTER', 'WANG', 'WANGGOU', 'WATCH', 'WATCHES',
            'WEATHER', 'WEATHERCHANNEL', 'WEBCAM', 'WEBER', 'WEBSITE', 'WED', 'WEDDING', 'WEIBO', 'WEIR', 'WF',
            'WHOSWHO', 'WIEN', 'WIKI', 'WILLIAMHILL', 'WIN', 'WINDOWS', 'WINE', 'WINNERS', 'WME', 'WOLTERSKLUWER',
            'WOODSIDE', 'WORK', 'WORKS', 'WORLD', 'WOW', 'WS', 'WTC', 'WTF', 'XBOX', 'XEROX', 'XFINITY', 'XIHUAN',
            'XIN', 'XXX', 'XYZ', 'YACHTS', 'YAHOO', 'YAMAXUN', 'YANDEX', 'YE', 'YODOBASHI', 'YOGA', 'YOKOHAMA', 'YOU',
            'YOUTUBE', 'YT', 'YUN', 'ZA', 'ZAPPOS', 'ZARA', 'ZERO', 'ZIP', 'ZM', 'ZONE', 'ZUERICH', 'ZW']
tlds_known = ['COM', 'NET', 'ORG', 'EDU', 'GOV', 'MIL', 'INFO', 'BIZ', 'ONLINE', 'ICU', 'TOP', 'XYZ', 'SITE',
              'CLUB', 'WANG', 'VIP', 'SHOP', 'WORK', 'FAIL', 'VIAJES', 'EXPOSED', 'CAM', 'LIVE', 'FIT', 'CASA',
              'BUZZ', 'LOAN', 'WIN', 'BID', 'STREAM', 'DESI', 'REVIEW', 'DATE', 'TRADE', 'PICS', 'AERO', 'BIZ',
              'COOP', 'MUSEUM', 'PRO' 'RU', 'US', 'TOKIO', 'IN', 'IR', 'AU', 'UK', 'DE', 'BR', 'CN', 'NL', 'EU',
              'FR', 'IT', 'TK', 'GA', 'SO', 'VG', 'TO', 'HK', 'PW', 'FM', 'KI', 'LA', 'UG']


def validate_tld(domain, compare_all_tlds):
    if compare_all_tlds:
        tlds = tlds_all
    else:
        tlds = tlds_known
    tld = str(domain).split(".").pop().upper()
    if tld in tlds:
        return True
    else:
        return False


def validate_ipv4(suspected_ipv4):
    try:
        if ipaddress.IPv4Address(suspected_ipv4).is_global:
            return True
        else:
            return False
    except ipaddress.AddressValueError:
        return False


def print_iocs(list_iocs, title):
    if len(list_iocs) == 0:
        return
    print("\n")
    print(colorama.Fore.LIGHTGREEN_EX + "#### {} ####".format(title.upper()))
    print()
    i = 1
    for ioc in list_iocs:
        print("[{}] {}".format(i, ioc))
        i += 1


def main():

    # parse arguments
    parser = argparse.ArgumentParser(description="Parse network IOC's from a text file (like dumped strings from ProcessHacker)")
    parser.add_argument("i", metavar="<text-file>", help="Input text file to parse.")
    parser.add_argument("-at", action="store_true", help="compare against all tlds exist (may cause a lot of FP's). default: only top popular & abused tlds.")
    args = parser.parse_args()

    # colorama initialization
    colorama.init(autoreset=True)

    # read input file
    try:
        with open(args.i, "rt") as input_file:
            input_data = input_file.read()
    except UnicodeDecodeError:
        print(colorama.Fore.LIGHTRED_EX + "\n[-] Cannot read binary files.\n")
        exit(1)

    # search ipv4s
    suspected_ipv6s = re.findall(re_ipv4, input_data)
    for suspected_ipv4 in suspected_ipv6s:
        if validate_ipv4(suspected_ipv4) and (suspected_ipv4 not in list_ipv4s):
            list_ipv4s.append(suspected_ipv4)
    list_ipv4s.sort()
    print_iocs(list_ipv4s, "ipv4s")

    # search domains
    suspected_domains = re.findall(re_domain, input_data)
    for suspected_domain in suspected_domains:
        if validate_tld(suspected_domain, args.at) and (suspected_domain not in list_domains):
            list_domains.append(suspected_domain)
    list_domains.sort()
    print_iocs(list_domains, "domains")

    # search urls
    suspected_urls = re.findall(re_url, input_data)
    for suspected_url in suspected_urls:
        # if suspected url is a substring of existing url in list, don't append
        is_substr = False
        for url in list_urls:
            if suspected_url in url:
                is_substr = True
                break
        if not is_substr:
            list_urls.append(suspected_url)
    list_urls.sort()
    print_iocs(list_urls, "urls")

    # search emails
    suspected_emails = re.findall(re_email, input_data)
    for suspected_email in suspected_emails:
        if validate_tld(suspected_email, args.at) and suspected_email not in list_emails:
            list_emails.append(suspected_email)
    list_emails.sort()
    print_iocs(list_emails, "emails")

    print("\n")


try:
    main()
except KeyboardInterrupt:
    print(colorama.Fore.LIGHTRED_EX + "\n[-] Script Interrupted by user.\n")

