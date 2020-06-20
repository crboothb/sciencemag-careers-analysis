library(ggplot2)
library(tidyr)
library(dplyr)

this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)

pronouns_tags=read.csv("../../data/bargraph_data/tag_bargraph_data_pronouns.csv")
# pronouns_all=read.csv("../../data/bargraph_data/all_bargraph_data_pronouns.csv")
# modal_tags=read.csv("../../data/bargraph_data/tag_bargraph_data_modals.csv")
# modal_all=read.csv("../../data/bargraph_data/all_bargraph_data_modals.csv")
# hedges_tags=read.csv("../../data/bargraph_data/tag_bargraph_data_hedges.csv")
# hedges_all=read.csv("../../data/bargraph_data/all_bargraph_data_hedges.csv")

### get tag medians ###

pronouns_tags = subset(pronouns_tags, select = -c(level_1, id))
# modal_tags = subset(modal_tags, select = -c(level_1, id))
# hedges_tags = subset(hedges_tags, select = -c(level_1, id))

pronouns_tags = pronouns_tags %>% group_by(level_0) %>% mutate(med_frac1 = median(frac1)) %>% mutate(med_frac2 = median(frac2))
# modal_tags = modal_tags %>% group_by(level_0) %>% mutate(med_frac = median(frac))
# hedges_tags = hedges_tags %>% group_by(level_0) %>% mutate(med_frac_h = median(frac_h)) %>% mutate(med_frac_b = median(frac_b))

pronoun_tags_med.short = aggregate(subset(pronouns_tags, select=-c(level_0)), by=list(pronouns_tags$level_0), FUN=median)
pronoun_tags_med = gather(pronoun_tags_med.short, key="type", value = "med", c("med_frac1","med_frac2"))
# modal_tags_med = aggregate(subset(modal_tags, select=-c(level_0)), by=list(modal_tags$level_0), FUN=median)
# hedges_tags_med.short = aggregate(subset(hedges_tags, select=-c(level_0)), by=list(hedges_tags$level_0), FUN=median)
# hedges_tags_med = gather(hedges_tags_med.short, key="type", value = "med", c("med_frac_h","med_frac_b"))

### get overall medians ###

# overall_pronoun_med = data.frame("type"=c("med_frac1","med_frac2"), "medians"=c(median(pronouns_all$frac1), median(pronouns_all$frac2) ) )
# overall_modal_med = c(median(modal_all$frac))
# overall_hedges_med = c(median(hedges_all$frac_h), median(hedges_all$frac_b))

### start plots ###

# pronoun_plot = ggplot(pronoun_tags_med, aes(y=med,x=Group.1, fill=type, color=type)) + geom_bar(stat="identity")+
#   facet_wrap(~type)+
#   # geom_vline(data=overall_pronoun_med, aes(xintercept=type))+
#   coord_flip()+
#   theme_minimal()
# 
# # print(pronoun_plot)

### trying permutation test ###

tags = unique(pronouns_tags$level_0)

full_set_first = pronouns_tags$frac1

jackknife.median = function(x, samp_size, overall) {
  # print(12)
  perm_set = sample(x,size=samp_size, replace = F)
  # print(median(perm_set))
  return(median(perm_set)-overall)
}

jackknife.permute = function(x,samp_size, nperm, overall) {
  perm.dist = replicate(nperm, jackknife.median(x, samp_size, overall = overall))
  return(perm.dist)
}

fd=function(x) {
  n=length(x)
  r=IQR(x)
  2*r/n^(1/3)
}
#^^^# http://ritsokiguess.site/docs/2017/06/08/histograms-and-bins/



n = 100
pvals = c()
tests = c()
tag_medians = c()

overall_med = median(pronouns_tags$frac1)

for(i in seq(1,16,1)){
  # print(i)
  # print(pronoun_tags_med.short$Group.1[i])
  samp = nrow(subset(pronouns_tags, level_0==pronoun_tags_med.short$Group.1[i]))
  # print(samp)
  tag_median = pronoun_tags_med.short$med_frac1[i]
  test.stat = tag_median-overall_med
  # print(test.stat)
  
  perms = jackknife.permute(x = pronouns_tags$frac1, samp_size=samp, nperm = n, overall = overall_med)
  #print("test")
  p = sum(abs(perms) >= abs(test.stat))/n
  #print(test)
  
  pvals = append(pvals, p)
  tests = append(tests, test.stat)
  tag_medians = append(tag_medians, tag_median)
  
  data <- data.frame("perms" = perms)

  # plot = ggplot(data, aes(x=perms))+geom_histogram(binwidth =fd)+
  #   # stat_bin(binwidth = "fd")+
  #   geom_vline(xintercept = test.stat)+
  #   ggtitle(pronoun_tags_med.short$Group.1[i])
  # print(plot)
  
}

tests.df = data.frame("tags"=pronoun_tags_med.short$Group.1,"pval"=pvals, "test_statistic"=tests, "tag_median"=tag_medians)

# write.csv(tests.df,"../../data/bargraph_data/first_sig_test.csv")
