import "package:app/api/lineQuerys.dart";
import "package:app/models/lineModel.dart";
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
  List<int> linesSelected = [1];
  List<int> lines = [];
  PanelController _panelController = new PanelController();

  @override
  void initState() {
    super.initState();
    getLines();
    // setState(() {
    //   lines = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    // });
  }

  void setCurrentRoute(List<LatLng> route) {
    setState(() {
      currentRoute = route;
    });
  }

  void getLines() async {
    List<Line> response = await LineQuerys().getLines();
    List<int> linesNumbers = response.map((line) => line.number).toList();
    print(linesNumbers);
    setState(() {
      lines = linesNumbers;
    });
    setState(() {
      linesSelected = [linesNumbers[0]];
    });
  }

  void setLinesSelected(List<int> lines) {
    setState(() {
      linesSelected = lines;
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
          lines: lines,
          setLines: setLinesSelected,
          linesSelected: linesSelected,
          openPanel: () {
            _panelController.open();
          },
          route: currentRoute),
      maxHeight: MediaQuery.of(context).size.height * 0.4,
      minHeight: MediaQuery.of(context).size.height * 0.03,
      color: Colors.transparent,
      renderPanelSheet: false,
    );
  }
}
