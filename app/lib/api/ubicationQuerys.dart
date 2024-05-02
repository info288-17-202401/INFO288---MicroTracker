import "package:flutter/material.dart";
import "package:app/models/microModel.dart";
import "package:dio/dio.dart";

class UbicationQuerys {
  final dio = Dio();
  Future<List<Micro>?> getMicrosCurrentPosition() async {
    final response =
        await dio.get("https://6633fb4f9bb0df2359a075b6.mockapi.io/api/micros");
    return Micro.fromJsonList(response.data);
  }
}
