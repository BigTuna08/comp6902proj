function [degs] = el_to_degs(M)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
M = M(:)
degs = zeros(1, max(M)+1);
for i = M'
   degs(1,i+1) = degs(1,i+1) + 1; 
end
end

