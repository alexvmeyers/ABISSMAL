# General purpose functions to run checks within customized data processing functions

################## Get user-specified values for formal arguments ##################

# Modified from https://stackoverflow.com/questions/66329835/how-to-get-all-parameters-passed-into-a-function-with-their-values

getFunctionParameters <- function() {
  
  # Get the environment in which the function was called
  pf <- parent.frame()      
  
  errTest <- try({eval(quote(list(...)), envir = pf)}, silent = TRUE)
  
  if(any(grepl("error", attributes(errTest)$class))){
    
    # Get the names of arguments
    nms <- sapply(ls(envir = pf, sorted = FALSE), as.name)
    
    # Get all user-specified values for arguments
    res <- c(lapply(nms, eval, envir = pf))
    
  } else {
    
    # Get the ... from the call
    dots <- eval(quote(list(...)), envir = pf)
    
    # Get the names of arguments that are not in the ...
    nms <- sapply(ls(envir = pf, sorted = FALSE), as.name)
    
    # Get all user-specified values for arguments
    res <- c(lapply(nms, eval, envir = pf), dots)
    
  }
  
  # Then remove any values without names
  res <- res[names(res) != ""]
  
  # Also remove orig_opts arguments, retain arguments for the function only
  res[-grep("orig_opts", names(res))]
  
}


############################## Formal arguments ####################################

check_defined <- function(y){

  err <- paste(y, "must be specified, and cannot be NULL or NA", sep = " ")
  
  if(is.null(y) | is.na(y) & y != ""){
    stop(err)
  }
  
}

# Check that arguments are strings
check_string <- function(y){
  
  err <- paste("Expected a string but", y, "is not a string", sep = " ")
  
  if(class(y) != "character"){
    stop(err)
  }
  
}

# Check that arguments are numeric 
check_numeric <- function(y){
  
  err <- paste("Expected a numeric value but", y, "is not numeric", sep = " ")
  
  if(class(y) != "numeric"){
    stop(err)
  }
  
}


# Check that arguments are Boolean
check_boolean <- function(y){
  
  err <- paste("Expected a Boolean value but", y, "is not Boolean", sep = " ")
  
  if(class(y) != "logical"){
    stop(err)
  }
  
}

# Check that arguments are NA
check_NA <- function(y){
  
  err <- paste("Expected an NA value but", y, "is not NA", sep = " ")
  
  if(length(y) == 1){
    if(!is.na(y)){
      stop(err)
    }
    
  } else if(length(y) > 1){
    if(!all(is.na(y))){
      stop(err)
    }
  }
  
}

# Check that arguments are NULL
check_null <- function(y){
  
  err <- paste("Expected a NULL value but", y, "is not NULL", sep = " ")
  
  if(!is.null(y)){
    stop(err)
  }
  
}

# Check that arguments are not NULL
check_not_null <- function(y){
  
  err <- paste("Expected a non-NULL value but", y, "is NULL", sep = " ")
  
  if(is.null(y)){
    stop(err)
  }
  
}

# Check that sensor arguments are written as expected
check_sensor_spelling <- function(y){
  
  err <- paste("The value provided for the sensor argument, ", y, ", is not correct, check your spelling or captialization", sep = "")
  
  if(!grepl("^RFID$|^IRBB$|^Video$", y)){
    stop(err)
  }
  
}

############################## Directories and Files ####################################

# Check that the each directory in a vector of directories exists
check_dirs <- function(path, y){
  
  err <- paste("The directory", y, "does not exist", sep = " ")
  
  if(!dir.exists(file.path(path, y))){
    stop(err)
  }
  
}

# Check that the given directory is not empty and does have files
# For earlier functions combining many raw data files into a single combined raw data file
check_dir_notEmpty <- function(path, pattern){
  
  err <- paste("The directory", path, "does not have", pattern, "files", sep = " ")
  
  if(length(list.files(path, pattern)) == 0){
    stop(err)
  }
  
}

# Check that the given file in the given directory exists (for later functions)
check_file <- function(path, y){
  
  err <- paste("The file", y, "does not exist in the directory", path, sep = " ")
  
  if(!file.exists(file.path(path, y))){
    stop(err)
  }
  
}

################################### Data #########################################

# Check that the data frame used for subsequent processing is a data frame
check_df_class <- function(df){
  
  if(!any(grepl("data.frame", class(df)))){
    stop('This object needs to be a data frame')
  }
  
}


# Check that a data frame has each column in a vector of columns specified in the formal arguments
check_fArgs_data_cols <- function(y, df){
  
  if(length(y) == 1){
     
      err <- paste("The column", y, "was not found in the data frame", sep = " ")
      
    if(!y %in% names(df)){
      stop(err)
    }
    
  } else if(length(y) > 1){
    
    sapply(1:length(y), function(z){
      
      err <- paste("The column", y[z], "was not found in the data frame", sep = " ")
      
      if(!y[z] %in% names(df)){
        stop(err)
      }
      
    })
    
  }
  
}

# Check that a data frame has each column in a vector of columns NOT specified in the formal arguments
check_data_cols <- function(y, df){
  
    err <- paste("The column", y, "was not found in the data frame", sep = " ")
    
    if(!y %in% names(df)){
      stop(err)
    }
}

# Check that a given column from the formal arguments does not have NAs 
check_fArgs_cols_nas <- function(y, df){
  
  if(length(y) == 1){
    
    err <- paste("The column", y, "has NA (missing) values", sep = " ")
    
    if(any(is.na(df[[y]]))){
      stop(err)
    }
    
  } else if(length(y) > 1){
    
    sapply(1:length(y), function(z){
      
      err <- paste("The column", y[z], "has NA (missing) values", sep = " ")
      
      if(any(is.na(df[[y[z]]]))){
        stop(err)
      }
      
    })
    
  }
  
}

# Check that a data frame has each column in a vector of columns NOT specified in the formal arguments does not have NAs
check_cols_nas <- function(y, df){
  
  err <- paste("The column", y, "has NA (missing) values", sep = " ")
  
  if(any(is.na(df[[y]]))){
    stop(err)
  }
  
}

# Check that any timestamps columns from the formal arguments are in the right format. This conditional also catches NAs in timestamps
check_tstmps_cols <- function(y, df, format){
  
  if(length(y) == 1){
    
    err <- paste("The column", y, "needs to be in a format compatible with temporal calculations", sep = " ")
    
    if(any(is.na(as.POSIXct(df[[y]], format = format)))){
      stop(err)
    }
    
  } else if(length(y) > 1){
    
    sapply(1:length(y), function(z){
      
      err <- paste("The column", y[z], "needs to be in a format compatible with temporal calculations", sep = " ")
      
      if(any(is.na(as.POSIXct(df[[y[z]]], format = format)))){
        stop(err)
      }
      
    })
    
  }
  
}

# Check that a given column has the expected values
check_col_values <- function(col_nm, df, vals){
  
  tmp_col <- col_nm
  tmp_vals <- vals
  
  err <- paste("The column", tmp_col, "does not have one or both of the expected values", paste(tmp_vals, collapse = "; "), sep = " ")
  
  if(!all(unique(df[[tmp_col]]) %in% tmp_vals)){
    stop(err)
  }
  
}