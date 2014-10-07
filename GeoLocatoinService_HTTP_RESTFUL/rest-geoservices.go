package main

//go get github.com/StefanSchroeder/Golang-Ellipsoid

import "github.com/go-martini/martini"
import "strings"
import "strconv"
import "github.com/StefanSchroeder/Golang-Ellipsoid/ellipsoid"
import "fmt"
import "encoding/json"

func calDistance(l1 string, l2 string, l3 string, l4 string) string {
	lf1, _ := strconv.ParseFloat(l1, 64)
	lf2, _ := strconv.ParseFloat(l2, 64)
	lf3, _ := strconv.ParseFloat(l3, 64)
	lf4, _ := strconv.ParseFloat(l4, 64)
	
	// Create Ellipsoid object with WGS84-ellipsoid, 
    // angle units are degrees, distance units are meter.
    geo1 := ellipsoid.Init("WGS84", ellipsoid.Degrees, ellipsoid.Mile, ellipsoid.Longitude_is_symmetric, ellipsoid.Bearing_is_symmetric)

	distance, _ := geo1.To(lf1, lf2, lf3, lf4)
	return fmt.Sprintf("%.2f", distance)
}

func main() {
  m := martini.Classic()
  m.Get("/geoCalDistance/:laglongs", func(params martini.Params) string {
		s := strings.Split(params["laglongs"], ",")
		lag1, long1, lag2, long2 := s[0], s[1], s[2], s[3]
		//string lag1, long1, lag2, long2 = s[0],s[1],s[2],s[3]
		dis := calDistance(lag1, long1, lag2, long2)
		mapD := map[string]string{"lat1":lag1, "long1":long1, "lat2":lag2, "long2":long2, "distance_in_miles":dis}
		slcB, _ := json.Marshal(mapD)
		return string(slcB)
	})
  
  m.Run()
}
