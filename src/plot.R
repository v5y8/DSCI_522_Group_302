# author: Carlina
# date: 2020-01-15

"This script creats a several figures as part of the EDA aligning with our Horse race in Hong Kong 
prediction dataset.

Usage: src/plot.R <file_path> <out_dir>

Options: 
<file_path>  Path (including filename) to training data from the wrangle.py, must be within the /data directory.
<out_dir>  Destination path of files to be saved, to be stored in /data directory.
" -> doc

library(tidyverse)
library(ggplot2)
library(docopt)
library(tidyr)

opt <- docopt(doc) #parse the text

main <- function(file_path, out_dir){
  
  # test to check that csv is inputted 
  if (substr(file_path, (nchar(file_path)+1)-3 ,nchar(file_path)) != "csv"){
    stop("Must have an csv file in file_path")
  }
  
  # read in data
  data_train <- read.csv(file_path)
  
  # Pre-wrangling for plotting
  data_train["plc"] <- gsub("[^0-9\\,]", "", data_train$plc)
  
  #Drop NAs and set types as numeric
  win_odds <- data_train %>%
    drop_na(winodds) %>%
    drop_na(plc) 
  win_odds$plc <- as.numeric(win_odds$plc)
  
  win_odds <- win_odds %>%
    group_by(winodds) %>%
    summarize(place_mean= mean(plc, na.rm=TRUE))
  
  
  #Plot line graph for Average numerical placement of horses by win odds
  p1 <- ggplot(win_odds) +
    geom_line(aes(x=winodds, y=place_mean), colour= "blue") + 
    labs(title= "Average numerical placement of horses by win odds", x= "Win odds", y= "Placement") +
    scale_y_continuous(breaks=c(1,2,3,4,5,6,7,8,9,10))
  
  ggsave(p1, file=paste(out_dir, '/numeric_placement.png', sep = ""))
}

main(opt[["file_path"]], opt[["out_dir"]])
