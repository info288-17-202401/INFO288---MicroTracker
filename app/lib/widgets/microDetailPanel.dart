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
    widget.closePanel();
    final response = await UbicationQuerys().getMicroRoute(id);
    widget.setCurrentRoute(response.route);
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
          child: Column(children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                Image.asset(
                    "assets/${context.watch<MicroProvider>().currentMicro.line}.png",
                    scale: 1.6),
                Column(
                  children: [
                    Text(context.watch<MicroProvider>().currentMicro.patent),
                    Text("Line")
                  ],
                )
              ],
            ),
            ElevatedButton(
                onPressed: () {
                  showRoute(Provider.of<MicroProvider>(context, listen: false)
                      .currentMicro
                      .line
                      .toString());
                },
                child: Text("Mostrar ruta"))
          ]),
        ),
      ),
    );
  }
}
