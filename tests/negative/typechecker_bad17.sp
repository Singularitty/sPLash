add:Int (a:Double, b:Int) {
  return a + b;
}

multiply:String (x:Int, y:Int) {
  return x * y;
}


main:Int () {
  a:String = 5;
  b:Double = "7";
  c:Int = add(a, b);
  d:String = multiply(c, 10);
  e:Int = d + "oops";
  return e;
}