// mobile/lib/screens/home_screen.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../core/storage/secure_storage_service.dart';
import '../presentation/providers/auth_provider.dart';
import 'lista_precio_producto.dart';
import 'tomar_pedidos_screen.dart';
import 'agregar_cliente_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String _nombreVendedor = 'Cargando...';

  @override
  void initState() {
    super.initState();
    _cargarNombre();
  }

  Future<void> _cargarNombre() async {
    final nombre = await SecureStorageService.getVendedorNombre();
    if (mounted) {
      setState(() {
        _nombreVendedor = (nombre != null && nombre.isNotEmpty)
            ? nombre
            : 'Vendedor';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF4F6F9),
      appBar: AppBar(
        title: const Text(
          'MOTO-TOP Móvil',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        backgroundColor: Colors.deepOrange,
        foregroundColor: Colors.white,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            tooltip: 'Cerrar sesión',
            onPressed: () => context.read<AuthProvider>().logout(),
          ),
        ],
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Banner de Bienvenida con nombre real
              Card(
                elevation: 1,
                color: Colors.white,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                  side: BorderSide(color: Colors.deepOrange.withOpacity(0.2)),
                ),
                child: Padding(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 18.0,
                    vertical: 16.0,
                  ),
                  child: Row(
                    children: [
                      CircleAvatar(
                        radius: 26,
                        backgroundColor: Colors.deepOrange.shade100,
                        child: const Icon(
                          Icons.person,
                          color: Colors.deepOrange,
                          size: 30,
                        ),
                      ),
                      const SizedBox(width: 14),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text(
                              'Bienvenido,',
                              style: TextStyle(
                                fontSize: 13,
                                color: Colors.grey,
                                fontWeight: FontWeight.w500,
                              ),
                            ),
                            const SizedBox(height: 2),
                            Text(
                              _nombreVendedor,
                              style: const TextStyle(
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                                color: Color(0xFF2C3E50),
                              ),
                              overflow: TextOverflow.ellipsis,
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 24),
              const Text(
                'Operaciones en Ruta',
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF333333),
                ),
              ),
              const SizedBox(height: 14),

              // Opción 1: Consultar lista de precios
              _buildMenuCard(
                icon: Icons.price_change_outlined,
                iconColor: Colors.blue.shade700,
                iconBg: Colors.blue.shade50,
                title: 'Consultar Lista de Precios',
                subtitle: 'Repuestos, stock en tiempo real y precios',
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => const ListaPreciosScreen(),
                    ),
                  );
                },
              ),
              const SizedBox(height: 12),

              // Opción 2: Tomar pedidos
              _buildMenuCard(
                icon: Icons.add_shopping_cart_rounded,
                iconColor: Colors.deepOrange,
                iconBg: Colors.deepOrange.shade50,
                title: 'Tomar Pedidos',
                subtitle: 'Cargar orden para un cliente asignado',
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => const TomarPedidoScreen(),
                    ),
                  );
                },
              ),
              const SizedBox(height: 12),

              // Opción 3: Agregar clientes
              _buildMenuCard(
                icon: Icons.person_add_alt_1_outlined,
                iconColor: Colors.teal.shade700,
                iconBg: Colors.teal.shade50,
                title: 'Agregar Clientes',
                subtitle: 'Dar de alta un nuevo comercio en la zona',
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const AgregarClienteScreen()),
                  );
                },
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildMenuCard({
    required IconData icon,
    required Color iconColor,
    required Color iconBg,
    required String title,
    required String subtitle,
    required VoidCallback onTap,
  }) {
    return Card(
      elevation: 0.5,
      color: Colors.white,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(14),
        side: BorderSide(color: Colors.grey.shade200),
      ),
      child: InkWell(
        borderRadius: BorderRadius.circular(14),
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 14.0),
          child: Row(
            children: [
              Container(
                width: 48,
                height: 48,
                decoration: BoxDecoration(
                  color: iconBg,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Icon(icon, color: iconColor, size: 26),
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      title,
                      style: const TextStyle(
                        fontSize: 15,
                        fontWeight: FontWeight.w600,
                        color: Color(0xFF2C3E50),
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      subtitle,
                      style: TextStyle(
                        fontSize: 12,
                        color: Colors.grey.shade600,
                      ),
                    ),
                  ],
                ),
              ),
              const Icon(Icons.arrow_forward_ios, size: 14, color: Colors.grey),
            ],
          ),
        ),
      ),
    );
  }
}
