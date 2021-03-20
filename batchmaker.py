
"""
This module offers a minimal functionality to set up first-level batches that
are readable in spm
"""

import scipy.io as sio    #for mat files
import numpy as np        #we may need this
from numpy.core.records import fromarrays


class TimingParams:
    def __init__(self,
                 units = "secs",
                 RT = 2.,
                 fmri_t = 16.,
                 fmri_t0 = 8.):
        
        """
        initializes timing parameters
        names in SPM-GUI: 
        units -> units for design
        RT -> interscan interval
        fmri_t -> microtime resolution
        fmri_t0 -> microtime onset
        """
        
        self.units = units
        self.RT = RT
        self.fmri_t = fmri_t
        self.fmri_t0 =fmri_t0
        
        dt = [('units', 'U10'), ('RT', np.float64), 
              ('fmri_t', np.float64), ('fmri_t0', np.float64)]

        self.mat = np.zeros((1,), dtype = dt)

        self.mat[0]['units'] = units
        self.mat[0]['RT'] = RT
        self.mat[0]['fmri_t'] = fmri_t
        self.mat[0]['fmri_t0'] = fmri_t0


class Conditions:
    
    def __init__(self,
                 names, #array/list of names
                 onsets, #an array of onsets for each condition
                 durations, #an array of durations for each condition
                 pmod = False,  #[ [names],  an array of values for paramModul, poly = 1] 
                 tmod = 0,
                 orth = 1):
        
        """
        initializes conditions
        names in SPM-GUI: 
        tmod -> time modulation
        pmod -> parametric modulations
        orth -> orthogonalize modulations
        """
        
        dt = [('name', 'U10'), ('onset', np.object), ('duration', np.object), 
              ('tmod', 'int'), ('pmod', np.object), ('orth', 'int')]
        cond = np.zeros((len(onsets),), dtype = dt)
        
        for i in range(len(onsets)):
            name = names[i]
            onset = np.array([[j] for j in onsets[i]])
            duration = np.array([[j] for j in durations[i]])
            tmod = tmod
            orth = orth
            if pmod:
                
                dt = [('name', 'U10'), ('param', np.object), ('poly', np.float)]
                pmodu = np.zeros((len(pmod[i]),), dtype = dt)
                
                
                for k in range(len(pmod[i])):
                    pmodu[k]['name'] = pmod[i][k][0]
                    pmodu[k]['param'] = np.array([[j] for j in pmod[i][k][1]]) 
                    pmodu[k]['poly'] = pmod[i][k][2]

            else:
                pmodu = fromarrays([[], []], names=[])
        
        
            cond[i]['name'] = name
            cond[i]['onset'] = onset
            cond[i]['duration'] = duration
            cond[i]['tmod'] = tmod
            cond[i]['orth'] = orth 
            cond[i]['pmod'] = pmodu #pmod
            
        self.mat = cond

class Session:
    
    def __init__(self,
                 scans, #array of paths of scan files, ordered by session, ie for 2 sessions: shape 2x500
                 cond, #array of conditions, ie for 2 sessions shape 2x6
                 multi_reg = [], #array of multi_reg paths
                 multi = [],
                 regress = [],
                 hpf = 128.0):
        
        """
        initializes sessions
        names in SPM-GUI: 
        scans -> 
        multi_reg -> multiple regressors
        multi -> multiple conditions
        hpf -> high-pass filter
        """        
        
        
        dt = [('scans', np.object), ('cond', np.object), ('multi', np.object), 
              ('regress', np.object), ('multi_reg', np.object), ('hpf', np.float)]
        sess = np.zeros((len(scans),), dtype=dt)

        for i in range(len(scans)):
            self.scans = np.array([[file] for file in scans[i]], dtype = np.object)
            #cond = {'empty':'empty'}
            self.multi = np.array([''], dtype = np.object)
            self.regress = fromarrays([[], []], names=[])
            self.multi_reg = np.array(multi_reg[i], dtype = np.object) 
            self.hpf = 128.0
        

            sess[i]['scans'] = self.scans
            sess[i]['cond'] = cond[i]
            sess[i]['multi'] = self.multi
            sess[i]['regress'] = self.regress
            sess[i]['multi_reg'] = self.multi_reg
            sess[i]['hpf'] = self.hpf


        self.mat = sess
        
        
class Batchfile:
    
    """
    constructs a first-level spm 'batchfile' readable in matlab
    """
    
    def __init__(self,
                 dir,
                 timingParams, #insert timingParams Object here
                 sessions, #insert sessions object here
                 fact = [],
                 bases = [0,0], #This could be looked into to include more derivations of HRF
                 volt = 1.,
                 globale = 'None',
                 mthres = 0.8,
                 mask = np.array([''], dtype = np.object),
                 cvi = 'AR(1)'
                 ):
        
        self.dir = np.array(dir, dtype = np.object)
        self.timing = timingParams.mat
        self.fact = fromarrays([[], []], names=[]) 
        hrf = {'derivs':bases}
        self.bases = {'hrf':hrf}
        self.volt = volt
        self.globale = globale
        self.mthres = mthres
        self.mask = mask
        self.cvi = cvi

        fmri_spec = {'fmri_spec' : {'dir' : self.dir, 'timing' : self.timing,
                    'sess' : sessions.mat, 'fact' : self.fact,
                    'bases' : self.bases, 'volt' : self.volt, 
                    'global' : self.globale, 'mthres' : self.mthres,
                    'mask' : self.mask,'cvi' : self.cvi} }
        
        #layer 3: a 1x1 struct called 'stats' containing fmri_spec
        stats = {'stats' : fmri_spec}
        
        #layer 2: a 1x1 struct called 'spm' containing 'stats'
        self.spm = {'spm' : stats}
        
        #outermost layer1: 1x1 cell containing one struct
        self.matlabbatch = np.array(self.spm, dtype = np.object)
        
    def export(self, name):
        
        """saving batchfile"""
        
        sio.savemat(name+'.mat', {'matlabbatch':self.matlabbatch})