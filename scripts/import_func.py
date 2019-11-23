import ast
import pandas as pd

# import .jl files. Works fine for both ediorial and tags
# takes path+filename as string as filename argument
# returns contents as a list, with each line in file as a list item

def import_jl(filename):
    filename = filename
    full = open(filename, "r")
    list = []
    for x in full:
        list.append(x)
    return list

# initially process content from imported jl files
# takes list of lines in original file as list argument
# takes "editorial" or "tags" as focus argument to indicate whether it's the editorial or tags

def process(list, focus):
    
    list_temp1 = []
    for line in list:
        if "null" in line:
            line = line.replace("null", "\'null\'")
        line = ast.literal_eval(line.lower())
        list_temp1.append(line)
    list = list_temp1

    if focus == "editorial":
        editorial_dict = {"headline":[], "preview":[],"authors":[],"date":[] }

        sidebar = ["How to keep a lab notebook",
                "Grad student unions dealt blow as proposed new rule says students aren’t ‘employees’",
                "What do we know about Ph.D. scientists’ career paths?",
                "Three lessons from industry that I’m taking back to academia"
                ]
        for line in list:
            if line["text"].replace("\n","")  in sidebar:
                if line["preview"] == "null":
                    continue

            editorial_dict["headline"].append(line["text"].replace("\n",""))
            editorial_dict["preview"].append(line["preview"].replace("\n","").replace("\r","").replace("  ",""))
            num_authors = (len(line["byline"].replace("<",">").split(">"))-5)//4
            au = line["byline"].replace("<",">").split(">")[4]
            for i in range(2,num_authors):
                au += ", " + line["byline"].replace("<",">").split(">")[i*4]
            editorial_dict["authors"].append(au)
            editorial_dict["date"].append(line["byline"].replace("<",">").split(">")[-5].replace(". ","-").replace(", ","-").replace(" ","").replace(",",""))

        editorial_df = pd.DataFrame(editorial_dict)
        editorial_df["date"] = pd.to_datetime(editorial_df.date, format='%b-%d-%Y')
        editorial_df.sort_values(by=["date"], inplace=True)
        out_df = editorial_df
        out_dict = editorial_dict
    
    elif focus == "tags":
        tags_dict = {"headline":[],"tags":[],"authors":[],"date":[],"time":[] }


        for line in list:
        # if "null" in line:
        #     line = line.replace("null", "\'null\'")
        #     line = ast.literal_eval(line)

            head = line["headline"].replace("\n","").replace("\"","")
            tags_dict["headline"].append(head)

            tags = line["tags"]
            unique_tags = []
            for tag in tags:
                if tag not in unique_tags:
                    unique_tags.append(tag)
            tags = unique_tags
            if len(tags) < 1:
                tags_dict["tags"].append("[]")
            elif len(tags[0])< 5:
                #tags_dict["tags"].append(", ".join(tags))
                tags_dict["tags"].append(tags)
            elif tags[0][:5] == "Read ":
                if tags[0][10:-1] not in tags[1]:
                    included = "false"
                    for tag in tags[2:]:
                        if tags[0][10:-1] in tag:
                            #tags_dict["tags"].append(", ".join(tags[1:]))
                            tags_dict["tags"].append(tags)
                            included = "true"
                            break
                    if included == "false":
                        tags[0] = tags[0][10:]
                        #tags_dict["tags"].append(", ".join(tags))
                        tags_dict["tags"].append(tags)

                else:
                    #tags_dict["tags"].append(", ".join(tags[1:]))
                    tags_dict["tags"].append(tags)
            else:
                #tags_dict["tags"].append(", ".join(tags))
                tags_dict["tags"].append(tags)

            num_authors = (len(line["byline"].replace("<",">").split(">"))-5)//4
            au = line["byline"].replace("<",">").split(">")[4]
            for i in range(2,num_authors):
                au += ", " + line["byline"].replace("<",">").split(">")[i*4]
            tags_dict["authors"].append(au)

            date_time = line["byline"].replace("<",">").split(">")[-5]
            time = date_time[-7:]
            date = date_time[:-9].replace(". ","-").replace(", ","-").replace(" ","").replace(",","")
            tags_dict["date"].append(date)
            tags_dict["time"].append(time)


        #print(tags_dict)

        tags_df = pd.DataFrame(tags_dict)
        tags_df.head()
        tags_df["date"] = pd.to_datetime(tags_df.date, format='%b-%d-%Y')
        tags_df["date"] = pd.to_datetime(tags_df["date"])
        tags_df.sort_values(by=["date"], inplace=True)
        out_df = tags_df
        out_dict = tags_dict
  
    return [out_df, out_dict]

# Why am I doing this? I'm trying to calculate the months from the date_seq 
# Right now, this function returns a sequence from the actual start of the publications to the most recent publications
# I would want later versions of this to be more flexible--maybe allowing the start and end times to be set in the function?

def cumulative():
    months_r = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    months_l = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # I need a list of cumulative days at the end of each month going forward
    cumulative_days = [31, 61, 92]
    cumulative_months = [13]

    for year in range(1997,2021):
        cumulative_months.append(cumulative_months[-1] + 12)
        if year%4 == 0:
            months = months_l
        else:
            months = months_r
        for month in range(1,13):
            #print(year, month)
            #print(months[month-1])
            cumulative_days.append(cumulative_days[-1]+months[month-1])
    return(cumulative_days, cumulative_months)