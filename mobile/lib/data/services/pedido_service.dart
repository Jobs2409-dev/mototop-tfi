// mobile/lib/data/services/pedido_service.dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../../core/api_constants.dart';
import '../../core/storage/secure_storage_service.dart';

class PedidoService {
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

  Future<List<dynamic>> getClientes() async {
    final url = Uri.parse(_buildUrl(ApiConstants.clientes));
    final headers = await _getHeaders();
    final res = await http.get(url, headers: headers);
    
    if (res.statusCode == 200) {
      final dynamic body = jsonDecode(res.body);
      return (body is Map && body.containsKey('results')) ? body['results'] : (body as List);
    }
    throw Exception('Error al cargar clientes (Status: ${res.statusCode})');
  }

  Future<List<dynamic>> getProductos() async {
    final url = Uri.parse(_buildUrl(ApiConstants.productos));
    final headers = await _getHeaders();
    final res = await http.get(url, headers: headers);
    
    if (res.statusCode == 200) {
      final dynamic body = jsonDecode(res.body);
      return (body is Map && body.containsKey('results')) ? body['results'] : (body as List);
    }
    throw Exception('Error al cargar productos (Status: ${res.statusCode})');
  }

  Future<bool> crearPedido({
    required int clienteId,
    required List<Map<String, dynamic>> items,
    String observaciones = '',
  }) async {
    final url = Uri.parse(_buildUrl(ApiConstants.pedidos));
    final headers = await _getHeaders();
    final vendedorId = await SecureStorageService.getVendedorId();

    final payload = {
      'cliente': clienteId,
      'origen': 'mobile',
      if (vendedorId != null) 'vendedor': vendedorId,
      'observaciones': observaciones,
      'detalles': items.map((i) => {
        'producto': i['producto_id'],
        'cantidad': i['cantidad'],
      }).toList(),
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