from scipy import signal
freq=1925

def base_peak(emg):

    maxes=signal.find_peaks(emg, height=.15)[0]

    peak=maxes[0]

    sum=0
    for i in range((peak-10),(peak+10)):
        sum=sum+emg[i]
    
    avg_peak=sum/20
    peak_ms = (peak-500)/freq * 1000

    return(avg_peak, peak_ms)


def condition_peak(emg):
    avg_time=36.36

    M1_avg=int((avg_time*freq/1000)+500)

    range_emg=emg[M1_avg-20:M1_avg+20]

    maxes=signal.find_peaks(range_emg, height=.1)[0]

    peak=maxes[0]
    peak=peak+M1_avg

    sum=0
    for i in range((peak-10),(peak+10)):
        sum=sum+emg[i]

    avg_peak=sum/20
    peak_ms = (peak-500)/freq * 1000

    return(avg_peak, peak_ms)


