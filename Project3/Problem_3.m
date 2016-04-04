% load the dataset with 100k ratings
% This data set consists of 100,000 ratings (1-5) from 943 users on 1682 movies
% The data is randomly ordered. This is a tab separated list of 
% user id | item id | rating | timestamp. 
load ('.\ml-100k\u.data');

% create a matrix named R containing user ratings with users on rows and movies on columns.
% Each entry (i, j) of the matrix is the rating that user i has given to movie j.
R = zeros(943,1682);
for i=1:100000
    R(u(i,1),u(i,2)) = u(i,3);
end

RThresholded = R;
% if a user has rated a movie 4 or higher, we conclude they liked it.
% so we set the corresponding entry to 1.
RThresholded(find(R > 3)) = 1;
% if a user has rated a movie 3 or lower, we conclude they didn't like it.
% so we set the corresponding entry to -1.
RThresholded(find(R <= 3)) = -1;

% create a row vector that is used to split the dataset into 10 parts
steps = [1, 10001, 20001, 30001, 40001, 50001, 60001, 70001, 80001, 90001];
% create a row vector containing a random permutation of the integers from 1 to 100000 inclusive.
index = randperm(100000);

% create four 3-dimentional matrices to store all recall values, precision values, sensitivity values and specificity values.
% 10-fold cross validation | different threshold | k=10, 50 and 100
recall = zeros(10,24,3);
precision = zeros(10,24,3);
sensitivity = zeros(10,24,3);
specificity = zeros(10,24,3);

% run the matrix factorization for each case
option = struct();
option.dis = false;
k = [10,50,100];
for i=1:length(k)
    % 10-fold cross validation    
    for crossValidation = 1:10
        temp = R;
        
        % replace test data points in matrix temp with "not a number"
        for j = steps(crossValidation):steps(crossValidation)+9999
            iCoord = u(index(j),1);
            jCoord = u(index(j),2);
            temp(iCoord,jCoord) = NaN;
        end     
        
        % call wnmfrule function in the Matrix Factorization Toolbox
        [U,V] = wnmfrule(temp,k(i),option);
        % estimate the matrix R
        UV = U*V;
        
        count = 1;
        % iterate several thresholds
        for threshold = 0.2:0.2:4.8
            UVThresholded = UV;
            % if the rating of a movie is greater than or equal to the threshold, we conclude the user liked it.
            UVThresholded(find(UV > threshold)) = 1;
            % if the rating of a movie is smaller than the threshold, we conclude they didn't like it.
            UVThresholded(find(UV <= threshold)) = -1;

            % find all predicted values and corresponding real values in two matrix in each cross validation.
            predicted = [];
            actual = [];
            for j = steps(crossValidation):steps(crossValidation)+9999
                iCoord = u(index(j),1);
                jCoord = u(index(j),2);
                predicted = [predicted UVThresholded(iCoord,jCoord)];
                actual = [actual RThresholded(iCoord,jCoord)];
            end
            
            sum = predicted+actual;
            diff = predicted-actual;
            % calculate true positives, false positives and false negatives.
            truePos = length(find(sum == 2));
            trueNeg = length(find(sum == -2));
            falsePos = length(find(diff == 2));
            falseNeg = length(find(diff == -2));
            
            % calculate sensitivity and specificity which are used for plotting ROC curve.
            sensitivity(crossValidation,count,i) = truePos/(truePos+falseNeg);
            specificity(crossValidation,count,i) = trueNeg/(trueNeg+falsePos);
            
            % calculate recall and precision
            recall(crossValidation,count,i) = truePos/(truePos+falseNeg);
            precision(crossValidation,count,i) = truePos/(truePos+falsePos);

            count = count+1;           
        end      
    end
end

meanSensitivity = mean(sensitivity,1);
meanSpecificity = mean(specificity,1);
meanRecall = mean(recall,1);
meanPrecision = mean(precision,1);


% Following code is used to plot the relevant figures

% figure(1);
% hold on; 
% plot(0.2:0.2:4.8,meanPrecision(:,:,1),'r'); 
% plot(0.2:0.2:4.8,meanPrecision(:,:,2), 'b'); 
% plot(0.2:0.2:4.8,meanPrecision(:,:,3),'g'); 
% xlabel('Threshold'); 
% ylabel('Precision');
% hold off;

% figure(2);
% hold on; 
% plot(0.2:0.2:4.8,meanRecall(:,:,1),'r'); 
% plot(0.2:0.2:4.8,meanRecall(:,:,2), 'b'); 
% plot(0.2:0.2:4.8,meanRecall(:,:,3),'g'); 
% xlabel('Threshold'); 
% ylabel('Recall');
% hold off;

% figure(3);
% hold on; 
% plot(meanRecall(:,:,1),meanPrecision(:,:,1),'r'); 
% plot(meanRecall(:,:,2),meanPrecision(:,:,2), 'b'); 
% plot(meanRecall(:,:,3),meanPrecision(:,:,3),'g'); 
% xlabel('Recall'); 
% ylabel('Precision');
% hold off;

% figure(4);
% hold on; 
% plot(1-meanSpecificity(:,:,1),meanSensitivity(:,:,1),'r'); 
% plot(1-meanSpecificity(:,:,2),meanSensitivity(:,:,2), 'b'); 
% plot(1-meanSpecificity(:,:,3),meanSensitivity(:,:,3),'g'); 
% title('ROC Curve')
% xlabel('False Positive Rate'); 
% ylabel('True Positive Rate');
% hold off;