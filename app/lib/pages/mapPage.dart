import "package:flutter/material.dart";
import "package:flutter_map/flutter_map.dart";
import "package:latlong2/latlong.dart";
import "package:app/models/microModel.dart";
import "package:app/api/ubicationQuerys.dart";
import 'package:app/providers/microProvider.dart';
import "package:provider/provider.dart";

class MapPage extends StatefulWidget {
  final Function openPanel;
  const MapPage({required this.openPanel, Key? key}) : super(key: key);

  @override
  _MapPageState createState() => _MapPageState();
}

class _MapPageState extends State<MapPage> {
  late MapController mapController;
  LatLng initialCenter = LatLng(-39.819955, -73.241229);
  double initialZoom = 16;
  List<int> linesSelected = [1];
  List<Micro> micros = [];

  @override
  void initState() {
    super.initState();
    mapController = MapController();
    getMicrosPosition();
  }

  @override
  void dispose() {
    super.dispose();
  }

  void getMicrosPosition() async {
    final response = await UbicationQuerys().getMicrosCurrentPosition();
    if (response != null) {
      setState(() {
        micros = response;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: MediaQuery.of(context).size.height,
      child: Stack(children: [
        FlutterMap(
          mapController: mapController,
          options: MapOptions(
            initialCenter: initialCenter,
            initialZoom: initialZoom,
          ),
          children: [
            TileLayer(
              urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
              userAgentPackageName: 'dev.fleaflet.flutter_map.example',
            ),
            MarkerLayer(markers: [
              for (final micro in micros)
                Marker(
                    width: 80.0,
                    height: 80.0,
                    point: micro.currentPosition!,
                    key: Key(micro.id.toString()),
                    child: IconButton(
                      icon: Icon(
                        Icons.fire_truck,
                        color: context.watch<MicroProvider>().currentMicro.id ==
                                micro.id
                            ? Colors.red
                            : Colors.blue,
                      ),
                      onPressed: () {
                        context.read<MicroProvider>().setCurrentMicro(micro);
                        widget.openPanel();
                      },
                      iconSize: 80,
                    )),
            ])
          ],
        ),
      ]),
    );
  }
}
