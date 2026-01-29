# 🚀 Documentación del Despliegue en Render

Este documento detalla el proceso completo llevado a cabo para desplegar la arquitectura de microservicios (API FastAPI + Base de Datos PostgreSQL) en la plataforma en la nube **Render.com**.

El despliegue se ha realizado separando la capa de datos y la capa de aplicación en dos servicios independientes, comunicados mediante variables de entorno seguras.

---

## Arquitectura del Despliegue

* **Plataforma:** Render
* **Repositorio de Origen:** [GitHub - Antthony94/Ejercicio_FastAPI...](https://github.com/Antthony94/Ejercicio_FastAPI_Containerizaci-n_del_API_con_p-ginas-web)
* **Servicio 1 (Backend):** Web Service corriendo **Docker**.
* **Servicio 2 (Datos):** Instancia gestionada de **PostgreSQL 15**.
* **Región:** Frankfurt  - Para minimizar la latencia.

---

## Paso 1: Creación de la Base de Datos (PostgreSQL)

El primer paso fue configurar la base de datos en la nube para sustituir al contenedor local.

1.  **Creación del servicio:** Desde el dashboard de Render, seleccioné **"New PostgreSQL"**.
2.  **Configuración de la instancia:**
    * **Nombre:** `videojuegos-db-anthony`
    * **Región:** `Frankfurt` (Misma región que la app para usar la red privada).
    * **Versión PostgreSQL:** `15` (Para garantizar compatibilidad total con el desarrollo local).
    * **Plan:** `Free Tier`.
3.  **Obtención de credenciales:**
    Una vez la base de datos estuvo en estado `Available`, Render proporcionó los **"Internal Connection Details"** necesarios para la conexión:
    * `Hostname`: (Host interno de la red privada de Render)
    * `Port`: `5432`
    * `Database`: `videojuegos_db_anthony`
    * `Username`: (Usuario generado automáticamente)
    * `Password`: (Contraseña segura generada por Render)

---

## Paso 2: Despliegue de la Aplicación (Web Service)

Para la aplicación FastAPI, aproveché la configuración `Dockerfile` ya existente en el repositorio para que Render construya el entorno automáticamente.

1.  **Vinculación con GitHub:**
    * Conecté mi cuenta de GitHub con Render.
    * Seleccioné el repositorio: `Ejercicio_FastAPI_Containerizaci-n_del_API_con_p-ginas-web`.
2.  **Configuración del Servicio Web:**
    * **Nombre del servicio:** `api-videojuegos-anthony`
    * **Runtime:** **Docker** (Render detectó automáticamente el `Dockerfile` en la raíz).
    * **Región:** `Frankfurt` (para baja latencia con la BBDD).
    * **Rama (Branch):** `main`.
    * **Plan:** `Free Tier`.

---

## Paso 3: Conexión App-BBDD (Variables de Entorno)

Este es el punto crítico del despliegue. Mi código en `src/data/db.py` está programado para leer variables de entorno. En lugar de escribir las credenciales en el código (mala práctica de seguridad), las inyecté desde el panel de Render.

En la sección **"Environment Variables"** del Web Service, definí las siguientes claves con los valores obtenidos de la base de datos creada en el Paso 1:

| Variable | Valor (Origen) | Descripción |
| :--- | :--- | :--- |
| `DB_HOST` | Hostname de PostgreSQL | Dirección del servidor de BBDD. |
| `DB_PORT` | `5432` | Puerto estándar de conexión. |
| `DB_NAME` | Database Name | Nombre de la base de datos. |
| `DB_USER` | Username | Usuario propietario. |
| `DB_PASSWORD` | Password (Oculto) | Contraseña de acceso. |

> **Nota técnica:** Gracias a estas variables, el script `db.py` detecta el puerto 5432 y activa automáticamente el driver `psycopg2` para PostgreSQL, sin necesidad de cambiar el código que usaba MySQL en local.

---

## Paso 4: Despliegue Automático (CI/CD)

Render está configurado para realizar **Continuous Deployment**.
1.  Cada vez que hago un `git push` a la rama `main` en GitHub.
2.  Render detecta el cambio automáticamente.
3.  Descarga el nuevo código, construye la imagen Docker de nuevo y redesplega el servicio sin intervención manual.

---

## Verificación del Funcionamiento

Tras finalizar el despliegue (Estado `Live`), se realizaron las siguientes comprobaciones:

1.  **Logs de Arranque:** Se verificó en la consola de Render que la aplicación iniciaba correctamente:
    ```text
    INFO:     Application startup complete.
    ==> Detected a new open port HTTP:8000
    ```
2.  **Conexión a Datos:** Se confirmó que la aplicación creaba las tablas e insertaba los datos en la base de datos remota.
3.  **Acceso Público:** Se accedió a la URL pública proporcionada por Render (`https://api-videojuegos-anthony.onrender.com`) y se comprobó que la interfaz web carga correctamente y muestra los datos dinámicos.

---

**Estado del Despliegue:** Funciona perfectamente.
