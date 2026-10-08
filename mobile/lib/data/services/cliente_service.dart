// mobile/lib/data/services/cliente_service.dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../../core/api_constants.dart';
import '../../core/storage/secure_storage_service.dart';

class ClienteService {
  String _buildUrl(String endpoint) {
    final base = ApiConstants.baseUrl.endsWith('/')
        ? ApiConstants.baseUrl.substring(0, ApiConstants.baseUrl.length - 1)
        : ApiConstants.baseUrl;
    final ep = endpoint.startsWith('/') ? endpoint : '/$endpoint';
    return '$base$ep';
  }

  Future<Map<String, String>> _getHeaders() async {
    final token = await SecureStorageService.getAccessToken();
    return {
      'Content-Type': 'application/json',
      if (token != null && token.isNotEmpty) 'Authorization': 'Bearer $token',
    };
  }

  // Obtiene las zonas disponibles para asignar al cliente
  Future<List<dynamic>> getZonas() async {
    final url = Uri.parse(_buildUrl('/zonas/'));
    final headers = await _getHeaders();
    final res = await http.get(url, headers: headers);

    if (res.statusCode == 200) {
      final dynamic body = jsonDecode(res.body);
      return (body is Map && body.containsKey('results')) ? body['results'] : (body as List);
    }
    throw Exception('Error al cargar zonas (Status: ${res.statusCode})');
  }

  // Registra un nuevo cliente en el backend
  Future<bool> crearCliente({
    required String nombre,
    required String apellido,
    required String nroDocumento,
    required String telefono,
    required String email,
    required String direccion,
    required String codigoPostal,
    required String localidad,
    required String provincia,
    required int zonaId,
  }) async {
    final url = Uri.parse(_buildUrl(ApiConstants.clientes));
    final headers = await _getHeaders();

    final payload = {
      'nombre': nombre,
      'apellido': apellido,
      'nro_documento': nroDocumento,
      'telefono': telefono,
      'email': email,
      'direccion': direccion,
      'codigo_postal': codigoPostal,
      'localidad': localidad,
      'provincia': provincia,
      'zona': zonaId,
    };

    final res = await http.post(
      url,
      headers: headers,
      body: jsonEncode(payload),
    );

    if (res.statusCode == 201 || res.statusCode == 200) {
      return true;
    } else {
      throw Exception(res.body);
    }
  }
}