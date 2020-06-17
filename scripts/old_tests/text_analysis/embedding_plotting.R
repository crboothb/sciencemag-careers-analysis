library(plotly)

token_embedding = read.csv("../data/reduced_umap.csv")
# token_embedding$log_advice_prop = log(token_embedding$advice_prop)

advice = token_embedding$advice_prop
top = mean(advice)+sd(advice)*1.5
bottom = mean(advice)-sd(advice)*1.5

ggplot(token_embedding, aes(x = advice_prop)) + geom_histogram() + geom_vline(xintercept = top) + geom_vline(xintercept = bottom)

token_embedding$advice = ifelse(token_embedding$advice_prop < top, "not","advice")

i = subset(token_embedding, advice_prop < top)
j = subset(token_embedding, advice_prop >= top)

pal = c("#db6d00","#ececec")

fig <- plot_ly(type = 'scatter', mode = 'markers')
fig <- fig %>%
  add_trace(
    x = i$axis1,
    y = i$axis2,
    text = i$token,
    hoverinfo = 'text',
    colors="#ececec",
    alpha = 0.3,
    showlegend = F
  )

fig <- fig %>%
  add_trace(
    x = j$axis1,
    y = j$axis2,
    text = j$token,
    hoverinfo = 'text',
    colors="#db6d00",
    showlegend = F
  )

#fig <- plot_ly(type = 'scatter', mode = 'markers',colors = pal)
#fig <- fig %>%
#  add_trace(
#    x = token_embedding$axis1,
#    y = token_embedding$axis2,
#    text = token_embedding$token,
#    hoverinfo = 'text',
#    color=~token_embedding$advice,
#    showlegend = F
#  )

fig




