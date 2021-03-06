# ex2---Titanic-Solve-Ready
---
title: "EX2"
author: "Alex&Liad"
date: "April 11, 2017"
output: html_document
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE)
```

## Installation of packages

This chunk consists the installation of all the relevant packages

```{r}
install.packages('e1071')
install.packages('ggplot2')
install.packages('tidyr')
install.packages('caTools')
install.packages('rpart')
install.packages('rpart.plot')
install.packages('C50')
install.packages('caret')
install.packages('lattice')
install.packages('class')
install.packages('gbm')
install.packages('caretEnsemble')
install.packages('plyr')
install.packages('mlbench')
install.packages('pROC')
```

## Importing Libraries

This chunk consists the import of the relevant libraries

```{r}
library(ggplot2)
library(tidyr)
library(caTools)
library(e1071)
library(rpart)
library(rpart.plot)
library(C50)
library(lattice)
library(class)
library(gbm)
library(caret)
library(caretEnsemble)
library(plyr)
library(mlbench)
library(pROC)
```

## Set Working Directory

This chunk consists the definition of the working directory

```{r}
knitr::opts_knit$set(root.dir = 'C:/Users/Liad/Desktop/Titanic Assignment')
getwd()
```

## Read the data

This chunk consists the read of the data

```{r}
dfTrain<-read.csv('train.csv')
dfTest<-read.csv('test.csv')
```

## Feel the data

This chunk consists the first 5 records of the train data

```{r}
head(dfTrain,5)
```

This chunk consists the summary of the train data

```{r}
summary(dfTrain)
```

This chunk consists the values of arttributes of the train data

```{r}
str(dfTrain)
```

## Prepration phase

After looking at the data, we decide not using the "Name" ,"cabin" and "Ticket" columns.
"Ticket" - We believe it will not indicat who will survive
"Cabin" - Too Many missing values 
We will clean those columns from the dataframe.
First, We will Fill the columns with the missing values.
THe columns we will fill are "Age"and "Embarked".
Also, we will turn the numeric columns to factors.
This chunk consists the actions of filling the missing data.

```{r}
dfTrain$Age = ifelse(is.na(dfTrain$Age),ave(dfTrain$Age, FUN = function(x) mean(x,na.rm=TRUE)),dfTrain$Age)
dfTrain$Fare = ifelse(is.na(dfTrain$Fare),ave(dfTrain$Fare, FUN = function(x) mean(x,na.rm=TRUE)),dfTrain$Fare)
mostCommon <- names(sort(table(dfTrain$Embarked), decreasing = TRUE))[1]
dfTrain$Embarked = ifelse(dfTrain$Embarked=="",mostCommon,ifelse(dfTrain$Embarked == 'S','S',ifelse(dfTrain$Embarked == 'C','C','Q')))
dfTrain$Pclass =as.factor(dfTrain$Pclass)
dfTrain$SibSp =as.factor(dfTrain$SibSp)
dfTrain$Parch =as.factor(dfTrain$Parch)
dfTrain$Embarked =as.factor(dfTrain$Embarked)
```

Finally, we will convert the dataset to a binary matrix (without "Age" and "Fare")
```{r}
binPclass <- as.factor(dfTrain$Pclass)
#binPclass <- data.frame(model.matrix(~.+0,data = dfTrain["Pclass"]))
binSex <- data.frame(model.matrix(~.+0,data = dfTrain["Sex"]))
binSibSp <-as.factor(dfTrain$SibSp)
#binSibSp <- data.frame(model.matrix(~.+0,data = dfTrain["SibSp"]))
binParch<-as.factor(dfTrain$Parch)
#binParch <- data.frame(model.matrix(~.+0,data = dfTrain["Parch"]))
binEmbarked <- data.frame(model.matrix(~.+0,data = dfTrain["Embarked"]))
tempName = apply(dfTrain['Name'], c(1,2), function(x) unlist(strsplit(trimws(unlist(strsplit(x, ","))[2], which = 'left'), ' '))[1])
binName<- data.frame(model.matrix(~.+0,data = data.frame(tempName)))
Survived<-dfTrain$Survived
Fare<-dfTrain$Fare
Age<-dfTrain$Age
dataframeTrain <- cbind(binPclass,binSex,Age,binSibSp,Fare,binEmbarked,Survived)
```

## Split the dfTrain to Train and Test for evaluation

This chunk consists the spliting of the train data to 80% train_set and to 20% of test_set

```{r}
set.seed(123)
split = sample.split(dataframeTrain$Survived,SplitRatio = 0.8)
training_set = subset(dataframeTrain, split==TRUE)
test_set = subset(dataframeTrain,split==FALSE)
```

## SVM - Train

```{r}
classifier = svm(formula= Survived ~., data = training_set,type = 'C-classification',gamma=1)
y_pred = predict(classifier,test_set[,-10])
table(y_pred,test_set$Survived)
model_accuracy = mean(y_pred==test_set$Survived)
model_accuracy
```

## Decision Tree - Train


```{r}
classifier = rpart(formula= Survived ~., data = training_set)
y_pred = predict(classifier,test_set[,-10])
testarray <-ifelse(y_pred>=0.5,'1','0')
table(testarray,test_set$Survived)
model_accuracy = mean(testarray==test_set$Survived)
model_accuracy
```


## Logistic regression - Train

This chunk consists the definition of the First model

```{r}
training_set$Age = round(as.numeric(training_set$Age))
training_set$Fare = round(as.numeric(training_set$Fare))
set.seed(123)
split = sample.split(dataframeTrain$Survived,SplitRatio = 0.8)
training_set = subset(dataframeTrain, split==TRUE)
test_set = subset(dataframeTrain,split==FALSE)
classifier = glm(formula= Survived ~.,
                 family = binomial, 
                data = training_set)
