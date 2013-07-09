from data import data

"""
    The purpose of this file is the main experimental data analysis
"""

class Data:
    #~ Constructor For the script
    def __init__(self, run=None):
        self.COPPER_MR      = 63.55
        self.IRON_MR        = 55.85
        self.ASSAY_GRAD     = 0.015
        self.run = run

    def GetExptRun(self):
        return self.run

    def GetRawIronData(self):
        return self.raw_data

    #~  Processing the iron data

    def iron_conc(self):
        self.raw_data = data.data_run(self.run)
        self.iron_data  = {}

        for k in self.raw_data :
            self.iron_data[k] = [self.raw_data[k][0], [], []]

            for v in self.raw_data[k][1]:
                self.iron_data[k][1].append(self.assay_equation(v))

            for v in self.raw_data[k][2]:
                self.iron_data[k][2].append(self.assay_equation(v))

        return self.iron_data

    """
        The function below calculates the mass of copper in solution by:
            - taking iron data and finding the moles and finding the original value

        ASSUMPTIONS:
            - at [0] represents the iron concentration at t = 0
                > If not in data I should add it manually
    """

    def copper_conc(self):
        self.iron_data = self.iron_conc()
        self.copper_data = {}

        for k in self.iron_data :
            self.copper_data[k] = [self.iron_data[k][0], []]

            temp = self.iron_data[k][1][0]

            for v in self.iron_data[k][1]:
                moles_iron_dt       = self.moles_iron(temp) - self.moles_iron(v)
                mass_copper         = self.mass_copper(moles_iron_dt)
                self.copper_data[k][1].append(mass_copper)

        return self.copper_data

        #~ for k,v in self.iron.iteritems():
            #~ print k, '=', v

    #~ Processing the iron data based on the rate equation
    def assay_equation(self, value):
        value = value * 100 / (1000 * self.ASSAY_GRAD)
        return value

    def moles_iron(self, mass_iron):
        moles_iron = mass_iron / self.IRON_MR
        return moles_iron

    def mass_copper(self, moles_iron):
        mass_copper = moles_iron * self.COPPER_MR / 2
        return mass_copper

#~ class Rates():
    """
        The main purpose of this class is to find the rates of the reaction from the data
    """
    #~ def __init__(self, run=None):
        #~ self.x = 1
    #~ data = Data(run = 7.4)
    #~ data.copper_conc()


if __name__  == "__main__":
    print "From Main"
#   app = DataPlot(run = 7.5)
    #~ print data.data_run('ALL')


