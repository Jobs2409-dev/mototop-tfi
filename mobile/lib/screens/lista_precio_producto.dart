// mobile/lib/screens/lista_precio_producto.dart
import 'package:flutter/material.dart';
import '../data/services/producto_service.dart';

class ListaPreciosScreen extends StatefulWidget {
  const ListaPreciosScreen({super.key});

  @override
  State<ListaPreciosScreen> createState() => _ListaPreciosScreenState();
}

class _ListaPreciosScreenState extends State<ListaPreciosScreen> {
  final _service = ProductoService();
  final _searchController = TextEditingController();

  List<dynamic> _todosLosProductos = [];
  List<dynamic> _productosFiltrados = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _cargarProductos();
    _searchController.addListener(_filtrarProductos);
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  Future<void> _cargarProductos() async {
    setState(() => _loading = true);
    try {
      final prods = await _service.listarProductos();
      if (!mounted) return;
      setState(() {
        _todosLosProductos = prods;
        _productosFiltrados = prods;
        _loading = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() => _loading = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Error al cargar la lista: $e'),
          backgroundColor: Colors.redAccent,
        ),
      );
    }
  }

  void _filtrarProductos() {
    final query = _searchController.text.trim().toLowerCase();
    setState(() {
      if (query.isEmpty) {
        _productosFiltrados = _todosLosProductos;
      } else {
        _productosFiltrados = _todosLosProductos.where((p) {
          final nombre = (p['nombre'] ?? '').toString().toLowerCase();
          return nombre.contains(query);
        }).toList();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF4F6F9),
      appBar: AppBar(
        title: const Text('Lista de Precios'),
        backgroundColor: Colors.deepOrange,
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: 'Actualizar precios',
            onPressed: _cargarProductos,
          ),
        ],
      ),
      body: Column(
        children: [
          // Barra de búsqueda rápida
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: TextField(
              controller: _searchController,
              decoration: InputDecoration(
                hintText: 'Buscar por repuesto o modelo...',
                prefixIcon: const Icon(Icons.search, color: Colors.deepOrange),
                suffixIcon: _searchController.text.isNotEmpty
                    ? IconButton(
                        icon: const Icon(Icons.clear, size: 20),
                        onPressed: () => _searchController.clear(),
                      )
                    : null,
                filled: true,
                fillColor: Colors.white,
                contentPadding: const EdgeInsets.symmetric(vertical: 0),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: BorderSide.none,
                ),
              ),
            ),
          ),

          // Contenido principal
          Expanded(
            child: _loading
                ? const Center(child: CircularProgressIndicator())
                : _productosFiltrados.isEmpty
                    ? Center(
                        child: Text(
                          _searchController.text.isEmpty
                              ? 'No hay productos disponibles.'
                              : 'Sin resultados para la búsqueda.',
                          style: const TextStyle(color: Colors.grey, fontSize: 15),
                        ),
                      )
                    : ListView.separated(
                        padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
                        itemCount: _productosFiltrados.length,
                        separatorBuilder: (_, __) => const SizedBox(height: 10),
                        itemBuilder: (context, index) {
                          final item = _productosFiltrados[index];
                          final nombre = item['nombre'] ?? 'Sin nombre';
                          final stock = item['stock'] ?? 0;
                          final precioStr = (item['precio_base'] ?? item['precio_venta'] ?? '0').toString();
                          final precio = double.tryParse(precioStr) ?? 0.0;

                          // Formato de rubros
                          final rubros = item['rubros'];
                          String rubrosStr = '';
                          if (rubros is List && rubros.isNotEmpty) {
                            rubrosStr = rubros
                                .map((r) => r is Map ? r['nombre'] : r.toString())
                                .join(', ');
                          }

                          return Card(
                            elevation: 0.5,
                            color: Colors.white,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                              side: BorderSide(color: Colors.grey.shade200),
                            ),
                            child: Padding(
                              padding: const EdgeInsets.all(14.0),
                              child: Row(
                                children: [
                                  // Ícono representativo
                                  Container(
                                    width: 44,
                                    height: 44,
                                    decoration: BoxDecoration(
                                      color: Colors.blue.shade50,
                                      borderRadius: BorderRadius.circular(10),
                                    ),
                                    child: Icon(Icons.build_circle_outlined, color: Colors.blue.shade700, size: 24),
                                  ),
                                  const SizedBox(width: 14),

                                  // Datos del producto
                                  Expanded(
                                    child: Column(
                                      crossAxisAlignment: CrossAxisAlignment.start,
                                      children: [
                                        Text(
                                          nombre,
                                          style: const TextStyle(
                                            fontWeight: FontWeight.bold,
                                            fontSize: 14,
                                            color: Color(0xFF2C3E50),
                                          ),
                                        ),
                                        if (rubrosStr.isNotEmpty) ...[
                                          const SizedBox(height: 2),
                                          Text(
                                            rubrosStr,
                                            style: TextStyle(fontSize: 11, color: Colors.grey.shade600),
                                          ),
                                        ],
                                        const SizedBox(height: 6),
                                        // Badge de stock
                                        Container(
                                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                                          decoration: BoxDecoration(
                                            color: stock > 0 ? Colors.green.shade50 : Colors.red.shade50,
                                            borderRadius: BorderRadius.circular(6),
                                          ),
                                          child: Text(
                                            stock > 0 ? 'Stock: $stock' : 'Sin Stock',
                                            style: TextStyle(
                                              fontSize: 11,
                                              fontWeight: FontWeight.w600,
                                              color: stock > 0 ? Colors.green.shade700 : Colors.red.shade700,
                                            ),
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),

                                  // Precio destacado
                                  Text(
                                    '\$${precio.toStringAsFixed(2)}',
                                    style: const TextStyle(
                                      fontSize: 16,
                                      fontWeight: FontWeight.bold,
                                      color: Colors.deepOrange,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          );
                        },
                      ),
          ),
        ],
      ),
    );
  }
}