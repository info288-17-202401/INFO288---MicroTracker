class Line {
  int number;
  String color;

  Line({
    required this.number,
    required this.color,
  });

  Line.fromJson(Map<String, dynamic> json)
      : number = json['number'],
        color = json['color'];

  static List<Line> fromJsonList(List<dynamic> jsonList) {
    return jsonList.map((json) => Line.fromJson(json)).toList();
  }
}
