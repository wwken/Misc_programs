package com.kw.datascience.userstats;

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.sql.SQLContext
import org.apache.spark.sql.SchemaRDD
import java.sql.Timestamp

// Define the schema using a case class.
case class User(name: String, ttime: Long);
case class Purchase(name: String, ttime: Long, quantity: Int);
case class Message(name: String, ttime: Long, count: Int);

object UserStats {
  
  val format = new java.text.SimpleDateFormat("yyyy-MM-dd");
  
  def toLong(s: String) : Long = {
    if(s.equalsIgnoreCase("na"))
    	0
    else
    	(format.parse(s).getTime / 1000.0).toLong
  }
  
  def toTimeStamp(l: Long) : String = {
    val s = (l * 1000)
    format.format(new java.sql.Timestamp(s))
  }
  
  def main(args: Array[String]) {
    //This line is just for place holder
    //val sc = new SparkContext("localhost", "hello" , "hello")
    val sparkConf = new SparkConf().setAppName("RDDRelation")
    val sc = new SparkContext(sparkConf)
    
    val sqlContext = new org.apache.spark.sql.SQLContext(sc);
    // Importing the SQL context gives access to all the SQL functions and implicit conversions.
    // createSchemaRDD is used to implicitly convert an RDD to a SchemaRDD.
    import sqlContext.createSchemaRDD;

    
    // Create an RDD of Person objects and register it as a table.
    val users = sc.textFile("/datawarehouse/csv/users.csv").zipWithIndex.collect({ case (x, n) if n > 0 => x }).map(_.split(",")).map(u => User(u(0), toLong(u(1))));
    users.registerTempTable("users");
    
    val purchases = sc.textFile("/datawarehouse/csv/purchases.csv").map(_.split(",")).zipWithIndex.collect({ case (x, n) if n > 0 => x }).map(p => Purchase(p(0), toLong(p(1)), p(2).trim.toInt));
    purchases.registerTempTable("purchases");
    
    val messages = sc.textFile("/datawarehouse/csv/messages.csv").map(_.split(",")).zipWithIndex.collect({ case (x, n) if n > 0 => x }).map(m => Message(m(0), toLong(m(1)), m(2).trim.toInt));
    messages.registerTempTable("messages");
    
    // 1) Question 1: What percentage of users make a purchase in their first 90 days after sign up (excluding their sign up day)?
    var allUsersPurchaseFirst90DaysTbl = sqlContext.sql("SELECT u.name as name, u.ttime as utime, p.ttime as ptime FROM users u JOIN purchases p on u.name = p.name where 0 < p.ttime - u.ttime and p.ttime - u.ttime < (24*3600*90) and p.quantity > 0");
    allUsersPurchaseFirst90DaysTbl.registerTempTable("allUsersPurchaseFirst90DaysTbl");
    val usersPurchaseFirst90DaysTbl = sqlContext.sql("SELECT a.name, a.utime, min(a.ptime) as eptime from allUsersPurchaseFirst90DaysTbl a group by a.name, a.utime");
    usersPurchaseFirst90DaysTbl.map(t => "Name:" + t(0) + ", u.td:" + toTimeStamp(t(1).toString.toLong) +",u.tt:" + t(1) + ",p.td:" + toTimeStamp(t(2).toString.toLong) + ",p.tt:" + t(2) + ",diff:"+(t(2).toString.toLong-t(1).toString.toLong)).collect().foreach(println);
    val count1 = usersPurchaseFirst90DaysTbl.count
    println(">>> # of users who make a purchase in their first 90 days after sign up (excluding their sign up day): " + count1)
    var allUsers = sqlContext.sql("select distinct(name) from users")
    val count2 = allUsers.count
    println(">>> # of users who sign up: " + count2)
    println(">>> 1) What percentage of users make a purchase in their first 90 days after sign up (excluding their sign up day)?: " + count1.toDouble / count2.toDouble)
    usersPurchaseFirst90DaysTbl.registerTempTable("usersPurchaseFirst90DaysTbl")	//Register this as temp table: allUsersRecordsMakePurchaseInFirst90DaysAfterSignUp
    usersPurchaseFirst90DaysTbl.cache	//Also cache it into memory so for speading up the next calculation
    
    // 2) Question 2: What percentage of users who purchased in the first 90 days received a message after their sign up date but before their first purchase date?
    val usersPurchaseFirst90DaysReceiveMessageInBetweenTbl = sqlContext.sql("select a.name, a.utime as utime, a.eptime as eptime, m.ttime as mtime from usersPurchaseFirst90DaysTbl a JOIN messages m on a.name=m.name where m.ttime > a.utime and m.ttime < a.eptime");
    usersPurchaseFirst90DaysReceiveMessageInBetweenTbl.map(t => "NName:" + t(0) + ", udate:" + toTimeStamp(t(1).toString.toLong) +",pdate:" + toTimeStamp(t(2).toString.toLong) + ",mdate:" + toTimeStamp(t(3).toString.toLong) + "").collect().foreach(println);
    val count3 = usersPurchaseFirst90DaysReceiveMessageInBetweenTbl.map(t => t(0).toString).distinct.count	//Just extract the name and distinct it
    println(">>> # of users who purchased in the first 90 days received a message after their sign up date but before their first purchase date: " + count3)
    println(">>> 2) What percentage of users who purchased in the first 90 days received a message after their sign up date but before their first purchase date?: " + count3.toDouble / count2.toDouble)
    
  }
}