import "package:latlong2/latlong.dart";

class Paradero {
  int id;
  int id_ruta_fk;
  LatLng position;

  Paradero({
    required this.id,
    required this.id_ruta_fk,
    required this.position,
  });

  Paradero.fromJson(Map<String, dynamic> json)
      : id = json['id'],
        id_ruta_fk = json['id_ruta_fk'],
        position = LatLng(
          json['coordinates']["x"],
          json['coordinates']["y"],
        );

  static List<Paradero> fromJsonList(List<dynamic> jsonList) {
    return jsonList.map((json) => Paradero.fromJson(json)).toList();
  }
}
