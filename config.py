import os
from dotenv import load_dotenv

load_dotenv()

SCRAPER_API_TOKEN = str(os.getenv('SCRAPER_API_TOKEN'))

MONGODB_USER = str(os.getenv('MONGODB_USER'))
MONGODB_PASSWORD = str(os.getenv('MONGODB_PASSWORD'))
MONGODB_IP = str(os.getenv('MONGODB_IP'))
MONGODB_PORT = str(os.getenv('MONGODB_PORT'))
MONGODB_URI = (
    f"mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_IP}:{MONGODB_PORT}/"
    f"?authSource=admin&readPreference=primary"
    "&appname=MongoDB%20Compass&ssl=false"
)

DROM_BRAND_LIST = ('acura', 'alfa_romeo', 'alpina', 'asia', 'aston_martin', 'audi', 'bentley', 'bmw', 'bogdan',
                   'brilliance', 'bugatti', 'buick', 'byd', 'cadillac', 'changan', 'chery', 'cheryexeed', 'chevrolet',
                   'chrysler', 'citroen', 'dacia', 'daewoo', 'daihatsu', 'daimler', 'datsun', 'derways', 'dodge',
                   'dongfeng', 'dw_hover', 'eagle', 'faw', 'ferrari', 'fiat', 'ford', 'foton', 'gac', 'gaz', 'geely',
                   'genesis', 'geo', 'gmc', 'great_wall', 'hafei', 'haima', 'haval', 'hawtai', 'honda', 'hummer',
                   'hyundai', 'infiniti', 'iran_khodro', 'isuzu', 'izh', 'jac', 'jaguar', 'jeep', 'kia', 'lada',
                   'lamborghini', 'lancia', 'land_rover', 'lexus', 'lifan', 'lincoln', 'lotus', 'luaz', 'luxgen',
                   'maserati', 'maybach', 'mazda', 'mercedes-benz', 'mercury', 'mg', 'mini', 'mitsubishi', 'mitsuoka',
                   'moskvitch', 'nissan', 'oldsmobile', 'opel', 'other', 'peugeot', 'plymouth', 'pontiac', 'porsche',
                   'proton', 'ravon', 'renault', 'renault_samsung', 'rolls-royce', 'rover', 'saab', 'saturn', 'scion',
                   'seat', 'skoda', 'smart', 'ssang_yong', 'subaru', 'suzuki', 'tagaz', 'tesla', 'tianye', 'toyota',
                   'uaz', 'volkswagen', 'volvo', 'vortex', 'xin_kai', 'zaz', 'zotye', 'zx')

AUTORU_BRAND_LIST = ('ac', 'acura', 'adler', 'alfa_romeo', 'alpina', 'alpine', 'amc', 'am_general', 'apal', 'ariel',
                     'aro', 'asia', 'aston_martin', 'audi', 'aurus', 'austin', 'austin_healey', 'autobianchi',
                     'avtokam', 'baic', 'bajaj', 'baltijas_dzips', 'batmobile', 'bentley', 'bertone', 'bilenkin',
                     'bio_auto', 'bitter', 'bmw', 'borgward', 'brabus', 'brilliance', 'bristol', 'bufori', 'bugatti',
                     'buick', 'byd', 'byvin', 'cadillac', 'callaway', 'carbodies', 'caterham', 'chana', 'changan',
                     'changfeng', 'changhe', 'chery', 'chevrolet', 'chrysler', 'citroen', 'cizeta', 'coggiola', 'cord',
                     'dacia', 'dadi', 'daewoo', 'daihatsu', 'daimler', 'dallara', 'datsun', 'deco_rides', 'delage',
                     'delorean', 'derways', 'desoto', 'de_tomaso', 'dkw', 'dodge', 'dongfeng', 'doninvest',
                     'donkervoort', 'ds', 'dw_hower', 'eagle', 'eagle_cars', 'e_car', 'e_mobil', 'excalibur', 'faw',
                     'ferrari', 'fiat', 'fisker', 'flanker', 'ford', 'foton', 'fso', 'fuqi', 'gac', 'gaz', 'geely',
                     'genesis', 'geo', 'gmc', 'gonow', 'gordon', 'gp', 'great_wall', 'hafei', 'haima', 'hanomag',
                     'haval', 'hawtai', 'heinkel', 'hindustan', 'hispano_suiza', 'holden', 'honda', 'horch', 'huanghai',
                     'hudson', 'hummer', 'hyundai', 'infiniti', 'innocenti', 'international', 'invicta', 'iran_khodro',
                     'isdera', 'isuzu', 'iveco', 'ig', 'jac', 'jaguar', 'jeep', 'jensen', 'jinbei', 'jmc', 'kanonir',
                     'kia', 'koenigsegg', 'kombat', 'ktm', 'vaz', 'lamborghini', 'lancia', 'land_rover', 'landwind',
                     'lexus', 'liebao', 'lifan', 'ligier', 'lincoln', 'logem', 'lotus', 'lti', 'luaz', 'lucid',
                     'luxgen', 'mahindra', 'marcos', 'marlin', 'marussia', 'maruti', 'maserati', 'maybach', 'mazda',
                     'mclaren', 'mega', 'mercedes', 'mercury', 'metrocab', 'mg', 'microcar', 'minelli', 'mini',
                     'mitsubishi', 'mitsuoka', 'morgan', 'morris', 'moscvich', 'nash', 'nissan', 'noble', 'oldsmobile',
                     'opel', 'osca', 'packard', 'pagani', 'panoz', 'perodua', 'peugeot', 'pgo', 'piaggio', 'plymouth',
                     'pontiac', 'porsche', 'premier', 'promo_auto', 'proton', 'puch', 'puma', 'qoros', 'qvale',
                     'rambler', 'ravon', 'reliant', 'renaissance_cars', 'renault', 'rezvani', 'rimac', 'rinspeed',
                     'roewe', 'rolls_royce', 'ronart', 'rover', 'saab', 'saipa', 'saleen', 'samsung', 'santana',
                     'saturn', 'scion', 'sears', 'seat', 'shanghai_maple', 'shuanghuan', 'simca', 'skoda', 'smart',
                     'smz', 'soueast', 'spectre', 'spyker', 'ssang_yong', 'steyr', 'studebaker', 'subaru', 'suzuki',
                     'tagaz', 'talbot', 'tata', 'tatra', 'tazzari', 'tesla', 'think', 'tianma', 'tianye', 'tofas',
                     'toyota', 'trabant', 'tramontana', 'triumph', 'tvr', 'uaz', 'ultima', 'vauxhall', 'vector',
                     'venturi', 'volkswagen', 'volvo', 'vortex', 'wanderer', 'wartburg', 'westfield', 'wiesmann',
                     'willis', 'w_motors', 'xinkai', 'xpeng', 'yulon', 'zastava', 'zaz', 'zenos', 'zenvo', 'zibar',
                     'zil', 'zis', 'zotye', 'zx')

