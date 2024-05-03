import "package:app/pages/mapPage.dart";
import "package:app/providers/microProvider.dart";
import "package:app/widgets/microDetailPanel.dart";
import "package:flutter/material.dart";
import "package:latlong2/latlong.dart";
import "package:provider/provider.dart";
import "package:sliding_up_panel/sliding_up_panel.dart";

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int currentPageIndex = 0;
  List<LatLng> currentRoute = [];
  PanelController _panelController = new PanelController();

  void setCurrentRoute(List<LatLng> route) {
    setState(() {
      currentRoute = route;
    });
  }

  @override
  Widget build(BuildContext context) {
    return SlidingUpPanel(
      controller: _panelController,
      panel: MicroDetailPanel(
        closePanel: () {
          _panelController.close();
        },
        setCurrentRoute: setCurrentRoute,
      ),
      body: MapPage(
          openPanel: () {
            _panelController.open();
          },
          route: currentRoute),
      maxHeight: MediaQuery.of(context).size.height * 0.7,
      minHeight: MediaQuery.of(context).size.height * 0.03,
      color: Colors.transparent,
      renderPanelSheet: false,
    );
  }
}
