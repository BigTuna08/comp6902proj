if ~exist('degs')
    M = dlmread('../../data/results/unweightedDegs.txt', '\t',0,0);
    degs = M(:,2)';
end

min_deg = min(degs);
max_deg = max(degs);
bin_edge_count = floor(log2(max_deg))+1
bin_edges = zeros(1,bin_edge_count);
for i=1:bin_edge_count
   bin_edges(i) = 2^i; 
end

histogram(degs,bin_edges); % create the plot
set(gca,'xscale','log'); % scale the x-axis
