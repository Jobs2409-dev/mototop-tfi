// mobile/lib/data/services/auth_service.dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../../core/api_constants.dart';
import '../../core/storage/secure_storage_service.dart';

Map<String, dynamic> _parseJwt(String token) {
  try {
    final parts = token.split('.');
    if (parts.length != 3) return {};
    final payload = utf8.decode(base64Url.decode(base64Url.normalize(parts[1])));
    return jsonDecode(payload);
  } catch (_) {
    return {};
  }
}

class AuthService {
  String? lastErrorMessage;

  Future<bool> login(String username, String password) async {
    lastErrorMessage = null;

    final base = ApiConstants.baseUrl.endsWith('/')
        ? ApiConstants.baseUrl.substring(0, ApiConstants.baseUrl.length - 1)
        : ApiConstants.baseUrl;

    final tokenUrl = Uri.parse('$base${ApiConstants.tokenObtain}');

    try {
      final tokenResponse = await http.post(
        tokenUrl,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'username': username.trim(),
          'password': password,
        }),
      );

      if (tokenResponse.statusCode != 200) {
        lastErrorMessage = 'Usuario o contraseña incorrectos';
        return false;
      }

      final tokenData = jsonDecode(tokenResponse.body);
      final accessToken = tokenData['access'] as String;
      final refreshToken = tokenData['refresh'] as String;

      final jwtPayload = _parseJwt(accessToken);
      final dynamic rawUserId = jwtPayload['user_id'];
      final int? loggedUserId = rawUserId is int
          ? rawUserId
          : (rawUserId != null ? int.tryParse(rawUserId.toString()) : null);

      int? currentVendedorId;
      String? currentVendedorNombre;

      try {
        final vendedoresUrl = Uri.parse('$base/vendedores/');
        final vendResponse = await http.get(
          vendedoresUrl,
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer $accessToken',
          },
        );

        if (vendResponse.statusCode == 200) {
          final dynamic body = jsonDecode(vendResponse.body);
          final List<dynamic> vendedores = (body is Map && body.containsKey('results'))
              ? body['results']
              : (body is List ? body : []);

          for (var v in vendedores) {
            if (v is Map) {
              final usuarioVal = v['usuario'];
              final dynamic rawVUserId = (usuarioVal is Map) ? usuarioVal['id'] : usuarioVal;
              final int? vendedorUserId = rawVUserId is int
                  ? rawVUserId
                  : (rawVUserId != null ? int.tryParse(rawVUserId.toString()) : null);

              final bool matchUser = (vendedorUserId != null && vendedorUserId == loggedUserId);
              final bool matchUsername = (v['username'] == username.trim());

              if (matchUser || matchUsername) {
                final dynamic estadoVal = v['estado'];
                final dynamic activoVal = v['activo'];

                bool estaInactivo = false;
                if (activoVal is bool && activoVal == false) {
                  estaInactivo = true;
                } else if (estadoVal != null) {
                  final estadoStr = estadoVal.toString().trim().toLowerCase();
                  if (estadoStr == 'inactivo' || estadoStr == 'baja') {
                    estaInactivo = true;
                  }
                }

                if (estaInactivo) {
                  lastErrorMessage = 'Tu cuenta de vendedor se encuentra inactiva.';
                  await SecureStorageService.clearTokens();
                  return false;
                }

                final dynamic rawId = v['id'];
                currentVendedorId = rawId is int ? rawId : int.tryParse(rawId.toString());

                // Obtenemos el nombre y apellido real
                final nom = (v['nombre'] ?? '').toString().trim();
                final ape = (v['apellido'] ?? '').toString().trim();
                final completo = '$nom $ape'.trim();
                currentVendedorNombre = completo.isNotEmpty ? completo : null;

                break;
              }
            }
          }
        }
      } catch (e) {
        print('Consulta opcional de vendedor omitida: $e');
      }

      await SecureStorageService.saveTokens(
        access: accessToken,
        refresh: refreshToken,
        vendedorId: currentVendedorId,
        vendedorNombre: currentVendedorNombre,
      );

      return true;
    } catch (e) {
      print('=== ERROR EN LOGIN ===: $e');
      lastErrorMessage = 'Error al conectar con el servidor: $e';
      return false;
    }
  }

  Future<void> logout() async {
    await SecureStorageService.clearTokens();
  }

  Future<bool> isAuthenticated() async {
    final token = await SecureStorageService.getAccessToken();
    return token != null && token.isNotEmpty;
  }
}