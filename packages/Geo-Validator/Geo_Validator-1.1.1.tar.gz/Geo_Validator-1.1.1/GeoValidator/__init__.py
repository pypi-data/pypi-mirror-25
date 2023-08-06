#!/usr/bin/python


def main():
    import csv,googlemaps,math, sys                 #imports:
                                                        #csv: allows editing .csv files
                                                        #googlemaps: gets lat/long from address or address form lat/long
                                                        #math
                                                        #sys
    try:                                            #Imports congfig file datat
        cfg = open(os.path.join(os.path.dirname(__file__), 'config.cfg'),"r")       
        for line in cfg:
            linearray  = line.split('=')
            if linearray[0].strip() == "Key":             #config key must be valid googlemaps api key for geocode
                Key     = str(linearray[1].strip("\n"))
            if linearray[0].strip() == "noise":           #noise float smaller = more acurate
                noise   = float(linearray[1].strip("\n"))
            if linearray[0].strip() == "debug":           #debug mode
                if linearray[1].strip("\n") == 'False':
                    debug = False
                else:
                    debug = True
        Key                     #makes sure vars are defined
        noise
        debug
    except:
        print("config file not correct") #catches andy config errors
        quit()
    
    try:                              #trys to access googlemaps api
        map   = googlemaps.Client(Key)
    except:
        print("Cant access googlemaps")   
        quit()
        
    if len(sys.argv) != 3:           #makes sure there is the proper amount of inputs
        print("please use geofencingValidator.py <input.csv> <output.csv>")
        quit()
                                         
    
    try:                           #tests for input file 
        f     = open(sys.argv[1],newline='')
    
    except:
        print(sys.argv[1]," is non existant!")
        quit()
    try:                          #tests to see if output file is accessable or creatable
        w     = open(sys.argv[2], 'w', newline='')
    
    except:
        print(sys.argv[2],"is in use or cannot be created!")
        quit()
    
    write = csv.writer(w, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)  #opens write file
    read  = csv.reader(f, delimiter='\t', quotechar="|")                           #opens read file
    array = [] # creates blank string
    print("Running...")
    
    for row in read:
        array.append("".join(row))                            #makes input one string
    for item in array:
        temparray = item.split('"')                           #seperates string by '"' creating an array with 3 elements
        try:                        
            
            street       = ""
            output       = ""
            check        = temparray[1]                       # gets address
            checkarray   = check.split(",")                   # splits address by ","
            correctarray = [0] * len(checkarray)              # creates an array 
            latlon       = temparray[2].lstrip(",")           #strips the "," from the front of ,lat,long
            lat,lon      = latlon.split(",")
            try:                                              #checks to make sure lat value is a float
                test =float(lat)
            except ValueError:
                if debug == True:
                    print("non numeric value for lat")
            try:                                              #checks to make sure lat value is a float
                test =float(lon)
            except ValueError:
                if debug == True:
                    print("non numeric value for long")
            addresses    = map.reverse_geocode(latlon,"","","english")   #gets list of addresses at location
            
            for address in addresses:                                    #for each address in the list
                for component in address["address_components"]:          #for each component of the address
                    if component["types"][0] == "street_number":         # combines street number with street name
                        street += component["long_name"]
                    if component["types"][0] == "route":
                        street += " " +component["short_name"]
                    try:                                                 #checks for street name in address array
                        i = checkarray.index(street)
                        correctarray[i] = 1                              #sets the corrisponding value in the correct array to true
                    except ValueError:
                        pass
                    try:                                                
                        i = checkarray.index(" "+component["long_name"]) #checks address array for component's long name
                        correctarray[i] = 1          
                    except ValueError:
                        pass
                    try:
                        i = checkarray.index(" "+component["short_name"]) #checks address array for component's short name
                        correctarray[i] = 1
                    except ValueError:
                        pass
    
    
            location = map.geocode(check)                         #gets address location
            lon2     = location[0]['geometry']['location']['lng'] #address lat
            lat2     = location[0]['geometry']['location']['lat'] #address long
            distlon  = (float(lon) - float(lon2))                 #distance formula 
            distlat  = float(lat) -float(lat2)
            dist     = math.sqrt((distlon**2)+(distlon**2))
            
            
            if correctarray[-1] == 1:       #checks the correct array for the last pos which is country
                output = "Right Country"
            if correctarray[-2] == 1:       #checks the correct array for the second to last pos which is state
                output = "Right State"
            if correctarray[-3] == 1:       #checks the correct array for the third to last pos which is city
                output = "Right City"
            if correctarray[-4] == 1:       #checks the correct array for the forth to last pos which is street + number
                output = "Right Place"
            if dist < noise:                #checks for to see if its in range for error
                output = "Right Place"
            if output == "":                #if output hasnt been set then the lat/long is outside the country 
                output = "Wrong Country"
                
            if debug == True:
                output += " Distance is: " + str(dist)
                print(check,lat,lon,output)
            write.writerow([check,lat,lon,output])  #writes to csv

        except IndexError:                          #if error write input to output
            if item != ",,":
                write.writerow(item.split(","))
                if debug == True:
                    print(item.split(","))
            else:
                write.writerow(["","",""])
                if debug == True:
                    print("")
            pass
        except:
            if debug == True:
                write.writerow(item.split(","))   #if error write input to output
                if debug == True:
                    print(item.split(","))

        
    print("done")
    f.close() #closes files
    w.close()

if __name__ == '__main__':main()