
from scipy import signal
freq=1925


def base_peak(emg):

    maxes = list(signal.find_peaks(emg[500:], height=find_peak_min_thresh(emg))[0])

    if maxes:
        peak=maxes[0]
        peak += 500

        sum=0
        for i in range((peak-10),(peak+10)):
            sum=sum+emg[i]
        
        avg_peak=sum/20
        peak_ms = (peak-500)/freq * 1000
    else:
        avg_peak=0
        peak_ms=0

    return(avg_peak, peak_ms)


def condition_peak(emg, avg_time):

    M1_avg=int((avg_time*freq/1000)+500)

    range_emg=emg[M1_avg-20:M1_avg+20]

    maxes = list(signal.find_peaks(range_emg, height=find_peak_min_thresh(emg))[0])
    if maxes:
        peak=maxes[0]
        peak=peak+M1_avg

        sum=0
        for i in range((peak-10),(peak+10)):
            sum=sum+emg[i]

        avg_peak=sum/20
        peak_ms = (peak-500)/freq * 1000
    else:
        return 0,0

    return(avg_peak, peak_ms)


def find_peak_min_thresh(emg):
    num = 5
    peaks = []
    factor = 1.5

    peaks_pos = list(signal.find_peaks(emg[0:400], height=0)[0])

    
    for x_pos in peaks_pos:
        peaks.append(emg[x_pos])

    peaks = sorted(peaks, reverse=True)

    return sum(peaks[:num])/num * factor

