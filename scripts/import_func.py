import ast

import numpy as np
import pandas as pd

#### Import Functions ####
## These functions import and do the initial data processing,
## and they assemble the working dataframes

# the function that houses all teh other initalizaiton functions


def init_df(
    filename, focus, test=False, out_form="df", genre="none", categories="limited"
):
    if categories == "all":
        categories = [
            "advice",
            "job market",
            "academic",
            "postdoc",
            "graduate",
            "workplace diversity",
            "midcareer",
            "non-disciplinary",
            "life and career balance",
            "industry",
            "career profiles",
            "government",
            "undergraduate",
            "working life",
            "early career",
            "career-related policy"
        ]
    elif categories == "limited":
        categories = [
            # "ctscinet", # no defined genre
            "career-related policy",
            "working life",
            "career profiles",
            # "life_and_career_balance",# no defined genre
            # "myscinet", # no defined genre
            # "issues_and_perspectives", # too much overlap with advice, no defined genre
            "advice",
        ]
    else:
        print(
            "enter either all or limited for categories. but you probably want limited"
        )

    raw = import_jl(filename)
    out = process(raw, focus=focus, out_form=out_form, genre=genre)

    df = out
    if genre != "WL":
        df = seq_dates(df, focus, genre=genre)
    for keyword in categories:
        df = id_x(df, keyword)
    # remove any articles published after 2019
    df = df[(df.year < 2020) & (df.year > 1997)]
    if focus != "editorial":
        # df = id_advice(df)
        df = id_columns(df)
        df = one_time(df)

    if test == True:
        print(df.head())

    df = category_type(df)
    return df


def import_jl(fname):
    """Import .jl files. Works fine for both ediorial and tags takes 
    path+filename as string as filename argument returns contents as a list, 
    with each line in file as a list item"""
    return open(fname, "r").readlines()

def category_type(df):
    df["category"] = np.where(
        (df["working_life"] == "yes"),
        "working_life",
        np.where(
            (df["career_related_policy"] == "yes"),
            "career_related_policy",
            np.where(
                (df["advice"] == "yes"),
                "advice",
                np.where(
                    (df["career_profiles"] == "yes"),
                    "career_profiles",
                    "uncategorized",
                ),
            ),
        ),
    )
    return(df)

# initially process content from imported jl files
# takes list of lines in original file as list argument
# takes "editorial", "tags", or "full" as focus argument to indicate whether it's the editorial or tags
# I think this one handles the dates and the items in the dates column are datetime objects
# out_form="dict" or "df"


