import "package:app/models/lineModel.dart";
import "package:dio/dio.dart";
import "package:flutter_dotenv/flutter_dotenv.dart";

class LineQuerys {
  final dio = Dio();

  Future<List<Line>> getLines() async {
    final response = await dio.get('${dotenv.env['API_URL']}/line');
    print("LINE QUERY");
    print(response.data);
    return Line.fromJsonList(response.data);
  }
}
