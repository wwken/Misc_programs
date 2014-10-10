package main

import (
  "testing"
  //"fmt"
  "strconv"
  "os"
  "log"
  "bufio"
  "strings"
  "net/http"
  //"fmt"
)

/* ********************************************************************************
 * Start: Helper function
 * ********************************************************************************
 */ 
func readLinesFromAPath (path string) []string {
	file, err := os.Open(path)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	var allLines []string
	for scanner.Scan() {
		allLines = append(allLines, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	return allLines
}
/* ********************************************************************************
 * End: Helper function
 * ********************************************************************************
 */ 

func Test_calDistance(t *testing.T) {
   res := calDistance("39.768434","-104.901872","44.7793732","-63.6734886")
   f, _ := strconv.ParseFloat(res, 64)
   if (f < 2118 || f > 2119) {
		t.Error("Excepted 2118 miles, but got ", f)
	}
	
   res1 := calDistance("0.00","0.00","0.00","0.00")
   f1, _ := strconv.ParseFloat(res1, 64)
   if ( f1 != 0) {
	   t.Error("Excepted 0 mile, but got ", f1)
   }
}

var g_allLines = readLinesFromAPath("data/gis-test-data-no-dist_km.csv")

func Benchmark_calDistance(b *testing.B) {
	for i := 0; i < b.N; i++ {
		for _, line := range g_allLines {
			s := strings.Split(line, ",")
			lat1, long1, lat2, long2 := s[1], s[2], s[3], s[4]
			calDistance(lat1,long1,lat2,long2)
			//println("There are", res, "miles from", lat1, long1, lat2, long2) 
		}
	}
}

func Benchmark_calDistanceService(b *testing.B) {
	for i := 0; i < b.N; i++ {
		for _, line := range g_allLines {
			s := strings.Split(line, ",")
			lat1, long1, lat2, long2 := s[1], s[2], s[3], s[4]
			_, err := http.Get("http://localhost:3000/geoCalDistance/"+lat1+","+long1+","+lat2+","+long2)
			if err != nil {
				log.Fatal(err)
			} else {
				println("Response obtained sucessfully!")
			}
			//println("There are", res, "miles from", lat1, long1, lat2, long2) 
		}
	}
	
}
