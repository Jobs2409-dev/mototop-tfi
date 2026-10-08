// mobile/lib/screens/tomar_pedidos_screen.dart
import 'package:flutter/material.dart';
import '../data/services/pedido_service.dart';

class TomarPedidoScreen extends StatefulWidget {
  const TomarPedidoScreen({super.key});

  @override
  State<TomarPedidoScreen> createState() => _TomarPedidoScreenState();
}

class _TomarPedidoScreenState extends State<TomarPedidoScreen> {
  final _service = PedidoService();
  final _obsController = TextEditingController();

  List<dynamic> _clientes = [];
  List<dynamic> _productos = [];
  int? _selectedClienteId;

  // Carrito: [{'producto_id': int, 'nombre': String, 'precio': double, 'cantidad': int}]
  final List<Map<String, dynamic>> _carrito = [];
  bool _loading = true;
  bool _enviando = false;

  @override
  void initState() {
    super.initState();
    _cargarDatos();
  }

  @override
  void dispose() {
    _obsController.dispose();
    super.dispose();
  }

  Future<void> _cargarDatos() async {
    setState(() => _loading = true);
    try {
      final c = await _service.getClientes();
      final p = await _service.getProductos();
      if (!mounted) return;
      setState(() {
        _clientes = c;
        _productos = p;
        if (_clientes.isNotEmpty) {
          _selectedClienteId = _clientes.first['id'];
        }
        _loading = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() => _loading = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error al cargar datos: $e'), backgroundColor: Colors.redAccent),
      );
    }
  }

  void _agregarOIncrementar(dynamic prod) {
    final id = prod['id'];
    final idx = _carrito.indexWhere((item) => item['producto_id'] == id);

    setState(() {
      if (idx >= 0) {
        _carrito[idx]['cantidad'] += 1;
      } else {
        final rawPrecio = prod['precio_base'] ?? prod['precio_venta'] ?? '0';
        _carrito.add({
          'producto_id': id,
          'nombre': prod['nombre'] ?? 'Repuesto',
          'precio': double.tryParse(rawPrecio.toString()) ?? 0.0,
          'cantidad': 1,
        });
      }
    });
  }

  void _decrementar(int index) {
    setState(() {
      if (_carrito[index]['cantidad'] > 1) {
        _carrito[index]['cantidad'] -= 1;
      } else {
        _carrito.removeAt(index);
      }
    });
  }

  double get _total => _carrito.fold(0.0, (acc, item) => acc + (item['precio'] * item['cantidad']));

  Future<void> _confirmarYEnviar() async {
    if (_selectedClienteId == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Seleccione un cliente')),
      );
      return;
    }
    if (_carrito.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Agregue al menos un repuesto al pedido')),
      );
      return;
    }

    setState(() => _enviando = true);

