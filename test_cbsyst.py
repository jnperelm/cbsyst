import unittest
import pandas as pd
import cbsyst.carbon_fns as cf
import cbsyst.boron_fns as bf
from cbsyst.cbsyst import Csys
from cbsyst.helpers import Bunch


class BoronFnTestCase(unittest.TestCase):
    """Test all B functions"""

    def test_Boron_Fns(self):
        ref = Bunch({'ABO3': 0.80882931,
                     'ABO4': 0.80463763,
                     'ABT': 0.80781778,
                     'BO3': 328.50895695,
                     'BO4': 104.49104305,
                     'BT': 433.,
                     'Ca': 0.0102821,
                     'H': 7.94328235e-09,
                     'Ks': {'K0': 0.02839188,
                            'K1': 1.42182814e-06,
                            'K2': 1.08155475e-09,
                            'KB': 2.52657299e-09,
                            'KSO4': 0.10030207,
                            'KW': 6.06386369e-14,
                            'KspA': 6.48175907e-07,
                            'KspC': 4.27235093e-07},
                     'Mg': 0.0528171,
                     'S': 35.,
                     'T': 25.,
                     'alphaB': 1.02725,
                     'dBO3': 46.30877684,
                     'dBO4': 18.55320208,
                     'dBT': 39.5,
                     'pH': 8.1})

        Ks = Bunch(ref.Ks)

        # Speciation
        self.assertAlmostEqual(bf.BT_BO3(ref.BT, ref.BO3, Ks),
                               ref.H,
                               msg='BT_BO3', places=6)

        self.assertAlmostEqual(bf.BT_BO4(ref.BT, ref.BO4, Ks),
                               ref.H,
                               msg='BT_BO4', places=6)

        self.assertAlmostEqual(bf.pH_BO3(ref.pH, ref.BO3, Ks),
                               ref.BT,
                               msg='pH_BO3', places=6)

        self.assertAlmostEqual(bf.pH_BO4(ref.pH, ref.BO4, Ks),
                               ref.BT,
                               msg='pH_BO4', places=6)

        self.assertAlmostEqual(bf.cBO3(ref.BT, ref.H, Ks),
                               ref.BO3,
                               msg='cBO3', places=6)

        self.assertAlmostEqual(bf.cBO4(ref.BT, ref.H, Ks),
                               ref.BO4,
                               msg='cBO4', places=6)

        self.assertEqual(bf.chiB_calc(ref.H, Ks),
                         1 / (1 + Ks.KB / ref.H),
                         msg='chiB_calc')

        # Isotopes
        self.assertEqual(bf.alphaB_calc(ref.T),
                         1.0293 - 0.000082 * ref.T,
                         msg='alphaB_calc')

        self.assertAlmostEqual(bf.pH_ABO3(ref.pH, ref.ABO3, Ks, ref.alphaB),
                               ref.ABT,
                               msg='pH_ABO3', places=6)

        self.assertAlmostEqual(bf.pH_ABO4(ref.pH, ref.ABO4, Ks, ref.alphaB),
                               ref.ABT,
                               msg='pH_ABO4', places=6)

        self.assertAlmostEqual(bf.cABO3(ref.H, ref.ABT, Ks, ref.alphaB),
                               ref.ABO3,
                               msg='cABO3', places=6)

        self.assertAlmostEqual(bf.cABO4(ref.H, ref.ABT, Ks, ref.alphaB),
                               ref.ABO4,
                               msg='cABO4', places=6)

        # Isotope unit conversions
        self.assertAlmostEqual(bf.A11_2_d11(0.807817779214075),
                               39.5,
                               msg='A11_2_d11', places=6)

        self.assertAlmostEqual(bf.d11_2_A11(39.5),
                               0.807817779214075,
                               msg='d11_2_A11', places=6)


