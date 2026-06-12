# PROYECTO: Implementación Sistema de Notificaciones - FastAPI

## CONTEXTO DEL PROYECTO

Tengo un proyecto FastAPI con arquitectura limpia parcialmente implementado en `/Users/yilmar/sites/yilmardev/python/fastapi-pillar/`.

### Arquitectura Actual

- **Stack**: Python 3.13, FastAPI, SQLModel, PostgreSQL, Docker
- **Capas**: Routers → Services → Repositories → Models
- **Testing**: pytest con fixtures configurados en `tests/conftest.py`
- **Base de datos**: PostgreSQL con Alembic para migraciones

### Ya Implementado (30%)

- ✅ Modelo User con email, password hasheado (bcrypt)
- ✅ Endpoint POST `/users` (registro)
- ✅ Endpoint GET `/users` (listar usuarios)
- ✅ Estructura: `user.py` en models, schemas, routers, services, repositories
- ✅ Tests básicos configurados
- ✅ Docker Compose con PostgreSQL

### Estructura de Carpetas Existente

```
app/
├── models/          # SQLModel tables
├── schemas/         # Pydantic schemas (request/response)
├── routers/         # API endpoints
├── services/        # Business logic
├── respositories/   # Data access layer (typo en el nombre original)
├── core/           # security.py (bcrypt functions)
├── dependencies/   # FastAPI dependencies
├── db/             # database.py, seed.py
└── config/         # settings.py
```

---

## OBJETIVO

Completar el **Challenge de Sistema de Notificaciones** implementando:

1. **Autenticación JWT completa**
2. **CRUD de Notificaciones**
3. **Sistema de Canales de Envío extensible**
4. **Seguridad y Autorización**

---

## PLAN DE IMPLEMENTACIÓN (4 STAGES)

### 📍 **INSTRUCCIONES DE USO**

Indica en qué **STAGE** estás para continuar desde ahí. Ejemplo: "Estoy en STAGE 2".

---

## STAGE 1: Sistema de Autenticación JWT

### Objetivo

Implementar login, generación de tokens JWT, y protección de endpoints.

### Tareas

#### 1.1 Instalar dependencias

```bash
# Agregar a pyproject.toml o requirements.txt
python-jose[cryptography]
passlib[bcrypt]  # ya existe bcrypt, verificar
```

#### 1.2 Configuración JWT

- **Archivo**: `app/core/security.py`
- **Agregar**:
  - `SECRET_KEY` en `app/config/settings.py` (leer de .env)
  - `ALGORITHM = "HS256"`
  - `ACCESS_TOKEN_EXPIRE_MINUTES = 30`
  - Función `create_access_token(data: dict) -> str`
  - Función `verify_token(token: str) -> dict`

#### 1.3 Schemas de autenticación

- **Archivo**: `app/schemas/auth.py` (CREAR)

```python
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str
```

#### 1.4 Servicio de autenticación

- **Opción A**: Agregar a `app/services/user_service.py`
  - Método `authenticate_user(email, password) -> User | None`
  - Usa `verify_password` de `core/security.py`

#### 1.5 Endpoint de login

- **Archivo**: `app/routers/auth.py` (CREAR) o agregar a `users.py`

```python
POST /auth/login
- Recibe UserLogin
- Valida credenciales
- Retorna Token con JWT
```

#### 1.6 Dependency para obtener usuario actual

- **Archivo**: `app/dependencies/user_dependencies.py`

```python
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    # Verificar token
    # Obtener user de DB
    # Lanzar HTTPException si inválido
```

#### 1.7 Tests

- **Archivo**: `tests/test_auth.py` (CREAR)
- Test login exitoso
- Test login con credenciales inválidas
- Test endpoint protegido sin token
- Test endpoint protegido con token válido

### ✅ Checkpoint Stage 1

- [ ] Login devuelve token JWT
- [ ] Token válido permite acceso a endpoints protegidos
- [ ] Token inválido retorna 401
- [ ] Tests pasan

---

## STAGE 2: Modelo y CRUD de Notificaciones

### Objetivo

Crear el modelo Notification y su CRUD completo.

### Tareas

#### 2.1 Modelo de Notification

