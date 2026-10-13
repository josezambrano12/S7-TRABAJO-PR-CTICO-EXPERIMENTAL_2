from datetime import date

# Nota mínima para aprobar (la escala es de 0 a 20)
NOTA_APROBACION = 10


# =====================================================================
# CLASE BASE: lo que los tres modelos comparten (NO SE TOCA)
# =====================================================================
class ModeloBase:
    """Padre de todos los modelos. Guarda el id y define el comportamiento común."""

    def __init__(self, id_registro):
        self.id = int(id_registro)

    # ---- ÚNICO MÉTODO DE CLASE DEL PROYECTO ----
    @classmethod
    def desde_diccionario(cls, datos):
        """Diccionario -> objeto. Escrito UNA vez y usado por los tres modelos.
        cls es la clase que llamó: Estudiante, Materia o Matricula."""
        datos = dict(datos)                 # copia, para no tocar el original
        id_registro = datos.pop("id")       # saco el id
        return cls(id_registro, **datos)    # el resto son los campos del modelo

    # ---- MÉTODOS DE INSTANCIA ----
    def a_diccionario(self):
        # Objeto -> diccionario. Cada hijo agrega sus campos.
        return {"id": self.id}

    def etiqueta(self):
        # POLIMORFISMO: cada hijo la reescribe a su manera
        return f"registro {self.id}"

    def __str__(self):
        # Lo que se ve al hacer print(objeto). Llama a etiqueta(),
        # así que cada modelo se imprime distinto sin cambiar esta línea.
        return f"[{self.id}] {self.etiqueta()}"


# =====================================================================
# HERENCIA: Persona es la base de Estudiante (ya estaba escrita)
# =====================================================================
class Persona(ModeloBase):
    """Todo lo que tiene una persona del sistema."""

    def __init__(self, id_registro, nombre, apellido, email):
        super().__init__(id_registro)      # el padre guarda el id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def a_diccionario(self):
        datos = super().a_diccionario()    # {"id": ...} que arma el padre
        datos["nombre"] = self.nombre
        datos["apellido"] = self.apellido
        datos["email"] = self.email
        return datos

    def etiqueta(self):
        return self.nombre_completo()


class Estudiante(Persona):
    """Estudiante ES UNA Persona, con carnet y carrera."""

    def __init__(self, id_registro, nombre, apellido, email, carnet="", carrera=""):
        super().__init__(id_registro, nombre, apellido, email)
        self.carnet = carnet
        self.carrera = carrera

    def a_diccionario(self):
        datos = super().a_diccionario()    # reutiliza lo de Persona
        datos["carnet"] = self.carnet
        datos["carrera"] = self.carrera
        return datos

    def etiqueta(self):
        # Sobrescribe y EXTIENDE la del padre
        return f"{super().etiqueta()} · {self.carnet} · {self.carrera or 'sin carrera'}"


# =====================================================================
# ÚNICA CLASE CON ATRIBUTO Y MÉTODO ESTÁTICO
# =====================================================================
class Materia(ModeloBase):
    """Materia ES UN ModeloBase. Los cupos hacen el papel del stock."""

    # ATRIBUTO ESTÁTICO (de clase): existe una sola vez, igual para todas las materias
    CUPOS_MAXIMOS = 30

    def __init__(self, id_registro, nombre, codigo, creditos, cupos=CUPOS_MAXIMOS):
        super().__init__(id_registro)
        self.nombre = nombre
        self.codigo = codigo
        self.creditos = int(creditos)
        self.cupos = int(cupos)

    # MÉTODO ESTÁTICO: regla que no necesita ninguna materia concreta
    @staticmethod
    def es_codigo_valido(valor):
        # Tres letras y luego números, ej: MAT101
        texto = str(valor).strip()
        return len(texto) >= 4 and texto[:3].isalpha() and texto[3:].isdigit()

    # MÉTODOS DE INSTANCIA: necesitan los datos de ESTA materia
    def hay_cupo(self):
        return self.cupos > 0

    def ocupar_cupo(self):
        self.cupos -= 1

    def liberar_cupo(self):
        self.cupos += 1

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre"] = self.nombre
        datos["codigo"] = self.codigo
        datos["creditos"] = self.creditos
        datos["cupos"] = self.cupos
        return datos

    def etiqueta(self):
        alerta = "" if self.hay_cupo() else " ⚠ sin cupo"
        return (f"{self.codigo} · {self.nombre} · {self.creditos} créditos · "
                f"cupos {self.cupos}/{Materia.CUPOS_MAXIMOS}{alerta}")


# =====================================================================
class Matricula(ModeloBase):
    """Matrícula simple: un estudiante, una materia, un periodo y una nota."""

    def __init__(self, id_registro, estudiante_id, materia_id, periodo,
                 nota=0.0, fecha=""):
        super().__init__(id_registro)
        self.estudiante_id = int(estudiante_id)
        self.materia_id = int(materia_id)
        self.periodo = periodo
        self.nota = float(nota)
        self.fecha = fecha or date.today().isoformat()

    def esta_aprobada(self):
        # Se calcula cada vez; NO se guarda, para que nunca quede
        # desactualizada si cambia la nota
        return self.nota >= NOTA_APROBACION

    def estado(self):
        if self.esta_aprobada():
            return "Aprobado"
        return "Reprobado"

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["estudiante_id"] = self.estudiante_id
        datos["materia_id"] = self.materia_id
        datos["periodo"] = self.periodo
        datos["nota"] = self.nota
        datos["fecha"] = self.fecha
        return datos

    def etiqueta(self):
        return (f"{self.periodo} · estudiante {self.estudiante_id} · "
                f"materia {self.materia_id} · "
                f"nota {self.nota:.1f} ({self.estado()})")