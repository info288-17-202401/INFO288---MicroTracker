import "package:app/models/paraderoModel.dart";
import "package:app/models/predictionModel.dart";
import "package:dio/dio.dart";
import "package:flutter_dotenv/flutter_dotenv.dart";

class ParaderoQuerys {
  final dio = Dio();

  Future<List<Paradero>> getParaderos() async {
    final response = await dio.get('${dotenv.env['API_URL']}/paraderos');
    return Paradero.fromJsonList(response.data);
  }

  Future<List<Prediction>> getPredictions(
      List<int> selectedLines, int paraderoId) async {
    final response = await dio.get('${dotenv.env['API_URL']}/prediction/',
        data: {"lines": selectedLines, "paraderoId": paraderoId});
    return Prediction.fromJsonList(response.data);
  }
}
