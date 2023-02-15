# Django Multitenant Store API

Este proyecto consiste en una aplicacion web para gestionar una multitienda basado en el principio multistore.

## Por Hacer
### Correcciones Finales
- [ ] Ubicacion de los productos, (Almacén).
- [ ] Filtro en la store por direccion del almacen del producto.
- [ ] Hacer una Vista exclusiva de las exportaciones en csv.
- [ ] Reportes en csv de:
    - [ ] Dashboard.
        - [ ] solo mi tienda.
        - [ ] vista general (Vista general de la tienda matriz de las ventas de sus subtiendas).
    - [ ] Ordenes.
    - [ ] Productos.
    - [ ] Usuarios.
    - [ ] Notificar por websocket la exportacion del archivo.
- [x] hacer un enlace del recibo a la tienda.
- [x] Ciudad como parametro no requerido en la direccion de facturacion.
- [x] Bug de la ruta del login, que aparece como "Iniciar Sesion / Home"
## Hecho
- [x] Poner ganado menos comision en los creditos de la tienda.
- [x] Vista para gestionar los pagos que tiene que hacer la tienda matriz.
- [x] Poner funcion de recuperar contraseña.
- [x] Vista de Freelancers basada en las asistencias de las product orders de la Tienda.
- [x] Error en usuario nuevo cuando paga por paypal o pago movil, no redirige.
- [x] boton de borrar producto.
- [x] Editar estado de la Transaccion en el admin, en caso de pago móvil.
- [x] Solo los Administradores de la empresa matriz pueden cambiar el estado de las ordenes.
- [x] Vista de contacto, usuarios que han comprado a la tienda.
- [x] Bug Agregar al carrito sin existencias.
- [x] Opcion de tienda matriz de ver solo su informacion, o la informacion global (Vuex).
- [x] filtro de precio en la vista de Producto.
- [x] Acreditar puntos cuando exista una asistencia asociada a cart items y/o product_orders y se complete una venta.
- [x] Modelo de Gift Card
- [x] Opcion de retirar lo ganado.
- [x] Chat tipo ws para comunicar operarios y/o freelancers con clientes.
- [x] Bug de foto de perfil de usuario registrado en formulario.
- [x] Error de Nombre y apellido del usuario al registrarse
- [x] Mejorar vista de detalle de producto en tienda.
- [x] Error En javascript de la Tienda para filtrar por precio.
- [x] Vista de detalle de cada Orden.
