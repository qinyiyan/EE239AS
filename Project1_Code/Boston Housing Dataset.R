library(glmnet)
# library()
boston_housing_data_raw <- read.csv(file = "housing_data.csv", header = TRUE, sep = ",")

#Problem 4

#linear model
fold_num = 10 #Folds
# sample from 1 to fold_num, nrow times (the number of observations in the data)
boston_housing_data_raw$id <- sample(1:fold_num, nrow(boston_housing_data_raw), replace = TRUE)
list <- 1:fold_num
result_temp_linear <- data.frame()
fit_linear_best <- list()
best_RMSE_difference_linear <- 1000.0
for (i in 1:fold_num){
    # remove rows with id i from dataframe to create training set
    # select rows with id i to create test set
    trainingset <- subset(boston_housing_data_raw, id %in% list[-i])
    testset <- subset(boston_housing_data_raw, id %in% c(i))

    # run a linear regression model
    fit_linear <- lm(MEDV ~ CRIM+ZN+INDUS+CHAS+NOX+RM+AGE+DIS+RAD+TAX+PTRATIO+B+LSTAT, data=trainingset)

    temp_prediction_linear <- as.data.frame(predict(fit_linear, testset[,-14]))
    # append this iteration's predictions to the end of the prediction_linear data frame
    cat("===========================================\n")
    cat(sprintf("No.%d\n", i))
    cat(sprintf("fit_linear coefficients:\n"))
    print(fit_linear$coefficients)

    result_temp_linear <- cbind(temp_prediction_linear, as.data.frame(testset[,14]))
    names(result_temp_linear) <- c("Predicted", "Actual")
    result_temp_linear$Difference <- abs(result_temp_linear$Actual - result_temp_linear$Predicted) ^ 2
    temp_linear_RMSE <- sqrt(sum(result_temp_linear$Difference) / length(result_temp_linear$Difference))
    cat(sprintf("Linear Model: The RMSE is %f\n", temp_linear_RMSE))
    if (best_RMSE_difference_linear > temp_linear_RMSE){
        best_RMSE_difference_linear <- temp_linear_RMSE
        fit_linear_best <- fit_linear
    }
}
#residuals versus fitted values plot
#plot(fit_linear_best)

#Fitted values and actual values scattered plot over time
prediction_all_data <- as.data.frame(predict(fit_linear_best, boston_housing_data_raw[,-14]))
difference_all_data <- cbind(prediction_all_data, as.data.frame(boston_housing_data_raw[,14]))
names(difference_all_data) <- c("Predicted", "Actual")
plot(c(1:length(difference_all_data$Predicted)), difference_all_data$Actual, type="p", col="red", cex=0.5, xlab="", ylab="Fitted values and actual values", main="Fitted values and actual values scattered plot over time")
points(c(1:length(difference_all_data$Predicted)), difference_all_data$Predicted, col="blue", cex=0.5)

#polynomial model
fold_num = 10 #Folds
boston_housing_data_raw$id <- sample(1:fold_num, nrow(boston_housing_data_raw), replace = TRUE)
list <- 1:fold_num
best_RMSE_difference_poly <- 1000.0
result_temp_poly <- data.frame()
fit_poly_best <- list()
for (i_degree in 1:30){
    sum_RMSE_difference_poly <- 0
    for (i in 1:fold_num){
        # remove rows with id i from dataframe to create training set
        # select rows with id i to create test set
        trainingset <- subset(boston_housing_data_raw, id %in% list[-i])
        testset <- subset(boston_housing_data_raw, id %in% c(i))

        # run a poly regression model
        fit_poly <- lm(MEDV ~ poly(CRIM, i_degree, raw=TRUE) + poly(ZN, i_degree, raw=TRUE) + poly(INDUS, i_degree, raw=TRUE) + poly(CHAS, i_degree, raw=TRUE) + poly(NOX, i_degree, raw=TRUE) + poly(RM, i_degree, raw=TRUE) + poly(AGE, i_degree, raw=TRUE) + poly(DIS, i_degree, raw=TRUE) + poly(RAD, i_degree, raw=TRUE) + poly(TAX, i_degree, raw=TRUE) + poly(PTRATIO, i_degree, raw=TRUE) + poly(B, i_degree, raw=TRUE) + poly(LSTAT, i_degree, raw=TRUE), data=trainingset)

        temp_prediction_poly <- as.data.frame(predict(fit_poly, newdata=testset[,-14]))
        # append this iteration's predictions to the end of the prediction_poly data frame
        result_temp_poly <- cbind(temp_prediction_poly, as.data.frame(testset[,14]))
        names(result_temp_poly) <- c("Predicted", "Actual")
        result_temp_poly$Difference <- abs(result_temp_poly$Actual - result_temp_poly$Predicted) ^ 2
        temp_poly_RMSE <- sqrt(sum(result_temp_poly$Difference) / length(result_temp_poly$Difference))
        sum_RMSE_difference_poly <- sum_RMSE_difference_poly + temp_poly_RMSE
        if (best_RMSE_difference_poly > temp_poly_RMSE){
            best_RMSE_difference_poly <- temp_poly_RMSE
            fit_poly_best <- fit_poly
        }
    }
    cat("===========================================\n")
    cat(sprintf("degree is %d\n", i_degree))
    cat(sprintf("Polynomial Model: The average RMSE is %f\n\n", sum_RMSE_difference_poly/fold_num))
}

