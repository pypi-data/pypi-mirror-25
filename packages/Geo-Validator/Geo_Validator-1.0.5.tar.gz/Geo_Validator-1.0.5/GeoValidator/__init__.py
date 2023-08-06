#!/usr/bin/python


def main():
    import csv,googlemaps,math, sys                               
    
    
    
    Key   = "AIzaSyB_eSK2KDuLVIN5TSN8evQMEclngev5ZE4" #Google Maps API Key Mush have GeoCode key 
    noise = .001                                      #Distance from Location coords that a coord is conciderd correct
    
    
    try:
        map   = googlemaps.Client(Key)
    except:
        print("Non operable Key")
        quit()
    if len(sys.argv) != 3:
        print("please use geofencingValidator.py <input.csv> <output.csv>")
        quit()
                                         
    
    try:
        f     = open(sys.argv[1],newline='')
    
    except:
        print(sys.argv[1]," is in use or non existant!")
        quit()
    try:
        w     = open(sys.argv[2], 'w', newline='')
    
    except:
        print(sys.argv[2],"is in use or non existant!")
        quit()
    
    write = csv.writer(w, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL) 
    read  = csv.reader(f, delimiter='\t', quotechar='|')                          
    array = []
    print("Running...")
    
    for row in read:
        array.append("".join(row))
    for item in array:
        temparray = item.split('"')
        try:
            
            street       = ""
            output       = ""
            check        = temparray[1]
            checkarray   = check.split(",")
            correctarray = [0] * len(checkarray)
            latlon       = temparray[2].lstrip(",")
            lat,lon      = (temparray[2].lstrip(",")).split(",")
            addresses    = map.reverse_geocode(latlon,"","","english")
            
            for address in addresses:
                for component in address["address_components"]:
                    if component["types"][0] == "street_number":
                        street += component["long_name"]
                    if component["types"][0] == "route":
                        street += " " +component["short_name"]
                    try:
                        i = checkarray.index(street)
                        correctarray[i] = 1
                    except ValueError:
                        pass
                    try:
                        i = checkarray.index(" "+component["long_name"])
                        correctarray[i] = 1
                    except ValueError:
                        pass
                    try:
                        i = checkarray.index(" "+component["short_name"])
                        correctarray[i] = 1
                    except ValueError:
                        pass
    
    
            location = map.geocode(check)
            lon2     = location[0]['geometry']['location']['lng']
            lat2     = location[0]['geometry']['location']['lat']
            distlon  = (float(lon) - float(lon2))
            distlat  = float(lat) -float(lat2)
            dist     = math.sqrt((distlon**2)+(distlon**2))
            
            
            if correctarray[-1] == 1:
                output = "Right Country"
            if correctarray[-2] == 1:
                output = "Right State"
            if correctarray[-3] == 1:
                output = "Right City"
            if correctarray[-4] == 1:
                output = "Right Place"
            if dist < noise:
                output = "Right Place"
            if output == "":
                outout = "Wrong Country"
            output += " Distance is: " + str(dist)
            
            write.writerow([check,lat,lon,output])
        except:
            pass
        
    print("done")
    f.close()
    w.close()

    