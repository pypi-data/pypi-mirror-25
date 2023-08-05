"""Module to detect slow waves.

"""
from logging import getLogger
from numpy import argmax, concatenate, hstack, sum, zeros, median, mean

from .spindle import detect_events, transform_signal, within_duration
from ..graphoelement import SlowWaves

lg = getLogger(__name__)
MAXIMUM_DURATION = 5

class DetectSlowWave:
    """Design slow wave detection on a single channel.
    
    Parameters
    ----------
    method : str
        one of the predefined methods
    frequency : tuple of float
        low and high frequency of SW band
    duration : tuple of float
        min and max duration of SWs        

    """
    def __init__(self, method='Massimini2004', duration=None):
        
        if duration is None:
            duration = (0.5, 3)
            
        self.method = method
        self.duration = duration
        
        if method == 'Massimini2004':
            self.det_butter = {'order': 4,
                               'freq': (0.1, 4.)}
            self.trough_duration = (0.3, 1.)
            self.max_trough_amp = - 80
            self.min_ptp = 140
            
        elif method == 'AASM/Massimini2004':
            self.det_butter = {'order': 4,
                               'freq': (0.1, 4.)}
            self.trough_duration = (0.25, 1.)
            self.max_trough_amp = - 40
            self.min_ptp = 75
        
        else:
            raise ValueError('Unknown method')
            
    def __repr__(self):
        return ('detsw_{0}_{3:04.1f}-{4:04.1f}s'
                ''.format(self.method, self.duration[0], self.duration[1]))
    
    def __call__(self, data):
        """Detect slow waves on the data.

        Parameters
        ----------
        data : instance of Data
            data used for detection

        Returns
        -------
        instance of graphoelement.SlowWaves
            description of the detected SWs

        """
        slowwave = SlowWaves()
        slowwave.chan_name = data.axis['chan'][0]

        all_slowwaves = []
        for i, chan in enumerate(data.axis['chan'][0]):
            lg.info('Detecting slow waves on chan %s', chan)
            time = hstack(data.axis['time'])
            dat_orig = hstack(data(chan=chan))
            
            if self.method == 'Massimini2004':
                sw_in_chan = detect_Massimini2004(
                        dat_orig, data.s_freq, time, self)
                
            elif self.method == 'AASM/Massimini2004':
                sw_in_chan = detect_Massimini2004(
                        dat_orig, data.s_freq, time, self)
                
            else:
                raise ValueError('Unknown method')

            for sw in sw_in_chan:
                sw.update({'chan': chan})
            all_slowwaves.extend(sw_in_chan)
            # end of loop over chan
            
        lg.info('number of SW: ' + str(len(all_slowwaves)))
        slowwave.events = sorted(all_slowwaves, key=lambda x: x['start'])
        
        return slowwave
    
def detect_Massimini2004(dat_orig, s_freq, time, opts):
    """Slow wave detection based on Massimini et al., 2004.
    
    Parameters
    ----------
    dat_orig : ndarray (dtype='float')
        vector with the data for one channel
    s_freq : float
        sampling frequency
    time : ndarray (dtype='float')
        vector with the time points for each sample
    opts : instance of 'DetectSlowWave'
        'det_butter' : dict
            parameters for 'butter',
        'duration' : tuple of float
            min and max duration of SW
        'min_ptp' : float
            min peak-to-peak amplitude   
        'trough_duration' : tuple of float
            min and max duration of first half-wave (trough)

    Returns
    -------
    list of dict
        list of detected SWs
    float
        SW density, per 30-s epoch
        
    References
    ----------
    Massimini, M. et al. J Neurosci 24(31) 6862-70 (2004).
    
    """
    lg.info('detection raw dat: ' + str(len(dat_orig)))
    lg.info('mean: ' + str(mean(dat_orig)) +' median: ' + str(median(dat_orig)))
    dat_det = transform_signal(dat_orig, s_freq, 'butter', opts.det_butter)
    lg.info('det filtered data: ' + str(len(dat_det)))
    lg.info('mean: ' + str(mean(dat_det)) +' median: ' + str(median(dat_det)))
    below_zero = detect_events(dat_det, 'upper_threshold', value=0.)
    
    if below_zero is not None:
        troughs = within_duration(below_zero, time, opts.trough_duration) 
        
        if troughs is not None:
            troughs = select_peaks(dat_det, troughs, opts.max_trough_amp)
            
            if troughs is not None:
                events = _add_pos_halfwave(dat_det, troughs, s_freq, opts)
                
                if len(events):
                    events = within_duration(events, time, opts.duration)
                    
                    sw_in_chan = make_slow_waves(events, dat_det, time, s_freq)

    else:
        lg.info('No slow wave found')
        sw_in_chan = []
        
    return sw_in_chan
    