#Problem 5(a)

fold_num = 10 #Folds
# sample from 1 to fold_num, nrow times (the number of observations in the data)
boston_housing_data_raw$id <- sample(1:fold_num, nrow(boston_housing_data_raw), replace = TRUE)
list <- 1:fold_num
result_temp_ridge <- data.frame()
fit_ridge_best <- list()
best_RMSE_difference_ridge <- 1000.0
sum_RMSE_difference_ridge <- 0
for (i_alpha in c(0.1,0.01,0.001)){
    for (i in 1:fold_num){
        # remove rows with id i from dataframe to create training set
        # select rows with id i to create test set
        trainingset <- subset(boston_housing_data_raw, id %in% list[-i])
        testset <- subset(boston_housing_data_raw, id %in% c(i))

        # run a ridge regression model
        training_x = model.matrix(MEDV ~ CRIM+ZN+INDUS+CHAS+NOX+RM+AGE+DIS+RAD+TAX+PTRATIO+B+LSTAT, trainingset)
        training_y = trainingset$MEDV
        fit_ridge <- glmnet(training_x, training_y, alpha = 0, lambda = i_alpha)

        test_x <- model.matrix(MEDV ~ CRIM+ZN+INDUS+CHAS+NOX+RM+AGE+DIS+RAD+TAX+PTRATIO+B+LSTAT, testset)
        temp_prediction_ridge <- as.data.frame(predict(fit_ridge, s=i_alpha, newx=test_x))
        # append this iteration's predictions to the end of the prediction_ridge data frame
        # cat(sprintf("fit_ridge coefficients:\n"))
        # print(coef(fit_ridge))

        result_temp_ridge <- cbind(temp_prediction_ridge, as.data.frame(testset[,14]))
        names(result_temp_ridge) <- c("Predicted", "Actual")
        result_temp_ridge$Difference <- abs(result_temp_ridge$Actual - result_temp_ridge$Predicted) ^ 2
        temp_ridge_RMSE <- sqrt(sum(result_temp_ridge$Difference) / length(result_temp_ridge$Difference))
        sum_RMSE_difference_ridge <- sum_RMSE_difference_ridge + temp_ridge_RMSE
        if (best_RMSE_difference_ridge > temp_ridge_RMSE){
            best_RMSE_difference_ridge <- temp_ridge_RMSE
            fit_ridge_best <- fit_ridge
        }
    }
    cat("===========================================\n")
    cat(sprintf("alpha = \n", i_alpha))
    cat(sprintf("Ridge Model: The average RMSE is %f\n", sum_RMSE_difference_ridge/fold_num))
}

#Problem 5(b)

fold_num = 10 #Folds
# sample from 1 to fold_num, nrow times (the number of observations in the data)
boston_housing_data_raw$id <- sample(1:fold_num, nrow(boston_housing_data_raw), replace = TRUE)
list <- 1:fold_num
result_temp_ridge <- data.frame()
fit_ridge_best <- list()
best_RMSE_difference_ridge <- 1000.0
sum_RMSE_difference_ridge <- 0
for (i_alpha in c(0.1,0.01,0.001)){
    for (i in 1:fold_num){
        # remove rows with id i from dataframe to create training set
        # select rows with id i to create test set
        trainingset <- subset(boston_housing_data_raw, id %in% list[-i])
        testset <- subset(boston_housing_data_raw, id %in% c(i))

        # run a ridge regression model
        training_x = model.matrix(MEDV ~ CRIM+ZN+INDUS+CHAS+NOX+RM+AGE+DIS+RAD+TAX+PTRATIO+B+LSTAT, trainingset)
        training_y = trainingset$MEDV
        fit_ridge <- glmnet(training_x, training_y, alpha = 1, lambda = i_alpha)

        test_x <- model.matrix(MEDV ~ CRIM+ZN+INDUS+CHAS+NOX+RM+AGE+DIS+RAD+TAX+PTRATIO+B+LSTAT, testset)
        temp_prediction_ridge <- as.data.frame(predict(fit_ridge, s=i_alpha, newx=test_x))
        # append this iteration's predictions to the end of the prediction_ridge data frame
        # cat(sprintf("fit_ridge coefficients:\n"))
        # print(coef(fit_ridge))

        result_temp_ridge <- cbind(temp_prediction_ridge, as.data.frame(testset[,14]))
        names(result_temp_ridge) <- c("Predicted", "Actual")
        result_temp_ridge$Difference <- abs(result_temp_ridge$Actual - result_temp_ridge$Predicted) ^ 2
        temp_ridge_RMSE <- sqrt(sum(result_temp_ridge$Difference) / length(result_temp_ridge$Difference))
        sum_RMSE_difference_ridge <- sum_RMSE_difference_ridge + temp_ridge_RMSE
        if (best_RMSE_difference_ridge > temp_ridge_RMSE){
            best_RMSE_difference_ridge <- temp_ridge_RMSE
            fit_ridge_best <- fit_ridge
        }
    }
    cat("===========================================\n")
    cat(sprintf("alpha = \n", i_alpha))
    cat(sprintf("Ridge Model: The average RMSE is %f\n", sum_RMSE_difference_ridge/fold_num))
}