prob_pred = predict(classifier,type = 'response',newdata=test_set[,-10])
testarray <-ifelse(prob_pred>=0.6,'1','0')
table(testarray,test_set$Survived)
model_accuracy = mean(testarray==test_set$Survived)
model_accuracy
```

## KNN - Train

This chunk consists the definition of the Second model

```{r}
set.seed(123)
y_pred = knn(train = training_set[,-10],
             test = test_set[,-10],
             cl = training_set[,10],
             k=3)
table(test_set[,10],y_pred)
model_accuracy = mean(y_pred==test_set$Survived)
model_accuracy
```

## Create the results files for Kaggle

## Prepration phase

```{r}
dfTest$Age = ifelse(is.na(dfTest$Age),ave(dfTest$Age, FUN = function(x) mean(x,na.rm=TRUE)),dfTest$Age)
dfTest$Fare = ifelse(is.na(dfTest$Fare),ave(dfTest$Fare, FUN = function(x) mean(x,na.rm=TRUE)),dfTest$Fare)
mostCommon <- names(sort(table(dfTest$Embarked), decreasing = TRUE))[1]
dfTest$Embarked = ifelse(dfTest$Embarked=="",mostCommon,ifelse(dfTest$Embarked == 'S','S',ifelse(dfTest$Embarked == 'C','C','Q')))
dfTest$Pclass =as.factor(dfTest$Pclass)
dfTest$SibSp =as.factor(dfTest$SibSp)
dfTest$Parch =as.factor(dfTest$Parch)
dfTest$Embarked =as.factor(dfTest$Embarked)
binPclass <-as.factor(dfTest$Pclass)
#binPclass <- data.frame(model.matrix(~.+0,data = dfTest["Pclass"]))
binSex <- data.frame(model.matrix(~.+0,data = dfTest["Sex"]))
binSibSp<-as.factor(dfTest$SibSp)
#binSibSp <- data.frame(model.matrix(~.+0,data = dfTest["SibSp"]))
binParch<-as.factor(dfTest$Parch)
#binParch <- data.frame(model.matrix(~.+0,data = dfTest["Parch"]))
binEmbarked <- data.frame(model.matrix(~.+0,data = dfTest["Embarked"]))
tempName = apply(dfTest['Name'], c(1,2), function(x) unlist(strsplit(trimws(unlist(strsplit(x, ","))[2], which = 'left'), ' '))[1])
binName<- data.frame(model.matrix(~.+0,data = data.frame(tempName)))
Survived<-dfTest$Survived
Fare<-dfTest$Fare
Age<-dfTest$Age
dataframeTest <- cbind(binPclass,binSex,Age,binSibSp,Fare,binEmbarked)
```

## Testing Phase

## Decision Tree


```{r}
classifier = rpart(formula= Survived ~., data =dataframeTrain)
y_pred = predict(classifier,dataframeTest)
testarray <-data.frame(result=ifelse(y_pred>=0.5,'1','0'))
DecisionTreeResults = cbind(PassengerId=dfTest$PassengerId,Survived=as.character(testarray$result))
write.csv(DecisionTreeResults,file="DecisionTreeresults.csv",row.names = F)
```

## SVM

```{r}
classifiersvm = svm(formula= Survived ~., data = dataframeTrain,type = 'C-classification',gamma=1)
y_predsvm = data.frame(result=predict(classifiersvm,dataframeTest))
svmResults = cbind(PassengerId=dfTest$PassengerId,Survived=as.character(y_predsvm$result))
write.csv(svmResults,file="svmResults.csv",row.names = F)
```

## Logistic regression

```{r}
dataframeTrain$Age = round(as.numeric(dataframeTrain$Age))
dataframeTrain$Fare = round(as.numeric(dataframeTrain$Fare))
dataframeTest$Age = round(as.numeric(dataframeTest$Age))
dataframeTest$Fare = round(as.numeric(dataframeTest$Fare))
classifier = glm(formula= Survived ~.,
                 family = binomial, 
                data = dataframeTrain)
