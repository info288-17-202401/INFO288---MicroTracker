class Prediction {
  String patent;
  int line;
  double distance;
  double time;
  Prediction({
    required this.patent,
    required this.line,
    required this.distance,
    required this.time,
  });

  Prediction.fromJson(Map<String, dynamic> json)
      : patent = json['patent'],
        line = json['line'],
        distance = json['distance'],
        time = json['time'];

  static List<Prediction> fromJsonList(List<dynamic> jsonList) {
    return jsonList.map((json) => Prediction.fromJson(json)).toList();
  }
}
