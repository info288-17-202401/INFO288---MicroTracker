import 'package:latlong2/latlong.dart';

class Micro {
  // String id;
  String patent;
  int brand;
  // String model;
  int line;
  LatLng? currentPosition;

  Micro({
    // required this.id,
    required this.patent,
    required this.brand,
    // required this.model,
    required this.line,
    required this.currentPosition,
  });
  Micro.fromJson(Map<String, dynamic> json)
      // : id = json['id'],
      : patent = json['patent'],
        brand = json['brand_id'],
        // model = json['model'],
        line = json['line_id'],
        currentPosition = LatLng(
          json['coordinates']["x"],
          json['coordinates']["y"],
        );
  static List<Micro> fromJsonList(List<dynamic> jsonList) {
    return jsonList.map((json) => Micro.fromJson(json)).toList();
  }
}
