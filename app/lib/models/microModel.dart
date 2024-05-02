import 'package:latlong2/latlong.dart';

class Micro {
  String id;
  String patent;
  String brand;
  String model;
  int line;
  LatLng? currentPosition;

  Micro({
    required this.id,
    required this.patent,
    required this.brand,
    required this.model,
    required this.line,
    required this.currentPosition,
  });
  Micro.fromJson(Map<String, dynamic> json)
      : id = json['id'],
        patent = json['patent'],
        brand = json['brand'],
        model = json['model'],
        line = json['line'],
        currentPosition = LatLng(
          json['currentPosition']["latitude"],
          json['currentPosition']["longitude"],
        );
  static List<Micro> fromJsonList(List<dynamic> jsonList) {
    return jsonList.map((json) => Micro.fromJson(json)).toList();
  }
}
