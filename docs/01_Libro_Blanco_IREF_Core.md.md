# El Libro Blanco de IREF

*Sistema de Interpretación y Registro de Resoluciones*

---

## 1. ¿Qué problema resuelve IREF?

Todos los años, las facultades emiten cientos de resoluciones: otorgan
créditos por pasantías, aprueban actividades extracurriculares, reconocen
cursos de posgrado, validan trayectorias académicas. Cada una de esas
resoluciones contiene información valiosa — quién hizo qué, cuándo, por
cuántos créditos — pero esa información queda atrapada en un documento de
texto, redactado en lenguaje jurídico-administrativo, pensado para ser
firmado y archivado, no para ser consultado.

El resultado es previsible: para saber cuántos créditos acumuló un alumno,
alguien tiene que abrir resolución por resolución y leerlas a mano. Para
armar un informe de gestión, alguien tiene que repetir ese trabajo
multiplicado por cientos de documentos. El conocimiento existe, está
firmado y es oficial, pero no está *disponible*.

IREF resuelve exactamente ese problema: toma el texto de una resolución
tal como fue redactada y lo convierte en datos estructurados — alumno,
padrón, actividad, créditos — listos para ser consultados, cruzados o
cargados en otro sistema. No cambia cómo se redactan las resoluciones; las
lee como ya existen, y les extrae lo que sirve.

---

## 2. ¿Por qué las resoluciones son una fuente de información?

Es común pensar las resoluciones como el *resultado final* de un trámite:
algo que se firma y se archiva. Pero antes de ser un papel firmado, una
resolución es un registro de un hecho académico real, validado por la
institución. Eso la convierte en algo distinto de un dato suelto cargado
en una planilla: es un dato con respaldo institucional.

A diferencia de una base de datos que alguien carga manualmente —y que
puede tener errores, omisiones o estar desactualizada— una resolución es
la fuente de verdad. Si una resolución dice que un alumno tiene 6 créditos
por una pasantía, eso *es* el dato oficial, no una copia de él.

El problema nunca fue la calidad de la información. Fue el formato: texto
libre, redactado por personas distintas, en momentos distintos, con
pequeñas variaciones de estilo entre resolución y resolución. IREF no
inventa información nueva; hace visible la que ya estaba ahí, dispersa en
cientos de documentos de texto.

---

## 3. ¿Qué significa interpretar una resolución?

Interpretar una resolución no es lo mismo que leerla. Leer es recorrer el
texto. Interpretar es reconocer, dentro de esa redacción jurídica, los
hechos concretos que describe: quién es el alumno, qué actividad realizó,
cuántos créditos le corresponden, y bajo qué legajo está identificado.

Esa interpretación tiene sus complejidades. Una misma idea —"se le
otorgan créditos por una actividad"— puede estar redactada de formas muy
distintas según quién escribió la resolución: a veces nombra al alumno
antes de la actividad, a veces después; a veces hay un solo alumno, a
veces hay un listado de diez; a veces la actividad se describe en el
mismo artículo, a veces se remite a un detalle en el "VISTO" del
documento.

IREF interpreta resoluciones distinguiendo estos **patrones de
redacción** y aplicando, para cada uno, la lógica de extracción que
corresponde. Esa es la función de los *Parsers*: cada uno sabe interpretar
un tipo particular de resolución, reconociendo sus variantes y
extrayendo, en todos los casos, el mismo tipo de dato estructurado.

Interpretar, en este sentido, es traducir el lenguaje administrativo a
datos consultables — sin perder fidelidad respecto del documento
original, que sigue siendo la fuente de verdad.

---

## 4. ¿Cómo puede crecer el sistema?

IREF no fue diseñado para resolver un único tipo de resolución, sino para
crecer a medida que aparecen nuevos tipos. La arquitectura del sistema
separa claramente tres responsabilidades — **detectar** el tipo de
resolución, **elegir** el intérprete correcto y **extraer** los datos — de
modo que sumar un nuevo tipo de resolución no requiere modificar lo que ya
funciona.

Esto significa que el crecimiento de IREF es **incremental por diseño**:
cada nuevo tipo de resolución (becas de investigación, licencias,
designaciones docentes, reconocimientos de materias) se incorpora como una
pieza nueva e independiente, sin tocar el motor central ni los tipos ya
soportados. El sistema no se reescribe para crecer: se le agregan piezas.

Esa misma lógica de crecimiento incremental aplica más allá del tipo de
resolución. El conjunto de datos que se extrae de cada una (hoy: alumno,
padrón, actividad, créditos) también puede ampliarse — sumando, por
ejemplo, carrera, fecha o número de expediente— a medida que la
institución identifique qué información necesita consultar.

En definitiva, IREF no es un programa cerrado pensado para un caso
puntual, sino una base sobre la cual cada nueva necesidad de la gestión
universitaria puede resolverse sumando una pieza, no reconstruyendo el
sistema.

---

## 5. ¿Qué impacto puede tener en la gestión universitaria?

El impacto más inmediato es de tiempo: lo que hoy requiere leer
resolución por resolución, IREF lo entrega de forma estructurada y
consultable. Eso libera horas de trabajo administrativo que hoy se
destinan a transcribir manualmente lo que ya está escrito en un documento
oficial.

Pero el impacto más profundo no es solo de eficiencia, sino de
**visibilidad**. Hoy, preguntas simples —¿cuántos créditos otorgó la
facultad este año por pasantías?, ¿qué actividades concentran más
participación estudiantil?, ¿qué carreras reconocen más actividades
extracurriculares?— son difíciles de responder porque la información está
repartida en cientos de documentos de texto. Con los datos estructurados
que produce IREF, esas preguntas dejan de requerir un relevamiento manual
y pasan a poder responderse con una consulta.

Eso habilita un tipo de gestión distinta: una gestión que puede mirar
patrones a lo largo del tiempo, detectar tendencias, y tomar decisiones
basadas en lo que efectivamente sucedió —no en lo que alguien recuerda
haber leído en una resolución hace seis meses.

En ese sentido, IREF no reemplaza ningún criterio institucional ni
automatiza decisiones: simplemente convierte en información consultable
algo que la institución ya decidió y ya firmó. El resto —qué hacer con
esa información— sigue siendo, como corresponde, una decisión humana.

---

*Este documento es un bosquejo conceptual. Cada capítulo puede ampliarse,
reordenarse o desdoblarse en secciones más extensas según el público al
que esté destinado (equipo técnico, autoridades de gestión, u otros
interesados).*
