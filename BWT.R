library(stringr)

bwt_encode <- function(s) {
  if(!require(stringr)) {
    install.packages("stringr")
  }
  library(stringr)
  
  if(!is.character(s)) stop("Not a string")
  l <- nchar(s)
  if(l==0) stop("Empty string")
  # table of circular strings
  table <- sapply(c(seq_along(1:l)),function(i) paste0(str_sub(s,i+1),str_sub(s,end=i)))
  table_sorted <- sort(table)
  # place of original string
  index <- match(s,table_sorted)
  # clustered string
  clust <- paste0(sapply(table_sorted, function(i) str_sub(i,-1,-1)))
  list(index,clust)
  
}


bwt_decode <- function(clust,index) {
  l <- length(clust)
  orig_clust <- clust
  for(i in seq_along(1:l-1)) {
    clust <- mapply(function(x,y) paste0(x,y),orig_clust,clust)
    clust <- sort(clust)
  }
  clust[index]
  
}

