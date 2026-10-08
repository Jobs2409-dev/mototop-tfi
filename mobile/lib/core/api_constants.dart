// mobile/lib/core/api_constants.dart
import 'package:flutter_dotenv/flutter_dotenv.dart';

class ApiConstants {
  static String get baseUrl {
    final url = dotenv.env['API_BASE_URL'] ?? 'http://127.0.0.1:8000/api';
    return url.endsWith('/') ? url.substring(0, url.length - 1) : url;
  }

  static const String tokenObtain = '/token/';
  static const String tokenRefresh = '/token/refresh/';
  static const String productos = '/productos/';
  static const String clientes = '/clientes/';
  static const String pedidos = '/pedidos/';
}
