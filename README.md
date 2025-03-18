# Blog Personal

Este es un proyecto de Blog Personal desarrollado como parte del roadmap de [roadmap.sh](https://roadmap.sh/projects/personal-blog). El blog permite a los usuarios leer artículos públicos y a los administradores gestionar (crear, editar y eliminar) artículos.

## Características

- **Vista de invitados:**
  - Ver una lista de artículos publicados.
  - Leer el contenido completo de cada artículo.

- **Panel de administración:**
  - Crear nuevos artículos.
  - Editar artículos existentes.
  - Eliminar artículos.
  - Cerrar sesión.

- **Autenticación:**
  - Inicio de sesión para administrador.
  - Este proyecto no contiene base de datos. Pero si deseas probar el proyecto con una BD, lo puedes hacer.
  Las credenciales de administrador, son las siguientes:
      ```bash
    User: admin
    Password: secret
    ```


## Tecnologías utilizadas

- **Frontend:**
  - HTML
  - CSS
  - Jinja2 (para plantillas)

- **Backend:**
  - Python
  - Flask (framework web)

- **Almacenamiento:**
  - Archivos JSON para almacenar los artículos.



## Instalación y ejecución

### Requisitos previos

- Python 3.x
- Flask (`pip install Flask`)
- `pytz` para manejo de zonas horarias (`pip install pytz`)

### Pasos para ejecutar el proyecto

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/RaykelJosue/personal_blog.git
   cd personal_blog
   ```

2. **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Iniciar la aplicación:**
    ```bash
    python run.py # El servidor estará en: http://localhost:5000
    ```

4. **Abre el navegador y escribe la URL:**
    ```bash
    http://localhost:5000
    ```
