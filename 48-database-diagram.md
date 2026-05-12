## 4.8. Database Design

El diseño de base de datos de SIRAN sigue los principios de Domain-Driven Design, organizando el esquema relacional en función de los Bounded Contexts identificados durante el proceso de Event Storming. Cada contexto acotado agrupa las entidades y relaciones que le son propias, garantizando una separación clara de responsabilidades y facilitando la escalabilidad y el mantenimiento del sistema.

El motor de base de datos seleccionado es **MySQL**, por su amplia compatibilidad con el ecosistema ASP.NET Core, su soporte a constraints relacionales (primary keys, foreign keys, índices únicos) y su robustez en entornos de producción orientados a datos clínicos. La nomenclatura de tablas y columnas sigue la convención **snake_case** en inglés, conforme a las convenciones de código establecidas para el proyecto.

Se priorizó la integridad referencial mediante el uso de claves foráneas explícitas entre tablas relacionadas, y se definieron índices únicos en campos de identificación natural (como `email` en usuarios) para evitar duplicados a nivel de base de datos. Los campos de auditoría (`created_at`, `updated_at`) se incluyeron en las tablas principales para mantener trazabilidad sobre la creación y modificación de registros.

A continuación se presenta el Database Diagram por cada Bounded Context identificado en la arquitectura del sistema.

---

### 4.8.1. Database Diagrams

#### Bounded Context: Identity and Access Management (IAM)

Este contexto gestiona la autenticación y el control de acceso. Las tablas `users`, `roles` y `user_roles` conforman el núcleo del módulo, permitiendo la asignación de múltiples roles a cada usuario mediante una tabla de relación. La tabla `refresh_tokens` soporta la persistencia de sesiones mediante tokens JWT de refresco.

```
+------------------+         +------------------+        +------------------+
|      users       |         |   user_roles     |        |      roles       |
+------------------+         +------------------+        +------------------+
| PK id            |<---+    | PK id            |    +-->| PK id            |
|    email         |    +----| FK user_id       |    |   |    name          |
|    password_hash |         | FK role_id       |----+   |    description   |
|    is_active     |         |    assigned_at   |        |    created_at    |
|    created_at    |         +------------------+        +------------------+
|    updated_at    |
+------------------+
        |
        | 1
        |
        * 
+----------------------+
|   refresh_tokens     |
+----------------------+
| PK id                |
| FK user_id           |
|    token             |
|    expires_at        |
|    revoked           |
|    created_at        |
+----------------------+
```

**Descripción de tablas:**

| Tabla | Descripción |
|---|---|
| `users` | Almacena las credenciales y estado de cada usuario registrado en el sistema. |
| `roles` | Define los roles disponibles: `parent` (padre) y `neonatologist` (neonatólogo). |
| `user_roles` | Tabla de relación N:M entre usuarios y roles. |
| `refresh_tokens` | Registra los tokens de refresco emitidos para mantener sesiones activas de forma segura. |

---

#### Bounded Context: Subscriptions and Payment Management

Gestiona los planes de suscripción disponibles y el estado de la suscripción de cada usuario. La tabla `subscriptions` registra el plan activo del usuario, su fecha de inicio, vencimiento y estado. La tabla `payment_transactions` mantiene el historial de pagos procesados.

```
+------------------+         +----------------------+        +------------------+
|   subscription   |         | payment_transactions |        |      plans       |
|     _plans       |         +----------------------+        +------------------+
+------------------+         | PK id                |        | PK id            |
| PK id            |<---+    | FK subscription_id   |        |    name          |
|    name          |    |    | FK plan_id           |----+   |    price         |
|    description   |    |    |    amount            |    +-->|    duration_days |
|    price         |    |    |    status            |        |    features      |
|    duration_days |    |    |    processed_at      |        |    created_at    |
|    created_at    |    |    +----------------------+        +------------------+
+------------------+    |
                        |
+----------------------+|
|    subscriptions     ||
+----------------------+|
| PK id                ||
| FK user_id           |<-- (FK to users.id in IAM)
| FK plan_id           |----+
|    status            |
|    started_at        |
|    expires_at        |
|    created_at        |
|    updated_at        |
+----------------------+
```

**Descripción de tablas:**