- **Archivo**: `app/models/notification.py` (CREAR)

```python
class Notification(SQLModel, table=True):
    id: UUID (primary_key)
    title: str (max 200 chars)
    content: str
    channel: str (email, sms, push)
    user_id: UUID (ForeignKey to User.id)
    status: str (pending, sent, failed)
    created_at: datetime
    updated_at: datetime
    sent_at: datetime | None
```

#### 2.2 Relación en User

- **Archivo**: `app/models/user.py`
- Agregar: `notifications: list["Notification"] = Relationship(back_populates="user")`

#### 2.3 Migración Alembic

```bash
alembic revision --autogenerate -m "add notification table"
alembic upgrade head
```

#### 2.4 Schemas

- **Archivo**: `app/schemas/notification.py` (CREAR)

```python
class NotificationBase(BaseModel):
    title: str = Field(max_length=200)
    content: str
    channel: Literal["email", "sms", "push"]

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(BaseModel):
    title: str | None
    content: str | None
    channel: Literal["email", "sms", "push"] | None

class NotificationRead(NotificationBase):
    id: UUID
    user_id: UUID
    status: str
    created_at: datetime
    sent_at: datetime | None
```

#### 2.5 Repository

- **Archivo**: `app/respositories/notification_repository.py` (CREAR)

```python
class NotificationRepository:
    def create(session, notification_data, user_id) -> Notification
    def get_by_id(session, notification_id, user_id) -> Notification | None
    def get_all_by_user(session, user_id, limit, offset) -> Sequence[Notification]
    def update(session, notification_id, update_data, user_id) -> Notification
    def delete(session, notification_id, user_id) -> bool
```

#### 2.6 Service

- **Archivo**: `app/services/notification_service.py` (CREAR)
- Inyectar repository
- Validaciones de negocio
- Llamar al sistema de envío (Stage 3)

#### 2.7 Router

- **Archivo**: `app/routers/notifications.py` (CREAR)

```python
POST /notifications (crear + enviar)
GET /notifications (listar propias)
GET /notifications/{id} (obtener una)
PATCH /notifications/{id} (modificar)
DELETE /notifications/{id} (eliminar)

# Todos protegidos con Depends(get_current_user)
```

#### 2.8 Registrar router

- **Archivo**: `app/main.py`

```python
from app.routers.notifications import router as notifications_router
app.include_router(notifications_router)
```

#### 2.9 Tests

- **Archivo**: `tests/test_notifications.py` (CREAR)
- Test crear notificación
- Test listar solo propias notificaciones
- Test modificar notificación
- Test eliminar notificación
- Test intentar acceder a notificación de otro usuario (debe fallar)

### ✅ Checkpoint Stage 2

- [ ] Modelo Notification en DB
- [ ] CRUD completo funcionando
- [ ] Usuarios solo ven/editan sus notificaciones
- [ ] Tests pasan

---

## STAGE 3: Sistema de Canales de Envío

### Objetivo

Implementar arquitectura extensible para canales usando Strategy Pattern.

### Tareas

#### 3.1 Interface de Canal

- **Archivo**: `app/channels/__init__.py` (CREAR CARPETA)
- **Archivo**: `app/channels/base.py` (CREAR)

```python
from abc import ABC, abstractmethod

class NotificationChannel(ABC):
    @abstractmethod
    def send(self, notification: Notification, user: User) -> dict:
        """
        Returns dict with:
        - success: bool
        - message: str
        - metadata: dict (optional)
        """
        pass

    @abstractmethod
    def validate(self, notification: Notification, user: User) -> bool:
        pass
```

#### 3.2 Implementar canales

- **Email**: `app/channels/email_channel.py`
  - Validar formato email usuario
  - Generar "template" (mock)
  - Registrar envío
  - Retornar success + metadata

- **SMS**: `app/channels/sms_channel.py`
  - Validar content <= 160 chars
  - Mock envío a número (user.phone o mock)
  - Registrar número y fecha

- **Push**: `app/channels/push_channel.py`
  - Validar token dispositivo (mock)
  - Formatear payload JSON
  - Registrar estado envío

#### 3.3 Factory de Canales

