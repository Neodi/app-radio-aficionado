# 🏗️ Clean Architecture - Quiz Scraper

Este proyecto ha sido refactorizado siguiendo los principios de **Clean Architecture**, organizando el código en capas bien definidas con responsabilidades claras.

## 📁 Estructura del Proyecto

```
src/
├── 🏛️ domain/                    # Capa de Dominio (Reglas de Negocio)
│   ├── entities/                 # Entidades del dominio
│   │   └── quiz_question.py     # Modelos Pydantic (QuizQuestion, Title, Option)
│   └── repositories/            # Interfaces de repositorio
│       └── quiz_repository.py   # Contratos para persistencia y web scraping
│
├── 🎯 application/               # Capa de Aplicación (Casos de Uso)
│   ├── use_cases/               # Casos de uso del negocio
│   │   └── quiz_use_cases.py    # ExtractQuizUseCase, LoadQuizUseCase, etc.
│   └── services/                # Servicios de aplicación
│       └── quiz_service.py      # Lógica de negocio compleja
│
├── 🔧 infrastructure/            # Capa de Infraestructura (Detalles Técnicos)
│   ├── repositories/            # Implementaciones de repositorios
│   │   └── json_quiz_repository.py  # Persistencia en JSON
│   ├── web_scraping/            # Web scraping con Selenium
│   │   ├── driver_config.py     # Configuración del driver
│   │   ├── image_downloader.py  # Descarga de imágenes
│   │   └── selenium_scraper.py  # Scraper principal
│   └── file_storage/            # Almacenamiento de archivos
│
├── 🖥️ presentation/              # Capa de Presentación (Interfaz de Usuario)
│   └── cli/                     # Interfaz de línea de comandos
│       └── quiz_scraper_cli.py  # CLI principal
│
└── 🛠️ shared/                    # Utilidades compartidas
    └── utils.py                 # Utilidades comunes
```

## 🎯 Principios de Clean Architecture

### 🏛️ **Capa de Dominio** (Innermost)
- **🚫 No depende de nada externo**
- Contiene las entidades y reglas de negocio puras
- Define las interfaces que deben implementar las capas externas

### 🎯 **Capa de Aplicación**
- **📋 Orquesta los casos de uso**
- Depende solo del dominio
- Contiene la lógica de aplicación específica

### 🔧 **Capa de Infraestructura**
- **🔌 Implementa las interfaces del dominio**
- Maneja detalles técnicos (BD, web scraping, archivos)
- Depende del dominio y aplicación

### 🖥️ **Capa de Presentación**
- **👤 Interfaz con el usuario**
- Orquesta los casos de uso
- Depende de aplicación e infraestructura

## 🚀 Cómo Usar la Nueva Arquitectura

### Ejecutar el Scraper
```bash
# Usando el nuevo entry point con Clean Architecture
uv run main_clean.py

# O usando el archivo legacy (mantiene compatibilidad)
uv run main.py
```

### Usar los Casos de Uso Programáticamente

```python
from src.application.use_cases.quiz_use_cases import ExtractQuizUseCase
from src.application.services.quiz_service import QuizService
from src.infrastructure.repositories.json_quiz_repository import JsonQuizQuestionRepository
from src.infrastructure.web_scraping.selenium_scraper import SeleniumWebScrapingRepository

# Configurar dependencias
quiz_repo = JsonQuizQuestionRepository()
web_scraper = SeleniumWebScrapingRepository()
quiz_service = QuizService()

# Crear caso de uso
extract_use_case = ExtractQuizUseCase(web_scraper, quiz_repo, quiz_service)

# Ejecutar extracción
result = extract_use_case.execute("https://example.com")
if result["success"]:
    print(f"Extraídas {result['total_questions']} preguntas")
```

## 🔄 Flujo de Dependencias

```
Presentation → Application → Domain
     ↓              ↓
Infrastructure → Application
```

## 🎨 Beneficios de Clean Architecture

### ✅ **Testabilidad**
- Cada capa puede ser probada independientemente
- Fácil creación de mocks y stubs

### ✅ **Mantenibilidad**
- Código organizado en responsabilidades claras
- Cambios en una capa no afectan otras

### ✅ **Flexibilidad**
- Fácil intercambio de implementaciones
- Soporte para múltiples interfaces (CLI, Web, API)

### ✅ **Escalabilidad**
- Arquitectura preparada para crecimiento
- Fácil adición de nuevas funcionalidades

## 🔧 Casos de Uso Disponibles

### 📥 **ExtractQuizUseCase**
Extrae preguntas desde una URL web
```python
result = extract_use_case.execute(url, save_legacy=True)
```

### 📖 **LoadQuizUseCase**
Carga preguntas desde almacenamiento
```python
result = load_use_case.execute(filename="quiz_data.json")
```

### 🔍 **SearchQuizUseCase**
Busca preguntas por términos
```python
result = search_use_case.execute(questions, "frecuencia")
```

### 📤 **ExportQuizUseCase**
Exporta en diferentes formatos
```python
result = export_use_case.execute(questions, "csv", "export")
```

## 🛠️ Extensibilidad

### Añadir Nueva Fuente de Datos
1. Crear nueva implementación de `WebScrapingRepository`
2. Registrar en la capa de presentación
3. ¡Listo! Los casos de uso funcionan igual

### Añadir Nueva Interfaz (API REST)
1. Crear controladores en nueva carpeta `presentation/api/`
2. Usar los mismos casos de uso
3. ¡Zero código duplicado!

### Añadir Nueva Persistencia (Base de Datos)
1. Implementar `QuizQuestionRepository` para BD
2. Cambiar la configuración en presentación
3. ¡El dominio y aplicación no cambian!

## 📦 Archivos Generados

La nueva arquitectura genera los mismos archivos que antes, pero con mejor organización:

- `preguntas/quiz_data.json` - Formato Pydantic estructurado
- `preguntas/quiz_data_legacy.json` - Formato de compatibilidad
- `preguntas/quiz_export_*.json/csv` - Exportaciones adicionales

## 🔄 Compatibilidad

El código legacy sigue funcionando, pero se recomienda migrar gradualmente a la nueva arquitectura para obtener todos los beneficios de Clean Architecture.

## 📚 Referencias

- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Dependency Inversion Principle](https://en.wikipedia.org/wiki/Dependency_inversion_principle)