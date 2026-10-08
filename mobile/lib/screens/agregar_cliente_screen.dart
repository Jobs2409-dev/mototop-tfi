// mobile/lib/screens/agregar_cliente_screen.dart
import 'package:flutter/material.dart';
import '../data/services/cliente_service.dart';

class AgregarClienteScreen extends StatefulWidget {
  const AgregarClienteScreen({super.key});

  @override
  State<AgregarClienteScreen> createState() => _AgregarClienteScreenState();
}

class _AgregarClienteScreenState extends State<AgregarClienteScreen> {
  final _formKey = GlobalKey<FormState>();
  final _service = ClienteService();

  // Controladores de formulario
  final _nombreController = TextEditingController();
  final _apellidoController = TextEditingController();
  final _documentoController = TextEditingController();
  final _telefonoController = TextEditingController();
  final _emailController = TextEditingController();
  final _direccionController = TextEditingController();
  final _cpController = TextEditingController();
  final _localidadController = TextEditingController();
  final _provinciaController = TextEditingController();

  List<dynamic> _zonas = [];
  int? _selectedZonaId;

  bool _loadingZonas = true;
  bool _guardando = false;

  @override
  void initState() {
    super.initState();
    _cargarZonas();
  }

  @override
  void dispose() {
    _nombreController.dispose();
    _apellidoController.dispose();
    _documentoController.dispose();
    _telefonoController.dispose();
    _emailController.dispose();
    _direccionController.dispose();
    _cpController.dispose();
    _localidadController.dispose();
    _provinciaController.dispose();
    super.dispose();
  }

  Future<void> _cargarZonas() async {
    try {
      final z = await _service.getZonas();
      if (!mounted) return;
      setState(() {
        _zonas = z;
        if (_zonas.isNotEmpty) {
          _selectedZonaId = _zonas.first['id'];
        }
        _loadingZonas = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() => _loadingZonas = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error al cargar zonas comerciales: $e')),
      );
    }
  }

  Future<void> _guardarCliente() async {
    if (!_formKey.currentState!.validate()) return;
    if (_selectedZonaId == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Debe seleccionar una zona comercial')),
      );
      return;
    }

    setState(() => _guardando = true);

    try {
      await _service.crearCliente(
        nombre: _nombreController.text.trim(),
        apellido: _apellidoController.text.trim(),
        nroDocumento: _documentoController.text.trim(),
        telefono: _telefonoController.text.trim(),
        email: _emailController.text.trim(),
        direccion: _direccionController.text.trim(),
        codigoPostal: _cpController.text.trim(),
        localidad: _localidadController.text.trim(),
        provincia: _provinciaController.text.trim(),
        zonaId: _selectedZonaId!,
      );

      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('¡Cliente registrado exitosamente!'),
          backgroundColor: Colors.green,
        ),
      );

