# Módulo: perfil.py
# Gestiona la visualización y edición del perfil de usuario
# Usa un archivo independiente perfiles.json para no interferir con el sistema actual

import json
import os
from flask import session, request, redirect, flash
from datetime import datetime

def cargar_perfiles():
    """
    Carga los perfiles desde perfiles.json
    Si el archivo no existe, retorna un diccionario vacío
    """
    try:
        with open("perfiles.json", "r", encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def guardar_perfiles(perfiles):
    """
    Guarda los perfiles en perfiles.json
    """
    with open('perfiles.json', 'w', encoding='utf-8') as archivo:
        json.dump(perfiles, archivo, ensure_ascii=False, indent=4)

def cargar_historial():
    """
    Función auxiliar para cargar historial (solo para estadísticas)
    NO modifica historial.json
    """
    try:
        with open("historial.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def ver_perfil():
    """
    Muestra la página de perfil del usuario
    """
    # Verificar si hay usuario en sesión
    if 'usuario' not in session:
        return redirect('/login')
    
    usuario = session['usuario']
    
    # Cargar datos del perfil desde perfiles.json
    perfiles = cargar_perfiles()
    perfil_data = perfiles.get(usuario, {})
    
    # Cargar historial solo para estadísticas (lectura, NO escritura)
    historial = cargar_historial()
    usuario_historial = historial.get(usuario, {})
    
    # Calcular estadísticas (solo lectura)
    total_compras = 0
    gasto_total = 0.0
    
    if "compras" in usuario_historial:
        compras = usuario_historial["compras"]
        for compra in compras:
            if compra.get("estado") == "finalizada":
                total_compras += 1
                for producto in compra.get("productos", []):
                    gasto_total += float(producto.get("precio", 0)) * producto.get("cantidad", 1)
    
    # Usar datos del perfil o valores por defecto
    nombre = perfil_data.get('nombre', 'No especificado')
    apellidos = perfil_data.get('apellidos', 'No especificados')
    email = perfil_data.get('email', 'No especificado')
    telefono = perfil_data.get('telefono', 'No especificado')
    direccion = perfil_data.get('direccion', 'No especificada')
    
    # Generar HTML
    html = f'''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mi Perfil - Chamba Store</title>
        <style>
            .perfil-container {{
                max-width: 800px;
                margin: 20px auto;
                padding: 30px;
                background: #ffffff;
                border-radius: 15px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }}
            .perfil-header {{
                text-align: center;
                margin-bottom: 30px;
                border-bottom: 2px solid #f0f0f0;
                padding-bottom: 20px;
            }}
            .perfil-info {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
                margin-bottom: 30px;
            }}
            .info-card {{
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid #007bff;
            }}
            .info-card h3 {{
                margin-top: 0;
                color: #333;
            }}
            .info-card p {{
                margin: 10px 0;
                color: #666;
            }}
            .estadisticas {{
                background: #f0f7ff;
                padding: 25px;
                border-radius: 10px;
                margin-bottom: 30px;
            }}
            .estadisticas h2 {{
                color: #0056b3;
                margin-top: 0;
            }}
            .estad-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
            }}
            .estad-item {{
                background: white;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
                box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            }}
            .estad-numero {{
                font-size: 24px;
                font-weight: bold;
                color: #007bff;
            }}
            .botones {{
                display: flex;
                justify-content: center;
                gap: 15px;
                margin-top: 30px;
            }}
            .btn {{
                display: inline-block;
                padding: 12px 25px;
                background: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
                transition: all 0.3s;
                border: none;
                cursor: pointer;
            }}
            .btn:hover {{
                background: #0056b3;
                transform: translateY(-2px);
            }}
            .btn-editar {{
                background: #28a745;
            }}
            .btn-editar:hover {{
                background: #218838;
            }}
            .btn-volver {{
                background: #6c757d;
            }}
            .btn-volver:hover {{
                background: #5a6268;
            }}
            .avatar {{
                width: 100px;
                height: 100px;
                background: #007bff;
                border-radius: 50%;
                margin: 0 auto 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 36px;
                font-weight: bold;
            }}
            .username {{
                font-size: 24px;
                font-weight: bold;
                color: #333;
            }}
            .rol {{
                color: #666;
                font-style: italic;
            }}
            .alert-success {{
                background: #d4edda;
                color: #155724;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
                border: 1px solid #c3e6cb;
            }}
        </style>
    </head>
    <body>
        <div class="perfil-container">
            <div class="perfil-header">
                <div class="avatar">
                    {usuario[0].upper() if usuario else "U"}
                </div>
                <div class="username">{usuario}</div>
                <div class="rol">Cliente de Chamba Store</div>
            </div>
            
            <div class="estadisticas">
                <h2>📊 Mis Estadísticas</h2>
                <div class="estad-grid">
                    <div class="estad-item">
                        <div class="estad-numero">{total_compras}</div>
                        <div>Compras realizadas</div>
                    </div>
                    <div class="estad-item">
                        <div class="estad-numero">{gasto_total:.2f}€</div>
                        <div>Total gastado</div>
                    </div>
                    <div class="estad-item">
                        <div class="estad-numero">{len(usuario_historial.get('notificaciones', []))}</div>
                        <div>Notificaciones</div>
                    </div>
                    <div class="estad-item">
                        <div class="estad-numero">{(gasto_total / total_compras) if total_compras > 0 else 0:.2f}€</div>
                        <div>Promedio por compra</div>
                    </div>
                </div>
            </div>
            
            <div class="perfil-info">
                <div class="info-card">
                    <h3>👤 Información Personal</h3>
                    <p><strong>Usuario:</strong> {usuario}</p>
                    <p><strong>Nombre:</strong> {nombre}</p>
                    <p><strong>Apellidos:</strong> {apellidos}</p>
                </div>
                
                <div class="info-card">
                    <h3>📞 Contacto</h3>
                    <p><strong>Email:</strong> {email}</p>
                    <p><strong>Teléfono:</strong> {telefono}</p>
                    <p><strong>Dirección:</strong> {direccion}</p>
                </div>
            </div>
            
            <div class="perfil-info">
                <div class="info-card">
                    <h3>📦 Actividad Reciente</h3>
                    <p><a href="/carrito">🛒 Ver mi carrito actual</a></p>
                    <p><a href="/notificaciones">🔔 Ver mis notificaciones ({len(usuario_historial.get('notificaciones', []))})</a></p>
                    <p><a href="/comentarios">💬 Mis comentarios</a></p>
                </div>
                
                <div class="info-card">
                    <h3>⚙️ Configuración</h3>
                    <p><a href="/editar-perfil">✏️ Editar información personal</a></p>
                    <p><a href="/" onclick="alert('Función en desarrollo')">🔐 Cambiar contraseña</a></p>
                    <p><a href="/logout">🚪 Cerrar sesión</a></p>
                </div>
            </div>
            
            <div class="botones">
                <a href="/editar-perfil" class="btn btn-editar">✏️ Editar Perfil</a>
                <a href="/" class="btn btn-volver">🏠 Volver al Inicio</a>
            </div>
        </div>
    </body>
    </html>
    '''
    
    return html

def editar_perfil():
    """
    Muestra formulario para editar perfil con datos actuales
    """
    if 'usuario' not in session:
        return redirect('/login')
    
    usuario = session['usuario']
    
    # Cargar datos actuales del perfil
    perfiles = cargar_perfiles()
    perfil_data = perfiles.get(usuario, {})
    
    # Generar formulario con los datos actuales
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Editar Perfil - Chamba Store</title>
        <style>
            .edit-container {{
                max-width: 600px;
                margin: 30px auto;
                padding: 30px;
                background: #ffffff;
                border-radius: 15px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }}
            .edit-header {{
                text-align: center;
                margin-bottom: 30px;
                border-bottom: 2px solid #f0f0f0;
                padding-bottom: 20px;
            }}
            .form-group {{
                margin-bottom: 25px;
            }}
            label {{
                display: block;
                margin-bottom: 8px;
                font-weight: bold;
                color: #333;
            }}
            input, textarea {{
                width: 100%;
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                box-sizing: border-box;
                font-size: 16px;
                transition: border-color 0.3s;
            }}
            input:focus, textarea:focus {{
                border-color: #007bff;
                outline: none;
            }}
            textarea {{
                height: 100px;
                resize: vertical;
            }}
            .btn-container {{
                display: flex;
                justify-content: center;
                gap: 15px;
                margin-top: 30px;
            }}
            .btn {{
                padding: 12px 30px;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s;
                font-size: 16px;
            }}
            .btn-guardar {{
                background: #28a745;
                color: white;
            }}
            .btn-guardar:hover {{
                background: #218838;
                transform: translateY(-2px);
            }}
            .btn-cancelar {{
                background: #6c757d;
                color: white;
                text-decoration: none;
                display: inline-flex;
                align-items: center;
                justify-content: center;
            }}
            .btn-cancelar:hover {{
                background: #5a6268;
                transform: translateY(-2px);
            }}
            .campo-info {{
                font-size: 14px;
                color: #666;
                margin-top: 5px;
                font-style: italic;
            }}
            .current-value {{
                font-size: 13px;
                color: #28a745;
                margin-top: 3px;
            }}
        </style>
    </head>
    <body>
        <div class="edit-container">
            <div class="edit-header">
                <h1>✏️ Editar Perfil</h1>
                <p>Actualiza tu información personal en Chamba Store</p>
            </div>
            
            <form method="POST" action="/actualizar-perfil">
                <div class="form-group">
                    <label for="nombre">Nombre:</label>
                    <input type="text" id="nombre" name="nombre" 
                           value="{perfil_data.get('nombre', '')}" 
                           placeholder="Tu nombre">
                    <div class="current-value">Actual: {perfil_data.get('nombre', 'No especificado')}</div>
                </div>
                
                <div class="form-group">
                    <label for="apellidos">Apellidos:</label>
                    <input type="text" id="apellidos" name="apellidos" 
                           value="{perfil_data.get('apellidos', '')}" 
                           placeholder="Tus apellidos">
                    <div class="current-value">Actual: {perfil_data.get('apellidos', 'No especificados')}</div>
                </div>
                
                <div class="form-group">
                    <label for="email">Email:</label>
                    <input type="email" id="email" name="email" 
                           value="{perfil_data.get('email', '')}" 
                           placeholder="tucorreo@ejemplo.com">
                    <div class="current-value">Actual: {perfil_data.get('email', 'No especificado')}</div>
                    <div class="campo-info">Para notificaciones y recuperación de cuenta</div>
                </div>
                
                <div class="form-group">
                    <label for="telefono">Teléfono:</label>
                    <input type="tel" id="telefono" name="telefono" 
                           value="{perfil_data.get('telefono', '')}" 
                           placeholder="+34 123 456 789">
                    <div class="current-value">Actual: {perfil_data.get('telefono', 'No especificado')}</div>
                </div>
                
                <div class="form-group">
                    <label for="direccion">Dirección:</label>
                    <textarea id="direccion" name="direccion" 
                              placeholder="Calle, número, ciudad, código postal">{perfil_data.get('direccion', '')}</textarea>
                    <div class="current-value">Actual: {perfil_data.get('direccion', 'No especificada')}</div>
                    <div class="campo-info">Para envío de productos</div>
                </div>
                
                <div class="btn-container">
                    <button type="submit" class="btn btn-guardar">💾 Guardar Cambios</button>
                    <a href="/perfil" class="btn btn-cancelar">❌ Cancelar</a>
                </div>
            </form>
        </div>
    </body>
    </html>
    '''
    return html

def actualizar_perfil():
    """
    Procesa el formulario de actualización de perfil
    y guarda los datos en perfiles.json (archivo NUEVO, independiente)
    """
    if 'usuario' not in session:
        return redirect('/login')
    
    usuario = session['usuario']
    
    # Obtener datos del formulario
    nombre = request.form.get('nombre', '').strip()
    apellidos = request.form.get('apellidos', '').strip()
    email = request.form.get('email', '').strip()
    telefono = request.form.get('telefono', '').strip()
    direccion = request.form.get('direccion', '').strip()
    
    # Cargar perfiles actuales
    perfiles = cargar_perfiles()
    
    # Crear o actualizar perfil del usuario
    if usuario not in perfiles:
        perfiles[usuario] = {}
    
    # Actualizar solo los campos que no estén vacíos
    if nombre:
        perfiles[usuario]['nombre'] = nombre
    if apellidos:
        perfiles[usuario]['apellidos'] = apellidos
    if email:
        perfiles[usuario]['email'] = email
    if telefono:
        perfiles[usuario]['telefono'] = telefono
    if direccion:
        perfiles[usuario]['direccion'] = direccion
    
    # Guardar perfiles actualizados
    guardar_perfiles(perfiles)
    
    # Mostrar mensaje de éxito y redirigir
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Perfil Actualizado - Chamba Store</title>
        <style>
            .success-container {{
                max-width: 600px;
                margin: 50px auto;
                padding: 40px;
                background: #ffffff;
                border-radius: 15px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                text-align: center;
            }}
            .success-icon {{
                font-size: 60px;
                color: #28a745;
                margin-bottom: 20px;
            }}
            .btn {{
                display: inline-block;
                padding: 12px 25px;
                margin: 10px;
                background: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
                transition: all 0.3s;
            }}
            .btn:hover {{
                background: #0056b3;
                transform: translateY(-2px);
            }}
            .btn-success {{
                background: #28a745;
            }}
            .btn-success:hover {{
                background: #218838;
            }}
            .profile-summary {{
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
                text-align: left;
            }}
        </style>
    </head>
    <body>
        <div class="success-container">
            <div class="success-icon">✅</div>
            <h1>¡Perfil Actualizado!</h1>
            <p>Tus datos han sido guardados correctamente en <strong>perfiles.json</strong>.</p>
            
            <div class="profile-summary">
                <h3>Resumen de tus datos:</h3>
                <p><strong>Nombre:</strong> {nombre if nombre else '(sin cambios)'}</p>
                <p><strong>Apellidos:</strong> {apellidos if apellidos else '(sin cambios)'}</p>
                <p><strong>Email:</strong> {email if email else '(sin cambios)'}</p>
                <p><strong>Teléfono:</strong> {telefono if telefono else '(sin cambios)'}</p>
                <p><strong>Dirección:</strong> {direccion if direccion else '(sin cambios)'}</p>
            </div>
            
            <p><em>Los datos se han guardado en un archivo independiente que no afecta al funcionamiento actual.</em></p>
            
            <div style="margin-top: 30px;">
                <a href="/perfil" class="btn btn-success">👤 Ver mi perfil actualizado</a>
                <a href="/editar-perfil" class="btn">✏️ Seguir editando</a>
                <a href="/" class="btn">🏠 Volver al inicio</a>
            </div>
        </div>
    </body>
    </html>
    '''
    
    return html