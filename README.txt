
problemática
a la hora de implementar un dataset en el entrenamiento de 
una red neuronal como la pix2pix es necesario que haya 
correlación entre los datos, sin embargo, esto no siempre 
es posible, por lo que en este trabajo se explora la 
alternativa de adaptar el dataset, con el objetivo de que 
no haya necesidad de que haya correlación entre los datos. 
Un ejemplo de este problema es encontrar pinturas junto a la 
foto en la cual está basada, por lo que su resolución solo 
sería posible si el usuario se dedicara a pintar cada una 
de las imágenes de entrenamiento o pagara para ello. 
Trabajo realizado
Se programó en Python, usando las librerías de opencv, un 
programa el cual permitía crear un juego de imágenes 
encuadradas y redimensionadas, una de ellas modificada, 
aplicando un filtro de erosión de 5X5 en diamante y una 
umbralizacion de 180 a cada canal de color por separado. 
Una vez creado el dataset, se procedió a entrenar el 
modelo pix2pix en Google colab, debido a problemas 
con la memoria RAM, se redujo el dataset a 50 imágenes.
 
Manual
pasos para usar el programa
1-guarde las imágenes que dese convertir en una carpeta.
 
2-modifique el nombre de las imágenes, nombrándolas en 
orden numérico.

3-copie y pegue los programas modificadorD.py, 
Modificador.py y Modificadorcolor.py a la carpeta.
4-abra ModificadorD.py y modifique el número final para 
que coincida con el número de imágenes.

5-guarde las imágenes modificadas (inician con “M- “) 
en una carpeta llamada input y las demás en una llamada 
output.

6-abra el código modelo_pix2pix.py y modifique la variable 
PATH, escribiendo la ruta de carpeta con las carpetas 
input y output.

7-coloque la carpeta checkpoint en esa carpeta.

8-ejecute el programa (el programa viene configurado 
para no entrenar la red, si desea entrenar la red, 
coloque las imágenes para su entrenamiento en sus 
respectivas carpetas y descomente la última línea)

Resultados
En los resultados se aprecia la falta de datos de 
entrenamiento, a pesar de ello, se obtuvo imágenes 
decentes, en las que se puede apreciar rasgos 
característicos de la pintura en acuarela.

el objetivo principal del proyecto era probar 
una nueva estrategia, la cual se implementó al 
ver que no había datasets de foto-pintura en la 
red, por lo que se recurrió a “adaptar la imagen” 
distorsionándola de tal forma que la imagen 
resultante de distorsionar una imagen real 
fuera similar a la distorsión de la imagen de 
una pintura, esto se logró usando filtro de 
erosión y umbralización a cada canal de color 
por separado, con el objetivo de que la imagen 
resultante fuese igual en una fotografía que 
en una pintura 
