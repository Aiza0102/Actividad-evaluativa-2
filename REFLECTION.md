
# REFLECTION.md

## Documentación de problemas y soluciones

### 1. Authentication (auth.py)

#### Problemas identificados:
- **Hardcoded Token**: El token de autenticación estaba hardcodeado en el código, lo que no es seguro ni flexible.
- **No validación de campos**: No había validación para la presencia de los campos `username` y `password`.
- **Falta de variables de entorno**: No se estaban utilizando variables de entorno para almacenar datos sensibles, como el token de autenticación.
- **Código redundante**: El código de validación de usuario y token era repetitivo en varias partes.

#### Soluciones aplicadas:
- **Uso de variables de entorno**: Se ha introducido la librería `dotenv` para cargar el token de autenticación desde un archivo `.env`.
- **Función de validación reutilizable**: Se ha creado una función `authenticate_user` que encapsula la lógica de validación del usuario.
- **Validación de campos**: Ahora se valida si los campos `username` y `password` están presentes en la solicitud.
- **Mejor manejo de respuestas**: Se implementaron respuestas con el formato `jsonify`, lo que facilita el trabajo con respuestas JSON y permite un manejo más limpio de los errores.

#### Supuestos y decisiones de diseño:
- **Uso de token predefinido**: A pesar de usar un token predefinido en el código de ejemplo, es posible implementar una autenticación más robusta, como JWT, si fuera necesario en el futuro.

---

### 2. Categories (categories.py)

#### Problemas identificados:
- **Hardcoded Token**: El token de autorización estaba también hardcodeado en el código.
- **Duplicación de validaciones**: Las validaciones de token se repetían en cada endpoint.
- **Falta de manejo adecuado de errores**: El manejo de errores para categorías no encontradas o faltantes no era claro.
- **No uso de variables de entorno**: Similar al archivo `auth.py`, no se estaban utilizando variables de entorno para almacenar datos sensibles.
  
#### Soluciones aplicadas:
- **Uso de variables de entorno**: Ahora se carga el token desde un archivo `.env`, lo que hace el código más seguro y flexible.
- **Mejor manejo de errores**: Se mejoraron los mensajes de error y las respuestas son más claras y consistentes con los estándares REST (por ejemplo, código 404 para no encontrado).
- **Modularización del código**: El código para la validación del token se extrajo en una función `is_valid_token` reutilizable.
- **Uso de `jsonify`**: Se comenzó a usar `jsonify` para devolver respuestas JSON estándar.

#### Supuestos y decisiones de diseño:
- **La categoría es única por nombre**: Se asumió que el nombre de la categoría es único, lo que evita duplicados, y no se implementó una validación más compleja.

---

### 3. Favorites (favorites.py)

#### Problemas identificados:
- **Hardcoded Token**: El token de autorización estaba también hardcodeado en el código.
- **Falta de validaciones**: No había validaciones adecuadas para los parámetros requeridos, como `user_id` y `product_id`.
- **No uso de variables de entorno**: El token no se cargaba desde un archivo `.env`, lo que era una mala práctica de seguridad.
- **Código repetido**: La validación del token se repetía en cada endpoint.

#### Soluciones aplicadas:
- **Uso de variables de entorno**: Ahora se carga el token de manera segura desde un archivo `.env`.
- **Validaciones de parámetros**: Se agregó una validación más rigurosa para los parámetros de entrada en los métodos `post` y `delete`.
- **Mejor manejo de errores**: Se mejoraron los mensajes de error para que sean más detallados y fáciles de entender.
- **Uso de `jsonify`**: Se adoptó `jsonify` para devolver respuestas JSON más limpias y consistentes.

#### Supuestos y decisiones de diseño:
- **El favorito debe ser único**: Se asumió que no debería haber duplicados de productos favoritos para un usuario.

---

### Diagramas y Material Visual

#### Diagrama de flujo de la autenticación:
```plaintext
1. El usuario envía un POST request con `username` y `password`.
2. Se valida la autenticación usando la función `authenticate_user`.
3. Si la autenticación es correcta, se genera un token y se devuelve.
4. Si no, se devuelve un error 401 Unauthorized.
```

#### Diagrama de flujo de la gestión de categorías:
```plaintext
1. El usuario envía un GET request para obtener categorías.
2. Se valida el token de autorización.
3. Si es válido, se devuelve la lista de categorías.
4. Si no es válido o falta el token, se devuelve un error 401 Unauthorized.
```

#### Diagrama de flujo de la creación de un nuevo recurso:
```plaintext
1. El usuario envía un POST request con los datos del nuevo recurso.
2. Se valida el token de autorización.
3. Se verifica si los datos del recurso son válidos.
4. Si los datos son válidos, se crea el nuevo recurso en la base de datos.
5. Si no, se devuelve un error 400 Bad Request.
6. Si la operación es exitosa, se devuelve un mensaje de éxito.
```

#### Diagrama de flujo de la eliminación de un recurso:
```plaintext
1. El usuario envía un DELETE request con el ID del recurso a eliminar.
2. Se valida el token de autorización.
3. Se verifica si el recurso existe.
4. Si el recurso existe, se elimina de la base de datos.
5. Si el recurso no existe, se devuelve un error 404 Not Found.
6. Si la operación es exitosa, se devuelve un mensaje de éxito.
```

#### Diagrama de flujo de la actualización de un recurso:
```plaintext
1. El usuario envía un PUT request con el ID del recurso y los nuevos datos.
2. Se valida el token de autorización.
3. Se verifica si el recurso existe.
4. Si el recurso existe, se actualizan los datos en la base de datos.
5. Si el recurso no existe, se devuelve un error 404 Not Found.
6. Si la operación es exitosa, se devuelve un mensaje de éxito.
```

#### Diagrama de flujo de la validación de datos de entrada:
```plaintext
1. El sistema recibe datos de entrada del usuario.
2. Se validan los datos en función de las reglas predefinidas.
3. Si los datos son válidos, se procesan.
4. Si los datos no son válidos, se devuelve un error 422 Unprocessable Entity con detalles sobre el error.
```

#### Diagrama de flujo de la generación de reportes:
```plaintext
1. El usuario solicita un reporte mediante un GET request.
2. Se valida el token de autorización.
3. Se procesan los datos para generar el reporte.
4. Si los datos son válidos, se genera y devuelve el reporte.
5. Si los datos no son válidos, se devuelve un error 400 Bad Request.
```

#### Diagrama de flujo del manejo de errores:
```plaintext
1. El sistema detecta un error durante la ejecución de una operación.
2. Se captura el error y se valida el tipo de error.
3. Se genera un mensaje de error adecuado para el tipo de error.
4. Se devuelve el mensaje de error con el código de estado HTTP correspondiente.
```

---

### Conclusión

Este proceso de refactorización permitió mejorar la seguridad al usar variables de entorno para almacenar el token de autenticación y al modularizar la lógica de validación del token. Además, se mejoró la estructura del código, facilitando su mantenimiento y extensión futura. Las validaciones de parámetros y el manejo de errores también se hicieron más robustos, lo que mejora la experiencia del desarrollador y del usuario final.
