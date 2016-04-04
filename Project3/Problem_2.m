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

% create a row vector that is used to split the dataset into 10 parts
steps = [1, 10001, 20001, 30001, 40001, 50001, 60001, 70001, 80001, 90001];
% create a row vector containing a random permutation of the integers from 1 to 100000 inclusive.
index = randperm(100000);
% create a 3-dimentional matrix to store all absolute errors
error = zeros(10,10000,3);

% run the matrix factorization for each case
option = struct();
option.dis = false;
% option.iter = 50;
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
        % estimate matrix R
        UV = U*V;
        
        % caculate the prediction error |Rpredicted-Ractual|
        testIndex = 1;
        for j = steps(crossValidation):steps(crossValidation)+9999
            iCoord = u(index(j),1);
            jCoord = u(index(j),2);
            error(crossValidation,testIndex,i) = abs(UV(iCoord,jCoord)-R(iCoord,jCoord));
            testIndex = testIndex + 1;
        end            
    end   
end

% calculate the average absolute error
meanError = mean(error,2);