- **Archivo**: `app/channels/factory.py`

```python
def get_channel(channel_type: str) -> NotificationChannel:
    channels = {
        "email": EmailChannel(),
        "sms": SMSChannel(),
        "push": PushChannel(),
    }
    if channel_type not in channels:
        raise ValueError(f"Unknown channel: {channel_type}")
    return channels[channel_type]
```

#### 3.4 Integrar en Service

- **Archivo**: `app/services/notification_service.py`

```python
def create_notification(self, data, user):
    # 1. Crear notification en DB
    notification = self.repo.create(...)

    # 2. Enviar por canal
    channel = get_channel(notification.channel)
    result = channel.send(notification, user)

    # 3. Actualizar status
    notification.status = "sent" if result["success"] else "failed"
    notification.sent_at = datetime.now() if result["success"] else None
    # Actualizar en DB

    return notification
```

#### 3.5 Tests

- **Archivo**: `tests/test_channels.py` (CREAR)
- Test EmailChannel.send()
- Test SMSChannel.validate() falla si > 160 chars
- Test PushChannel mock
- Test Factory retorna canal correcto
- Test crear notificación dispara envío

### ✅ Checkpoint Stage 3

- [ ] 3 canales implementados
- [ ] Factory permite agregar nuevos canales fácilmente
- [ ] Crear notificación dispara envío automático
- [ ] Status se actualiza según resultado
- [ ] Tests pasan

---

## STAGE 4: Seguridad y Refinamientos

### Objetivo

Asegurar endpoints, validaciones finales, documentación.

### Tareas

#### 4.1 Proteger todos los endpoints de notificaciones

- Verificar que todos usen `Depends(get_current_user)`

#### 4.2 Validación de ownership

- En repository o service, verificar que `notification.user_id == current_user.id`

#### 4.3 Enum para canales

- **Archivo**: `app/models/notification.py`

```python
from enum import Enum

class ChannelType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
```

#### 4.4 Variables de entorno

- Documentar en `.env.example`:

```
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### 4.5 README actualizado

- Agregar sección de Autenticación
- Documentar endpoints de notificaciones
- Ejemplos de uso con curl

#### 4.6 Tests de integración

- **Archivo**: `tests/test_integration.py` (CREAR)
- Flujo completo: register → login → create notification → verify sent

#### 4.7 Manejo de errores

- Verificar que todos los errores retornan status codes apropiados
- 401 para no autenticado
- 403 para no autorizado (notificación de otro user)
- 404 para no encontrado
- 422 para validación

### ✅ Checkpoint Stage 4

- [ ] Todos los endpoints protegidos
- [ ] No se puede acceder a datos de otros usuarios
- [ ] Documentación actualizada
- [ ] Tests de integración completos
- [ ] Manejo de errores robusto

---

## CONSIDERACIONES TÉCNICAS

### Patrón de Arquitectura a Seguir

Mantén la estructura existente:

```
Router (recibe request)
  → Service (lógica de negocio)
    → Repository (acceso a datos)
      → Model (SQLModel)
```

### Testing

- Usa fixtures de `conftest.py` existentes
- Usa `db_session` para tests con DB
- Usa `client` para tests de endpoints
- Marca tests: `@pytest.mark.integration`, `@pytest.mark.unit`

### Base de Datos

- Genera migración Alembic para cada cambio en models
- Usa `alembic upgrade head` antes de tests

### Docker

- Ejecuta tests en Docker: `docker compose run test`
- Usa base de datos de test separada

---

## CÓMO USAR ESTE PROMPT

1. **Indica tu stage actual**: "Estoy en STAGE 2" o "Empezar desde STAGE 1"
2. **Pide implementación paso a paso**: "Implementa tarea 2.3"
3. **Verifica checkpoints**: Al terminar un stage, verifica todos los checkpoints
4. **Pide tests**: "Genera tests para el STAGE 2"

---

## ESTADO ACTUAL

**STAGE COMPLETADO**: Ninguno (proyecto base al 30%)

**PRÓXIMO**: Iniciar STAGE 1 - Sistema de Autenticación JWT

---

¿En qué STAGE quieres que empiece o continúe?
