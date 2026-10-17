# backend/core/serializers.py
from rest_framework import serializers
from .models import *
from django.db import transaction
from django.db.models import Sum
from django.contrib.auth.models import User


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed


class ClienteTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # Verificar si tiene un perfil de Cliente asociado
        if not hasattr(user, 'cliente'):
            raise AuthenticationFailed(
                "Acceso denegado: Esta cuenta no está registrada como cliente."
            )

        data['rol'] = 'cliente'
        data['cliente_id'] = user.cliente.id
        data['nombre_completo'] = f"{user.cliente.nombre} {user.cliente.apellido or ''}".strip()

        return data

class VendedorTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Valida username y password con Django
        data = super().validate(attrs)
        user = self.user

        # Permitir superusuarios/staff para desarrollo o testing si lo deseas
        if user.is_superuser or user.is_staff:
            data['rol'] = 'admin'
            return data

        # Verificar si tiene un perfil de Vendedor asociado
        if not hasattr(user, 'vendedor'):
            raise AuthenticationFailed(
                "Acceso denegado: Esta aplicación es exclusiva para vendedores."
            )

        # Verificar si el vendedor está activo
        if user.vendedor.estado != 'activo':
            raise AuthenticationFailed(
                "Acceso denegado: Su cuenta de vendedor se encuentra inactiva."
            )

        # Agregamos datos útiles para la app en la respuesta
        data['rol'] = 'vendedor'
        data['vendedor_id'] = user.vendedor.id
        data['nombre_completo'] = f"{user.vendedor.nombre} {user.vendedor.apellido or ''}".strip()

        return data

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'


class RubroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubro
        fields = '__all__'


# PRODUCTO ======================================================

# ProductoSerializer
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
       
# Prodcuto READ  
class ProductoReadSerializer(serializers.ModelSerializer):
    proveedores = serializers.SerializerMethodField()
    rubros = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = '__all__'

    def get_proveedores(self, obj):
        relaciones = ProveedorProducto.objects.filter(producto=obj)
        proveedores = [rel.proveedor for rel in relaciones]
        return ProveedorSerializer(proveedores, many=True).data

    def get_rubros(self, obj):
        relaciones = RubroProducto.objects.filter(producto=obj)
        rubros = [rel.rubro for rel in relaciones]
        return RubroSerializer(rubros, many=True).data
   

# Prodcuto WRITE
class ProductoWriteSerializer(serializers.ModelSerializer):
    
    proveedores = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    rubros = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Producto
        fields = [
            "id",
            "nombre",
            "stock",
            "precio_base",
            "img",
            "proveedores",
            "rubros",
        ]

    @transaction.atomic
    def create(self, validated_data):
        proveedores_ids = validated_data.pop("proveedores", [])
        rubros_ids = validated_data.pop("rubros", [])

        producto = Producto.objects.create(**validated_data)

        for prov_id in proveedores_ids:
            ProveedorProducto.objects.create(
                producto=producto,
                proveedor_id=prov_id
            )

        for rubro_id in rubros_ids:
            RubroProducto.objects.create(
                producto=producto,
                rubro_id=rubro_id
            )

        return producto

    @transaction.atomic
    def update(self, instance, validated_data):
        proveedores_ids = validated_data.pop("proveedores", None)
        rubros_ids = validated_data.pop("rubros", None)

        if proveedores_ids is not None:
            ProveedorProducto.objects.filter(producto=instance).delete()
            for prov_id in proveedores_ids:
                ProveedorProducto.objects.create(
                    producto=instance,
                    proveedor_id=prov_id
                )

        if rubros_ids is not None:
            RubroProducto.objects.filter(producto=instance).delete()
            for rubro_id in rubros_ids:
                RubroProducto.objects.create(
                    producto=instance,
                    rubro_id=rubro_id
                )

        return super().update(instance, validated_data)
   
# CLIENTE ======================================================

# Cliente Serializer     
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
    

# Vendedor Serializer
class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = ['id', 'nombre', 'apellido', 'telefono', 'comision', 'estado', 'zona', 'usuario']
    

# PEDIDO =====================================================

