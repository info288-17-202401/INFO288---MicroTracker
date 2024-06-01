import "package:app/models/microModel.dart";
import "package:app/models/routeModel.dart";
import "package:dio/dio.dart";
import "package:flutter_dotenv/flutter_dotenv.dart";

class UbicationQuerys {
  final dio = Dio();
  Future<List<Micro>> getMicrosCurrentPosition() async {
    final response = await dio.get('${dotenv.env['API_URL']}/microbus');
    return Micro.fromJsonList(response.data);
  }

  Future<Route> getMicroRoute(String id) async {
    final response = await dio
        .get("https://6633fb4f9bb0df2359a075b6.mockapi.io/api/routes/$id");
    print(response.data);
    return Route.fromJson(response.data);
  }
}
