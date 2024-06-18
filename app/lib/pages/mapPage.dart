import "package:app/api/paraderosQuerys.dart";
import "package:app/models/paraderoModel.dart";
import "package:app/models/predictionModel.dart";
import "package:app/widgets/lineList.dart";
import "package:app/widgets/predictionList.dart";
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
import "package:flutter_dotenv/flutter_dotenv.dart";

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
  bool showPredictions = false;
  LatLng initialCenter = LatLng(-39.819955, -73.241229);
  double initialZoom = 16;
  List<Micro> micros = [];
  List<Prediction> predictions = [];
  List<Paradero> paraderos = [];
  LatLng? _currentPosition;
  Location location = Location();

  @override
  void initState() {
    super.initState();
    getCurrentPosition();
    getMicrosPosition();
    getParaderos();
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

  void getParaderos() async {
    final response = await ParaderoQuerys().getParaderos();
    if (response != null) {
      setState(() {
        paraderos = response;
      });
    }
  }

  void getPredictions(int paraderoId) async {
    final response =
        await ParaderoQuerys().getPredictions(widget.linesSelected, paraderoId);
    print(response);
    if (response != null) {
      setState(() {
        predictions = response;
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
              for (final paradero in paraderos)
                _animatedMapController.mapController.camera.zoom >= 14
                    ? Marker(
                        width: 30.0,
                        height: 30.0,
                        point: paradero.position,
                        key: Key(paradero.id.toString()),
                        child: GestureDetector(
                            onTap: () {
                              setState(() {
                                showPredictions = true;
                              });
                              getPredictions(paradero.id);
                              print("Paradero ${paradero.id} clicked");
                              print('ENV: ${dotenv.env['API_URL']}');
                            },
                            child: Image.asset("assets/paradero.png")))
                    : Marker(point: paradero.position, child: Container()),
              for (final micro in micros)
                Marker(
                    width: 80.0,
                    height: 80.0,
                    point: micro.currentPosition!,
                    key: Key(micro.patent.toString()),
                    child: GestureDetector(
                      onTap: () {
                        context.read<MicroProvider>().setCurrentMicro(micro);
                        widget.openPanel();
                        _animatedMapController.animateTo(
                            dest: micro.currentPosition!, zoom: initialZoom);
                      },
                      child: Image.asset("assets/${micro.line}.png"),
                    )),
              _currentPosition == null
                  ? Marker(
                      point: initialCenter,
                      child: Icon(Icons.person_pin_circle),
                      width: 0.0,
                    )
                  : Marker(
                      width: 50.0,
                      height: 50.0,
                      point: _currentPosition!,
                      child: Transform.translate(
                        offset: Offset(
                            0, -25), // Ajusta este valor según sea necesario
                        child:
                            Image.asset("assets/userUbication.png", scale: 1.6),
                      ),
                    ),
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
        showPredictions
            ? PredictionList(
                closePanel: () {
                  setState(() {
                    showPredictions = false;
                  });
                },
                predictions: predictions)
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