def process(list, focus, out_form, genre="none"):

    list_temp1 = []
    for line in list:
        if focus == "tags":
            line = line.replace("Read more ", "")
        if "null" in line:
            line = line.replace("null", "'null'")
        line = ast.literal_eval(line.lower())
        list_temp1.append(line)
    list = list_temp1

    if focus == "editorial":
        editorial_dict = {"headline": [], "preview": [], "authors": [], "date": []}

        sidebar = [
            "how to keep a lab notebook",
            "grad student unions dealt blow as proposed new rule says students aren’t ‘employees’",
            "what do we know about ph.d. scientists’ career paths?",
            "three lessons from industry that i’m taking back to academia",
        ]
        for line in list:
            if line["text"].replace("\n", "") in sidebar:
                if line["preview"] == "null":
                    continue

            editorial_dict["headline"].append(line["text"].replace("\n", ""))
            editorial_dict["preview"].append(
                line["preview"].replace("\n", "").replace("\r", "").replace("  ", "")
            )
            num_authors = (len(line["byline"].replace("<", ">").split(">")) - 5) // 4
            au = line["byline"].replace("<", ">").split(">")[4]
            for i in range(2, num_authors):
                au += ", " + line["byline"].replace("<", ">").split(">")[i * 4]
            editorial_dict["authors"].append(au)
            editorial_dict["date"].append(
                line["byline"]
                .replace("<", ">")
                .split(">")[-5]
                .replace(". ", "-")
                .replace(", ", "-")
                .replace(" ", "")
                .replace(",", "")
            )

        if out_form == "df":
            editorial_df = pd.DataFrame(editorial_dict)
            if genre != "WL":
                editorial_df["date"] = pd.to_datetime(
                    editorial_df.date, format="%b-%d-%Y"
                )
            editorial_df.sort_values(by=["date"], inplace=True)
            out = editorial_df
        elif out_form == "dict":
            out = editorial_dict
        elif out_form == "both":
            editorial_df = pd.DataFrame(editorial_dict)
            editorial_df["date"] = pd.to_datetime(editorial_df.date, format="%b-%d-%Y")
            editorial_df.sort_values(by=["date"], inplace=True)
            out1 = editorial_df
            out2 = editorial_dict
            out = [out1, out2]

    elif focus == "tags" or focus == "full":
        if focus == "tags":
            tags_dict = {
                "headline": [],
                "tags": [],
                "authors": [],
                "date": [],
                "time": [],
            }
        else:
            tags_dict = {
                "id": [],
                "headline": [],
                "tags": [],
                "authors": [],
                "date": [],
                "time": [],
                "text": [],
                "bio": [],
            }

        id_count = 0
        for line in list:
            # if "null" in line:
            #     line = line.replace("null", "\'null\'")
            #     line = ast.literal_eval(line)

            tags_dict["id"].append(id_count)
            id_count += 1
            head = line["headline"].replace("\n", "").replace('"', "")
            tags_dict["headline"].append(head)

            tags = line["tags"]
            unique_tags = []
            for tag in tags:
                tag = tag.replace("read more ", "").replace("how-tos", "how-to")
                if tag not in unique_tags:
                    unique_tags.append(tag)
            tags = unique_tags
            if len(tags) < 1:
                tags_dict["tags"].append("[]")
            elif len(tags[0]) < 5:
                # tags_dict["tags"].append(", ".join(tags))
                tags_dict["tags"].append(tags)
            elif tags[0][:5] == "Read ":
                if tags[0][10:-1] not in tags[1]:
                    included = "false"
                    for tag in tags[2:]:
                        if tags[0][10:-1] in tag:
                            # tags_dict["tags"].append(", ".join(tags[1:]))
                            tags_dict["tags"].append(tags)
                            included = "true"
                            break
                    if included == "false":
                        tags[0] = tags[0][10:]
                        # tags_dict["tags"].append(", ".join(tags))
                        tags_dict["tags"].append(tags)

                else:
                    # tags_dict["tags"].append(", ".join(tags[1:]))
                    tags_dict["tags"].append(tags)
            else:
                # tags_dict["tags"].append(", ".join(tags))
                tags_dict["tags"].append(tags)

            num_authors = (len(line["byline"].replace("<", ">").split(">")) - 5) // 4
            au = line["byline"].replace("<", ">").split(">")[4]
            au_list = [au]
            for i in range(2, num_authors):
                au += ", " + line["byline"].replace("<", ">").split(">")[i * 4]
                au_list.append(line["byline"].replace("<", ">").split(">")[i * 4])
            tags_dict["authors"].append(au)

            date_time = line["byline"].replace("<", ">").split(">")[-5]
            time = date_time[-7:]
            date = (
                date_time[:-9]
                .replace(". ", "-")
                .replace(", ", "-")
                .replace(" ", "")
                .replace(",", "")
            )
            tags_dict["date"].append(date)
            tags_dict["time"].append(time)
            if focus == "full":
                f_text_list = []
                w_text_list = line["text"]
                bio_text = []
                for string in w_text_list:
                    record = True
                    # still not working :/
                    # if string == '  by ':
                    #     record = False
                    # if string == ", ":
                    #     record = False
                    if (
                        "doi:" in string
                    ):  # == '  by ' or string == 'enter keywords, locations or job types to start searching for your new science career.':
                        record = False
                    if au_list[0] in string:
                        bio_text.append(string)
                        record = False
                    if "enter keywords, locations or job types" in string:
                        break
                    if record == True:
                        f_text_list.append(string.strip().replace("\n", ""))
                f_text = "".join(f_text_list)
                # print(w_text)
                # print("#######################################")
                # last 16 lines are junk
                tags_dict["text"].append(f_text)
                tags_dict["bio"].append(bio_text)

        # print(tags_dict)
        if out_form == "df" and genre != "WL":
            tags_df = pd.DataFrame(tags_dict)
            tags_df.head()
            tags_df["date"] = pd.to_datetime(tags_df.date, format="%b-%d-%Y")
            tags_df["date"] = pd.to_datetime(tags_df["date"])
            tags_df.sort_values(by=["date"], inplace=True)
            out = tags_df
        elif out_form == "dict":
            out = tags_dict
        elif out_form == "both" and genre != "WL":
            tags_df = pd.DataFrame(tags_dict)
            tags_df.head()
            tags_df["date"] = pd.to_datetime(tags_df.date, format="%b-%d-%Y")
            tags_df["date"] = pd.to_datetime(tags_df["date"])
            tags_df.sort_values(by=["date"], inplace=True)
            out1 = tags_df
            out2 = tags_dict
            out = [out1, out2]
        else:
            # print("please enter third argument, 'out_form' as 'df','dict', or 'both' ")
            tags_df = pd.DataFrame(tags_dict)
            out = tags_df

    else:
        print("please enter second argument 'focus' as 'editorial','tags', or 'full' ")

    return out


