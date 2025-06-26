from src.database.db_mysql import get_connection
from src.models.pedido_extra_model import PedidoExtra

class PedidoExtraService():
    @staticmethod
    def insertar_extras_pedido(pedido_id, extras):
        """
        Inserta los extras asociados a un pedido en la base de datos.

        Args:
            pedido_id: ID del pedido al que pertenecen los extras
            extras: Lista de diccionarios con información de extras
                   Cada extra debe tener: extra_id, cantidad, sub_total

        Returns:
            bool: True si la inserción fue exitosa, False en caso contrario
        """
        connection = None
        try:
            if not pedido_id:
                print("ERROR: ID de pedido inválido o no proporcionado")
                return False

            if not extras or not isinstance(extras, list):
                # Si no hay extras, es un caso válido (pedido sin extras)
                print("INFO: No hay extras para insertar")
                return True

            connection = get_connection()
            print(f"INFO: Insertando {len(extras)} extras para pedido #{pedido_id}")

            for i, extra in enumerate(extras):
                try:
                    # Extraer datos del extra
                    extra_id = extra.get('extra_id')
                    cantidad = extra.get('cantidad')
                    sub_total = extra.get('sub_total')

                    # Validar datos requeridos
                    if not all([extra_id, cantidad is not None, sub_total is not None]):
                        missing_fields = []
                        if not extra_id: missing_fields.append('extra_id')
                        if cantidad is None: missing_fields.append('cantidad')
                        if sub_total is None: missing_fields.append('sub_total')

                        print(f"ERROR: Datos incompletos en extra #{i+1}: faltan {', '.join(missing_fields)}")
                        continue

                    # Insertar en la base de datos
                    sql = "INSERT INTO Pedido_Extra (pedido_id, extra_id, cantidad, sub_total) VALUES (?, ?, ?, ?)"
                    connection.execute(sql, (
                        pedido_id,
                        extra_id,
                        cantidad,
                        sub_total
                    ))
                    print(f"INFO: Extra #{extra_id} agregado al pedido #{pedido_id}")

                except Exception as e:
                    print(f"ERROR: No se pudo insertar extra #{i+1}: {str(e)}")
                    connection.rollback()
                    return False

            # Confirmar todos los cambios
            connection.commit()
            print(f"INFO: {len(extras)} extras insertados exitosamente para pedido #{pedido_id}")
            return True

        except Exception as e:
            print(f"ERROR al insertar extras: {str(e)}")
            if connection:
                connection.rollback()
            return False

        finally:
            if connection:
                connection.close()

    @classmethod
    def get_pedido_extra(cls, id):
        """
        Recupera todos los extras asociados a un pedido.

        Args:
            id: ID del pedido

        Returns:
            list: Lista de extras asociados al pedido
        """
        connection = None
        try:
            connection = get_connection()
            sql = "SELECT * FROM Pedido_Extra WHERE pedido_id = ?"
            datos = connection.execute(sql, (id, )).fetchall()

            pedidos_extras = []
            for dato in datos:
                # dato: (pedido_id, extra_id, cantidad, sub_total)
                _pedido_extra = PedidoExtra(dato[0], dato[1], dato[2], dato[3])
                pedidos_extras.append(_pedido_extra.to_json())

            return pedidos_extras

        except Exception as ex:
            print(f"ERROR al recuperar extras del pedido: {str(ex)}")
            return []

        finally:
            if connection:
                connection.close()
