import "package:app/widgets/lineList.dart";
import "package:app/widgets/mapButton.dart";
import "package:flutter/material.dart";
import "package:flutter_map/flutter_map.dart";
import "package:latlong2/latlong.dart";
import "package:app/models/microModel.dart";
import "package:app/api/ubicationQuerys.dart";
import 'package:app/providers/microProvider.dart';
import "package:location/location.dart";
import "package:provider/provider.dart";
import "package:app/library/animated_map_controller.dart";

class MapPage extends StatefulWidget {
  final List<LatLng> route;
  final Function openPanel;
  final List<int> linesSelected;
  final Function setLines;
  final List<int> lines;
  const MapPage(
      {required this.lines,
      required this.setLines,
      required this.linesSelected,
      required this.route,
      required this.openPanel,
      Key? key})
      : super(key: key);

  @override
  _MapPageState createState() => _MapPageState();
}

class _MapPageState extends State<MapPage> with TickerProviderStateMixin {
  late final _animatedMapController = AnimatedMapController(vsync: this);
  bool showLines = false;
  LatLng initialCenter = LatLng(-39.819955, -73.241229);
  double initialZoom = 16;
  List<Micro> micros = [];
  LatLng? _currentPosition;
  Location location = Location();

  @override
  void initState() {
    super.initState();
    getCurrentPosition();
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
        micros = response
            .where((micro) => widget.linesSelected.contains(micro.line))
            .toList();
      });
    }
    print("MICROS UPDATED");
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
          mapController: _animatedMapController.mapController,
          options: MapOptions(
            initialCenter: initialCenter,
            initialZoom: initialZoom,
          ),
          children: [
            TileLayer(
              urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
              userAgentPackageName: 'dev.fleaflet.flutter_map.example',
            ),
            PolylineLayer(polylines: [
              Polyline(
                color: Colors.blue,
                strokeWidth: 8.0,
                points: widget.route,
              )
            ]),
            MarkerLayer(markers: [
              _currentPosition == null
                  ? Marker(
                      point: initialCenter,
                      child: Icon(Icons.person_pin_circle),
                    )
                  : Marker(
                      point: _currentPosition!,
                      alignment: const Alignment(-0.5, -2),
                      child: Icon(
                        Icons.person_pin_circle,
                        color: Colors.blue,
                        size: 50,
                      ),
                    ),
              for (final micro in micros)
                Marker(
                    width: 80.0,
                    height: 80.0,
                    point: micro.currentPosition!,
                    key: Key(micro.id.toString()),
                    child: GestureDetector(
                      onTap: () {
                        context.read<MicroProvider>().setCurrentMicro(micro);
                        widget.openPanel();
                        _animatedMapController.animateTo(
                            dest: micro.currentPosition!, zoom: initialZoom);
                      },
                      child: Image.asset("assets/${micro.line}.png"),
                    )),
            ]),
          ],
        ),
        showLines
            ? LineList(
                updateLines: getMicrosPosition,
                lines: widget.lines,
                setLines: widget.setLines,
                linesSelected: widget.linesSelected,
                closePanel: () {
                  setState(() {
                    showLines = false;
                  });
                },
              )
            : SizedBox.shrink(),
        Positioned(
            bottom: MediaQuery.of(context).size.height * 0.1,
            right: 20,
            child: Column(
              children: [
                MapButton(
                    icon: Icon(Icons.line_style),
                    onClick: () {
                      setState(() {
                        showLines = !showLines;
                      });
                    }),
                MapButton(
                    icon: Icon(Icons.gps_fixed),
                    onClick: () {
                      _animatedMapController.animateTo(
                          dest: _currentPosition!, zoom: initialZoom);
                    })
              ],
            ))
      ]),
    );
  }
}
