import "package:app/api/ubicationQuerys.dart";
import "package:flutter/material.dart";
import 'package:app/providers/microProvider.dart';
import "package:latlong2/latlong.dart";
import "package:provider/provider.dart";

class MicroDetailPanel extends StatefulWidget {
  final Function closePanel;
  final Function setCurrentRoute;
  const MicroDetailPanel(
      {required this.setCurrentRoute, required this.closePanel, Key? key})
      : super(key: key);

  @override
  _MicroDetailPanelState createState() => _MicroDetailPanelState();
}

class _MicroDetailPanelState extends State<MicroDetailPanel> {
  void showRoute(String id) async {
    if (id != "0") {
      widget.closePanel();
      final response = await UbicationQuerys().getMicroRoute(id);
      widget.setCurrentRoute(response.route);
    } else {
      print("Error: No se puede mostrar la ruta de un micro sin id");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.7),
        border: Border.all(color: Colors.black, width: 2),
        borderRadius: BorderRadius.all(Radius.circular(50)),
      ),
      margin: EdgeInsets.only(left: 20, right: 20, bottom: 40),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Center(
          child: Column(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    Image.asset(
                        "assets/${context.watch<MicroProvider>().currentMicro.line}.png",
                        scale: 1.6),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          context.watch<MicroProvider>().currentMicro.patent,
                          style: const TextStyle(
                              color: Colors.black,
                              fontSize: 25,
                              inherit: false,
                              fontWeight: FontWeight.bold),
                        ),
                        Text(
                          "Line: ${context.watch<MicroProvider>().currentMicro.line}",
                          style: const TextStyle(
                              color: Colors.black,
                              fontSize: 30,
                              inherit: false),
                        ),
                        ElevatedButton(
                            onPressed: () {
                              showRoute(Provider.of<MicroProvider>(context,
                                      listen: false)
                                  .currentMicro
                                  .line
                                  .toString());
                            },
                            child: Text("Mostrar ruta"))
                      ],
                    )
                  ],
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    Image.asset("assets/passenger.png", scale: 1.6),
                    Text(
                      "Pasajeros: ",
                      style: const TextStyle(
                          color: Colors.black, fontSize: 20, inherit: false),
                    ),
                    Text(
                      context
                          .watch<MicroProvider>()
                          .currentMicro
                          .passengers
                          .toString(),
                      style: const TextStyle(
                          color: Colors.black, fontSize: 20, inherit: false),
                    )
                  ],
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    Image.asset("assets/speedometer.png", scale: 1.6),
                    Text(
                      "Velocidad \nPromedio: ",
                      style: const TextStyle(
                          color: Colors.black, fontSize: 20, inherit: false),
                    ),
                    Text(
                      context
                          .watch<MicroProvider>()
                          .currentMicro
                          .velocity
                          .toString(),
                      style: const TextStyle(
                          color: Colors.black, fontSize: 20, inherit: false),
                    )
                  ],
                ),
              ]),
        ),
      ),
    );
  }
}
