from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from env.env import dir_chromedriver
from selenium import webdriver

def iniciar_driver():
    try:
        options = Options()
        options.add_argument(f"user-data-dir=C:\\Users\\juand\\AppData\\Local\\Google\\Chrome\\User Data")  
        options.add_argument(f"profile-directory=Profile 1") 

        # Ruta al ejecutable de ChromeDriver
        service = Service(dir_chromedriver)  

        # Crear el driver
        driver = webdriver.Chrome(service=service, options=options)
        # driver = webdriver.Chrome(service=service)

        # Maximizar la ventana del navegador
        driver.maximize_window()

        # driver.quit() #Cierra todas las ventanas del navegador y finaliza la sesión de WebDriver.
        # #driver.close() #Cierra solo la ventana actual del navegador.

        return driver
    except Exception as e:
        driver.quit() 
        print("Error al abrir el navegador: ", e)
        return "Las credenciales son incorrectas o el controlador de Chrome no se abrió correctamente."
