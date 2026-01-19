# test_perfil.py

import os
import json

def test_archivo_perfil_existe():
    """Verifica que perfil.py existe y puede ser importado"""
    assert os.path.exists("perfil.py"), " perfil.py no existe"
    
    try:
        # Intentar importar las funciones principales
        from perfil import (
            cargar_perfiles,
            guardar_perfiles,
            ver_perfil,
            editar_perfil,
            actualizar_perfil
        )
        print(" perfil.py importado correctamente")
        return True
    except ImportError as e:
        print(f" Error importando perfil.py: {e}")
        return False

def test_funciones_existen():
    """Verifica que las funciones principales están definidas"""
    with open("perfil.py", "r", encoding="utf-8") as f:
        contenido = f.read()
    
    funciones = [
        "def cargar_perfiles():",
        "def guardar_perfiles(",
        "def ver_perfil():",
        "def editar_perfil():",
        "def actualizar_perfil():"
    ]
    
    for funcion in funciones:
        assert funcion in contenido, f" Falta función: {funcion}"
    
    print(" Todas las funciones principales existen")
    return True

def test_rutas_en_app():
    """Verifica que las rutas están en app.py"""
    assert os.path.exists("app.py"), " app.py no existe"
    
    with open("app.py", "r", encoding="utf-8") as f:
        contenido = f.read()
    
    rutas = [
        "@app.route('/perfil')",
        "@app.route('/editar-perfil'",
        "@app.route('/actualizar-perfil'"
    ]
    
    for ruta in rutas:
        assert ruta in contenido, f" Falta ruta: {ruta}"
    
    print(" Todas las rutas están en app.py")
    return True

def test_menu_tiene_perfil():
    """Verifica que el menú tiene enlace a perfil"""
    assert os.path.exists("menu.py"), " menu.py no existe"
    
    with open("menu.py", "r", encoding="utf-8") as f:
        contenido = f.read()
    
    # Buscar el enlace al perfil
    if '"Mi Perfil"' in contenido and '"/perfil"' in contenido:
        print(" Menú tiene enlace 'Mi Perfil'")
        return True
    elif 'perfil' in contenido.lower():
        print("  Menú hace referencia a perfil (revisar texto exacto)")
        return True
    else:
        print(" Menú no tiene enlace claro al perfil")
        return False

def test_estructura_perfiles_json():
    """Explica cómo será perfiles.json"""
    print("\n perfiles.json se creará automáticamente con esta estructura:")
    print("""
  {
    "nombre_usuario": {
      "nombre": "Ejemplo",
      "apellidos": "Apellidos",
      "email": "email@ejemplo.com",
      "telefono": "123456789",
      "direccion": "Dirección"
    }
  }
  """)
    
    if os.path.exists("perfiles.json"):
        print(" perfiles.json ya existe")
        # Verificar que tiene formato JSON válido
        try:
            with open("perfiles.json", "r", encoding="utf-8") as f:
                json.load(f)
            print(" perfiles.json tiene formato JSON válido")
        except json.JSONDecodeError:
            print(" perfiles.json no tiene formato JSON válido")
    else:
        print("  perfiles.json no existe aún (se creará automáticamente)")
    
    return True

def run_all_tests():
    """Ejecuta todos los tests"""
    print("EJECUTANDO TESTS PARA LA SECCIÓN DE PERFIL")
    print("=" * 50)
    
    tests = [
        ("Archivo perfil.py existe", test_archivo_perfil_existe),
        ("Funciones definidas", test_funciones_existen),
        ("Rutas en app.py", test_rutas_en_app),
        ("Menú actualizado", test_menu_tiene_perfil),
        ("Estructura perfiles.json", test_estructura_perfiles_json)
    ]
    
    resultados = []
    
    for nombre_test, funcion_test in tests:
        print(f"\n🔍 {nombre_test}:")
        try:
            if funcion_test():
                resultados.append((nombre_test))
            else:
                resultados.append(( nombre_test))
        except AssertionError as e:
            print(f"  {e}")
            resultados.append((nombre_test))
        except Exception as e:
            print(f"   Error inesperado: {e}")
            resultados.append(( nombre_test))
    
    print("\n" + "=" * 50)
    print(" RESULTADOS:")
    
    exitos = sum(1 for resultado in resultados if resultado[0] == "✅")
    total = len(resultados)
    
    for simbolo, nombre in resultados:
        print(f"  {simbolo} {nombre}")
    
    print(f"\n {exitos}/{total} tests pasaron")
    
    if exitos == total:
        print("\n ¡TODO CORRECTO! La sección de perfil está lista.")
        print("   Ejecuta la app y prueba en http://127.0.0.1:5000/perfil")
    else:
        print(f"\n  {total - exitos} test(s) fallaron. Revisa los errores.")
    
    print("=" * 50)

if __name__ == "__main__":
    run_all_tests()