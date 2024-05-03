import "package:app/api/ubicationQuerys.dart";
import "package:flutter/material.dart";
import 'package:app/providers/microProvider.dart';
import "package:latlong2/latlong.dart";
import "package:provider/provider.dart";

class MicroDetailPanel extends StatefulWidget {
  final Function closePanel;
  const MicroDetailPanel({required this.closePanel, Key? key})
      : super(key: key);

  @override
  _MicroDetailPanelState createState() => _MicroDetailPanelState();
}

class _MicroDetailPanelState extends State<MicroDetailPanel> {
  List<LatLng> route = [];
  void getRoute(String id) async {
    final response = await UbicationQuerys().getMicroRoute(id);
    if (response != null) {
      setState(() {
        route = response.route;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.all(Radius.circular(50))),
      margin: EdgeInsets.only(left: 20, right: 20, bottom: 40),
      child: Center(
        child: Column(children: [
          Text("MicroDetail"),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              Text("Image"),
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
                getRoute(Provider.of<MicroProvider>(context, listen: false)
                    .currentMicro
                    .line
                    .toString());
                context.read<MicroProvider>().setCurrentRoute(route);
                widget.closePanel();
              },
              child: Text("Mostrar ruta"))
        ]),
      ),
    );
  }
}
