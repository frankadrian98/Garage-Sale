# Garage-Sale

Las ventas de garaje son una nueva modalidad de tiendas que se está haciendo muy popular en Cuba, debido a los altos precios de los artículos importados. Un ejemplo de estas es la ubicada en 17 e/ 2 y 4 la cual tiene como principal objetivo vender a la población artículos nuevos o de segunda mano con la mejor calidad posible para la satisfacción de todos sus clientes.

Esta tienda cuenta con varios empleados que realizan diferentes tipos de servicios como: el portero el cual es el encargado de la seguridad del local y de guardar los bolsos o mochilas que los clientes pueden tener, el vendedor que atienden a los clientes para orientarlos mejor acerca de los productos en venta y el cajero, encargado de los pagos a realizar por los clientes y de la contabilidad general.

El local es bastante amplio por lo tanto existen diversas formas de distribuir los productos en venta. Por ejemplo: los artículos en exhibición, los cuales son los que están a la vista de cualquier transeúnte que pase por los alrededores del local y se puedan interesar por alguno de estos o por ver q más ofrecen dentro, las prendas que se exhiben en los colgadores los cuales dan una mejor vista a los clientes de que forma son estos artículos y como les pudiera quedar disminuyendo el tiempo de estancia de estos en el establecimiento, y los productos de menor visibilidad los cuales se deben doblar para que ocupen menos espacio, el vendedor tiene que enseñarle a los clientes cual es la forma de estos. También se cuenta con  un vestidor en donde los clientes se pueden hacer pruebas de los productos. 

Debido a las medidas higiénicas que se deben tener solo pueden entrar al local una capacidad limitada de clientes, lo que hace que se creen colas fuera del local, lo cual genera  inconformidad en los clientes debido a que esta produce una demora significativa que en algunos casos les obliga a abandonar su inteción de compra. 
No se tiene a disposición ninguna información que permita calcular la cantidad de clientes que llegan a cierta hora del día, tampoco que cantidad de personal debe atender en cada momento del día para mentener la menor cantidad de personas en la cola. Como riesgo principal ante esta situación se puede identificar que si el tiempo de espera en la cola por pqrte de los clientes es excesivo, estos podrían optar para en una próxima oportunidad no ir a la tienda, es decir, se estaría perdiendo al cliente debido a una mala estrategia de atención.

El precio de cada artículo varía según su calidad. Se sabe que en el local deben existir tanto artículos colgados como artículos doblados debido a que la cantidad de mercancía es demasiado grande y se requiere que toda esta se le exhiba al cliente. 

Se desea simular el proceso de las ventas, variando las formas de organizar los productos y también a los empleados para minimizar el tiempo de espera del cliente en las colas y también para maximizar la ganancia total de la tienda.

<<<<<<< HEAD

=======
>>>>>>> 2554b46c226f2da51476b2570e783f17e7bb9738
Para la simulación:

Elementos del Sistema :
* Caja (Recepción de Pagos)
* Servidor (Atención al Cliente)
* Cliente (Interactúa con los demás agentes y tiene un nivel de tolerancia según la cantidad de personas que se encuentren en la cola)

-Simularemos por un tiempo de 3 horas = 10 800 segundos

-El usuario define la cantidad de clientes que llegarán en ese espacio de tiempo  (máximo 500 clientes)

-Los clientes llegarán cada 2 minutos (120 segundos) en promedio según una distribución de Poisson

- Se simula dado un sistema de colas dada la Teoría M/M/s, la cual tiene s cantidad de servidores 

-El tiempo promedio para que el servidor procese a un cliente es de aproximadamente 160 segundos. 
  Utilizamos una distribución de Poisson para que este número sea discreto y no negativo.

- Cada cliente tiene una tolerancia de 5 personas en la cola a la cual se debe unir, es decir, si en una cola hay 5 o más personas el cliente decidirá unirse a otra y si todas tienen esta cantidad de personas , entonces no se unirá a ninguna, decidira irse y se pierde al cliente.
<<<<<<< HEAD
Esto pasa tanto en la cola para el servidor como en la cola para el cajero.
=======
Esto pasa tanto en la cola para el servidor como en la cola para el cajero.
>>>>>>> 2554b46c226f2da51476b2570e783f17e7bb9738
