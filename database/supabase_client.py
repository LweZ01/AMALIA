import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any, Optional
import traceback
import os
from dotenv import load_dotenv

class SupabaseClient:
    """Cliente para interactuar con PostgreSQL/Supabase"""
    
    def __init__(self, database_url: str = None):
            """
            Inicializa el cliente de base de datos
            
            Args:
                database_url: URL de conexión a PostgreSQL (opcional, si no se proporciona
                            se construye desde las variables de entorno)
            """
            # Cargar variables de entorno
            load_dotenv()
            
            if database_url:
                self.database_url = database_url
            else:
                pass
                # Construir la URL de conexión desde las variables de entorno
                user = os.getenv("user")
                password = os.getenv("password")
                host = os.getenv("host")
                port = os.getenv("port")
                dbname = os.getenv("dbname")
                
                # Construir la URL de conexión para el pooler
                self.database_url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
                
            self.connection = None
    
    def connect(self):
        """Establece conexión con la base de datos"""
        try:
            if self.connection is None or self.connection.closed:
                self.connection = psycopg2.connect(
                    self.database_url,
                    sslmode='require',
                    cursor_factory=RealDictCursor
                )
                self.connection.autocommit = False
            return self.connection
        except Exception as e:
            raise
    
    def disconnect(self):
        """Cierra la conexión con la base de datos"""
        if self.connection and not self.connection.closed:
            self.connection.close()
    
    def test_connection(self) -> bool:
        """
        Prueba la conexión a la base de datos
        
        Returns:
            True si la conexión es exitosa, False en caso contrario
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT version()")
            version_info = cursor.fetchone()
            cursor.close()
            conn.commit()
            return True
        except Exception as e:
            pass
            # Verificar variables de entorno cargadas
            if self.connection and not self.connection.closed:
                self.connection.rollback()
            return False
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """
        Ejecuta una consulta SELECT y retorna los resultados
        
        Args:
            query: Consulta SQL
            params: Parámetros para la consulta
            
        Returns:
            Lista de diccionarios con los resultados
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            conn.commit()
            return results
        except Exception as e:
            if conn and not conn.closed:
                conn.rollback()
            return []
    
    def execute_update(self, query: str, params: tuple = None) -> bool:
        """
        Ejecuta una consulta INSERT, UPDATE o DELETE
        
        Args:
            query: Consulta SQL
            params: Parámetros para la consulta (opcional)
            
        Returns:
            True si la operación fue exitosa, False en caso contrario
        """
        conn = None
        try:
            conn = self.connect()
            cursor = conn.cursor()            
            cursor.execute(query, params)
            conn.commit()            
            cursor.close()
            return True
        except Exception as e:
            if conn and not conn.closed:
                conn.rollback()
            return False
    
    def execute_many(self, query: str, params_list: List[tuple]) -> bool:
        """
        Ejecuta múltiples operaciones INSERT/UPDATE
        
        Args:
            query: Consulta SQL
            params_list: Lista de tuplas con parámetros
            
        Returns:
            True si todas las operaciones fueron exitosas
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            if conn and not conn.closed:
                conn.rollback()
            return False
    
    # ==================== USUARIOS ====================
    
    def get_user_by_credentials(self, nombre_usuario: str, contraseña: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un usuario por nombre_usuario y contraseña
        
        Args:
            nombre_usuario: Nombre de usuario
            contraseña: Contraseña del usuario
            
        Returns:
            Diccionario con los datos del usuario o None
        """
        
        query = """
            SELECT id_usuario, nombre_usuario, contrasena, rol
            FROM usuario
            WHERE nombre_usuario = %s AND contrasena = %s
        """
        results = self.execute_query(query, (nombre_usuario, contraseña))
        
        if results:
            return results[0]
        else:
            pass
            # Debug: buscar solo por nombre de usuario
            debug_query = "SELECT id_usuario, nombre_usuario, contrasena, rol FROM usuario WHERE nombre_usuario = %s"
            debug_results = self.execute_query(debug_query, (nombre_usuario,))
            if debug_results:
                pass  # Usuario existe pero contraseña no coincide
            else:
                all_users = self.execute_query("SELECT nombre_usuario FROM usuario")
            return None

    # ==================== ESTUDIANTES ====================
    
    def get_all_estudiantes(self) -> List[Dict[str, Any]]:
        """Obtiene todos los estudiantes con información del grado"""
        query = """
            SELECT e.cedula, e.nombre, e.apellido, e.fecha_nacimiento,
                e.municipio, e.telefono, e.correo, e.id_grado,
                e.estado, e.pais, e.observacion, e.id_mencion,
                e.seccion,
                g.nombre_grado
            FROM estudiante e
            LEFT JOIN grado g ON e.id_grado = g.id_grado
            ORDER BY e.apellido, e.nombre
        """
        return self.execute_query(query)
    
    def get_estudiante_by_cedula(self, cedula: str) -> Optional[Dict[str, Any]]:
        """Obtiene un estudiante por su cédula"""
        query = """
            SELECT e.cedula, e.nombre, e.apellido, e.fecha_nacimiento,
                e.municipio, e.telefono, e.correo, e.id_grado,
                e.estado, e.pais, e.observacion, e.id_mencion,
                e.seccion,
                g.nombre_grado
            FROM estudiante e
            LEFT JOIN grado g ON e.id_grado = g.id_grado
            WHERE e.cedula = %s
        """
        results = self.execute_query(query, (cedula,))
        return results[0] if results else None

    def create_estudiante(self, cedula: str, nombre: str, apellido: str,
                        fecha_nacimiento: str, municipio: str = None,
                        telefono: str = None, correo: str = None,
                        id_grado: int = None, estado: str = None,
                        pais: str = None, observacion: str = None,
                        id_mencion: int = None, seccion: str = None) -> bool:
        """Crea un nuevo estudiante con los nuevos campos de la tabla"""
        try:
            pass
            
            # Validaciones básicas de seguridad
            if not cedula or not nombre or not apellido or not fecha_nacimiento:
                return False
            
            # Verificar que el grado existe (si se proporciona)
            if id_grado is not None:
                grado = self.get_grado_by_id(id_grado)
                if not grado:
                    return False
            
            query = """
                INSERT INTO estudiante 
                (cedula, nombre, apellido, fecha_nacimiento, municipio, 
                telefono, correo, id_grado, estado, pais, observacion, id_mencion, seccion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            result = self.execute_update(query, (cedula, nombre, apellido, fecha_nacimiento,
                                                municipio, telefono, correo, id_grado,
                                                estado, pais, observacion, id_mencion, seccion))
            
            if result:
                pass
                
                # ASIGNAR AUTOMÁTICAMENTE LAS ASIGNATURAS DEL GRADO (solo si tiene grado asignado)
                if id_grado is not None:
                    asignacion_result = self.asignar_asignaturas_estudiante(cedula, id_grado)
                    
                    if not asignacion_result:
                        pass  # Advertencia: problemas al asignar asignaturas
                else:
                    pass  # No se asignaron asignaturas
                
                return True
            else:
                return False
            
        except Exception as e:
            import traceback
            return False

    def update_estudiante(self, cedula: str, **kwargs) -> bool:
        """Actualiza un estudiante existente"""
        allowed_fields = ['nombre', 'apellido', 'fecha_nacimiento',
                        'municipio', 'telefono', 'correo', 'id_grado',
                        'estado', 'pais', 'observacion', 'id_mencion', 'seccion']
        
        fields = []
        values = []
        id_grado_nuevo = None
        id_grado_actual = None
        
        # Primero obtener el grado actual del estudiante
        if 'id_grado' in kwargs:
            query_grado_actual = "SELECT id_grado FROM estudiante WHERE cedula = %s"
            resultado = self.execute_query(query_grado_actual, (cedula,))
            if resultado:
                id_grado_actual = resultado[0]['id_grado']
        
        for key, value in kwargs.items():
            if key in allowed_fields:
                fields.append(f"{key} = %s")
                values.append(value)
                
                if key == 'id_grado':
                    id_grado_nuevo = value
        
        if not fields:
            return False
        
        values.append(cedula)
        query = f"UPDATE estudiante SET {', '.join(fields)} WHERE cedula = %s"
        result = self.execute_update(query, tuple(values))
        
        # Si se cambió de grado, procesar asignaturas según historial
        if result and id_grado_nuevo is not None and id_grado_actual is not None:
            pass
            
            # Usar la nueva función con lógica de aprobado/reprobado
            self.asignar_asignaturas_estudiante(cedula, id_grado_nuevo, id_grado_actual)
        
        return result

    def delete_estudiante(self, cedula: str) -> bool:
        """Elimina un estudiante por su cédula"""
        query = "DELETE FROM estudiante WHERE cedula = %s"
        return self.execute_update(query, (cedula,))

    def asignar_asignaturas_estudiante(self, cedula_estudiante: str, id_grado_nuevo: int, id_grado_actual: int = None) -> bool:
        """
        Asigna asignaturas a un estudiante basado en su historial académico y mención
        
        Args:
            cedula_estudiante: Cédula del estudiante
            id_grado_nuevo: ID del nuevo grado
            id_grado_actual: ID del grado actual (para determinar qué asignaturas pasar)
            
        Returns:
            True si se procesó correctamente
        """
        try:
            pass
            
            # ============ PASO 0: OBTENER MENCIÓN DEL ESTUDIANTE ============
            query_mencion = "SELECT id_mencion FROM estudiante WHERE cedula = %s"
            resultado_mencion = self.execute_query(query_mencion, (cedula_estudiante,))
            
            if not resultado_mencion:
                return False
            
            id_mencion = resultado_mencion[0].get('id_mencion')
            
            # ============ PASO 1: OBTENER HISTORIAL DEL ESTUDIANTE ============
            
            # Obtener todas las calificaciones del estudiante
            query_calificaciones = """
                SELECT c.codigo_asignatura, c.nota_final, a.nombre_asignatura, a.id_grado
                FROM calificacion c
                JOIN asignatura a ON c.codigo_asignatura = a.codigo
                WHERE c.cedula_estudiante = %s
            """
            calificaciones = self.execute_query(query_calificaciones, (cedula_estudiante,))
            
            # ============ PASO 2: GUARDAR EN HISTORIAL ACADÉMICO ============
            for cal in calificaciones:
                # VALIDAR: Solo guardar en historial si tiene nota_final
                if cal['nota_final'] is None:
                    continue
                
                # Determinar si está aprobado (nota >= 9.5)
                estado = "APROBADO" if cal['nota_final'] >= 9.5 else "REPROBADO"
                
                # Verificar si ya existe en historial
                query_check_historial = """
                    SELECT id_historial 
                    FROM historial_academico 
                    WHERE cedula_estudiante = %s AND codigo_asignatura = %s
                """
                existe = self.execute_query(query_check_historial, (cedula_estudiante, cal['codigo_asignatura']))
                
                if not existe:
                    pass
                    # Insertar en historial
                    query_insert_historial = """
                        INSERT INTO historial_academico 
                        (cedula_estudiante, codigo_asignatura, nombre_asignatura, 
                        id_grado, nota_final, estado, fecha_curso)
                        VALUES (%s, %s, %s, %s, %s, %s, CURRENT_DATE)
                    """
                    self.execute_update(query_insert_historial, (
                        cedula_estudiante, cal['codigo_asignatura'], cal['nombre_asignatura'],
                        cal['id_grado'], cal['nota_final'], estado
                    ))
                else:
                    pass
            
            # ============ PASO 3: ELIMINAR CALIFICACIONES ACTUALES ============
            query_delete_calificaciones = """
                DELETE FROM calificacion 
                WHERE cedula_estudiante = %s
            """
            self.execute_update(query_delete_calificaciones, (cedula_estudiante,))
            
            # ============ PASO 4: ASIGNAR NUEVAS ASIGNATURAS (CON FILTRO DE MENCIÓN) ============
            
            # Obtener asignaturas del nuevo grado filtradas por mención
            if id_mencion:
                pass
                # Si tiene mención, filtrar por mención
                query_asignaturas_nuevo = """
                    SELECT codigo, nombre_asignatura
                    FROM asignatura
                    WHERE id_grado = %s AND id_mencion = %s
                    ORDER BY nombre_asignatura
                """
                asignaturas_nuevo_grado = self.execute_query(query_asignaturas_nuevo, (id_grado_nuevo, id_mencion))
            else:
                pass
                # Si NO tiene mención, asignar todas
                query_asignaturas_nuevo = """
                    SELECT codigo, nombre_asignatura
                    FROM asignatura
                    WHERE id_grado = %s
                    ORDER BY nombre_asignatura
                """
                asignaturas_nuevo_grado = self.execute_query(query_asignaturas_nuevo, (id_grado_nuevo,))
            
            # ============ PASO 5: RE-ASIGNAR MATERIAS REPROBADAS ============
            if id_grado_actual is not None:
                pass
                
                # Obtener materias reprobadas del grado actual
                query_reprobadas = """
                    SELECT ha.codigo_asignatura, ha.nombre_asignatura
                    FROM historial_academico ha
                    WHERE ha.cedula_estudiante = %s 
                    AND ha.id_grado = %s 
                    AND ha.estado = 'REPROBADO'
                    ORDER BY ha.fecha_curso DESC
                """
                materias_reprobadas = self.execute_query(query_reprobadas, (cedula_estudiante, id_grado_actual))
                
                # Re-asignar materias reprobadas
                for materia in materias_reprobadas:
                    query_insert_reprobada = """
                        INSERT INTO calificacion 
                        (cedula_estudiante, codigo_asignatura, nota_1, ajuste_1, 
                        nota_2, ajuste_2, nota_3, ajuste_3, nota_final)
                        VALUES (%s, %s, NULL, 0.0, NULL, 0.0, NULL, 0.0, NULL)
                    """
                    self.execute_update(query_insert_reprobada, (
                        cedula_estudiante, materia['codigo_asignatura']
                    ))
            
            # ============ PASO 6: ASIGNAR MATERIAS DEL NUEVO GRADO ============
            
            # Verificar qué materias ya tiene asignadas (incluyendo reprobadas)
            query_asignadas = "SELECT codigo_asignatura FROM calificacion WHERE cedula_estudiante = %s"
            ya_asignadas = [a['codigo_asignatura'] for a in 
                        self.execute_query(query_asignadas, (cedula_estudiante,))]
            
            # Asignar solo las materias que no tiene
            asignaturas_a_asignar = []
            for asignatura in asignaturas_nuevo_grado:
                if asignatura['codigo'] not in ya_asignadas:
                    asignaturas_a_asignar.append((
                        cedula_estudiante, asignatura['codigo'], 
                        None, 0.0, None, 0.0, None, 0.0, None  # Notas en NULL para nuevas
                    ))
            
            if asignaturas_a_asignar:
                query_insert_nuevas = """
                    INSERT INTO calificacion 
                    (cedula_estudiante, codigo_asignatura, nota_1, ajuste_1, 
                    nota_2, ajuste_2, nota_3, ajuste_3, nota_final)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                success = self.execute_many(query_insert_nuevas, asignaturas_a_asignar)
                
                if success:
                    pass
                else:
                    pass
            else:
                pass
            
            return True
            
        except Exception as e:
            import traceback
            return False

    # ==================== DOCENTES ====================
    
    def get_all_docentes(self) -> List[Dict[str, Any]]:
        """Obtiene todos los docentes"""
        query = """
            SELECT d.cedula, d.nombre, d.apellido, d.correo,
                   d.telefono, d.especialidad
            FROM docente d
            ORDER BY d.apellido, d.nombre
        """
        return self.execute_query(query)
    
    def get_docente_by_cedula(self, cedula: str) -> Optional[Dict[str, Any]]:
        """Obtiene un docente por su cédula"""
        query = """
            SELECT d.cedula, d.nombre, d.apellido, d.correo,
                   d.telefono, d.especialidad
            FROM docente d
            WHERE d.cedula = %s
        """
        results = self.execute_query(query, (cedula,))
        return results[0] if results else None
    
    def create_docente(self, cedula: str, nombre: str, apellido: str, 
                    correo: str, telefono: str, especialidad: str) -> bool:
        """Crea un nuevo docente"""
        try:
            pass
            # Validaciones básicas de seguridad
            if not cedula or not nombre or not apellido:
                return False
            
            # Verificar que el docente no exista
            docente_existente = self.get_docente_by_cedula(cedula)
            if docente_existente:
                return False
            
            query = """
                INSERT INTO docente (cedula, nombre, apellido, correo, telefono, especialidad)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            return self.execute_update(query, (cedula, nombre, apellido, correo, telefono, especialidad))
        except Exception as e:
            return False
    
    def update_docente(self, cedula: str, **kwargs) -> bool:
        """Actualiza un docente existente"""
        allowed_fields = ['nombre', 'apellido', 'correo', 'telefono', 'especialidad']
        
        fields = []
        values = []
        for key, value in kwargs.items():
            if key in allowed_fields:
                fields.append(f"{key} = %s")
                values.append(value)
        
        if not fields:
            return False
        
        values.append(cedula)
        query = f"UPDATE docente SET {', '.join(fields)} WHERE cedula = %s"
        return self.execute_update(query, tuple(values))
    
    def delete_docente(self, cedula: str) -> bool:
        """Elimina un docente"""
        query = "DELETE FROM docente WHERE cedula = %s"
        return self.execute_update(query, (cedula,))
    
    # ==================== ASIGNATURAS ====================
    
    def get_all_asignaturas(self) -> List[Dict[str, Any]]:
        """Obtiene todas las asignaturas con información del grado y docente"""
        query = """
            SELECT a.codigo, a.nombre_asignatura, a.id_grado, a.cedula_docente, a.id_mencion,
                g.nombre_grado,
                d.nombre as docente_nombre, d.apellido as docente_apellido
            FROM asignatura a
            LEFT JOIN grado g ON a.id_grado = g.id_grado
            LEFT JOIN docente d ON a.cedula_docente = d.cedula
            ORDER BY a.nombre_asignatura
        """
        return self.execute_query(query)
    
    def get_asignatura_by_codigo(self, codigo: str) -> Optional[Dict[str, Any]]:
        """Obtiene una asignatura por su código"""
        query = """
            SELECT a.codigo, a.nombre_asignatura, a.id_grado,
                   g.nombre_grado, a.cedula_docente,
                   d.nombre as docente_nombre, d.apellido as docente_apellido
            FROM asignatura a
            LEFT JOIN grado g ON a.id_grado = g.id_grado
            LEFT JOIN docente d ON a.cedula_docente = d.cedula
            WHERE a.codigo = %s
        """
        results = self.execute_query(query, (codigo,))
        return results[0] if results else None
    
    def create_asignatura(self, codigo: str, nombre_asignatura: str,
                        id_grado: int, id_mencion: int, cedula_docente: str = None) -> bool:
        """Crea una nueva asignatura"""
        try:
            # Validaciones básicas de seguridad
            if not codigo or not nombre_asignatura or id_grado is None:
                return False
            
            # Verificar que el grado existe
            grado = self.get_grado_by_id(id_grado)
            if not grado:
                return False
            
            # Verificar que el docente existe SOLO si se proporciona cédula
            if cedula_docente and cedula_docente.strip():  # Si hay cédula y no está vacía
                docente = self.get_docente_by_cedula(cedula_docente)
                if not docente:
                    return False
            else:
                # Si no hay cédula o está vacía, establecer como None
                cedula_docente = None
            
            # Verificar que el código no exista
            asignatura_existente = self.get_asignatura_by_codigo(codigo)
            if asignatura_existente:
                return False
            
            # Insertar la asignatura
            query = """
                INSERT INTO asignatura (codigo, nombre_asignatura, id_grado, id_mencion, cedula_docente)
                VALUES (%s, %s, %s, %s, %s)
            """
            return self.execute_update(query, (codigo, nombre_asignatura, id_grado, id_mencion, cedula_docente))
        except Exception as e:
            return False
    
    def update_asignatura(self, codigo: str, **kwargs) -> bool:
        """Actualiza una asignatura existente"""
        allowed_fields = ['nombre_asignatura', 'id_grado', 'cedula_docente', 'id_mencion']
        
        fields = []
        values = []
        for key, value in kwargs.items():
            if key in allowed_fields:
                pass
                # Validar que el grado existe si se está actualizando
                if key == 'id_grado' and value is not None:
                    grado = self.get_grado_by_id(value)
                    if not grado:
                        return False
                
                # Validar que el docente existe si se está actualizando (solo si NO es None)
                if key == 'cedula_docente' and value is not None:
                    docente = self.get_docente_by_cedula(value)
                    if not docente:
                        return False
                
                # Agregar campo a la actualización (permite None para cedula_docente)
                fields.append(f"{key} = %s")
                values.append(value)
        
        if not fields:
            return False
        
        values.append(codigo)
        query = f"UPDATE asignatura SET {', '.join(fields)} WHERE codigo = %s"
        return self.execute_update(query, tuple(values))
    
    def delete_asignatura(self, codigo: str) -> bool:
        """Elimina una asignatura"""
        query = "DELETE FROM asignatura WHERE codigo = %s"
        return self.execute_update(query, (codigo,))
    
    # ==================== CALIFICACIONES ====================
    
    def get_calificaciones_by_estudiante(self, cedula_estudiante: str) -> List[Dict[str, Any]]:
        """Obtiene todas las calificaciones de un estudiante"""
        query = """
            SELECT c.codigo_calificacion, c.cedula_estudiante, c.codigo_asignatura, 
            c.nota_1, c.ajuste_1, 
            c.nota_2, c.ajuste_2, 
            c.nota_3, c.ajuste_3, 
            c.nota_final, a.nombre_asignatura, a.codigo
            FROM calificacion c
            JOIN asignatura a ON c.codigo_asignatura = a.codigo
            WHERE c.cedula_estudiante = %s
            ORDER BY a.nombre_asignatura
        """
        return self.execute_query(query, (cedula_estudiante,))   

    def get_all_calificaciones(self) -> List[Dict[str, Any]]:
        """Obtiene todas las calificaciones del sistema"""
        query = """
            SELECT c.codigo_calificacion, c.cedula_estudiante, c.codigo_asignatura,
                c.nota_1, c.ajuste_1, c.nota_2,
                c.ajuste_2, c.nota_3, c.ajuste_3,
                c.nota_final,
                e.nombre AS nombre_estudiante,
                e.apellido AS apellido_estudiante,
                a.nombre_asignatura,
                a.codigo
            FROM calificacion c
            JOIN estudiante e ON c.cedula_estudiante = e.cedula
            JOIN asignatura a ON c.codigo_asignatura = a.codigo
            ORDER BY e.apellido, e.nombre, a.nombre_asignatura
        """
        return self.execute_query(query)
    
    def create_calificacion(self, cedula_estudiante: str, codigo_asignatura: str,
                      nota_1: float = None, nota_2: float = None, nota_3: float = None,
                      ajuste_1: float = 0.0, ajuste_2: float = 0.0, ajuste_3: float = 0.0) -> bool:
        """Registra una nueva calificación"""
        # Calcular nota final
        notas = [n for n in [nota_1, nota_2, nota_3] if n is not None]
        nota_final = sum(notas) / len(notas) if notas else 0.0
        
        query = """
            INSERT INTO calificacion (cedula_estudiante, codigo_asignatura, nota_1, ajuste_1, nota_2, 
                                    ajuste_2, nota_3, ajuste_3, nota_final)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        return self.execute_update(query, (cedula_estudiante, codigo_asignatura, nota_1, ajuste_1, nota_2,
                                        ajuste_2, nota_3, ajuste_3, nota_final))
    
    def update_calificacion(self, codigo_calificacion: str, **kwargs) -> bool:
        """Actualiza una calificación existente"""
        allowed_fields = ['nota_1', 'ajuste_1', 'nota_2', 'ajuste_2', 'nota_3', 'ajuste_3', 'nota_final']
        
        fields = []
        values = []
        for key, value in kwargs.items():
            if key in allowed_fields:
                fields.append(f"{key} = %s")
                values.append(value)
        
        if not fields:
            return False
        
        # Recalcular nota final si se actualizan las notas
        if any(k in kwargs for k in ['nota_1', 'nota_2', 'nota_3']):
            pass
            # Obtener calificación actual
            query_current = "SELECT nota_1, nota_2, nota_3 FROM calificacion WHERE codigo_calificacion = %s"
            current = self.execute_query(query_current, (codigo_calificacion,))
            if current:
                nota_1 = kwargs.get('nota_1', current[0]['nota_1'])
                nota_2 = kwargs.get('nota_2', current[0]['nota_2'])
                nota_3 = kwargs.get('nota_3', current[0]['nota_3'])
                notas = [n for n in [nota_1, nota_2, nota_3] if n is not None]
                nota_final = sum(notas) / len(notas) if notas else None
                fields.append("nota_final = %s")
                values.append(nota_final)
        
        values.append(codigo_calificacion)
        query = f"UPDATE calificacion SET {', '.join(fields)} WHERE codigo_calificacion = %s"
        return self.execute_update(query, tuple(values))

    def delete_calificacion(self, codigo_calificacion: str) -> bool:
        """Elimina una calificación"""
        query = "DELETE FROM calificacion WHERE codigo_calificacion = %s"
        return self.execute_update(query, (codigo_calificacion,))
    
    # ==================== GRADOS ====================
    
    def get_all_grados(self) -> List[Dict[str, Any]]:
        """Obtiene todos los grados"""
        query = """
            SELECT id_grado, nombre_grado
            FROM grado
            ORDER BY nombre_grado
        """
        return self.execute_query(query)

    def get_grado_by_id(self, grado_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un grado por su ID"""
        query = """
            SELECT id_grado, nombre_grado
            FROM grado
            WHERE id_grado = %s
        """
        results = self.execute_query(query, (grado_id,))
        return results[0] if results else None

    def create_grado(self, nombre_grado: str) -> bool:
        """Crea un nuevo grado - Versión simple (retorna bool)"""
        query = """
            INSERT INTO grado (nombre_grado)
            VALUES (%s)
        """
        try:
            return self.execute_update(query, (nombre_grado,))
        except Exception as e:
            return False

    def update_grado(self, grado_id: int, nombre_grado: str) -> bool:
        """Actualiza un grado"""
        query = """
            UPDATE grado
            SET nombre_grado = %s
            WHERE id_grado = %s
        """
        return self.execute_update(query, (nombre_grado, grado_id))

    def delete_grado(self, grado_id: int) -> bool:
        """Elimina un grado"""
        query = """
            DELETE FROM grado
            WHERE id_grado = %s
        """
        return self.execute_update(query, (grado_id,))

    def get_estudiantes_by_grado(self, id_grado: int) -> List[Dict[str, Any]]:
        """Obtiene todos los estudiantes de un grado específico"""
        query = """
            SELECT e.cedula, e.nombre, e.apellido, e.fecha_nacimiento,
                e.municipio, e.telefono, e.correo, e.id_grado,
                e.estado, e.pais, e.observacion, e.id_mencion,
                e.seccion,
                g.nombre_grado
            FROM estudiante e
            LEFT JOIN grado g ON e.id_grado = g.id_grado
            WHERE e.id_grado = %s
            ORDER BY e.apellido, e.nombre
        """
        return self.execute_query(query, (id_grado,))
    
    def get_estudiantes_by_grado_seccion(self, id_grado: int, seccion: str) -> List[Dict[str, Any]]:
        """Obtiene todos los estudiantes de un grado y sección específica"""
        query = """
            SELECT e.cedula, e.nombre, e.apellido, e.fecha_nacimiento,
                e.municipio, e.telefono, e.correo, e.id_grado,
                e.estado, e.pais, e.observacion, e.id_mencion,
                e.seccion,
                g.nombre_grado
            FROM estudiante e
            LEFT JOIN grado g ON e.id_grado = g.id_grado
            WHERE e.id_grado = %s AND e.seccion = %s
            ORDER BY e.apellido, e.nombre
        """
        return self.execute_query(query, (id_grado, seccion))

    def insert_grado(self, nombre_grado: str) -> Optional[Dict[str, Any]]:
        """Inserta un nuevo grado y retorna el registro creado"""
        query = """
            INSERT INTO grado (nombre_grado)
            VALUES (%s)
            RETURNING id_grado, nombre_grado
        """
        results = self.execute_query(query, (nombre_grado,))
        return results[0] if results else None

    # ==================== PERÍODOS ACADÉMICOS ====================
    
    def get_all_periodos(self) -> List[Dict[str, Any]]:
        """Obtiene todos los períodos académicos"""
        query = """
            SELECT id_periodo, anio, fecha_inicio, fecha_fin
            FROM periodo_academico
            ORDER BY anio DESC, fecha_inicio DESC
        """
        return self.execute_query(query)
    
    def get_periodo_by_id(self, periodo_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un período académico por su ID"""
        query = """
            SELECT id_periodo, anio, fecha_inicio, fecha_fin
            FROM periodo_academico
            WHERE id_periodo = %s
        """
        results = self.execute_query(query, (periodo_id,))
        return results[0] if results else None
    
    def create_periodo(self, anio: int, fecha_inicio: str, fecha_fin: str) -> bool:
        """Crea un nuevo período académico"""
        query = """
            INSERT INTO periodo_academico (anio, fecha_inicio, fecha_fin)
            VALUES (%s, %s, %s)
        """
        return self.execute_update(query, (anio, fecha_inicio, fecha_fin))
    
    # ==================== HISTORIAL ACADÉMICO ====================
    
    def get_historial_completo_estudiante(self, cedula_estudiante: str) -> Dict[str, Any]:
        """
        Obtiene el historial académico completo de un estudiante organizado por año (1ro a 6to)
        
        Args:
            cedula_estudiante: Cédula del estudiante
            
        Returns:
            Diccionario con:
            - info_estudiante: Datos del estudiante
            - historial_por_año: Dict con keys '1', '2', '3', '4', '5', '6' 
            conteniendo las materias y notas de cada año
        """
        try:
            pass
            # 1. Obtener información básica del estudiante (CON NUEVOS CAMPOS)
            query_estudiante = """
                SELECT e.cedula, e.nombre, e.apellido, e.fecha_nacimiento, 
                    e.id_grado, e.pais, e.estado, e.municipio, 
                    e.observacion, e.id_mencion, e.seccion, g.nombre_grado
                FROM estudiante e
                LEFT JOIN grado g ON e.id_grado = g.id_grado
                WHERE e.cedula = %s
            """
            estudiante = self.execute_query(query_estudiante, (cedula_estudiante,))
            
            if not estudiante:
                return None
            
            info_estudiante = estudiante[0]
            
            # 2. Obtener TODAS las calificaciones del historial académico
            # Esto incluye las materias que ya completó en años anteriores
            query_historial = """
                SELECT h.id_historial, h.cedula_estudiante, h.codigo_asignatura,
                    h.nota_final, h.estado, h.fecha_curso,
                    a.nombre_asignatura, a.id_grado, g.nombre_grado
                FROM historial_academico h
                JOIN asignatura a ON h.codigo_asignatura = a.codigo
                JOIN grado g ON a.id_grado = g.id_grado
                WHERE h.cedula_estudiante = %s
                ORDER BY a.id_grado, a.nombre_asignatura
            """
            historial = self.execute_query(query_historial, (cedula_estudiante,))
            
            # 3. Obtener calificaciones actuales (del año en curso)
            query_actuales = """
                SELECT c.codigo_calificacion, c.cedula_estudiante, c.codigo_asignatura,
                    c.nota_final,
                    a.nombre_asignatura, a.id_grado, g.nombre_grado
                FROM calificacion c
                JOIN asignatura a ON c.codigo_asignatura = a.codigo
                JOIN grado g ON a.id_grado = g.id_grado
                WHERE c.cedula_estudiante = %s
                ORDER BY a.id_grado, a.nombre_asignatura
            """
            actuales = self.execute_query(query_actuales, (cedula_estudiante,))
            
            # 4. Organizar por año (1ro a 6to)
            historial_por_año = {
                '1': [],
                '2': [],
                '3': [],
                '4': [],
                '5': [],
                '6': []
            }
            
            # Extraer número de año del nombre del grado (ej: "1er Año" -> 1)
            import re
            
            # Procesar historial (materias completadas)
            for registro in historial:
                nombre_grado = registro['nombre_grado']
                # Buscar el primer número en el nombre del grado
                match = re.search(r'(\d+)', nombre_grado)
                if match:
                    año = match.group(1)
                    if año in historial_por_año:
                        historial_por_año[año].append({
                            'nombre_asignatura': registro['nombre_asignatura'],
                            'nota_final': registro['nota_final'],
                            'estado': registro['estado'],
                            'origen': 'historial'  # Marca que viene del historial
                        })
            
            # Procesar calificaciones actuales
            for registro in actuales:
                nombre_grado = registro['nombre_grado']
                match = re.search(r'(\d+)', nombre_grado)
                if match:
                    año = match.group(1)
                    if año in historial_por_año:
                        pass
                        # Verificar si ya existe esta materia en el historial
                        materia_existe = any(
                            m['nombre_asignatura'] == registro['nombre_asignatura'] 
                            for m in historial_por_año[año]
                            if m.get('origen') == 'historial'
                        )
                        
                        # Solo agregar si no existe en historial (evitar duplicados)
                        if not materia_existe:
                            nota = registro['nota_final'] if registro['nota_final'] is not None else 0.0
                            historial_por_año[año].append({
                                'nombre_asignatura': registro['nombre_asignatura'],
                                'nota_final': nota,
                                'estado': 'EN CURSO',  # Marca que está cursando actualmente
                                'origen': 'actual'
                            })
            
            return {
                'info_estudiante': info_estudiante,
                'historial_por_año': historial_por_año
            }
            
        except Exception as e:
            import traceback
            return None

    def get_materias_por_grado(self, id_grado: int) -> List[Dict[str, Any]]:
        """
        Obtiene todas las materias de un grado específico
        
        Args:
            id_grado: ID del grado
            
        Returns:
            Lista de materias del grado
        """
        query = """
            SELECT codigo, nombre_asignatura, id_grado, cedula_docente
            FROM asignatura
            WHERE id_grado = %s
            ORDER BY nombre_asignatura
        """
        return self.execute_query(query, (id_grado,))
    
    def execute_function(self, function_name: str) -> bool:
        """Ejecuta una función de PostgreSQL usando psycopg2"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            # Ejecutar la función
            query = f"SELECT {function_name}();"
            cursor.execute(query)
            
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            if conn and not conn.closed:
                conn.rollback()
            return False

    def __del__(self):
        """Destructor: cierra la conexión al destruir el objeto"""
        self.disconnect()