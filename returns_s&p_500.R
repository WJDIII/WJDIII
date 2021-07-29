#libraries used
library(quantmod)
#loading s&p 500 constituent data
constituents <- read.csv("C:\\Syracuse DataScience\\IST 719 Information Visualization\\Final Project\\s-and-p-500-companies_zip\\data\\constituents_csv.csv"
                         , stringsAsFactors = FALSE)

constituents <- constituents[-c(64,78),]

#function returns adjusted close for symbol entered
adj_close <- function(ticker) 
  {
  library(quantmod)
  price_data <- getSymbols(ticker, from="2020-1-1", to=Sys.Date()+1, auto.assign=F)
  final <- price_data[,6]
  final <- as.data.frame(final)
  }
#retrieving all adjusted closes from the list
all_adjusted_close <- lapply(constituents$Symbol, adj_close)
#Stack overflow ##converts list values to data frame (returns from all constituents)
df <- data.frame(matrix(unlist(all_adjusted_close), ncol = max(length(all_adjusted_close)), byrow=FALSE))
#creating list of ticker symbols
ticker_list <- as.list(constituents$Symbol)
#naming returns of data frame columns
colnames(df) <- c(ticker_list)
###converting to XTS
dates <- seq(as.Date("2020-1-1"), length = nrow(df), by = "days")
##loading xts package
library(xts)
###adding dates to xts objects
ts_df <- xts(df, order.by = dates)
##lapply to convert prices to daily returns(from quantmod) for comparisons
daily_returns_constituents <- lapply(ts_df, dailyReturn)
##converting list to dataframe (again)
df_dr <- data.frame(matrix(unlist(daily_returns_constituents)
                        , ncol = max(length(daily_returns_constituents)), byrow=FALSE))
###adding ticker column names (again)
colnames(df_dr) <- c(ticker_list)


unique(constituents$Sector)
par(mar=c(5,11,4,5))
barplot(table(constituents$Sector),main = "Companies by Industry in the S&P 500"
        , xlab="Count of Companies", xlim = c(0,100), horiz = T, las=2)
