import "package:flutter/material.dart";
import "package:app/models/microModel.dart";

class MicroProvider with ChangeNotifier {
  Micro _currentMicro = Micro(
      id: "No seleccionado",
      patent: "No disponible",
      brand: "No disponible",
      model: "No disponible",
      line: 0,
      currentPosition: null);

  Micro get currentMicro => _currentMicro;

  void setCurrentMicro(Micro micro) {
    _currentMicro = micro;
    notifyListeners();
  }
}
