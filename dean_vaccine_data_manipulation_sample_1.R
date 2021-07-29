#Ryan Dean
#Final Exam
#6/27/2021
#I completed the final exam with help from the professor, the book, and my notes

#Question 1
vax <- usVaccines
plot(vax)
diff_vax <- diff(vax)
plot(diff_vax)
vax
summary(usVaccines)
#change points for variance
library(changepoint)
na.omit(vax)
par(mfrow=c(3,2))
vaxdf <- data.frame(diff_vax)
chgpnt.DTP1 <- cpt.var(vaxdf$DTP1)
plot(chgpnt.DTP1, main="DTP1 Difference", ylab="vaccinated change")
chgpnt.Hep <- cpt.var(vaxdf$HepB_BD)
plot(chgpnt.Hep, main="HepB_BD Difference", ylab="vaccinated change")
chgpnt.Pol3 <- cpt.var(vaxdf$Pol3)
plot(chgpnt.Pol3, main="Pol3 Difference", ylab="vaccinated change")
chgpnt.Hib3 <- cpt.var(vaxdf$Hib3)
plot(chgpnt.Hib3, main="Hib3 Difference", ylab="vaccinated change")
chgpnt.MCV1 <- cpt.var(vaxdf$MCV1)
plot(chgpnt.MCV1, main="MCV1 Difference", ylab="vaccinated change")
#Question 2
vaxReport <- allSchoolsReportStatus
View(vaxReport)
vaxReport
summary(vaxReport)
#Proportion Table
vaxTable <- table(vaxReport$pubpriv, vaxReport$reported)
prop.table(vaxTable)
barplot(vaxTable)
#Question 3
#converting columns to get vaccine rate
vaccination_rates <- data.frame(c("DTPvaxpct", "Poliovaxpct", "HepBvaxpct", "MMRvaxpct"))
vaccination_rates$DTPvaxpct <- 1-(sum(districts$WithoutDTP)/sum(districts$Enrolled))
vaccination_rates$Poliovaxpct <- 1-(sum(districts$WithoutPolio)/sum(districts$Enrolled))
vaccination_rates$HepBvaxpct <- 1-(sum(districts$WithoutHepB)/sum(districts$Enrolled))
vaccination_rates$MMRvaxpct <- 1-(sum(districts$WithoutMMR)/sum(districts$Enrolled))
summary(usVaccines)
summary(districts)
summary(vaccination_rates)
#Question 4
districts_cor <- data.frame(districts$WithoutDTP, districts$WithoutPolio, districts$WithoutMMR, districts$WithoutHepB)
corr_matrix <- round(cor(districts_cor),3)
corr_matrix
#Predictive Analysis
#Question 5
#logistic regression for binary classification
library(MASS)
library(MCMCpack)
districts$DistrictComplete <- as.numeric(districts$DistrictComplete)
districts_regression <- districts[,2:13]
#sub-setting the data set in order to generate a random sample 
reported <- subset(districts_regression, DistrictComplete == 1)
notreported <- subset(districts_regression, DistrictComplete == 0)
summary(reported)
summary(notreported)
str(reported)
str(notreported)
#random sample from reported to try to reduce the effect of the reported variable
reportedSample <- reported[sample(nrow(reported), 100),]
#combining the data frames
districts_regression <- rbind(reportedSample, notreported)
#EDA and Transformations
hist(districts_regression$Enrolled)
districts_regression$Enrolled <- log(districts_regression$Enrolled)
hist(districts_regression$Enrolled)
#hist(districts_regression$TotalSchools)
#districts_regression$TotalSchools <- log(districts_regression$TotalSchools)
#hist(districts_regression$TotalSchools)

#districtsLOGIT$Enrolled <- (districts$Enrolled/enrolledsum)*100 
#districtsLOGIT$Enrolled <- (districts$Enrolled/sum(districts$Enrolled))*100
#districtsLOGIT$TotalSchools <- (districts$TotalSchools/sum(districts$TotalSchools))*100
distOut <- glm(DistrictComplete ~ PctChildPoverty + PctFreeMeal + PctFamilyPoverty + Enrolled + TotalSchools, 
               binomial(), districts_regression, control= list(maxit=100))
summary(distOut)

#distOut2 <- glm(DistrictComplete ~ PctChildPoverty + PctFreeMeal + PctFamilyPoverty, 
               #binomial(), districtsLOGIT, control= list(maxit=100))
#summary(distOut2)

distOUTBayes <- MCMClogit(DistrictComplete ~ PctChildPoverty + PctFreeMeal + PctFamilyPoverty + Enrolled + TotalSchools,
                          districts_regression) 
summary(distOUTBayes)

#Question 6
enrolled_regression <- lm(PctUpToDate ~ PctChildPoverty + PctFreeMeal + PctFamilyPoverty + Enrolled + TotalSchools,
                    districts_regression)
summary(enrolled_regression)

library(BayesFactor)
uptodateBayes <- lmBF(PctUpToDate ~ PctChildPoverty + PctFreeMeal + PctFamilyPoverty + Enrolled + TotalSchools,
                      districts_regression, posterior=TRUE, iterations=1000)
summary(uptodateBayes)
#Question 7
beliefregression <- lm(PctBeliefExempt ~ PctChildPoverty + PctFreeMeal + PctFamilyPoverty + Enrolled + TotalSchools,
                    districts_regression)
summary(beliefregression)
beliefBayes <- lmBF(PctBeliefExempt ~ PctChildPoverty + PctFreeMeal + PctFamilyPoverty + Enrolled + TotalSchools,
                    districts_regression, posterior=TRUE, iterations=1000)
summary(beliefBayes)
#Question 8
#poverty and other things such as school district size and enrollment make a difference, shows California laws are strict in keep people vaxxed