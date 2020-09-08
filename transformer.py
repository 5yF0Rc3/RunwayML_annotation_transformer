import json
import csv


# settings
n_files = 853 # from the xml / csv
folder = "annotations/" # of the  xml / csv
rw_folder = "images/" # of the Runway folder, empty if upladet with no subfolder
filename = "maksssksksss" # of the images
use_csv = False
csv_name = "train.csv"

# keys from the xml and Id from Runway
dict_id = {
    "with_mask": "902fb1b8-bb91-436d-9281-7458d3cc4fd0",
    "without_mask": "1b097101-f59f-4fcd-b2b9-843e5e902469"
    }

files = []

# create list with the files
for i in range(n_files):
    files.append(filename + str(i))

# presetting the dicts
dict_images = []
dict_box = {"type": "BOUNDING_BOX",
        "boundingBox": []}
dict_files = {}
dict_end = {"categories": [
    {
      "id": "902fb1b8-bb91-436d-9281-7458d3cc4fd0",
      "createdAt": "2020-09-08T07:31:25.455Z",
      "updatedAt": "2020-09-08T07:31:25.455Z",
      "annotationGroupId": "39c4d136-b0eb-46da-9ec6-7a075fefa38e",
      "name": "with_mask",
      "color": "#d60000",
      "deleted": "false"
    },
    {
      "id": "1b097101-f59f-4fcd-b2b9-843e5e902469",
      "createdAt": "2020-09-08T07:31:28.252Z",
      "updatedAt": "2020-09-08T07:31:28.252Z",
      "annotationGroupId": "39c4d136-b0eb-46da-9ec6-7a075fefa38e",
      "name": "without_mask",
      "color": "#8c3bff",
      "deleted": "false"
    }
  ]}


def value_search(pos, s, start, end):
    # return the value between start, end and in order with pos
    if pos != 0:
        for i in range(pos):
            s = s[s.find(end)+len(end):]
    return s[s.find(start)+len(start):s.find(end)]

def load_csv():
    with open(csv_name, newline="") as csvfile:
        datareader = csv.reader(csvfile, dialect="excel")
        #data_dict = {}
        data_list = []
        rowlist = []
        temp = []
        # saves the file into a list
        for row in datareader:
            rowlist.append(row)
        # splits the data at ; for german files, "," for rest
        for i in range(len(rowlist)):    
            temp.append(rowlist[i][0].strip().split(',', 50))
        # columns of data_list
        for i in range(len(temp[0])):
            data_list.append([])
        # seperates the datas in row into colums, sorted for Empty, Float, String
        for i in range(len(temp)):
            for j in range(len(temp[0])):
                if temp[i][j] == "":
                    data_list[j].append(None)
                else:
                    try:
                        data_list[j].append(float(temp[i][j]))
                    except:
                        data_list[j].append(temp[i][j])


for i in range(len(files)):
    with open(folder + files[i] + str(".xml")) as f:
        content = []
        # load the context of the fils into a list
        for line in f:
            content.append(str(f.read()))
        
        # count the <objects>
        n_obj = content[0].count("<object>")

        # used for calc the % value of X/Y
        width = int(value_search(0, content[0], "<width>", "</width>"))
        height = int(value_search(0, content[0], "<height>", "</height>"))


        # get the rectangle of each mark, sort it to the category
        dict_images = []
        for j in range(n_obj):
            obj = value_search(j, content[0], "<object>", "</object>")

            categoryId = value_search(0,obj, "<name>", "</name>")

            if categoryId in dict_id:
                dict_box["categoryId"] = dict_id[categoryId]
                
            xmin = int(value_search(0,obj, "<xmin>", "</xmin>")) / width
            ymin = int(value_search(0,obj, "<ymin>", "</ymin>")) / height
            xmax = int(value_search(0,obj, "<xmax>", "</xmax>")) / width
            ymax = int(value_search(0,obj, "<ymax>", "</ymax>")) / height
            dict_box["boundingBox"] = [xmin, ymin, xmax, ymax]

            dict_images.append(dict(dict_box))
            
    # merge all the dicts
    dict_files[rw_folder + files[i] + str(".png")] = dict_images
    dict_end["files"] = dict_files
    #print(dict_end)

# Export Json
out_file = open("data.json", "w")
json.dump(dict_end, out_file)
out_file.close()



