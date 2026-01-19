import pytest
import json
from unittest.mock import patch
from app import app, cargar_usuarios, guardar_usuarios, cargar_historial, guardar_historial

# --------------------------
# FIXTURES
# --------------------------
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
            "compras": [],
            "notificaciones": [],
            "preferencias": {"recibir_notificaciones": True}
        }
    }

# --------------------------
# LOGIN
# --------------------------
class TestLogin:
    """Tests para el sistema de login"""

    def test_get_login_page(self, client):
        response = client.get('/login')
        assert response.status_code == 200
        assert b'usuario' in response.data.lower()

    @patch('app.cargar_usuarios')
    def test_login_successful(self, mock_load, client, mock_usuarios):
        mock_load.return_value = mock_usuarios
        response = client.post('/login', data={
            'usuario': 'test_user',
            'contrasenha': 'test_password'
        }, follow_redirects=True)
        assert response.status_code == 200
        with client.session_transaction() as sess:
            assert sess.get('usuario') == 'test_user'

    @patch('app.cargar_usuarios')
    def test_login_wrong_password(self, mock_load, client, mock_usuarios):
        mock_load.return_value = mock_usuarios
        response = client.post('/login', data={
            'usuario': 'test_user',
            'contrasenha': 'wrong_password'
        })
        assert response.status_code == 200
        assert b'Credenciales incorrectas' in response.data or b'incorrectas' in response.data

    @patch('app.cargar_usuarios')
    def test_login_nonexistent_user(self, mock_load, client, mock_usuarios):
        mock_load.return_value = mock_usuarios
        response = client.post('/login', data={
            'usuario': 'nonexistent_user',
            'contrasenha': 'any_password'
        })
        assert response.status_code == 200
        assert b'no existe' in response.data or b'existe' in response.data

# --------------------------
# REGISTRO
# --------------------------
class TestRegistro:
    """Tests para el sistema de registro"""

    def test_get_registro_page(self, client):
        response = client.get('/registro')
        assert response.status_code == 200

    @patch('app.guardar_historial')
    @patch('app.guardar_usuarios')
    @patch('app.cargar_historial')
    @patch('app.cargar_usuarios')
    def test_registro_successful(self, mock_load_users, mock_load_hist, 
                                mock_save_users, mock_save_hist, 
                                client, mock_usuarios, mock_historial):
        """Prueba un registro exitoso con checkbox marcado"""
        mock_load_users.return_value = mock_usuarios.copy()
        mock_load_hist.return_value = mock_historial.copy()

        # Registro con checkbox marcado
        response = client.post('/registro', data={
            'usuario': 'new_user',
            'contrasena': 'new_password',
            'recibir_notificaciones': 'on'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert mock_save_users.called
        assert mock_save_hist.called

        # Comprobar que la preferencia se guardó
        historial = mock_load_hist.return_value
        assert 'new_user' in historial
        assert historial['new_user']['preferencias']['recibir_notificaciones'] is True

        # Registro sin marcar el checkbox
        response = client.post('/registro', data={
            'usuario': 'new_user2',
            'contrasena': 'new_password2'
            # no enviamos 'recibir_notificaciones'
        }, follow_redirects=True)
        historial = mock_load_hist.return_value
        assert 'new_user2' in historial
        assert historial['new_user2']['preferencias']['recibir_notificaciones'] is False

    @patch('app.cargar_usuarios')
    def test_registro_existing_user(self, mock_load, client, mock_usuarios):
        mock_load.return_value = mock_usuarios
        response = client.post('/registro', data={
            'usuario': 'test_user',
            'contrasena': 'any_password'
        })
        assert response.status_code == 200
        assert b'ya existe' in response.data or b'existe' in response.data

# --------------------------
# LOGOUT
# --------------------------
class TestLogout:
    """Tests para el sistema de logout"""

    def test_logout(self, client):
        with client.session_transaction() as sess:
            sess['usuario'] = 'test_user'
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        with client.session_transaction() as sess:
            assert 'usuario' not in sess

# --------------------------
# NOTIFICACIONES
# --------------------------
class TestNotificaciones:
    """Tests para el sistema de notificaciones según preferencias"""

    @patch('app.cargar_historial')
    def test_notificaciones_logged_in(self, mock_load_hist, client, mock_historial):
        mock_load_hist.return_value = mock_historial.copy()

        # Usuario logueado
        with client.session_transaction() as sess:
            sess['usuario'] = 'test_user'

        response = client.get('/notificaciones')
        assert response.status_code == 200
        # Verifica que la sección de notificaciones aparece
        assert b'Notificaciones Personalizadas' in response.data

    @patch('app.cargar_historial')
    def test_notificaciones_disabled(self, mock_load_hist, client, mock_historial):
        # Usuario con notificaciones desactivadas
        historial = mock_historial.copy()
        historial['test_user']['preferencias']['recibir_notificaciones'] = False
        mock_load_hist.return_value = historial

        with client.session_transaction() as sess:
            sess['usuario'] = 'test_user'

        response = client.get('/notificaciones')
        assert response.status_code == 200
        # Debe mostrar mensaje de que no hay notificaciones
        assert b'Te avisaremos' in response.data or b'ninguna' in response.data.lower()