AVITO_BRAND_LIST = ('ac', 'acura', 'adler', 'alfa_romeo', 'alpina', 'amc', 'apal', 'aro', 'asia', 'aston_martin',
                    'audi', 'austin', 'austin_healey', 'avtokam', 'bajaj', 'baltijas_dzips', 'barkas', 'baw', 'bentley',
                    'bio_auto', 'bmw', 'bogdan', 'brilliance', 'buick', 'byd', 'cadillac', 'caterham', 'changan',
                    'changfeng', 'changhe', 'chery', 'cheryexeed', 'chevrolet', 'chrysler', 'citroen', 'dacia', 'dadi',
                    'daewoo', 'daihatsu', 'daimler', 'datsun', 'derways', 'desoto', 'dkw', 'dodge', 'dongfeng',
                    'doninvest', 'ds', 'dw_hower', 'eagle', 'eraz', 'excalibur', 'faw', 'ferrari', 'fiat', 'ford',
                    'foton', 'gac', 'gaz', 'geely', 'genesis', 'geo', 'gmc', 'gp', 'great_wall', 'hafei', 'haima',
                    'haval', 'hawtai', 'honda', 'huanghai', 'hudson', 'hummer', 'hyundai', 'infiniti', 'iran_khodro',
                    'isuzu', 'iveco', 'izh', 'jac', 'jaguar', 'jeep', 'jinbei', 'jmc', 'jonway', 'kia', 'kombat',
                    'vaz_lada', 'lamborghini', 'lancia', 'land_rover', 'landwind', 'ldv', 'lexus', 'lifan', 'lincoln',
                    'lti', 'luaz', 'luxgen', 'mahindra', 'maserati', 'maybach', 'mazda', 'mercedes-benz', 'mercury',
                    'metrocab', 'mg', 'mini', 'mitsubishi', 'mitsuoka', 'morgan', 'moskvich', 'nissan', 'nysa',
                    'oldsmobile', 'opel', 'packard', 'peugeot', 'plymouth', 'pontiac', 'porsche', 'proton', 'puch',
                    'raf', 'ravon', 'renault', 'renault_samsung', 'rocar', 'rolls_royce', 'rover', 'saab', 'saturn',
                    'scion', 'seat', 'shuanghuan', 'skoda', 'sma', 'smart', 'smz', 'ssangyong', 'steyr', 'studebaker',
                    'subaru', 'suzuki', 'tagaz', 'tata', 'tatra', 'tazzari', 'tesla', 'tianma', 'tianye', 'toyota',
                    'trabant', 'triumph_165', 'uaz', 'vauxhall', 'vis', 'volkswagen', 'volvo', 'vortex', 'wanderer',
                    'wartburg', 'westfield', 'willys', 'xin_kai', 'zaz', 'zil', 'zis', 'zotye', 'zuk', 'zx')
