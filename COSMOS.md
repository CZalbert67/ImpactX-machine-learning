# Guía de Conexión a Cosmos DB - ImpactX Machine Learning

Esta guía contiene la configuración de acceso y código en **Python** para conectar modelos de Machine Learning a **Azure Cosmos DB NoSQL** con el fin de leer y procesar datos.

## Credenciales de Conexión (Desarrollo / Pruebas)

* **Account Endpoint:** `https://impactx-db-west-final.documents.azure.com:443/`
* **Account Key (Lectura y Escritura):** `<REPLACE_WITH_YOUR_COSMOS_KEY>`
* **Base de Datos Principal:** `ImpactX-Data`
* **Base de Datos Temporal/Test:** `TestDatabase`

---

## 🐍 Integración con Python para Ciencia de Datos y ML

Instala el SDK oficial de Azure Cosmos DB en Python:
```bash
pip install azure-cosmos pandas
```

### Script de Conexión y Conversión a DataFrame de Pandas:
Usa este snippet para consultar información histórica e importarla como un DataFrame de Pandas para entrenamiento o predicción:

```python
from azure.cosmos import CosmosClient
import pandas as pd

# Configuración
endpoint = "https://impactx-db-west-final.documents.azure.com:443/"
key = "<REPLACE_WITH_YOUR_COSMOS_KEY>"

# Inicializar cliente
client = CosmosClient(endpoint, credential=key)

# Seleccionar Base de datos y Contenedor
database = client.get_database_client("ImpactX-Data")
container = database.get_container_client("TuContenedor")

# Realizar Consulta SQL en NoSQL
query = "SELECT * FROM c"
items = list(container.query_items(
    query=query,
    enable_cross_partition_query=True
))

# Convertir los resultados JSON directamente a un DataFrame de Pandas
df = pd.DataFrame(items)

# Limpiar campos de sistema de Cosmos DB (opcional)
system_columns = ['_rid', '_self', '_etag', '_attachments', '_ts']
df = df.drop(columns=[col for col in system_columns if col in df.columns])

print("Datos cargados correctamente:")
print(df.head())
```

---

## Cómo usar Cosmos DB Studio para Validaciones Locales

Como científico de datos, puedes usar Cosmos DB Studio para verificar las propiedades disponibles en los documentos JSON y planear tus features:

1. Descarga e instala **Cosmos DB Studio**.
2. Crea una nueva conexión ingresando los siguientes datos:
   * **Name:** `ImpactX`
   * **Endpoint:** `https://impactx-db-west-final.documents.azure.com:443/`
   * **Key:** `<REPLACE_WITH_YOUR_COSMOS_KEY>`
   * **Serverless:** Desmarcado
   * **Folder:** En blanco
3. Haz clic en **OK**.
4. Haz doble clic en el contenedor bajo `ImpactX-Data`.
5. En la ventana central escribe tu consulta analítica, ej:
   ```sql
   SELECT * FROM c WHERE c.name = "ImpactX Connection Test"
   ```
6. Haz clic en el botón de **Play (Triángulo Negro)**.
