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

% entry (i, j) of the matrix R is 0 if user i has not rated movie j yet.
temp = R;
% replace 0 in matrix temp with "not a number"
temp(find(R == 0)) = NaN;

% weight matrix w contains 1 in entries where we have known data points 
% and 0 in entries where the data is missing
W = zeros(943,1682);
W(find(R > 0)) = 1;

% run the matrix factorization for each case
option = struct();
option.dis = false;
k = [10,50,100];
LSE = zeros(length(k),1);
for j=1:length(k)
    % call wnmfrule function in the Matrix Factorization Toolbox
    [U,V] = wnmfrule(temp,k(j),option);
    % calculate the total least squared error 
    LSE(j) = sqrt(sum(sum((W .* (R - U*V)).^2)));        
end