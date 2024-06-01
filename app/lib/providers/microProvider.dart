import "package:flutter/material.dart";
import "package:app/models/microModel.dart";
import "package:latlong2/latlong.dart";

class MicroProvider with ChangeNotifier {
  Micro _currentMicro = Micro(
      // id: "No seleccionado",
      patent: "None",
      brand: 0,
      // model: "No disponible",
      line: 0,
      currentPosition: null);
  List<LatLng?> _currentRoute = [];

  Micro get currentMicro => _currentMicro;
  List<LatLng?> get currentRoute => _currentRoute;

  void setCurrentMicro(Micro micro) {
    _currentMicro = micro;
    notifyListeners();
  }

  void setCurrentRoute(List<LatLng?> route) {
    _currentRoute = route;
    notifyListeners();
  }
}