class CarbonFnTestCase(unittest.TestCase):
    """Test all C functions"""

    def test_Carbon_Fns(self):
        ref = Bunch({'BT': 433,
                     'CO2': 9.7861814,
                     'CO3': 238.511253,
                     'Ca': 0.0102821,
                     'DIC': 2000,
                     'H': 7.94328235e-09,
                     'HCO3': 1751.7025656,
                     'Ks': {'K0': 0.028391881804015685,
                            'K1': 1.4218281371391736e-06,
                            'K2': 1.0815547472209423e-09,
                            'KB': 2.5265729902477677e-09,
                            'KSO4': 0.10030207107256615,
                            'KW': 6.0638636861053757e-14,
                            'KspA': 6.4817590680119676e-07,
                            'KspC': 4.2723509278625912e-07},
                     'Mg': 0.0528171,
                     'S': 35.,
                     'T': 25.,
                     'TA': 2340.84212345,
                     'fCO2': 344.68238018419373,
                     'pCO2': 345.78871573110143,
                     'pH': 8.1,
                     'unit': 1000000.0})

        Ks = Bunch(ref.Ks)

        self.assertAlmostEqual(cf.CO2_pH(ref.CO2, ref.pH, Ks),
                               ref.DIC,
                               msg='CO2_pH', places=6)

        self.assertAlmostEqual(cf.CO2_HCO3(ref.CO2, ref.HCO3, Ks)[0],
                               ref.H,
                               msg='CO2_HCO3 (zf)', places=6)

        self.assertAlmostEqual(cf.CO2_CO3(ref.CO2, ref.CO3, Ks)[0],
                               ref.H,
                               msg='CO2_CO3 (zf)', places=6)

        self.assertAlmostEqual(cf.CO2_TA(ref.CO2 / ref.unit,
                                         ref.TA / ref.unit,
                                         ref.BT / ref.unit, Ks)[0],
                               ref.H,
                               msg='CO2_TA (zf)', places=6)

        self.assertAlmostEqual(cf.CO2_DIC(ref.CO2, ref.DIC, Ks)[0],
                               ref.H,
                               msg='CO2_DIC (zf)', places=6)

        self.assertAlmostEqual(cf.pH_HCO3(ref.pH, ref.HCO3, Ks),
                               ref.DIC,
                               msg='pH_HCO3', places=6)

        self.assertAlmostEqual(cf.pH_CO3(ref.pH, ref.CO3, Ks),
                               ref.DIC,
                               msg='pH_CO3', places=6)

        self.assertAlmostEqual(cf.pH_TA(ref.pH,
                                        ref.TA / ref.unit,
                                        ref.BT / ref.unit, Ks) * ref.unit,
                               ref.CO2,
                               msg='pH_TA', places=6)

        self.assertAlmostEqual(cf.pH_DIC(ref.pH, ref.DIC, Ks),
                               ref.CO2,
                               msg='pH_DIC', places=6)

        self.assertAlmostEqual(cf.HCO3_CO3(ref.HCO3, ref.CO3, Ks)[0],
                               ref.H,
                               msg='HCO3_CO3 (zf)', places=6)

        self.assertAlmostEqual(cf.HCO3_TA(ref.HCO3 / ref.unit,
                                          ref.TA / ref.unit,
                                          ref.BT / ref.unit, Ks)[0],
                               ref.H,
                               msg='HCO3_TA (zf)', places=6)

        self.assertAlmostEqual(cf.HCO3_DIC(ref.HCO3, ref.DIC, Ks)[0],
                               ref.H,
                               msg='HCO3_DIC (zf)', places=6)

        self.assertAlmostEqual(cf.CO3_TA(ref.CO3 / ref.unit,
                                         ref.TA / ref.unit,
                                         ref.BT / ref.unit, Ks)[0],
                               ref.H,
                               msg='CO3_TA (zf)', places=6)

        self.assertAlmostEqual(cf.CO3_DIC(ref.CO3, ref.DIC, Ks)[0],
                               ref.H,
                               msg='CO3_DIC (zf)', places=6)

        self.assertAlmostEqual(cf.TA_DIC(ref.TA / ref.unit,
                                         ref.DIC / ref.unit,
                                         ref.BT / ref.unit, Ks)[0],
                               ref.H,
                               msg='TA_DIC (zf)', places=6)

        self.assertAlmostEqual(cf.cCO2(ref.H, ref.DIC, Ks),
                               ref.CO2,
                               msg='cCO2', places=6)

        self.assertAlmostEqual(cf.cCO3(ref.H, ref.DIC, Ks),
                               ref.CO3,
                               msg='cCO3', places=6)

        self.assertAlmostEqual(cf.cHCO3(ref.H, ref.DIC, Ks),
                               ref.HCO3,
                               msg='cHCO3', places=6)

        self.assertAlmostEqual(cf.cTA(ref.CO2, ref.H, ref.BT, Ks, unit=ref.unit),
                               ref.TA,
                               msg='cTA', places=5)

        self.assertAlmostEqual(cf.fCO2_to_CO2(ref.fCO2, Ks),
                               ref.CO2,
                               msg='fCO2_to_CO2', places=6)

        self.assertAlmostEqual(cf.CO2_to_fCO2(ref.CO2, Ks),
                               ref.fCO2,
                               msg='CO2_to_fCO2', places=6)

        self.assertAlmostEqual(cf.fCO2_to_pCO2(ref.fCO2, ref.T),
                               ref.pCO2,
                               msg='fCO2_to_pCO2', places=6)

        self.assertAlmostEqual(cf.pCO2_to_fCO2(ref.pCO2, ref.T),
                               ref.fCO2,
                               msg='pCO2_to_fCO2', places=6)


