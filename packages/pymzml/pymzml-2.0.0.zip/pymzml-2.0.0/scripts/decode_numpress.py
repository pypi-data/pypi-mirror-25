import sys
sys.path.insert(0, '..')
import pymzml

Reader = pymzml.run.Reader('../tests/data/Fusion001225.mzML')
ot = pymzml.obo.OboTranslator('3.79.0')

spec = Reader[500]
print('raw')
print(spec.peaks('raw')[:5])
print('reprofiled')
print(spec.peaks('reprofiled')[:5])
print('centroided')
print(spec.peaks('centroided')[:5])
