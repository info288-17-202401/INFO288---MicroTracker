import 'package:app/pages/homePage.dart';
import 'package:flutter/material.dart';
import "package:provider/provider.dart";
import "package:app/providers/microProvider.dart";

void main() {
  runApp(MultiProvider(providers: [
    ChangeNotifierProvider(create: (_) => MicroProvider()),
  ], child: const MyApp()));
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Flutter Demo',
      theme: ThemeData.dark(),
      home: const HomePage(),
    );
  }
}