# DetallePedido (escritura) Serializer sin información del producto  
class DetallePedidoWriteSerializer(serializers.ModelSerializer):
    
    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError("Cantidad inválida")
        return value

    class Meta:
        model = DetallePedido
        fields = ['producto', 'cantidad']
      
#  DetallePedido (lectura) Serializer con información del producto 
class DetallePedidoReadSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()

    class Meta:
        model = DetallePedido
        fields = ['id', 'producto', 'cantidad', 'precio_unitario', 'subtotal']

class PedidoWriteSerializer(serializers.ModelSerializer):
    detalles = DetallePedidoWriteSerializer(many=True, write_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'vendedor', 'origen', 'observaciones', 'detalles']
        extra_kwargs = {
            'vendedor': {'required': False, 'allow_null': True},
            'observaciones': {'required': False, 'allow_blank': True, 'allow_null': True},
        }

    @transaction.atomic
    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles', [])
        pedido = Pedido.objects.create(**validated_data)

        for detalle in detalles_data:
            producto = detalle['producto']

            detalle_obj = DetallePedido(
                pedido=pedido,
                producto=producto,
                cantidad=detalle['cantidad'],
                precio_unitario=producto.precio_base
            )
            detalle_obj.save()

        return pedido


# Pedido Serializer para lectura, que incluye detalles con información del producto y cliente con información completa
class PedidoReadSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer()
    vendedor = VendedorSerializer()
    detalles = DetallePedidoReadSerializer(many=True)
    facturada = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'vendedor', 'origen', 'fecha_pedido', 'estado', 'total', 'detalles', 'facturada']

    def get_facturada(self, obj):
        try:
            _ = obj.factura
            return True
        except Factura.DoesNotExist:
            return False
            
# FACTURA ================================================================   
class DetalleFacturaReadSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()

    class Meta:
        model = DetalleFactura
        fields = ['producto', 'cantidad', 'precio_unitario', 'subtotal']
        
class FacturaReadSerializer(serializers.ModelSerializer):
    detalles = DetalleFacturaReadSerializer(many=True)
    pagada = serializers.SerializerMethodField()
    monto_pagado = serializers.SerializerMethodField()
    monto_pendiente = serializers.SerializerMethodField()
    estado_pago = serializers.SerializerMethodField()

    class Meta:
        model = Factura
        fields = ['id', 'pedido', 'fecha_emision', 'total', 'detalles', 'pagada', 'monto_pagado', 'monto_pendiente', 'estado_pago']

    def get_pagada(self, obj):
        return obj.esta_pagada()
    
    def get_monto_pagado(self, obj):
        return obj.calcular_monto_pagado()
    
    def get_monto_pendiente(self, obj):
        return obj.calcular_pendiente()
    
    def get_estado_pago(self, obj):
        return obj.get_estado_pago()
             
# Pago
class PagoSerializer(serializers.ModelSerializer):

    def validate(self, data):
        factura = data.get('factura')
        monto = data.get('monto')
        # Si no envían estado, por defecto asume 'completado' (cobro inmediato)
        estado = data.get('estado', 'completado')
        
        # Asignar el estado completado por defecto si no venía en los datos
        data['estado'] = estado

        if self.instance:
            factura = factura or self.instance.factura
            monto = monto or self.instance.monto
            estado = estado or self.instance.estado

        if monto is None or monto <= 0:
            raise serializers.ValidationError(
                "El monto a cobrar debe ser mayor a $0.00"
            )

        # Calculamos el saldo pendiente actual de la factura
        pendiente = factura.calcular_pendiente()
        
        if self.instance and self.instance.estado == 'completado':
            # Si se está editando un pago existente, sumamos su monto previo para recalcular correctamente
            pendiente += self.instance.monto

        # VALIDACIÓN STRICTA: El monto cobrado NUNCA puede superar el pendiente
        if monto > pendiente:
            raise serializers.ValidationError(
                f"El monto a cobrar (${monto:.2f}) no puede superar el saldo pendiente de la factura (${pendiente:.2f})."
            )

        return data

    class Meta:
        model = Pago
        fields = ['id', 'factura', 'fecha_pago', 'monto', 'metodo_pago', 'estado', 'referencia']
        extra_kwargs = {
            'estado': {'required': False, 'default': 'completado'}
        }

    class Meta:
        model = Pago
        fields = ['id', 'factura', 'fecha_pago', 'monto', 'metodo_pago', 'estado', 'referencia']
        
    
