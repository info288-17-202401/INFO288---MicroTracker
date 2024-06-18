import 'package:latlong2/latlong.dart';

class Route {
  int id;
  List<LatLng> route;
  int line_id;

  Route({
    required this.id,
    required this.route,
    required this.line_id,
  });

  Route.fromJson(Map<String, dynamic> json)
      : id = json['id'],
        route = (json['route'] as List)
            .map((point) => LatLng(point["x"], point["y"]))
            .toList(),
        line_id = json['line_id'];

  static List<Route> fromJsonList(List<dynamic> jsonList) {
    return jsonList.map((json) => Route.fromJson(json)).toList();
  }
}
