# t8-client

## Descripción

t8-client es una aplicación de línea de comandos diseñada para interactuar con la API del T8. Permite obtener información sobre formas de onda y espectros, además de realizar diversas acciones como listarlos, descargarlos y representarlos gráficamente.

## Estructura del proyecto

El proyecto sigue las recomendaciones de estructura en Python:

```
t8-client/
│
├── src/                       # Código fuente
│   └── t8_client/             # Paquete principal
│       ├── __init__.py
│       ├── main.py            # Punto de entrada principal
│       ├── commands.py        # Definición de comandos
│       ├── api_client.py      # Cliente para interactuar con la API
│       ├── utils.py           # Funciones auxiliares
│       └── ...
│
├── output/                    # Directorio de salida
│   ├── figures/               # Gráficos generados
│   └── reports/               # Informes generados
│
├── tests/                     # Pruebas unitarias
│   ├── __init__.py
│   ├── test_commands.py
│   ├── test_api_client.py
│   └── ...
│
├── pyproject.toml             # Configuración de dependencias y metadatos
├── poetry.lock                # Archivo de bloqueo de dependencias
├── README.md                  # Documentación del proyecto
├── config/                    # Archivos de configuración (opcional)
├── .gitignore                 # Archivos a ignorar por Git
└── .env                       # Variables de entorno (opcional)
```

## Instalación

Para instalar `t8-client`, se recomienda usar Poetry:

```sh
poetry install
```

## Uso

La aplicación se ejecuta mediante el comando `t8-client`, el cual requiere un usuario, contraseña y host. Estos valores pueden pasarse como argumentos o establecerse en variables de entorno.

```sh
# Sin variables de entorno
$ t8-client -u <user> -p <passw> -h <host> <subcomando> ...

# Con variables de entorno
$ t8-client <subcomando> ...
```

### Subcomandos disponibles

- `list-waves`: Lista formas de onda disponibles.
- `list-spectra`: Lista espectros disponibles.
- `get-wave`: Obtiene una forma de onda y la guarda en formato CSV.
- `get-spectrum`: Obtiene un espectro y lo guarda en formato CSV.
- `plot-wave`: Representa una forma de onda en una gráfica.
- `plot-spectrum`: Representa un espectro en una gráfica.

Ejemplo de uso:

```sh
$ t8-client list-waves -M machine1 -p point1 -m mode1
2023-10-28T00:04:16
2024-01-05T04:28:28
```

```sh
$ t8-client get-wave -M machine1 -p point1 -m mode1 -t 2023-10-28T00:04:16
```

## Pruebas

Las pruebas se ejecutan con `pytest`:

```sh
pytest tests/
```

## Estilo de código

El proyecto sigue los estándares de programación en Python:

- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)

## Licencia

Este proyecto está bajo la licencia MIT.
