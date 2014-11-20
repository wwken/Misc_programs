
<b>To build the jar file, run:</b>
	mvn clean package

After building it, we are ready to run it.  But before that, we need to download the sample data.  For now, this program can only process the WikiPedia dump dataset which can be obtained from: http://dumps.wikimedia.org/enwiki/  We can pick any thing from there to download.  

<b>Assuming we downloaded the towiki-latest-pages-articles.xml.bz2 in the Downloads folder and our neo4j is installed in /usr/local/neo4j-community-2.1.5/, here is the way to run the program:</b>

	bzip2 -dc ~/Downloads/towiki-latest-pages-articles.xml.bz2 | java -classpath ./target/neo4jDataImport-1.0-SNAPSHOT.jar com.wwken.neo4jdataimport.DataImporterRunner towiki-links.xml /usr/local/neo4j-community-2.1.5/data/graph.db

where the program will read the standard input as piped from decompressing the compressed bz2 wiki data file and take two arguments (the first argument can be any file name which you want to store the intermedium xml parsed data and the second parameter, as mentioned above, is the Neo4j path installed locally). 

Now the Neo4j database should have all the above data populated.

Here is the related blog: http://wwken.wordpress.com/2014/11/20/tutorial-how-to-bulk-import-wikipedia-data-into-the-neo4j-graph-database-programatically/


