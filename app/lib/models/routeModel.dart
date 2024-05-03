import 'package:latlong2/latlong.dart';

class Route {
  String id;
  List<LatLng> route;

  Route({
    required this.id,
    required this.route,
  });

  Route.fromJson(Map<String, dynamic> json)
      : id = json['id'],
        route = (json['route'] as List)
            .map((point) => LatLng(point["lat"], point["lon"]))
            .toList();

  static List<Route> fromJsonList(List<dynamic> jsonList) {
    return jsonList.map((json) => Route.fromJson(json)).toList();
  }
}
