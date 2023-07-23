# Controlador de música automático para Valorant con Opera GX y YouTube
¿No te ha ocurrido que cuando juegas al Valorant te gustaría estar escuchando música pero que cuando comience la ronda esta música se pause automáticamente para que no interrumpa tu concentración en el juego? Este programa apunta a hacer eso mismo. El programa, dependiendo de lo que ocurra en el juego, bajará/subirá el volumen y/o pausará/reanudará el video musical que estés escuchando. El cambio de volumen se hace de forma progresiva para que no suene muy brusco este cambio.

## Instrucciones de uso
1. Edita el archivo *ValorantAutoMusica.py* y cambia el valor de la variable *rutaPrograma* por la ruta donde tengas este programa. En la siguiente versión del programa esto ya no será necesario
2. Abre la consola de Windows y ejecuta este programa (*py ValorantAutoMusica.py* en la consola, o *python* en vez de *py*, depende cómo lo tengas configurado)
3. Abre el Opera GX y abre YouTube (si ya lo tienes abierto, ignora este paso)
4. Abre Valorant y ya lo tendrías en funcionamiento, en el menú el volumen asignado por defecto es el 100%

Recuerda que antes tienes que tener la consola en la ruta donde está este programa y que tienes que tener instaladas las librerías de Python necesarias para que funcione el programa (pip install -r requirements.txt)

## Consideraciones a tener en cuenta
1. Disponible solo para Valorant ejecutándose en 1080p
2. Solo funciona si el idioma de los textos del juego están en español de España (ignoro si el español de Latinoamérica es idéntico)
3. Solo Opera GX y YouTube, si utilizas otro navegador tendrás que cambiar un poco del código del programa, lo siento
4. Funciona mucho mejor si tienes el Valorant en modo pantalla completa sin bordes. El modo de pantalla completa da muchos problemas y el modo ventana hace que ya no se ajuste a 1080p tal y como están las imágenes del programa
5. El juego hace uso de lo que se ve en pantalla, no inyecta código ni modifica archivos internos del juego por lo que no es detectable ni baneable, tampoco estás haciendo trampas de ningún tipo así que no es una preocupación. No obstante, para controlar Opera GX se tiene que hacer uso de su PID para controlar la ventana ya que esta no es visible en la pantalla.

# El estado del programa es una BETA
El programa aún no está completamente funcional, quedan muchas cosas por optimizar como la velocidad de análisis (ya que consume un buen porcentaje de CPU), la región de análisis, varios estados del juego (no detecta cuando estás en el menú de compra de arma dentro de una partida) y que tienes que cambiar manualmente una variable del programa para que funcione en el caso particular de cada uno. También es sabido que en el mapa *Icebox* al ser un lugar muy blanco haga falsos positivos con el programa. Los falsos positivos son un problema pues como detecta que hay que, por ejemplo, pausar el video musical, el programa ejecuta la acción de pulsar el espacio para pausar el video pero estás jugando y el personaje de repente salta él solo.
