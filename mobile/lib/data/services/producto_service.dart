// mobile/lib/data/services/producto_service.dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../../core/api_constants.dart';
import '../../core/storage/secure_storage_service.dart';

class ProductoService {
  Future<List<dynamic>> listarProductos() async {
    final token = await SecureStorageService.getAccessToken();
    final url = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.productos}');

    final response = await http.get(
      url,
      headers: {
        'Content-Type': 'application/json',
        if (token != null && token.isNotEmpty) 'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      final dynamic body = jsonDecode(response.body);
      // Soporta respuesta en lista directa o paginada en results
      if (body is Map && body.containsKey('results')) {
        return body['results'] as List<dynamic>;
      }
      return body as List<dynamic>;
    } else {
      throw Exception('Error al obtener productos (Status: ${response.statusCode})');
    }
  }
}