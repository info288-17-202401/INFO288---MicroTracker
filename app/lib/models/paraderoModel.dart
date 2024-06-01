import "package:latlong2/latlong.dart";

class Paradero {
  int id;
  LatLng position;

  Paradero({
    required this.id,
    required this.position,
  });

  Paradero.fromJson(Map<String, dynamic> json)
      : id = json['id'],
        position = LatLng(
          json['coordinates']["x"],
          json['coordinates']["y"],
        );

  static List<Paradero> fromJsonList(List<dynamic> jsonList) {
    return jsonList.map((json) => Paradero.fromJson(json)).toList();
  }
}