def select_peaks(data, events, limit):
    """Check whether event is satisfies amplitude limit.

    Parameters
    ----------
    data : ndarray (dtype='float')
        vector with data
    events : ndarray (dtype='int')
        N x 3 matrix with start, peak/trough, end samples
    limit : float
        low and high limit for spindle duration

    Returns
    -------
    ndarray (dtype='int')
        N x 2+ matrix with start, peak, end samples

    """
    selected = abs(data[events[:, 1]]) >= abs(limit)

    return events[selected, :]

def make_slow_waves(events, data, time, s_freq):
    """Create dict for each slow wave, based on events of time points.

    Parameters
    ----------
    events : ndarray (dtype='int')
        N x 5 matrix with start, trough, zero, peak, end samples
    data : ndarray (dtype='float')
        vector with the data
    time : ndarray (dtype='float')
        vector with time points
    s_freq : float
        sampling frequency

    Returns
    -------
    list of dict
        list of all the SWs, with information about start_time, 
        trough_time, zero_time, peak_time, end_time, duration (s), trough_val, 
        peak_val, peak-to-peak amplitude (signal units), area_under_curve 
        (signal units * s)
    """
    slow_waves = []
    for ev in events:
        one_sw = {'start': time[ev[0]],
                  'trough_time': time[ev[1]],
                  'zero_time': time[ev[2]],
                  'peak_time': time[ev[3]],
                  'end': time[ev[4]-1],
                  'trough_val': data[ev[1]],
                  'peak_val': data[ev[3]],
                  'dur': (ev[4] - ev[0]) / s_freq,
                  'area_under_curve': sum(data[ev[0]: ev[4]]) / s_freq,
                  'ptp': ev[3] - ev[1]
                  }
        slow_waves.append(one_sw)

    return slow_waves

def _add_pos_halfwave(data, events, s_freq, opts):
    """Find the next zero crossing and the intervening peak and add them to 
    events. If no zero found before max_dur, event is discarded. If 
    peak-to-peak is smaller than min_ptp, the event is discarded.
    
    Parameters
    ----------
    data : ndarray (dtype='float')
        vector with the data
    events : ndarray (dtype='int')
        N x 3 matrix with start, peak, end samples    s_freq : float
        sampling frequency
    opts : instance of 'DetectSlowWave'
        'duration' : tuple of float
            min and max duration of SW
        'min_ptp' : float
            min peak-to-peak amplitude   
            
    Returns
    -------
    ndarray (dtype='int')
        N x 5 matrix with start, trough, - to + zero crossing, peak, and end 
        samples
    """
    max_dur = opts.duration[1]
    
    if max_dur is None:
        max_dur = MAXIMUM_DURATION    
    window = s_freq * max_dur
    
    peak_and_zero = zeros((events.shape[0], 2))
    events = concatenate((events, peak_and_zero), axis=1)
    selected = []
    
    for ev in events:
        ev[4] = ev[2] + argmax(data[ev[2]: ev[0] + window] < 0) # quickest way
        
        if ev[4] == 0:
            selected.append(False)
            continue
        
        ev[3] = argmax(data[ev[2]: ev[4]])
        
        if abs(data[ev[1]] - data[ev[3]]) < opts.min_p2p:
            selected.append(False)
            continue
        
        selected.append(True)
            
    return events[selected, :]
            
        
    

    