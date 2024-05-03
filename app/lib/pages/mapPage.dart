import "package:flutter/material.dart";
import "package:flutter_map/flutter_map.dart";
import "package:latlong2/latlong.dart";
import "package:app/models/microModel.dart";
import "package:app/api/ubicationQuerys.dart";
import 'package:app/providers/microProvider.dart';
import "package:location/location.dart";
import "package:provider/provider.dart";

class MapPage extends StatefulWidget {
  final List<LatLng> route;
  final Function openPanel;
  const MapPage({required this.route, required this.openPanel, Key? key})
      : super(key: key);

  @override
  _MapPageState createState() => _MapPageState();
}

class _MapPageState extends State<MapPage> {
  late MapController mapController;
  LatLng initialCenter = LatLng(-39.819955, -73.241229);
  double initialZoom = 16;
  List<int> linesSelected = [1];
  List<Micro> micros = [];
  LatLng? _currentPosition;
  Location location = Location();

  @override
  void initState() {
    super.initState();
    getCurrentPosition();
    mapController = MapController();
    getMicrosPosition();
    location.onLocationChanged.listen((LocationData newPosition) {
      setState(() {
        _currentPosition =
            LatLng(newPosition.latitude!, newPosition.longitude!);
      });
      print("CURRENT POSITION CHANGED");
      getMicrosPosition();
    });
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

  Future<LocationData> getLocation() async {
    bool _serviceEnabled;
    PermissionStatus _permissionGranted;

    _serviceEnabled = await location.serviceEnabled();
    if (!_serviceEnabled) {
      _serviceEnabled = await location.requestService();
      if (!_serviceEnabled) {
        return Future.error("Error: Servicio de ubicación no habilitado.");
      }
    }

    _permissionGranted = await location.hasPermission();
    if (_permissionGranted == PermissionStatus.denied) {
      _permissionGranted = await location.requestPermission();
      if (_permissionGranted != PermissionStatus.granted) {
        return Future.error("Error: Permiso de ubicación denegado.");
      }
    }
    return await location.getLocation();
  }

  void getCurrentPosition() async {
    try {
      LocationData xd = await getLocation();
      setState(() {
        _currentPosition = LatLng(xd.latitude!, xd.longitude!);
      });
    } catch (e) {
      print("ERROR EN GETCURRENTPOSITION FUNCTION: $e");
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
              _currentPosition == null
                  ? Marker(
                      point: initialCenter,
                      child: Icon(Icons.location_city),
                    )
                  : Marker(
                      point: _currentPosition!,
                      child: Icon(Icons.location_city)),
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
            ]),
            PolylineLayer(polylines: [
              Polyline(
                color: Colors.blue,
                strokeWidth: 8.0,
                points: widget.route,
              )
            ])
          ],
        ),
      ]),
    );
  }
}
