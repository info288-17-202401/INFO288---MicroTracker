import "package:flutter/material.dart";
import 'package:app/providers/microProvider.dart';
import "package:provider/provider.dart";
import "package:sliding_up_panel/sliding_up_panel.dart";

class MicroDetailPanel extends StatefulWidget {
  const MicroDetailPanel({Key? key}) : super(key: key);

  @override
  _MicroDetailPanelState createState() => _MicroDetailPanelState();
}

class _MicroDetailPanelState extends State<MicroDetailPanel> {
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
          )
        ]),
      ),
    );
  }
}