| Tabla | Descripción |
|---|---|
| `plans` | Catálogo de planes disponibles (básico, premium, profesional) con precios y duración. |
| `subscriptions` | Registro de la suscripción activa de cada usuario, incluyendo fechas y estado. |
| `payment_transactions` | Historial de transacciones de pago asociadas a cada suscripción. |

---

#### Bounded Context: Profiles and Preferences Management

Almacena los perfiles personales de cada usuario según su rol, así como las preferencias de notificación y parámetros clínicos configurados para el seguimiento del neonato.

```
+------------------+         +----------------------+
|  parent_profiles |         | neonatologist_       |
+------------------+         | profiles             |
| PK id            |         +----------------------+
| FK user_id       |<--+     | PK id                |
|    full_name     |   |     | FK user_id           |<-- (FK to users.id in IAM)
|    phone         |   |     |    full_name         |
|    address       |   |     |    license_number    |
|    created_at    |   |     |    specialty         |
|    updated_at    |   |     |    hospital          |
+------------------+   |     |    created_at        |
                       |     |    updated_at        |
                       |     +----------------------+
                       |
              (FK to users.id in IAM)

+----------------------------+
|   notification_preferences |
+----------------------------+
| PK id                      |
| FK user_id                 |<-- (FK to users.id in IAM)
|    email_alerts            |
|    push_alerts             |
|    sms_alerts              |
|    alert_threshold_level   |
|    updated_at              |
+----------------------------+
```

**Descripción de tablas:**

| Tabla | Descripción |
|---|---|
| `parent_profiles` | Datos personales del padre o tutor del neonato registrado. |
| `neonatologist_profiles` | Datos profesionales del médico neonatólogo, incluyendo matrícula y especialidad. |
| `notification_preferences` | Configuración de canales y niveles de alerta preferidos por el usuario. |

---

#### Bounded Context: Resource and Asset Management

Gestiona los registros clínicos del neonato: datos de identificación, registros de salud con parámetros medidos y las observaciones adicionales ingresadas por padres o profesionales.

```
+------------------+         +----------------------+       +----------------------+
|    neonates      |         |   health_records     |       |    observations      |
+------------------+         +----------------------+       +----------------------+
| PK id            |<---+    | PK id                | <--+  | PK id                |
| FK parent_id     |    +----| FK neonate_id        |    |  | FK neonate_id        |
|    full_name     |         |    recorded_at       |    |  | FK user_id           |
|    birth_date    |         |    weight_kg         |    |  |    content           |
|    birth_weight  |         |    temperature_c     |    |  |    recorded_at       |
|    gestational   |         |    feeding_ml        |    +--| FK health_record_id  |
|    _weeks        |         |    skin_color        |       |    created_at        |
|    gender        |         |    respiratory_rate  |       +----------------------+
|    created_at    |         |    heart_rate        |
+------------------+         |    notes             |
                             |    created_at        |
                             +----------------------+
```

**Descripción de tablas:**

| Tabla | Descripción |
|---|---|
| `neonates` | Información de identificación del recién nacido: nombre, fecha de nacimiento, semanas de gestación, sexo y peso al nacer. |
| `health_records` | Registro de los parámetros clínicos medidos en cada sesión: temperatura, peso, alimentación, frecuencia respiratoria y cardíaca, coloración de piel. |
| `observations` | Anotaciones adicionales vinculadas a un neonato o a un registro de salud específico, ingresadas por padres o neonatólogos. |

---

#### Bounded Context: Service Execution and Monitoring

Constituye el núcleo operativo del sistema. Las tablas de este contexto almacenan las alertas generadas automáticamente al detectar valores fuera del rango clínico esperado, así como el registro de eventos de validación de parámetros.

```
+------------------+         +----------------------+
|     alerts       |         | validation_events    |
+------------------+         +----------------------+
| PK id            |         | PK id                |
| FK neonate_id    |<--+     | FK health_record_id  |
| FK health_       |   |     | FK alert_id          |----+
|    record_id     |   |     |    parameter_name    |    |
|    alert_type    |   |     |    measured_value    |    |
|    severity      |   |     |    expected_min      |    |
|    description   |   |     |    expected_max      |    |
|    status        |   +---->|    validation_result |    |
|    generated_at  |         |    validated_at      |    |
|    resolved_at   |<--------+---------------------+    |
+------------------+                                    |
                                                        |
                                     (FK to alerts.id) -+
```

