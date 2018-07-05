./scripts/clear_all_data.sh
wait
cd clique_solver
git clone https://github.com/ryanrossi/pmc.git
wait
cd pmc-master
cp ../../other/Makefile-pmc Makefile   # original file won't compile with newer c++ compiler, this replaces it
wait
make
wait
cd ../..
echo "Directory stucture created and clique solver installed"