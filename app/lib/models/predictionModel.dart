class Prediction {
  String microbus_id;
  int line_id;
  double distance;
  double time;
  Prediction({
    required this.microbus_id,
    required this.line_id,
    required this.distance,
    required this.time,
  });

  Prediction.fromJson(Map<String, dynamic> json)
      : microbus_id = json['microbus_id'],
        line_id = json['line_id'],
        distance = json['distance'],
        time = json['time'];

  static List<Prediction> fromJsonList(List<dynamic> jsonList) {
    return jsonList.map((json) => Prediction.fromJson(json)).toList();
  }
}
