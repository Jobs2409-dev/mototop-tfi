// mobile/lib/core/storage/secure_storage_service.dart
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class SecureStorageService {
  static const _storage = FlutterSecureStorage();
  static const _keyAccess = 'jwt_access_token';
  static const _keyRefresh = 'jwt_refresh_token';
  static const _keyVendedorId = 'vendedor_id';
  static const _keyVendedorNombre = 'vendedor_nombre';

  static Future<void> saveTokens({
    required String access,
    required String refresh,
    int? vendedorId,
    String? vendedorNombre,
  }) async {
    await _storage.write(key: _keyAccess, value: access);
    await _storage.write(key: _keyRefresh, value: refresh);
    if (vendedorId != null) {
      await _storage.write(key: _keyVendedorId, value: vendedorId.toString());
    }
    if (vendedorNombre != null && vendedorNombre.isNotEmpty) {
      await _storage.write(key: _keyVendedorNombre, value: vendedorNombre);
    }
  }

  static Future<String?> getAccessToken() async {
    return await _storage.read(key: _keyAccess);
  }

  static Future<String?> getRefreshToken() async {
    return await _storage.read(key: _keyRefresh);
  }

  static Future<int?> getVendedorId() async {
    final val = await _storage.read(key: _keyVendedorId);
    return val != null ? int.tryParse(val) : null;
  }

  static Future<String?> getVendedorNombre() async {
    return await _storage.read(key: _keyVendedorNombre);
  }

  static Future<void> clearTokens() async {
    await _storage.delete(key: _keyAccess);
    await _storage.delete(key: _keyRefresh);
    await _storage.delete(key: _keyVendedorId);
    await _storage.delete(key: _keyVendedorNombre);
  }
}
