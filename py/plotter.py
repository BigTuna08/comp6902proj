import sys
from pylab import *
from ResultsManager import ResultsManager



if __name__ == '__main__':
    if len(sys.argv) > 2:
        rm = ResultsManager()
        var_name = sys.argv[1]
        res = rm.get_all_data(var_name, var_name)
        res = res.get(sys.argv[2])

        vals = rm.get_values(var_name)

        assert len(vals) == len(res), "Bad!"

        plot(vals, res)
        show()
    else:
        print("Requires 2 args\n"
              "1)- varible name\n"
              "2)- result type")