**Descripción de tablas:**

| Tabla | Descripción |
|---|---|
| `alerts` | Almacena las alertas generadas por el sistema al detectar parámetros fuera de rango. Incluye tipo, nivel de severidad, estado (activa/resuelta) y timestamps. |
| `validation_events` | Registro de cada validación ejecutada sobre un parámetro clínico, detallando el valor medido, el rango esperado y el resultado de la validación. |

---

#### Bounded Context: Dashboard and Analytics

Persiste los reportes generados para padres y neonatólogos, almacenando resúmenes estadísticos y referencias a los datos que los originaron, para optimizar la carga de las vistas analíticas.

```
+----------------------+        +----------------------+
|       reports        |        |  report_snapshots    |
+----------------------+        +----------------------+
| PK id                |<---+   | PK id                |
| FK neonate_id        |    +---| FK report_id         |
| FK generated_by_     |        |    parameter_name    |
|    user_id           |        |    min_value         |
|    report_type       |        |    max_value         |
|    date_from         |        |    avg_value         |
|    date_to           |        |    sample_count      |
|    format            |        |    computed_at       |
|    created_at        |        +----------------------+
+----------------------+
```

**Descripción de tablas:**

| Tabla | Descripción |
|---|---|
| `reports` | Cabecera del reporte generado: neonato evaluado, usuario que lo solicitó, rango de fechas, tipo (resumen o clínico) y formato. |
| `report_snapshots` | Estadísticas precalculadas (mínimo, máximo, promedio) por parámetro clínico, para agilizar la visualización sin recalcular sobre `health_records`. |

---

#### Bounded Context: Loyalty and Engagement

Gestiona el contenido informativo de la plataforma (Landing Page), incluyendo testimonios de usuarios y preguntas frecuentes, elementos que fortalecen la confianza y captación de nuevos usuarios.

```
+----------------------+        +----------------------+
|     testimonials     |        |       faqs           |
+----------------------+        +----------------------+
| PK id                |        | PK id                |
| FK user_id           |        |    question          |
|    content           |        |    answer            |
|    rating            |        |    category          |
|    is_published      |        |    is_active         |
|    published_at      |        |    created_at        |
|    created_at        |        |    updated_at        |
+----------------------+        +----------------------+
```

**Descripción de tablas:**

| Tabla | Descripción |
|---|---|
| `testimonials` | Almacena los testimonios de usuarios publicados en el Landing Page, con su calificación y estado de publicación. |
| `faqs` | Preguntas frecuentes organizadas por categoría que se muestran en la sección informativa de la plataforma. |

---

#### Vista consolidada de relaciones entre Bounded Contexts

Las relaciones entre contextos se resuelven mediante **claves foráneas lógicas** (referencias al `id` de `users` del contexto IAM), siguiendo el principio de que cada Bounded Context es autónomo en su propio esquema pero puede hacer referencia a identificadores compartidos. En un despliegue con base de datos única (monolito modular), estas referencias se implementan como foreign keys explícitas. En un despliegue distribuido (microservicios), se gestionan mediante eventos de dominio y consistencia eventual.

| Contexto origen | Campo de enlace | Contexto destino |
|---|---|---|
| Profiles & Preferences | `user_id` | IAM → `users.id` |
| Subscriptions & Payments | `user_id` | IAM → `users.id` |
| Resource & Asset Management | `parent_id` en `neonates` | Profiles → `parent_profiles.id` |
| Service Execution & Monitoring | `neonate_id`, `health_record_id` | Resource & Asset → tablas correspondientes |
| Dashboard & Analytics | `neonate_id`, `generated_by_user_id` | IAM y Resource & Asset |
| Loyalty & Engagement | `user_id` en `testimonials` | IAM → `users.id` |

> **Nota:** Los diagramas físicos completos con notación entidad-relación han sido elaborados en la herramienta **Vertabelo** / **LucidChart** y se encuentran disponibles en el repositorio del proyecto bajo la ruta `assets/database/`. Las imágenes exportadas de dichas herramientas deben incluirse en esta sección una vez finalizado el diseño definitivo de cada bounded context.