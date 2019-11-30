import import_func as imp
import tags_work as tgs
import desc_vis as vis

elist = "../data/editorials-1.jl"
tags = "../data/by_article_110219.jl"
full = "../data/by_article_fulltext_112919-2.jl"
test_full = "../data/full_text.jl"

# editorial = imp.import_jl(elist)
# tags = imp.import_jl(tags)
full = imp.import_jl(test_full)

# out_edi = imp.process(editorial, "editorial")
# out_tag = imp.process(tags, "tags")
out_full = imp.process(full, focus = "full", out_form = "dict")

# print(out_full[0].sort_values(by = "date").head())

# edi_df = out_edi[0]
# edi_dict = out_edi[1]

# tag_df = out_tag[0]
# tag_dict = out_tag[1]

full_df = out_full

# print(out_full["headline"][0])
# print(out_full["tags"])
# print(out_full["authors"])
# print(out_full["date"])
# print(out_full["time"])
print(len(out_full["text"]))
print(len(out_full["bio"]))

for line in out_full["text"]:
    print("\n\n#######\n\n")
    print(line)
# for line in out_full["bio"]:
#     print("#######")
#     print(line)




# print(out_full["text"][0][0])  
# print("#####") 
# print(out_full["text"][0][2])   
# print("#####") 
# print(out_full["text"][0][3])   
# print("#####") 
# print(out_full["text"][0][4])   
# print("#####") 
# print(out_full["text"][0][5])   
# print("#####") 
# print(out_full["text"][0][6])   



# print(edi_df.head)
# print(tag_df.head)

# print(len(edi_df))
# print(len(editorial))
# print(len(tag_df))
# print(len(tags))
# print(len(edi_df)-len(tag_df))

# cumulative = imp.cumulative()

# print(cumulative[0])
# print(cumulative[1])

# edi_df = imp.seq_dates(edi_df, "editorial")
# tag_df = imp.seq_dates(tag_df, "tags")
# print(tag_df.tail(10))

# print(edi_df.head())
# print(tag_df.head())

# columns = imp.id_columns(tag_df)
# columns = tgs.seperate_tags(columns)

# inc_dict = tgs.tag_incidence(columns, lifespan = True, id_col_tag = True, binary = True)

# col_diffs = tgs.id_column_tags(inc_dict, binary=True)

# print(len(inc_dict))
# print(len(col_diffs))