    try {
      await _service.crearPedido(
        clienteId: _selectedClienteId!,
        items: _carrito,
        observaciones: _obsController.text.trim(),
      );

      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('¡Pedido enviado a Central con éxito!'),
          backgroundColor: Colors.green,
        ),
      );

      setState(() {
        _carrito.clear();
        _obsController.clear();
      });
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error al enviar pedido: $e'), backgroundColor: Colors.redAccent),
      );
    } finally {
      if (mounted) setState(() => _enviando = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF4F6F9),
      appBar: AppBar(
        title: const Text('Tomar Pedido'),
        backgroundColor: Colors.deepOrange,
        foregroundColor: Colors.white,
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : Column(
              children: [
                // Selector de cliente
                Container(
                  padding: const EdgeInsets.all(14.0),
                  color: Colors.white,
                  child: DropdownButtonFormField<int>(
                    value: _selectedClienteId,
                    decoration: InputDecoration(
                      labelText: 'Cliente Destino',
                      prefixIcon: const Icon(Icons.storefront_outlined, color: Colors.deepOrange),
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                      contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                    ),
                    items: _clientes.map<DropdownMenuItem<int>>((c) {
                      final nom = c['nombre'] ?? '';
                      final ape = c['apellido'] ?? '';
                      final razon = c['razon_social'] ?? '';
                      final display = razon.isNotEmpty ? razon : '$nom $ape'.trim();
                      return DropdownMenuItem<int>(
                        value: c['id'],
                        child: Text(display, overflow: TextOverflow.ellipsis),
                      );
                    }).toList(),
                    onChanged: (val) => setState(() => _selectedClienteId = val),
                  ),
                ),
                const Divider(height: 1),

                // Lista de productos para seleccionar
                Expanded(
                  flex: 3,
                  child: ListView.separated(
                    padding: const EdgeInsets.all(12),
                    itemCount: _productos.length,
                    separatorBuilder: (_, __) => const SizedBox(height: 8),
                    itemBuilder: (context, idx) {
                      final p = _productos[idx];
                      final stock = p['stock'] ?? 0;
                      final rawPrecio = p['precio_base'] ?? p['precio_venta'] ?? '0';
                      final precio = double.tryParse(rawPrecio.toString()) ?? 0.0;

                      return Card(
                        elevation: 0.5,
                        color: Colors.white,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(10),
                          side: BorderSide(color: Colors.grey.shade200),
                        ),
                        child: ListTile(
                          title: Text(
                            p['nombre'] ?? '',
                            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
                          ),
                          subtitle: Text('Stock: $stock — \$${precio.toStringAsFixed(2)}'),
                          trailing: IconButton(
                            icon: const Icon(Icons.add_circle, color: Colors.deepOrange, size: 28),
                            onPressed: () => _agregarOIncrementar(p),
                          ),
                        ),
                      );
                    },
                  ),
                ),

                // Resumen del Carrito actual
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                  color: Colors.grey.shade200,
                  alignment: Alignment.centerLeft,
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text(
                        'Ítems del Pedido',
                        style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: Colors.black87),
                      ),
                      Text('${_carrito.length} seleccionados', style: const TextStyle(fontSize: 12, color: Colors.grey)),
                    ],
                  ),
                ),
                Expanded(
                  flex: 2,
                  child: _carrito.isEmpty
                      ? const Center(
                          child: Text(
                            'Tocá el botón (+) en un repuesto para agregarlo',
                            style: TextStyle(color: Colors.grey, fontSize: 13),
                          ),
                        )
                      : ListView.builder(
                          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                          itemCount: _carrito.length,
                          itemBuilder: (context, idx) {
                            final item = _carrito[idx];
                            final subtotal = item['cantidad'] * item['precio'];
                            return Card(
                              elevation: 0,
                              margin: const EdgeInsets.symmetric(vertical: 4),
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(8),
                                side: BorderSide(color: Colors.grey.shade300),
                              ),
                              child: Padding(
                                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                                child: Row(
                                  children: [
                                    Expanded(
                                      child: Column(
                                        crossAxisAlignment: CrossAxisAlignment.start,
                                        children: [
                                          Text(
                                            item['nombre'],
                                            style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13),
                                            overflow: TextOverflow.ellipsis,
                                          ),
                                          Text(
                                            '\$${item['precio']} c/u — Subtotal: \$${subtotal.toStringAsFixed(2)}',
                                            style: TextStyle(fontSize: 11, color: Colors.grey.shade700),
                                          ),
                                        ],
                                      ),
                                    ),
                                    IconButton(
                                      icon: const Icon(Icons.remove_circle_outline, color: Colors.redAccent, size: 20),
                                      onPressed: () => _decrementar(idx),
                                    ),
                                    Text('${item['cantidad']}', style: const TextStyle(fontWeight: FontWeight.bold)),
                                    IconButton(
                                      icon: const Icon(Icons.add_circle_outline, color: Colors.green, size: 20),
                                      onPressed: () => setState(() => item['cantidad'] += 1),
                                    ),
                                  ],
                                ),
                              ),
                            );
                          },
                        ),
                ),

                // Barra inferior: Total y Enviar
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    boxShadow: [
                      BoxShadow(color: Colors.black.withOpacity(0.06), blurRadius: 4, offset: const Offset(0, -2))
                    ],
                  ),
                  child: Row(
                    children: [
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            const Text('Total Estimado', style: TextStyle(fontSize: 11, color: Colors.grey)),
                            Text(
                              '\$${_total.toStringAsFixed(2)}',
                              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.deepOrange),
                            ),
                          ],
                        ),
                      ),
                      ElevatedButton.icon(
                        onPressed: (_carrito.isEmpty || _enviando) ? null : _confirmarYEnviar,
                        icon: _enviando
                            ? const SizedBox(
                                width: 18,
                                height: 18,
                                child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2),
                              )
                            : const Icon(Icons.send),
                        label: Text(_enviando ? 'ENVIANDO...' : 'ENVIAR PEDIDO'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.deepOrange,
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
    );
  }
}