# Envio   
class EnvioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Envio
        fields = '__all__'
        extra_kwargs = {
            'pedido': {'required': False},
            'empresa_transporte': {'required': False},
        }

    def validate(self, data):
        pedido = data.get('pedido') or self.instance.pedido

        if pedido.estado != 'confirmado':
            raise serializers.ValidationError(
                "No se puede crear/modificar envío sin pedido confirmado"
            )

        return data
# COMPRA ====================================================

# Detalle compra read
class DetalleCompraReadSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()

    class Meta:
        model = DetalleCompra
        fields = ['producto', 'cantidad', 'precio_unitario', 'subtotal']

# Detalle compra Write
class DetalleCompraWriteSerializer(serializers.ModelSerializer):
    
    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError("Cantidad inválida")
        return value

    class Meta:
        model = DetalleCompra
        fields = ['producto', 'cantidad']
        
# Compra Write
class CompraWriteSerializer(serializers.ModelSerializer):
    detalles = DetalleCompraWriteSerializer(many=True, write_only=True)

    class Meta:
        model = Compra
        fields = ['proveedor', 'detalles']

    @transaction.atomic
    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles', [])
        compra = Compra.objects.create(**validated_data)

        for detalle in detalles_data:
            producto = detalle['producto']
            detalle_obj = DetalleCompra(
                compra=compra,
                producto=producto,
                cantidad=detalle['cantidad'],
                precio_unitario=producto.precio_base
            )
            detalle_obj.save()

        return compra

# Compra Read
class CompraReadSerializer(serializers.ModelSerializer):
    detalles = DetalleCompraReadSerializer(many=True)

    class Meta:
        model = Compra
        fields = ['id', 'proveedor', 'fecha_compra', 'estado', 'total', 'detalles']

# Zona Serializer

class ZonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zona
        fields = '__all__'

# Promocion Serializer
class PromocionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocion
        fields = '__all__'

# ProductoPromocion Serializer
class ProductoPromocionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoPromocion
        fields = '__all__'

# Factura Write Serializer
class FacturaWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Factura
        fields = ['pedido', 'tipo_comprobante']

    def validate(self, data):
        pedido = data['pedido']
        if Factura.objects.filter(pedido=pedido).exists():
            raise serializers.ValidationError("El pedido ya tiene factura")
        return data

    @transaction.atomic
    def create(self, validated_data):
        pedido = validated_data['pedido']

        if pedido.estado != 'confirmado':
            raise serializers.ValidationError("El pedido debe estar confirmado")

        factura = Factura.objects.create(**validated_data, total=0)

        for d in pedido.detalles.all():
            DetalleFactura.objects.create(
                factura=factura,
                producto=d.producto,
                cantidad=d.cantidad,
                precio_unitario=d.precio_unitario,
                subtotal=d.subtotal
            )

        factura.calcular_total()

        return factura

class UserWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    
# GeminiChatSerializer

class GeminiChatSerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=1000, required=True)
    
    

# SOLICITUD DE VISITA ==============================================

class SolicitudVisitaWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitudVisita
        fields = [
            'id', 'comercio', 'contacto', 'telefono', 'email',
            'direccion', 'localidad', 'zona', 'vendedor',
            'observaciones', 'estado'
        ]
        extra_kwargs = {
            'vendedor': {'required': False, 'allow_null': True},
            'observaciones': {'required': False, 'allow_blank': True, 'allow_null': True},
            'estado': {'required': False, 'default': 'pendiente'}
        }


class SolicitudVisitaReadSerializer(serializers.ModelSerializer):
    zona = ZonaSerializer()
    vendedor = VendedorSerializer()

    class Meta:
        model = SolicitudVisita
        fields = [
            'id', 'comercio', 'contacto', 'telefono', 'email',
            'direccion', 'localidad', 'zona', 'vendedor',
            'observaciones', 'estado', 'fecha_creacion'
        ]