def cumulative(genre="none"):
    months_r = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    months_l = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # I need a list of cumulative days at the end of each month going forward
    if genre != "advice":
        cumulative_days = [31, 61, 92]
        cumulative_months = [13]
        start = 1997
    else:
        cumulative_days = [31]
        cumulative_months = [1]
        start = 1997

    for year in range(start, 2025):
        cumulative_months.append(cumulative_months[-1] + 12)
        if year % 4 == 0:
            months = months_l
        else:
            months = months_r
        for month in range(1, 13):
            # print(year, month)
            # print(months[month-1])
            cumulative_days.append(cumulative_days[-1] + months[month - 1])
    return (cumulative_days, cumulative_months)


# need to add appropriate cumulative columns to the dataframes
# takes the dataframe
# focus indicates whether it's "tags" or "editoral"
# calls cumulative() on its own--don't worry about it


def seq_dates(df, focus, genre="none"):

    df["start"] = min(df["date"])
    df["date_seq"] = df["date"] - df["start"]
    df["date_seq"] = df["date_seq"].map(lambda x: str(x)[:-14])
    df["date_seq"] = df["date_seq"].astype(int)
    if genre == "advice":
        df["date_seq"] = df["date_seq"] + 30
    else:
        df["date_seq"] = df["date_seq"] + 18
    m_seq = []
    for n_days in df["date_seq"]:
        m_seq.append(cumul_to(n_days, "d", genre=genre))
    df["month_seq"] = m_seq
    if genre != "advice":
        df["month_seq"] = df["month_seq"] + 9
    y_seq = []
    for n_months in df["month_seq"]:
        y_seq.append(cumul_to(n_months, "m", genre=genre))

    df["year"] = y_seq

    # remove unnecessary columns after manipulation
    df.drop("start", axis=1, inplace=True)

    return df


def cumul_to(n, unit, genre="none"):

    cumul_both = cumulative(genre=genre)
    cumulative_days = cumul_both[0]
    cumulative_months = cumul_both[1]

    if unit in ["m", "month", "months"]:
        for months in cumulative_months:
            if n < months:
                if genre == "advice":
                    year = cumulative_months.index(months) + 1997
                else:
                    year = cumulative_months.index(months) + 1996
                return year
    elif unit in ["d", "day", "days"]:
        for days in cumulative_days:
            if n < days:
                month = cumulative_days.index(days) + 1
                return month
    else:
        print(
            'error in imp.cumul_to_year: set unit argument to "d" for days or "m" for months'
        )


# for counting the number of times each author publishes
# takes the dataframe
# returns either a 2 column dataframe with the author and count only "count"
# or the full dataframe with the number of times author has published appended "full"
# ^^^ indicated by output argument


def author_num(df, output):
    # authors = df["authors"].value_counts()
    authors_count = {}
    for byline in df.authors:
        byline = byline.split(", ")
        for author in byline:
            if author in authors_count.keys():
                authors_count[author] += 1
            else:
                authors_count[author] = 1
    for byline in df.authors:
        if ", " in byline:
            coauthors = byline.split(", ")
            count = 0
            for author in coauthors:
                count += authors_count[author]
            if byline not in authors_count.keys():
                authors_count[byline] = count // len(coauthors)
            else:
                authors_count[byline] += count // len(coauthors)

    authors2df = {"author": [], "n_posts_author": []}
    for key in authors_count.keys():
        authors2df["author"].append(key)
        authors2df["n_posts_author"].append(authors_count[key])

    authors_df = pd.DataFrame(authors2df)

    if output == "count":
        return authors_df

    authors_df["writer"] = authors_df.author
    authors_df = authors_df.rename(columns={"authors": "n_posts_author"})
    tags_authors = pd.merge(df, authors_df, left_on="authors", right_on="writer")
    tags_authors.drop("writer", axis=1, inplace=True)

    if output == "full":
        return tags_authors


# for identifying which articles are columns
# takes the dataframe
# requires the tags column in order to work
# theshold indicates the number of articles written by author required to consider it a column
# theshold's default value is 4


def id_columns(df, threshold=5):
    df_authors = author_num(df, "full")

    df_authors["column1"] = ["yes" if "column" in x else "no" for x in df["tags"]]
    df_authors["column2"] = np.where(
        (df_authors["n_posts_author"] >= threshold)
        | (df_authors["column1"] == "yes") & (df_authors["working_life"] == "no"),
        "yes",
        "no",
    )

    return df_authors


def one_time(df, threshold=1):
    if "column1" not in df.columns.values:
        df = id_columns(df)
    df["one_time"] = np.where(
        (df["n_posts_author"] < threshold + 1)
        & (df["column2"] == "no")
        & (df["advice"] == "no"),
        "yes",
        "no",
    )
    return df


def id_advice(df):
    df["advice"] = ["yes" if "advice" in x else "no" for x in df["tags"]]
    return df


def id_x(df, tag):
    tag_no_space = tag.replace(" ", "_").replace("-", "_")
    df[tag_no_space] = ["yes" if tag in x else "no" for x in df["tags"]]
    return df