class ReferenceDataTestCase(unittest.TestCase):
    """Test `yt` against reference data."""

    def test_Bockmon_Data(self):
        # Measured data from paper
        batch_A = {'S': 33.190,
                   'TA': 2215.08,
                   'DIC': 2015.72,
                   'pH': 7.8796}

        batch_B = {'S': 33.186,
                   'TA': 2216.26,
                   'DIC': 2141.94,
                   'pH': 7.5541}

        pH = [batch_A['pH'], batch_B['pH']]
        TA = [batch_A['TA'], batch_B['TA']]
        DIC = [batch_A['DIC'], batch_B['DIC']]
        S = [batch_A['S'], batch_B['S']]
        BT = 433.

        # Csys calculations
        # TA from pH and DIC
        cTA = Csys(pH=pH, DIC=DIC, BT=BT, S=S)
        # Calculate % differences from measured
        dTA = (100 * (TA - cTA.TA) / TA)

        self.assertLess(max(abs(dTA)), 0.2, msg='TA from DIC and pH')

        # pH from TA and DIC
        cpH = Csys(DIC=DIC, TA=TA, BT=BT, S=S)
        # Calculate % differences from measured
        dpH = (100 * (pH - cpH.pH) / pH)

        self.assertLess(max(abs(dpH)), 0.2, msg='pH from TA and DIC')

        # DIC from pH and TA
        cDIC = Csys(pH=pH, TA=TA, BT=BT, S=S)
        # Calculate % differences from measured
        dDIC = (100 * (DIC - cDIC.DIC) / DIC)

        self.assertLess(max(abs(dDIC)), 0.2, msg='DIC from TA and pH')

    def test_Luecker_Data(self):
        ld = pd.read_csv('cbsyst/test_data/Luecker2000/Luecker2000_Table3.csv', comment='#')

        # Calculate using cbsys
        # TA from DIC and fCO2
        cTA = Csys(DIC=ld.DIC.values, fCO2=ld.fCO2.values, T=ld.Temp.values, S=ld.Sal.values)
        dTA = 100 * (ld.TA - cTA.TA) / ld.TA
        self.assertLess(max(abs(dTA)), 1, msg='TA from DIC and fCO2, % difference.')

        # fCO2 from TA and DIC
        cfCO2 = Csys(TA=ld.TA.values, DIC=ld.DIC.values, T=ld.Temp.values, S=ld.Sal.values, BT=433)
        dfCO2 = 100 * (ld.fCO2 - cfCO2.fCO2) / ld.fCO2
        self.assertLess(max(abs(dfCO2)), 10, msg='fCO2 from DIC and TA, % difference.')

        # DIC from TA and fCO2
        cDIC = Csys(TA=ld.TA.values, fCO2=ld.fCO2.values, T=ld.Temp.values, S=ld.Sal.values)
        dDIC = 100 * (ld.DIC - cDIC.DIC) / ld.DIC
        self.assertLess(max(abs(dDIC)), 1, msg='DIC from fCO2 and TA, % difference.')


if __name__ == '__main__':
    unittest.main()