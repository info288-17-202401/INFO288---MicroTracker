import "package:flutter/material.dart";
import "package:latlong2/latlong.dart";

class MapButton extends StatefulWidget {
  final Function onClick;
  final Icon icon;
  const MapButton({required this.icon, required this.onClick, Key? key})
      : super(key: key);

  @override
  _MapButtonState createState() => _MapButtonState();
}

class _MapButtonState extends State<MapButton> {
  @override
  Widget build(BuildContext context) {
    return Center(
      child: Container(
        decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(100),
            boxShadow: [
              BoxShadow(
                  color: Colors.black.withOpacity(0.2),
                  spreadRadius: 1,
                  blurRadius: 5)
            ],
            border: Border.all(color: Colors.blue, width: 2)),
        child: IconButton(
            color: Colors.blue,
            onPressed: () {
              widget.onClick();
            },
            icon: widget.icon),
      ),
    );
  }
}
