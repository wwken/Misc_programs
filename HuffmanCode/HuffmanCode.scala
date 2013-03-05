/**
 * @author ken Wu
 * @date 01/03/2013
 *
 *  Huffman code:
	
	E.g. 
	Input: huffman1(List(("a", 90), ("b", 35), ("c", 67), ("d", 2), ("e", 13), ("f", 20), ("g", 39)))
	output: List((g,00), (c,01), (b,100), (d,10100), (e,10101), (f,1011), (a,11))
 * 
 */

object HuffmanCode {
  abstract class N[X] {
    val freq: Int
    def toStr: List[(X, String)] = toStrPre("")
    def toStrPre(prefix: String): List[(X, String)]
  }
  case class INode[X](left: N[X], right: N[X]) extends N[X] {
    val freq: Int = left.freq + right.freq
    def toStrPre(prefix: String): List[(X, String)] =
      left.toStrPre(prefix + "0") ::: right.toStrPre(prefix + "1")
  }
  case class Node[X](element: X, freq: Int) extends N[X] {
    def toStrPre(prefix: String): List[(X, String)] = List((element, prefix))
  }

  def huffman1[X](ls: List[(X, Int)]): List[(X, String)] = {
    import collection.immutable.Queue
    def getSmallest(q1: Queue[N[X]], q2: Queue[N[X]]) = {
      if ( !q2.isEmpty && ( q1.isEmpty || q2.front.freq < q1.front.freq)) {
        (q2.front, q1, q2.dequeue._2)
      }
      else {
        (q1.front, q1.dequeue._2, q2)
      }
    }
    def huffman2(q1: Queue[N[X]], q2: Queue[N[X]]): List[(X, String)] = {
      if (q1.length == 0 && q2.length == 1) (q2.front).toStr
      else {
        val (v1, q3, q4) = getSmallest(q1, q2)
        //println(v1 + ", " + q3 + ", " + q4)
        val (v2, q5, q6) = getSmallest(q3, q4)
        huffman2(q5, q6.enqueue(INode(v1, v2)))
      }
    }
    huffman2(Queue.Empty.enqueue(ls sort { _._2 < _._2 } map { elem => Node(elem._1, elem._2) }), Queue.Empty)
  }
 
  
  def main(args: Array[String]): Unit = {}
}
