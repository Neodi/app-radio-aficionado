"""
Archivo principal legacy - Mantiene compatibilidad mientras migras a Clean Architecture.
Para usar la nueva arquitectura, ejecuta: uv run main_clean.py
"""

def main():
    """Función principal legacy con mensaje informativo."""
    print("🔧 App Radio Aficionado - Scraper de Cuestionarios")
    print("=" * 50)
    print("")
    print("⚠️  NOTA: Estás usando el archivo legacy main.py")
    print("✨ Para usar la nueva Clean Architecture, ejecuta:")
    print("   uv run main_clean.py")
    print("")
    print("📚 La nueva arquitectura ofrece:")
    print("  • Mejor organización del código")
    print("  • Mayor facilidad de testing")
    print("  • Extensibilidad mejorada")
    print("  • Separación clara de responsabilidades")
    print("")
    print("📖 Lee CLEAN_ARCHITECTURE.md para más detalles")
    
    # Ofrecer ejecutar la nueva versión
    try:
        response = input("\n¿Quieres ejecutar la nueva Clean Architecture ahora? (s/n): ")
        if response.lower() in ['s', 'si', 'sí', 'yes', 'y']:
            print("\n🚀 Ejecutando Clean Architecture...")
            from src.presentation.cli.quiz_scraper_cli import main as clean_main
            clean_main()
        else:
            print("\n👍 ¡Perfecto! Ejecuta 'uv run main_clean.py' cuando estés listo")
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Prueba ejecutando directamente: uv run main_clean.py")


if __name__ == "__main__":
    main()
