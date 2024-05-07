import "package:flutter/material.dart";

class LineList extends StatefulWidget {
  final List<int> lines;
  final List<int> linesSelected;
  final Function setLines;
  final Function updateLines;
  final Function closePanel;
  const LineList(
      {required this.closePanel,
      required this.updateLines,
      required this.linesSelected,
      required this.setLines,
      required this.lines,
      Key? key})
      : super(key: key);

  @override
  _LineListState createState() => _LineListState();
}

class _LineListState extends State<LineList> {
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
                for (int i = 0; i < widget.lines.length; i++)
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    // mainAxisSize: MainAxisSize.min,
                    children: [
                      widget.linesSelected.contains(widget.lines[i])
                          ? IconButton(
                              onPressed: () {
                                setState(() {
                                  widget.linesSelected.remove(widget.lines[i]);
                                  widget.setLines(widget.linesSelected);
                                  widget.updateLines();
                                });
                              },
                              icon: const Icon(Icons.check_box),
                            )
                          : IconButton(
                              onPressed: () {
                                setState(() {
                                  widget.linesSelected.add(widget.lines[i]);
                                  widget.setLines(widget.linesSelected);
                                  widget.updateLines();
                                });
                              },
                              icon: const Icon(Icons.check_box_outline_blank),
                            ),
                      Text(
                        "Linea ${widget.lines[i]}",
                        style: const TextStyle(
                          fontSize: 20,
                          inherit: false,
                          color: Colors.black,
                        ),
                      ),
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
