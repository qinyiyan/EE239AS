% importdata from u.data
u = importdata('Z:\Desktop\Problem5\ml-100k\u.data');
numUser = max(u(:,1));
numMovie = max(u(:,2));
Rating = zeros(numUser,numMovie);
for i=1:100000
    Rating(u(i,1),u(i,2)) = u(i,3);
end

[num_user num_movie] = size(Rating);
lambda = [0.01,0.1,1];

option = struct();
% option.dis = false;
option.itr = 1;

k = [10,50,100];

Rating_2 = Rating;
Rating_2(find(Rating == 0)) = NaN;

index = randperm(100000);
steps = [1,10001,20001,30001,40001,50001,60001,70001,80001,90001];

% set threshold > 3
Rating_threshold = Rating;
Rating_threshold(find(Rating <= 3)) = 0;
Rating_threshold(find(Rating > 3)) = 1;
Rating_threshold(isnan(Rating_2)) = NaN;

precision = zeros(numUser,10,length(k),length(lambda));
HitRate = zeros(numUser,10,length(k),length(lambda),30);
FalseRate = zeros(numUser,10,length(k),length(lambda),30);
for i = 1:length(lambda)
    for j = 1:length(k)
        for Cross_validation = 1:10
        	Rating_temp = Rating_2;
        	Rating_test = ones(size(Rating_2));
        	for st = steps(Cross_validation):steps(Cross_validation) + 9999
            	ind = index(st);            
            	Rating_temp(u(ind,1),u(ind,2)) = NaN;
            	Rating_test(u(ind,1),u(ind,2)) = NaN;
        	end        
        
        [U,V] = wnmfrule_for_part5(Rating_temp,k(j),lambda(i),option);
        UV = U*V;
        % find index of test data
        Index_test = isnan(Rating_test);
        Predict = -1*inf(size(UV));
        Predict(Index_test) = UV(Index_test);
        test = NaN(size(Predict));
        test(Index_test) = Rating_threshold(Index_test);
        
		% find top 5 movies and ignore those without rating
        	for user=1:numUser
            	[sortedValues,sortIndex] = sort(Predict(user,:),'descend');
            	top_movie = sortIndex(1:5);
            	total = 0;
            	for movie = 1:5
                	if(~isnan(test(user,top_movie(movie))))
                    	total = total + 1;
                    	if(test(user,top_movie(movie)))
                        	precision(user,Cross_validation,j,i) = precision(user,Cross_validation,j,i)+1;
                    	end                  
                	end
            	end
			% calculate the precision
            if(total)
                precision(user,Cross_validation,j,i) = precision(user,Cross_validation,j,i)/total;
            else
                precision(user,Cross_validation,j,i) = 0;
            end           
			
			% calculate the number of movies liked by users and not liked by users
           
            	for L = 1:30
					Hit_temp = 0;
					False_temp = 0;
					for L_temp = 1 : L;
                		if(~isnan(test(user,sortIndex(L_temp))))                    
                    		if(test(user,sortIndex(L_temp)))
                        		Hit_temp = Hit_temp + 1;
                            elseif(test(user,sortIndex(L_temp))==0)
                        		False_temp = False_temp + 1;
                    		end
                		end
                    end
                % calculate hit rate and false-alarm rate
                    if (((length(find(test(user,:) == 1)))~=0) && ((length(find(test(user,:) == 0)))~=0))
                        HitRate(user,Cross_validation,j,i,L) = Hit_temp / (length(find(test(user,:) == 1)));
                        FalseRate(user,Cross_validation,j,i,L) = False_temp / (length(find(test(user,:) == 0)));
                    end
        		end
			end 
        end      
    end
end
Final_precision = mean(mean(mean(mean(precision)))); 
Final_HitRate = mean(mean(HitRate));
Final_FalseRate = mean(mean(FalseRate));
temp_precision = mean(mean(precision));

for i = 1:length(lambda)
    for j = 1:length(k)
		x = Final_FalseRate(:,:,j,i,1:30);
		y = Final_HitRate(:,:,j,i,1:30);
        plot(x(:),y(:),'-');
	end
end