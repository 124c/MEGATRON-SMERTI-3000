setwd("~/Projects/It4Fin")
data <- read.csv("eurusd_h1.csv", stringsAsFactors = F)

View(data)
all(data$high >= data$low)

data$time <- as.factor(data$time)

library(dplyr)
library(ggplot2)

as.Date("1999/04/08")

data <- mutate(data,
               year = as.Date(date,
                              format = "%Y.%m.%d") %>% 
                 format(format = "%Y") %>% 
                 as.factor)

group_by(data, year) %>% 
  summarise(n = n())

data$day <- rep(NA, nrow(data))

for (i in unique(data$year)) {
  data$day[data$year == i] <- 1:(sum(data$year == i))
}

data[4555, ]

ggplot(data, aes(x = day, y = close))+
  geom_line()+
  facet_wrap(~ year)


eurusd <- data$close[data$year == "2010"]

plot(data$day[data$year == "2010"], eurusd, type = "l")

# (1:10)[-1] # == tail(1:10, -1)
# (1:10)[-length(1:10)] # == head(1:10, -1)

r <- 100 * log(tail(eurusd, -1) / head(eurusd, -1))
plot(r, type = "h")

size <- 24

v_mean <- rep(NA, 1000)
for (i in 1:1000) {
  v_mean[i] <- mean(r[0:(size - 1) + i])
}
plot(v_mean, type = "l")
signal <- sign(v_mean)

profit <- r[1:1000 + size] * signal
plot(sapply(1:1000,
            function(n) sum(profit[1:n])),
     type = "l")

# momentum <- function(data, t, size = 24) {
#   learning_sample <- data[t - 1:size]
#   r_mean <- mean(learning_sample)
#   if (r_mean > 0) {
#     print("buy")
#   }
#   if (r_mean < 0) {
#     print("sell")
#   }
#   if (r_mean == 0) {
#     print("hold")
#   } else {
#     print("etc.")
#   }
# }

momentum <- function(data, t, size = 24) {
  learning_sample <- data[t - 1:size]
  r_mean <- mean(learning_sample)
  # if (r_mean > 0) {
  #   return(1)
  # }
  # if (r_mean < 0) {
  #   return(-1)
  # }
  # if (r_mean == 0) {
  #   return(0)
  # } else {
  #   print("etc.")
  # }
  return(sign(r_mean))
}

momentum <- function(data, t, size = 24) {
  require(magrittr)
  data[t - 1:size] %>% 
    mean %>%
    sign %>% 
    return
}

momentum(r, 30)
plot(6:60,
     sapply(6:60,
            function(size) {
              trading <- 60 + 1:1000
              profit <- r[trading] *
                sapply(trading, momentum,
                       data = r, size = size)
              return(sum(profit))
            }),
     type = "h")

lines(6:60,
     sapply(6:60,
            function(size) {
              trading <- 1000 + 60 + 1:1000
              profit <- r[trading] *
                sapply(trading, momentum,
                       data = r, size = size)
              return(sum(profit))
            }),
    col = "red")

meanreverse <- function(data, t, size = 24) {
  return(-momentum(data, t, size))
}

library(pracma)
??hurstexp
hurstexp(r[1:6], 3)$He

start <- 1000

trading_rule <- function(data, t, size) {
  learning_sample <- data[t - 1:size]
  Hurst <- hurstexp(learning_sample, size/3, F)$He
  if (Hurst > 0.5) {
    return(momentum(data, t, size))
  }
  if (Hurst < 0.5) {
    return(meanreverse(data, t, size))
  }
  if (Hurst == 0.5) {
    return(0)
  }
}

trading <- 1000:2000
profit <- r[trading] *
  sapply(trading, trading_rule,
         data = r, size = 30)
plot(trading, sapply(1:length(profit),
                     function(n) sum(profit[1:n])),
     type = "l")

profit <- r[trading] *
  sapply(trading, momentum,
         data = r, size = 30)
lines(trading, sapply(1:length(profit),
                     function(n) sum(profit[1:n])),
     col = "blue")

profit <- r[trading] *
  sapply(trading, meanreverse,
         data = r, size = 30)
lines(trading, sapply(1:length(profit),
                      function(n) sum(profit[1:n])),
      col = "red")