      Navigator.pop(context); // Vuelve al Home tras guardar
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Error al registrar cliente: $e'),
          backgroundColor: Colors.redAccent,
        ),
      );
    } finally {
      if (mounted) setState(() => _guardando = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF4F6F9),
      appBar: AppBar(
        title: const Text('Registrar Nuevo Cliente'),
        backgroundColor: Colors.deepOrange,
        foregroundColor: Colors.white,
      ),
      body: _loadingZonas
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              padding: const EdgeInsets.all(16.0),
              child: Form(
                key: _formKey,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    // Sección: Datos del Comercio / Persona
                    _buildSectionHeader('Datos Personales / Comercio', Icons.business_outlined),
                    const SizedBox(height: 10),
                    Card(
                      elevation: 0.5,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      child: Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Column(
                          children: [
                            TextFormField(
                              controller: _nombreController,
                              decoration: const InputDecoration(
                                labelText: 'Nombre o Razón Social *',
                                border: OutlineInputBorder(),
                                prefixIcon: Icon(Icons.storefront),
                              ),
                              validator: (val) => (val == null || val.trim().isEmpty) ? 'Campo obligatorio' : null,
                            ),
                            const SizedBox(height: 12),
                            TextFormField(
                              controller: _apellidoController,
                              decoration: const InputDecoration(
                                labelText: 'Apellido / Contacto',
                                border: OutlineInputBorder(),
                                prefixIcon: Icon(Icons.person_outline),
                              ),
                            ),
                            const SizedBox(height: 12),
                            TextFormField(
                              controller: _documentoController,
                              decoration: const InputDecoration(
                                labelText: 'DNI / CUIT *',
                                border: OutlineInputBorder(),
                                prefixIcon: Icon(Icons.badge_outlined),
                              ),
                              validator: (val) => (val == null || val.trim().isEmpty) ? 'Campo obligatorio' : null,
                            ),
                            const SizedBox(height: 12),
                            TextFormField(
                              controller: _telefonoController,
                              keyboardType: TextInputType.phone,
                              decoration: const InputDecoration(
                                labelText: 'Teléfono de Contacto *',
                                border: OutlineInputBorder(),
                                prefixIcon: Icon(Icons.phone_outlined),
                              ),
                              validator: (val) => (val == null || val.trim().isEmpty) ? 'Campo obligatorio' : null,
                            ),
                            const SizedBox(height: 12),
                            TextFormField(
                              controller: _emailController,
                              keyboardType: TextInputType.emailAddress,
                              decoration: const InputDecoration(
                                labelText: 'Email *',
                                border: OutlineInputBorder(),
                                prefixIcon: Icon(Icons.email_outlined),
                              ),
                              validator: (val) => (val == null || val.trim().isEmpty) ? 'Campo obligatorio' : null,
                            ),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 20),

                    // Sección: Ubicación y Zona
                    _buildSectionHeader('Ubicación y Zona Comercial', Icons.location_on_outlined),
                    const SizedBox(height: 10),
                    Card(
                      elevation: 0.5,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      child: Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Column(
                          children: [
                            TextFormField(
                              controller: _direccionController,
                              decoration: const InputDecoration(
                                labelText: 'Dirección Comercial *',
                                border: OutlineInputBorder(),
                                prefixIcon: Icon(Icons.map_outlined),
                              ),
                              validator: (val) => (val == null || val.trim().isEmpty) ? 'Campo obligatorio' : null,
                            ),
                            const SizedBox(height: 12),
                            Row(
                              children: [
                                Expanded(
                                  flex: 2,
                                  child: TextFormField(
                                    controller: _localidadController,
                                    decoration: const InputDecoration(
                                      labelText: 'Localidad *',
                                      border: OutlineInputBorder(),
                                    ),
                                    validator: (val) => (val == null || val.trim().isEmpty) ? 'Requerido' : null,
                                  ),
                                ),
                                const SizedBox(width: 10),
                                Expanded(
                                  flex: 1,
                                  child: TextFormField(
                                    controller: _cpController,
                                    decoration: const InputDecoration(
                                      labelText: 'CP *',
                                      border: OutlineInputBorder(),
                                    ),
                                    validator: (val) => (val == null || val.trim().isEmpty) ? 'Requerido' : null,
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 12),
                            TextFormField(
                              controller: _provinciaController,
                              decoration: const InputDecoration(
                                labelText: 'Provincia *',
                                border: OutlineInputBorder(),
                                prefixIcon: Icon(Icons.terrain_outlined),
                              ),
                              validator: (val) => (val == null || val.trim().isEmpty) ? 'Campo obligatorio' : null,
                            ),
                            const SizedBox(height: 14),
                            // Selector de Zona
                            DropdownButtonFormField<int>(
                              value: _selectedZonaId,
                              decoration: const InputDecoration(
                                labelText: 'Zona Comercial *',
                                border: OutlineInputBorder(),
                                prefixIcon: Icon(Icons.explore_outlined),
                              ),
                              items: _zonas.map<DropdownMenuItem<int>>((z) {
                                return DropdownMenuItem<int>(
                                  value: z['id'],
                                  child: Text(z['nombre'] ?? 'Sin nombre'),
                                );
                              }).toList(),
                              onChanged: (val) => setState(() => _selectedZonaId = val),
                            ),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 24),

                    // Botón de Guardar
                    ElevatedButton.icon(
                      onPressed: _guardando ? null : _guardarCliente,
                      icon: _guardando
                          ? const SizedBox(
                              width: 18,
                              height: 18,
                              child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2),
                            )
                          : const Icon(Icons.save_outlined),
                      label: Text(_guardando ? 'REGISTRANDO...' : 'GUARDAR CLIENTE'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.teal.shade700,
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(vertical: 14),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                        textStyle: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                      ),
                    ),
                    const SizedBox(height: 16),
                  ],
                ),
              ),
            ),
    );
  }

  Widget _buildSectionHeader(String title, IconData icon) {
    return Row(
      children: [
        Icon(icon, size: 20, color: Colors.deepOrange),
        const SizedBox(width: 8),
        Text(
          title,
          style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: Color(0xFF2C3E50)),
        ),
      ],
    );
  }
}