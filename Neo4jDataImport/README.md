<pre>
<b>To build the jar file, run:</b>
	mvn clean package

<b>Assuming we downloaded the towiki-latest-pages-articles.xml.bz2 as the wiki data file and our neo4j is installed in /usr/local/neo4j-community-2.1.5/, here is the way to run the program:</b>

	bzip2 -dc ~/Downloads/towiki-latest-pages-articles.xml.bz2 | java -classpath ./target/neo4jDataImport-1.0-SNAPSHOT.jar com.wwken.neo4jdataimport.DataImporterRunner towiki-links.xml /usr/local/neo4j-community-2.1.5/data/graph.db

Now the Neo4j database should have all the above data populated

</pre>