prob_pred = predict(classifier,type = 'response',newdata=dataframeTest)
testarray <-data.frame(result=ifelse(prob_pred>=0.5,'1','0'))
glmResults = cbind(PassengerId=dfTest$PassengerId,Survived=as.character(testarray$result))
write.csv(glmResults,file="glmresults.csv",row.names = F)
```

## KNN

This chunk consists the definition of the Second model

```{r}
set.seed(123)
y_pred = knn(train = dataframeTrain[,-10],
             test = dataframeTest,
             cl = dataframeTrain[,10],
             k=3)
knnResults = cbind(PassengerId=dfTest$PassengerId,Survived=as.character(y_pred))
write.csv(knnResults,file="KNNresults.csv",row.names = F)
```

## Ensemble with caret
```{r}
dfTrain$Pclass = as.factor(dfTrain$Pclass)
dfTrain$Sex = as.factor(dfTrain$Sex)
dfTrain$Age = as.factor(dfTrain$Age)
dfTrain$SibSp = as.factor(dfTrain$SibSp)
dfTrain$Fare = as.factor(dfTrain$Fare)
dfTrain$Embarked = as.factor(dfTrain$Embarked)
dfTrain$Survived = factor(dfTrain$Survived, levels=c(1,0), labels=c("Yes","No"))
dfTest$Pclass = as.factor(dfTest$Pclass)
dfTest$Sex = as.factor(dfTest$Sex)
dfTest$Age = as.factor(dfTest$Age)
dfTest$SibSp = as.factor(dfTest$SibSp)
dfTest$Fare = as.factor(dfTest$Fare)
dfTest$Embarked = as.factor(dfTest$Embarked)
control <-
  trainControl(
    method = "cv",
    number = 5,
    savePredictions = 'final',
    classProbs = TRUE,
    summaryFunction = twoClassSummary
)
models <- caretList(
  Survived ~ Pclass+SibSp+Sex+Embarked,
  data = dfTrain,
  trControl = control,
  metric = "ROC",
  methodList = c("glm","rpart")
)
y_predens <- as.data.frame(predict(models, newdata=dfTest))
y_res = y_predens$glm + y_predens$rpart
y_res = ifelse(y_res>=1,0,1)
ensResults = cbind(PassengerId=dfTest$PassengerId,Survived=as.character(y_res))
write.csv(ensResults,file="ENSresults.csv",row.names = F)
```
