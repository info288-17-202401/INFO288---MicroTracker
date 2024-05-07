import "package:flutter/material.dart";

class LineList extends StatefulWidget {
  final List<int> lines;
  final List<int> linesSelected;
  final Function setLines;
  const LineList(
      {required this.linesSelected,
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
    return Center(
      child: Container(
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
          padding: EdgeInsets.all(8.0),
          child: Column(
            children: [
              for (final line in widget.lines)
                Text(
                  "Line $line",
                  style: TextStyle(
                    fontSize: 20,
                    inherit: false,
                    color: Colors.black,
                  ),
                ),
            ],
            mainAxisSize: MainAxisSize.min,
          ),
        ),
      ),
    );
  }
}
