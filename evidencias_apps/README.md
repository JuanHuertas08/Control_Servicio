# Evidencias de acceso a aplicaciones

Este script abre los primeros links del listado de aplicaciones. Toma una captura cuando carga la página y otra después del login, si la app lo requiere. Con eso genera un informe en Word.

Solo navega y consulta, no guarda ningún registro.

## Requisitos (una sola vez)

```bash
pip install playwright python-docx openpyxl
python -m playwright install chromium
```

## Uso

1. Conecta la **VPN del ICBF**.
2. Ejecuta el script:

```bash
python generar_evidencias.py "Listado_de_Aplicaciones_Para_Pruebas_de_Aplicaciones_2026.xlsx"
```

Las capturas y el Word quedan en la carpeta `evidencias_AAAAMMDD_HHMM/`.

### Opciones

| Opción | Uso |
|---|---|
| `--manual` | Pausa en cada app para que inicies sesión o navegues a mano. Pulsa Enter para continuar. Úsalo si el login automático falla. |
| `--cantidad 24` | Número de links a probar, contando desde el primero. Por defecto: todos. |
| `--desde 25` | Empieza desde la app n.º 25, contando sin las "No probar". |
| `--solo 19,23,25` | Prueba solo las apps con esos números (los del informe). |
| `--incluir-no-probar` | Incluye las apps marcadas "No probar" como "No Aplica". Por defecto se omiten. |
| `--hoja "Criticidad Windows"` | Hoja del Excel que se va a leer. |
| `--oculto` | Ejecuta el navegador sin abrir ventana. |
| `--salida archivo.docx` | Nombre del Word que se genera. |

## Estados

- **OK**: la página carga y el login funciona, o la app no requiere login.
- **Revisar**: la página carga, pero el login automático no se pudo confirmar. Verifícalo con `--manual`.
- **Falla**: la página no carga (timeout, error HTTP o sin VPN).
- **No Aplica**: la app está marcada como "No probar" en el listado.
