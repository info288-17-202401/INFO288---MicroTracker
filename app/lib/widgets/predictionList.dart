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
          width: 350,
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
              children: widget.predictions.isEmpty
                  ? [
                      Text(
                        "No hay microbuses en camino",
                        style: TextStyle(
                            color: Colors.grey,
                            inherit: false,
                            fontWeight: FontWeight.bold,
                            fontSize: 20),
                      )
                    ]
                  : [
                      for (int i = 0; i < widget.predictions.length; i++)
                        Container(
                          decoration: BoxDecoration(
                            border: Border.all(
                              color: Colors.black.withOpacity(0.5),
                            ),
                            borderRadius: BorderRadius.circular(20),
                          ),
                          padding: EdgeInsets.all(10),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceAround,
                            // mainAxisSize: MainAxisSize.min,
                            children: [
                              Image.asset(
                                "assets/${widget.predictions[i].line_id}.png",
                                scale: 4.0,
                              ),
                              Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Row(
                                    children: [
                                      const Text(
                                        "Microbus ",
                                        style: TextStyle(
                                          fontSize: 18,
                                          color: Colors.black,
                                          inherit: false,
                                        ),
                                      ),
                                      Text(
                                        widget.predictions[i].microbus_id
                                            .toString(),
                                        style: const TextStyle(
                                          fontSize: 18,
                                          color: Colors.black,
                                          inherit: false,
                                          fontWeight: FontWeight.bold,
                                        ),
                                      ),
                                    ],
                                  ),
                                  Row(
                                    children: [
                                      const Text(
                                        "a ",
                                        style: TextStyle(
                                          fontSize: 15,
                                          color: Colors.black,
                                          inherit: false,
                                        ),
                                      ),
                                      Text(
                                        "${widget.predictions[i].distance} m",
                                        style: const TextStyle(
                                          fontSize: 15,
                                          color: Colors.black,
                                          inherit: false,
                                          fontWeight: FontWeight.bold,
                                        ),
                                      ),
                                    ],
                                  )
                                ],
                              ),
                              Column(
                                children: [
                                  const Text(
                                    "Llega en",
                                    style: TextStyle(
                                      fontSize: 18,
                                      color: Colors.black,
                                      inherit: false,
                                    ),
                                  ),
                                  Text(
                                    "${widget.predictions[i].time} min",
                                    style: const TextStyle(
                                      fontSize: 18,
                                      color: Colors.black,
                                      inherit: false,
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                ],
                              ),
                            ],
                          ),
                        )
                    ],
            ),
          ),
        ),
      ),
    ]);
  }
}
