import pytest
import json
import os
from unittest.mock import patch, mock_open
from Comentarios import app, cargar_usuarios, guardar_usuarios, cargar_historial, guardar_historial

@pytest.fixture
def client():
    """Crea un cliente de prueba para la aplicación Flask"""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_key'
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_usuarios():
    """Datos de prueba para usuarios.json"""
    return {
        "test_user": "test_password",
        "existing_user": "existing_pass"
    }

@pytest.fixture
def mock_historial():
    """Datos de prueba para historial.json"""
    return {
        "test_user": {
            "compras": [
                {
                    "fecha": "01/01/2024 10:00",
                    "estado": "finalizada",
                    "productos": [
                        {"nombre": "Producto Test", "precio": 10.0, "cantidad": 1}
                    ]
                }
            ],
            "notificaciones": [
                {
                    "texto": "¡Bienvenido!",
                    "link": "/catalogo",
                    "fecha": "01/01/2024 10:00",
                    "tipo": "info"
                }
            ]
        }
    }

class TestLogin:
    """Tests para el sistema de login"""
    
    def test_get_login_page(self, client):
        """Verifica que la página de login se carga correctamente"""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'usuario' in response.data or b'login' in response.data.lower()
    
    @patch('Comentarios.cargar_usuarios')
    def test_login_successful(self, mock_load, client, mock_usuarios):
        """Prueba un login exitoso"""
        mock_load.return_value = mock_usuarios
        
        response = client.post('/login', data={
            'usuario': 'test_user',
            'contrasenha': 'test_password'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        with client.session_transaction() as sess:
            assert sess.get('usuario') == 'test_user'
    
    @patch('Comentarios.cargar_usuarios')
    def test_login_wrong_password(self, mock_load, client, mock_usuarios):
        """Prueba login con contraseña incorrecta"""
        mock_load.return_value = mock_usuarios
        
        response = client.post('/login', data={
            'usuario': 'test_user',
            'contrasenha': 'wrong_password'
        })
        
        assert response.status_code == 200
        assert b'Credenciales incorrectas' in response.data or b'incorrectas' in response.data
    
    @patch('Comentarios.cargar_usuarios')
    def test_login_nonexistent_user(self, mock_load, client, mock_usuarios):
        """Prueba login con usuario inexistente"""
        mock_load.return_value = mock_usuarios
        
        response = client.post('/login', data={
            'usuario': 'nonexistent_user',
            'contrasenha': 'any_password'
        })
        
        assert response.status_code == 200
        assert b'no existe' in response.data or b'existe' in response.data


class TestRegistro:
    """Tests para el sistema de registro"""
    
    def test_get_registro_page(self, client):
        """Verifica que la página de registro se carga"""
        response = client.get('/registro')
        assert response.status_code == 200
    
    @patch('Comentarios.guardar_historial')
    @patch('Comentarios.guardar_usuarios')
    @patch('Comentarios.cargar_historial')
    @patch('Comentarios.cargar_usuarios')
    def test_registro_successful(self, mock_load_users, mock_load_hist, 
                                mock_save_users, mock_save_hist, 
                                client, mock_usuarios, mock_historial):
        """Prueba un registro exitoso"""
        mock_load_users.return_value = mock_usuarios.copy()
        mock_load_hist.return_value = mock_historial.copy()
        
        response = client.post('/registro', data={
            'usuario': 'new_user',
            'contrasena': 'new_password'
        })
        
        assert response.status_code == 200
        assert mock_save_users.called
        assert mock_save_hist.called
        assert b'registrado' in response.data or b'correctamente' in response.data
    
    @patch('Comentarios.cargar_usuarios')
    def test_registro_existing_user(self, mock_load, client, mock_usuarios):
        """Prueba registro con usuario existente"""
        mock_load.return_value = mock_usuarios
        
        response = client.post('/registro', data={
            'usuario': 'test_user',
            'contrasena': 'any_password'
        })
        
        assert response.status_code == 200
        assert b'ya existe' in response.data or b'existe' in response.data


class TestLogout:
    """Tests para el sistema de logout"""
    
    def test_logout(self, client):
        """Prueba que el logout elimina la sesión"""
        with client.session_transaction() as sess:
            sess['usuario'] = 'test_user'
        
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        
        with client.session_transaction() as sess:
            assert 'usuario' not in sess


class TestNotificaciones_registro:
    """Tests para el sistema de notificaciones estando registrado"""
    
    def test_notificaciones_sin_login(self, client):
        """Verifica la página de notificaciones sin login"""
        response = client.get('/notificaciones')
        assert response.status_code == 200
        assert b'Inicia' in response.data or b'sesi' in response.data
    
    @patch('Comentarios.cargar_historial')
    def test_notificaciones_logged_in(self, mock_load_hist, client, mock_historial):
        """Verifica la página de notificaciones con login"""
        mock_load_hist.return_value = mock_historial.copy()
        
        with client.session_transaction() as sess:
            sess['usuario'] = 'test_user'
        
        response = client.get('/notificaciones')
        assert response.status_code == 200
    
    def test_limpiar_notificaciones(self, client):
        """Prueba limpiar notificaciones"""
        with client.session_transaction() as sess:
            sess['usuario'] = 'test_user'
        
        response = client.post('/limpiar_notificaciones', follow_redirects=False)
        assert response.status_code == 302
        assert '/notificaciones' in response.location
    
    def test_generar_recomendaciones(self, client):
        """Prueba generar nuevas recomendaciones"""
        with client.session_transaction() as sess:
            sess['usuario'] = 'test_user'
        
        response = client.post('/generar_recomendaciones', follow_redirects=False)
        assert response.status_code == 302
        assert '/notificaciones' in response.location



if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])





