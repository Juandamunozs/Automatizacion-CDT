import os

# Ruta del directorio actual (env.py)
dir_proyect = os.path.dirname(os.path.abspath(__file__))

# Ruta de los directorios principales
dir_assets = os.path.join(dir_proyect, '..', 'assets')
dir_module = os.path.join(dir_proyect, '..', 'module')
dir_res = os.path.join(dir_proyect, '..', 'res')
dir_service = os.path.join(dir_proyect, '..', 'service')
dir_db = os.path.join(dir_proyect, '..', 'db')
dir_res = os.path.join(dir_proyect, '..', 'res')

# Ruta de ejecutables como ChromeDriver
dir_chromedriver = r"C:\\selenium\\chromedriver.exe"

# Ruta de los subdirectorios
dir_logo = os.path.join(dir_assets, 'image', 'logo.jpeg')
dir_screenshot = os.path.join(dir_assets, 'screenshots')
dir_img_calendar = os.path.join(dir_assets, 'screenshots', 'screenshot.png')
dir_pdf = os.path.join(dir_module, 'pdf', "tasas_cdt.pdf")

user_email = "lifesnapco@gmail.com"
password_email = "bhcf jhfk jvkw ibro"