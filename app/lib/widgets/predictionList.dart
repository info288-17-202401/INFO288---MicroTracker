import "package:app/models/predictionModel.dart";
import "package:flutter/material.dart";

class PredictionList extends StatefulWidget {
  final List<Prediction> predictions;
  final Function closePanel;
  const PredictionList(
      {required this.closePanel, required this.predictions, Key? key})
      : super(key: key);

  @override
  _PredictionListState createState() => _PredictionListState();
}

class _PredictionListState extends State<PredictionList> {
  @override
  Widget build(BuildContext context) {
    return Stack(children: [
      GestureDetector(
        onTap: () {
          widget.closePanel();
        },
        child: Container(
          color: Colors.transparent,
        ),
      ),
      Center(
        child: Container(
          width: 200,
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(20),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.2),
                spreadRadius: 1,
                blurRadius: 5,
              )
            ],
          ),
          child: Padding(
            padding: const EdgeInsets.all(8.0),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                for (int i = 0; i < widget.predictions.length; i++)
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    // mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(widget.predictions[i].patent.toString()),
                      Text(widget.predictions[i].line.toString()),
                      Text(widget.predictions[i].time.toString())
                    ],
                  )
              ],
            ),
          ),
        ),
      ),
    ]);
  }
}
